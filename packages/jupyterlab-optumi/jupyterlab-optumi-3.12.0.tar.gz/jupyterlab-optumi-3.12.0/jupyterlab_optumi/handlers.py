'''
Copyright (C) Optumi Inc - All rights reserved.

You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
'''

## Jupyter imports
from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
from tornado.escape import json_decode
from tornado.ioloop import IOLoop
from tornado.web import authenticated
import nbformat, subprocess

from ._version import __version__

## Standard library imports

# Generic Operating System Services
import os, io, time, re, datetime

# File and Directory Access
import tempfile

# Python Runtime Services
import traceback

# Concurrent execution
from threading import Lock, Thread

# Internet Protocols and Support
import uuid
from urllib import request, parse
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode
from http.cookiejar import DefaultCookiePolicy, CookieJar
import requests

# Internet Data Handling
import json, mimetypes, base64

# Networking and Interprocess Communication
import socket, ssl, select

# Data Compression and Archiving
from zipfile import ZipFile, ZIP_DEFLATED

# Cryptographic Services
import hashlib

# Numeric and Mathematical Modules
import random, math

# Structured Markup Processing Tools
import html

## Other imports
from cryptography import x509
from cryptography.hazmat.backends import default_backend

## Flags
# WARNING: This flag will show error tracebacks where normally not shown, but it will cause some < 500 response codes to be 500
DEBUG = False

lock = Lock()
## We need to somehow timeout/remove old progress data from these
compressionProgress = {}
uploadProgress = {}
launchStatus = {}
downloadProgress = {}

# Optumi temp dir
TEMP_DIR = tempfile.gettempdir() + "/optumi"

loginProgress = None

# This is OKTA stuff
LOGIN_SERVER = 'https://olh.optumi.net:8443'
REDIRECT_URI = LOGIN_SERVER + '/redirect'
BASE_URL = 'https://login.optumi.com'
AUTH_SERVER_ID = 'default'
CLIENT_ID = '0oa1seifygaiUCgoA5d7'

LOGIN_WRAP_START = '<div style="position: absolute;top: 40%;width: 100%;"><div style="display: grid;justify-content: center;"><img style="margin: auto;" src="https://www.optumi.com/wp-content/uploads/2020/10/optumi-logo-header.png" srcset="https://www.optumi.com/wp-content/uploads/2020/10/optumi-logo-header.png 1x" width="200" height="50" alt="Optumi Logo" retina_logo_url="" class="fusion-standard-logo"><div style="text-align: center;font-size: 1.5rem">'
LOGIN_WRAP_END = '</div></div></div>'

jupyterDrive = ""
jupyterHome = ""
userHome = ""

login_state = None
login_pkce = None
login_token = None

jupyter_log = None
# Windows doesn't support colors
COLOR_START = '' if os.name == 'nt' else '\033[94m'
COLOR_END = '' if os.name == 'nt' else '\033[0m'

def optumi_log(message):
    try:
        requests.request("POST", 'https://ocl.optumi.net:8443/message', json={ 'message': '[' + datetime.datetime.now().isoformat() + '] ' + message })
    except Exception as e:
        print(e)

def optumi_format_and_log(c=None, message=''):
    if c is None:
        formatted = COLOR_START + '[Optumi]' + COLOR_END + ' ' + message
    else:
        formatted = COLOR_START + '[Optumi]' + COLOR_END + ' ' + c.__class__.__name__ + ': ' + message

    try:
        # Use a new thread to send the message so any connection issues don't hold up this thread
        Thread(target=optumi_log, args=(formatted, )).start()
    except Exception as e:
            print(e)

    return formatted

dev_version = 'dev' in __version__.lower()

split_version = __version__.split('.')
jupyterlab_major = split_version[0]
optumi_major = split_version[1]
PORTAL = 'portal' + jupyterlab_major + (optumi_major if len(optumi_major) == 2 else '0' + optumi_major) + '.optumi.net'
PORTAL_PORT = 8443
PORTAL_DOMAIN_AND_PORT = PORTAL + ':' + str(PORTAL_PORT)

# File constants
CUTOFF_SIZE = 10 * 1024 * 1024 # Currently we have a 10 MB cutoff size
MIN_CHUNK_SIZE = 1 * 1024 * 1024 # Currently we have a 1 MB max chunk size
MAX_CHUNK_SIZE = 20 * 1024 * 1024 # Currently we have a 20 MB max chunk size

domain_and_port = PORTAL_DOMAIN_AND_PORT
def get_path(domain_and_port_override=None):
    # If there is no domain passed in, use the global domain
    if domain_and_port_override == None: return 'https://' + domain_and_port
    return 'https://' + domain_and_port_override

class VersionHandler(IPythonHandler):
    @authenticated
    async def get(self):
        try:
            self.write(json.dumps({'version': __version__, 'userHome': userHome, 'jupyterHome': jupyterHome}))
        except Exception as e:
            # 401 unauthorized
            self.set_status(401)
            self.write(json.dumps({'message': 'Encountered error while getting version'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

class CheckLoginHandler(IPythonHandler):
    @authenticated
    async def get(self):
        try:
            extension_version = __version__
            response = await IOLoop.current().run_in_executor(None, exchange_versions, extension_version)
            if response.geturl().endswith('/login'):
                self.write(json.dumps({'message': 'Not logged in', 'loginFailed': True}))
                return
            if not getattr(response, 'geturl', False) or response.getcode() != 200:
                self.write(json.dumps({'loginFailedMessage': response.read().decode('utf-8'), 'message': 'Version exchange failed', 'loginFailed': True}))
                jupyter_log.error(optumi_format_and_log(self, str(response)))
                IOLoop.current().run_in_executor(None, logout)
                return
            controller_version = response.read().decode('utf-8')
            response = await IOLoop.current().run_in_executor(None, get_new_agreement)
            if not getattr(response, 'geturl', False) or response.getcode() != 200:
                self.write(json.dumps({'message': 'Encountered error while getting new user agreement', 'loginFailed': True}))
                jupyter_log.error(optumi_format_and_log(self, str(response)))
                IOLoop.current().run_in_executor(None, logout)
                return
            newAgreement = True
            buf = io.BytesIO()
            blocksize = 4096 # just made something up
            size = 0
            while True:
                read = response.read(blocksize)
                if not read:
                    break
                buf.write(read)
                size += len(read)
            if size == 0:
                newAgreement = False
            else:
                with open("Agreement.html", "wb") as f:
                    f.write(base64.decodebytes(buf.getvalue()))
            response = await IOLoop.current().run_in_executor(None, get_user_information, True)
            self.set_status(response.getcode())
            user_information = json.load(response)
            user_information['newAgreement'] = newAgreement
            user_information['message'] = 'Logged in successfully'
            self.write(user_information)
        except Exception as e:
            # We do not want to print an error here, since it can be part of normal operation
            self.set_status(200)
            self.write(json.dumps({'message': 'Encountered error while getting user information', 'loginFailed': True}))
            if DEBUG: raise e

class LoginHandler(IPythonHandler):
    @authenticated
    async def get(self):
        global login_token
        global loginProgress
        global domain_and_port
        try:
            if login_token is None:
                self.set_status(401)
                self.write(json.dumps({'message': 'Not authorized'}))
                return
            else:
                login_status, message = await IOLoop.current().run_in_executor(None, login_rest_server, PORTAL, PORTAL_PORT, login_token)
                
                if dev_version: 
                    jupyter_log.info(optumi_format_and_log(self, 'REST login completed'))
                else:
                    optumi_format_and_log(self, 'REST login completed')

            # Reset the login progress
            loginProgress = None
            login_token = None
            if login_status == 1:
                ## Set the domain
                domain_and_port = message
                ### NOTE: If we succeed logging in but fail after, we want to try to logout
                ## Exchange versions
                extension_version = __version__
                response = await IOLoop.current().run_in_executor(None, exchange_versions, extension_version)
                if response.geturl().endswith('/login'):
                    self.write(json.dumps({'message': 'Not logged in', 'loginFailedMessage': 'Unable to log in', 'loginFailed': True}))
                    return
                if not getattr(response, 'geturl', False) or response.getcode() != 200:
                    self.write(json.dumps({'loginFailedMessage': response.read().decode('utf-8'), 'message': 'Version exchange failed', 'loginFailed': True}))
                    jupyter_log.error(optumi_format_and_log(self, str(response)))
                    IOLoop.current().run_in_executor(None, logout)
                    return
                controller_version = response.read().decode('utf-8')

                if dev_version: 
                    jupyter_log.info(optumi_format_and_log(self, 'Exchanged controller versions'))
                else:
                    optumi_format_and_log(self, 'Exchanged controller versions')

                ## Get new agreement
                response = await IOLoop.current().run_in_executor(None, get_new_agreement)
                if not getattr(response, 'geturl', False) or response.getcode() != 200:
                    self.write(json.dumps({'loginFailedMessage': 'Unable to get agreement', 'message': 'Getting agreement failed', 'loginFailed': True}))
                    jupyter_log.error(optumi_format_and_log(self, str(response)))
                    IOLoop.current().run_in_executor(None, logout)
                    return
                newAgreement = True
                buf = io.BytesIO()
                blocksize = 4096 # just made something up
                size = 0
                while True:
                    read = response.read(blocksize)
                    if not read:
                        break
                    buf.write(read)
                    size += len(read)
                if size == 0:
                    newAgreement = False
                else:
                    with open("Agreement.html", "wb") as f:
                        f.write(base64.decodebytes(buf.getvalue()))
                # We should check that the versions are valid
                if dev_version: 
                    jupyter_log.info(optumi_format_and_log(self, 'Connected to Optumi controller version ' + controller_version))
                else:
                    optumi_format_and_log(self, 'Connected to Optumi controller version ' + controller_version)

                ## Get user information
                response = await IOLoop.current().run_in_executor(None, get_user_information, True)
                if not getattr(response, 'geturl', False) or response.getcode() != 200:
                    self.set_status(response.getcode())
                    self.write(json.dumps({'loginFailedMessage': 'Unable to get user information', 'message': 'Unable to get user information', 'loginFailed': True}))
                    jupyter_log.error(optumi_format_and_log(self, str(response)))
                    IOLoop.current().run_in_executor(None, logout)
                    return
                user_information = json.load(response)
                user_information['newAgreement'] = newAgreement
                user_information['message'] = 'Logged in successfully'
                self.write(json.dumps(user_information))
            elif login_status == -1:
                self.write(json.dumps({'loginFailedMessage': message, 'message': 'Login failed with message: ' + message, 'loginFailed': True}))
                jupyter_log.info(optumi_format_and_log(self, 'Login failed with message: ' + message))
            elif login_status == -2:
                self.write(json.dumps({'loginFailedMessage': 'Login failed', 'loginFailed': True, 'message': 'Login failed due to invalid request', 'domainFailed': True}))
                jupyter_log.info(optumi_format_and_log(self, 'Login failed'))
            
            if dev_version: 
                jupyter_log.info(optumi_format_and_log(self, 'Login completed'))
            else:
                optumi_format_and_log(self, 'Login completed')

        except Exception as e:
            self.set_status(401)
            self.write(json.dumps({'loginFailedMessage': 'Login failed', 'loginFailed': True, 'message': 'Encountered error while handling login'}))
            IOLoop.current().run_in_executor(None, logout)
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

def generate_pkce():
    code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8')
    code_verifier = re.sub('[^a-zA-Z0-9]+', '', code_verifier)
    
    code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8')
    code_challenge = code_challenge.replace('=', '')

    return { 'code_verifier': code_verifier, 'code_challenge': code_challenge }

def generate_state():
    randomCharset = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    ret = ''
    for i in range(64):
        ret += randomCharset[random.randint(0, len(randomCharset)-1)]
    return ret

class OauthLoginHandler(IPythonHandler):
    @authenticated
    async def get(self):
        global login_state
        global login_pkce

        if dev_version: 
            jupyter_log.info(optumi_format_and_log(self, 'OAUTH login initiated'))
        else:
            optumi_format_and_log(self, 'OAUTH login initiated')

        try:
            login_pkce = generate_pkce()
            login_state = { 'state': generate_state(), 'origin': self.request.protocol + "://" + self.request.host }

            data = {
                'client_id': CLIENT_ID,
                'response_type': 'code',
                'scope': 'openid',
                'redirect_uri': REDIRECT_URI,
                'state': json.dumps(login_state),
                'code_challenge_method': 'S256',
                'code_challenge': login_pkce['code_challenge']
            }
            url_data = parse.urlencode(data)
            url = BASE_URL + '/oauth2/' + AUTH_SERVER_ID + '/v1/authorize?' + url_data

            self.redirect(url)
        except Exception as e:
            self.set_status(401)
            self.write(json.dumps({'message': 'Encountered error setting login state'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

class OauthCallbackHandler(IPythonHandler):
    @authenticated
    async def get(self):
        global login_state
        global login_pkce
        global login_token
        global loginProgress
        try:
            code = self.get_argument('code')
            state = json.loads(self.get_argument('state'))

            if json.dumps(login_state, sort_keys=True) != json.dumps(state, sort_keys=True):
                raise Exception('State does not match expected state in oauth callback')

            ## Exchange code for access and id token

            url = 'https://dev-68278524.okta.com/oauth2/' + AUTH_SERVER_ID + '/v1/token'

            payload = {
                'client_id': CLIENT_ID,
                'grant_type': 'authorization_code',
                'redirect_uri': REDIRECT_URI,
                'code': code,
                'code_verifier': login_pkce['code_verifier']
            }
            
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            # Reset these so they can't be used again
            login_state = None
            login_pkce = None

            login_token = response.text

            loginProgress = 'Allocating...'

            # # # If we want to access parts of the token here, we can do so like this:
            # # json.loads(token)
            # # print(token['access_token'])
            # # print(token['id_token'])

            self.write(LOGIN_WRAP_START + 'You have successfully logged into Optumi and you can close this tab' + LOGIN_WRAP_END)
        except Exception as e:
            self.set_status(401)
            self.write(json.dumps({'message': 'Encountered error while handling oauth callback'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

class SignAgreementHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            timeOfSigning = data['timeOfSigning']
            hashOfSignedAgreement = hash_file("Agreement.html")
            response = await IOLoop.current().run_in_executor(None, sign_agreement, timeOfSigning, hashOfSignedAgreement)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() == 200:
                os.remove("Agreement.html")
            if response.getcode() >= 300: jupyter_log.info(optumi_format_and_log(self, str(response)))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error signing agreement'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

class GetUserInformationHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            includeAll = data['includeAll']
            response = await IOLoop.current().run_in_executor(None, get_user_information, includeAll)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_format_and_log(self, str(response)))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error getting user information'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

class SetUserInformationHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            param = data['param']
            value = data['value']
            response = await IOLoop.current().run_in_executor(None, set_user_information, param, value)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_format_and_log(self, str(response)))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error setting user information'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

class LogoutHandler(IPythonHandler):
    @authenticated
    async def get(self):
        try:
            response = await IOLoop.current().run_in_executor(None, logout)
            self.set_status(response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_format_and_log(self, str(response)))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while logging out'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

class PreviewNotebookHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            nbConfig = data['nbConfig']
            includeExisting = data['includeExisting']
            response = await IOLoop.current().run_in_executor(None, preview_notebook, nbConfig, includeExisting)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_format_and_log(self, str(response)))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while previewing notebook'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

class SetupNotebookHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            name = data['name']
            timestamp = data['timestamp']
            notebook = data['notebook']
            nbConfig = data['nbConfig']
            response = await IOLoop.current().run_in_executor(None, setup_notebook, name, timestamp, notebook, nbConfig)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_format_and_log(self, str(response)))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while setting up notebook'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

class LaunchNotebookHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            requirementsFile = data.get('requirementsFile')     # we use .get() for params that are not required
            paths = data.get('paths')
            expanded = [] if paths is None else [os.path.expanduser(f) for f in paths]
            hashes = [hash_file(f) for f in expanded]
            stats = [os.stat(f) if os.path.isfile(f) else None for f in expanded]
            creationTimes = [datetime.datetime.utcfromtimestamp(stat.st_ctime).isoformat() + 'Z' if stat != None else str(None) for stat in stats]
            lastModificationTimes = [datetime.datetime.utcfromtimestamp(stat.st_mtime).isoformat() + 'Z' if stat != None else str(None) for stat in stats]
            sizes = [str(stat.st_size) if stat else str(None) for stat in stats]
            uuid = data['uuid']
            timestamp = data['timestamp']
            IOLoop.current().run_in_executor(None, launch_notebook, requirementsFile, hashes, paths, creationTimes, lastModificationTimes, sizes, uuid, timestamp)
            self.write(json.dumps({'message': 'success', 'hashes': hashes, 'files': paths, 'filesmod': lastModificationTimes, 'filessize': sizes}))
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while launching notebook'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

class GetLaunchStatusHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            uuid = data['uuid']
            json_map = await IOLoop.current().run_in_executor(None, get_launch_status, uuid)
            if json_map == {}:
                self.set_status(204) # 204 No content
            else:
                self.write(json.dumps(json_map))
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while getting launch status'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

def get_launch_status(key):
    data = {}
    try:
        lock.acquire()
        data = launchStatus[key]
    except:
        pass
    finally:
        lock.release()
    return data

class GetUploadProgressHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            keys = data['keys']
            json_map = await IOLoop.current().run_in_executor(None, get_upload_progress, keys)
            if json_map == {}:
                self.set_status(204) # 204 No content
            else:
                self.write(json.dumps(json_map))
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while getting upload progress'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

def get_upload_progress(keys):
    data = {}
    try:
        lock.acquire()
        if keys == []:
            for key in uploadProgress:
                data[key] = uploadProgress[key]
        else:
            for key in keys:
                if key in uploadProgress:
                    data[key] = uploadProgress[key]
    except:
        pass
    finally:
        lock.release()
    return data

class GetCompressionProgressHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            keys = data['keys']
            json_map = await IOLoop.current().run_in_executor(None, get_compression_progress, keys)
            if json_map == {}:
                self.set_status(204) # 204 No content
            else:
                self.write(json.dumps(json_map))
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while getting compression progress'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

def get_compression_progress(keys):
    data = {}
    try:
        lock.acquire()
        if keys == []:
            for key in compressionProgress:
                data[key] = compressionProgress[key]
        else:
            for key in keys:
                if key in compressionProgress:
                    data[key] = compressionProgress[key]
    except:
        pass
    finally:
        lock.release()
    return data

class GetLoginProgressHandler(IPythonHandler):
    @authenticated
    async def get(self):
        try:
            if loginProgress == None:
                self.set_status(204) # 204 No content
            else:
                self.write(loginProgress)
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while getting login progress'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e


class StopNotebookHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            workload = data['workload']
            module = data['module']
            response = await IOLoop.current().run_in_executor(None, stop_notebook, workload, module)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_format_and_log(self, str(response)))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while stopping notebook'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

class TeardownNotebookHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            workload = data['workload']
            module = data['module']
            response = await IOLoop.current().run_in_executor(None, teardown_notebook, workload, module)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_format_and_log(self, str(response)))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while tearing down notebook'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

class GetMachinesHandler(IPythonHandler):
    @authenticated
    async def get(self):
        try:
            response = await IOLoop.current().run_in_executor(None, get_machines)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_format_and_log(self, str(response)))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while getting machines'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

class GetNotebookConfigHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            nbKey = data['nbKey']
            response = await IOLoop.current().run_in_executor(None, get_notebook_config, nbKey)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_format_and_log(self, str(response)))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while getting notebook config'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

class SetNotebookConfigHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            nbKey = data['nbKey']
            nbConfig = data['nbConfig']
            response = await IOLoop.current().run_in_executor(None, set_notebook_config, nbKey, nbConfig)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_format_and_log(self, str(response)))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while setting notebook config'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

class PullPackageUpdateHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            nbKeys = data['nbKeys']
            response = await IOLoop.current().run_in_executor(None, pull_package_update, nbKeys)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_format_and_log(self, str(response)))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while pulling package update'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

class PushPackageUpdateHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            nbKey = data['nbKey']
            label = data.get('label')
            paths = data.get('paths')
            expanded = [] if paths is None else [os.path.expanduser(f) for f in paths]
            hashes = [hash_file(f) for f in expanded]
            update = data['update']
            response = await IOLoop.current().run_in_executor(None, push_package_update, nbKey, label, hashes, paths, update)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_format_and_log(self, str(response)))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while pulling package update'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

class PullWorkloadConfigHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            workload = data['workload']
            response = await IOLoop.current().run_in_executor(None, pull_workload_config, workload)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_format_and_log(self, str(response)))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while pulling workload config'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

class PushWorkloadConfigHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            workload = data['workload']
            nbConfig = data['nbConfig']
            response = await IOLoop.current().run_in_executor(None, push_workload_config, workload, nbConfig)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_format_and_log(self, str(response)))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while pushing workload config'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e


class GetDataConnectorsHandler(IPythonHandler):
    @authenticated
    async def get(self):
        try:
            response = await IOLoop.current().run_in_executor(None, get_data_connectors)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_format_and_log(self, str(response)))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while getting data connectors'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

class AddDataConnectorHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            dataService = data['dataService']
            name = data['name']
            info = data['info']
            response = await IOLoop.current().run_in_executor(None, add_data_connector, dataService, name, info)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(json.dumps({'message': response.read().decode('utf-8')}))
            if response.getcode() >= 300: jupyter_log.info(optumi_format_and_log(self, str(response)))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while adding data connector'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

class RemoveDataConnectorHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            name = data['name']
            response = await IOLoop.current().run_in_executor(None, remove_data_connector, name)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_format_and_log(self, str(response)))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while removing data connector'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

class GetIntegrationsHandler(IPythonHandler):
    @authenticated
    async def get(self):
        try:
            response = await IOLoop.current().run_in_executor(None, get_integrations)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_start(self) + str(response))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_start(self) + str(e))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while getting environment variables'}))
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG: raise e

class AddIntegrationHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            name = data['name']
            info = data['info']
            response = await IOLoop.current().run_in_executor(None, add_integration, name, info)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(json.dumps({'message': response.read().decode('utf-8')}))
            if response.getcode() >= 300: jupyter_log.info(optumi_start(self) + str(response))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_start(self) + str(e))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while adding environment variable'}))
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG: raise e

class RemoveIntegrationHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            name = data['name']
            response = await IOLoop.current().run_in_executor(None, remove_integration, name)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_start(self) + str(response))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_start(self) + str(e))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while removing environment variable'}))
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG: raise e

class PushWorkloadInitializingUpdateHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            uuid = data['uuid']
            update = data['update']
            response = await IOLoop.current().run_in_executor(None, push_workload_initializing_update, uuid, update)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_format_and_log(self, str(response)))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while pushing workload status update'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

class PullWorkloadStatusUpdatesHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            uuids = data['uuids']
            lastInitializingLines = data['lastInitializingLines']
            lastPreparingLines = data['lastPreparingLines']
            lastRunningLines = data['lastRunningLines']
            response = await IOLoop.current().run_in_executor(None, pull_workload_status_updates, uuids, lastInitializingLines, lastPreparingLines, lastRunningLines)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_format_and_log(self, str(response)))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while pulling workload status update'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

class PullModuleStatusUpdateHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            workloadUUIDs = data['workloadUUIDs']
            moduleUUIDs = data['moduleUUIDs']
            lastUpdateLines = data['lastUpdateLines']
            lastOutputLines = data['lastOutputLines']
            lastMonitorings = data.get('lastMonitorings')     # we use .get() for params that are not required
            lastPatches = data['lastPatches']
            response = await IOLoop.current().run_in_executor(None, pull_module_status_updates, workloadUUIDs, moduleUUIDs, lastUpdateLines, lastOutputLines, lastMonitorings, lastPatches)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_format_and_log(self, str(response)))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while pulling module status update'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

class ListFilesHandler(IPythonHandler):
    @authenticated
    async def get(self):
        try:
            response = await IOLoop.current().run_in_executor(None, list_files)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_format_and_log(self, str(response)))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while listing files'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

class DeleteFilesHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            hashes = data['hashes']
            paths = data['paths']
            creationTimes = data['creationTimes']
            directory = data['directory']
            response = await IOLoop.current().run_in_executor(None, delete_files, hashes, paths, creationTimes, directory)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_format_and_log(self, str(response)))
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while listing files'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

class CancelProgressHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            key = data['key']
            IOLoop.current().run_in_executor(None, cancel_progress, key)
            self.write(json.dumps({'message': 'success'}))
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while canceling uploading files'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

def cancel_progress(key):
    data = {}
    try:
        lock.acquire()
        if key in compressionProgress:
            compressionProgress[key]['progress'] = -1
        else:
            compressionProgress[key] = { 'progress': -1 }
        if key in uploadProgress:
            uploadProgress[key]['progress'] = -1
        else:
            uploadProgress[key] = { 'progress': -1 }
    except:
        pass
    finally:
        lock.release()
    return data

class UploadFilesHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            key = data['key']
            paths = [os.path.expanduser(path) for path in data['paths']]
            compress = data['compress']
            storageTotal = data['storageTotal']
            storageLimit = data['storageLimit']
            autoAddOnsEnabled = data['autoAddOnsEnabled']
            IOLoop.current().run_in_executor(None, upload_files, key, paths, compress, storageTotal, storageLimit, autoAddOnsEnabled)
            self.write(json.dumps({'message': 'success'}))
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while uploading files'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

class DownloadFilesHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            key = data['key']
            hashes = data['hashes']
            paths = data['paths']
            sizes = data['sizes']
            overwrite = data['overwrite']
            directory = data.get('directory') # We use .get() for values that might be null
            response = await IOLoop.current().run_in_executor(None, download_files, key, hashes, paths, sizes, overwrite, directory)
            # We only expect a response if something went wrong
            if response != None: raise response
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while saving notebook output file'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

class GetNotebookOutputFilesHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            workloadUUID = data['workloadUUID']
            moduleUUID = data['moduleUUID']
            key = data['key']
            paths = data['paths']
            sizes = data['sizes']
            overwrite = data['overwrite']
            directory = data.get('directory') # We use .get() for values that might be null
            response = await IOLoop.current().run_in_executor(None, get_notebook_output_files, workloadUUID, moduleUUID, key, paths, sizes, overwrite, directory)
            # We only expect a response if something went wrong
            if response != None: raise response
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while saving notebook output file'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

class GetDownloadProgressHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            keys = data['keys']
            json_map = await IOLoop.current().run_in_executor(None, get_download_progress, keys)
            if json_map == {}:
                self.set_status(204) # No content
            else:
                self.write(json.dumps(json_map))
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while getting download progress'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

def get_download_progress(keys):
    data = {}
    try:
        lock.acquire()
        if keys == []:
            for key in downloadProgress:
                data[key] = downloadProgress[key]
        else:
            for key in keys:
                if key in downloadProgress:
                    data[key] = downloadProgress[key]
    except:
        pass
    finally:
        lock.release()
    return data

class GetBalanceHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            startTime = data['startTime']
            endTime = data['endTime']
            response = await IOLoop.current().run_in_executor(None, get_balance, startTime, endTime)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_format_and_log(self, str(response)))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while getting total billing'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

class GetDetailedBillingHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            startTime = data['startTime']
            endTime = data['endTime']
            response = await IOLoop.current().run_in_executor(None, get_detailed_billing, startTime, endTime)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_format_and_log(self, str(response)))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while getting total billing'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

class DeleteMachineHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            uuid = data['uuid']
            response = await IOLoop.current().run_in_executor(None, delete_machine, uuid)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_format_and_log(self, str(response)))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while deleting machine'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

class CreatePortalHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            redirect = data['redirect']
            response = await IOLoop.current().run_in_executor(None, create_portal, redirect)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_format_and_log(self, str(response)))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while creating portal'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

class CreateCheckoutHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            items = data['items']
            redirect = data['redirect']
            response = await IOLoop.current().run_in_executor(None, create_checkout, items, redirect)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_format_and_log(self, str(response)))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while creating checkout'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

class CancelSubscriptionHandler(IPythonHandler):
    @authenticated
    async def get(self):
        try:
            response = await IOLoop.current().run_in_executor(None, cancel_subscription)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_format_and_log(self, str(response)))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while canceling subscription'}))
            jupyter_log.error(optumi_format_and_log(self, str(e)))
            if DEBUG: raise e

# Get a windows path in a format we can use on linux
def extract_drive_and_fix_path(path):
    # Extract the drive
    drive, path = os.path.splitdrive(path)

    # Switch slashes to correct direction
    path = path.replace('\\', '/')

    return drive, path

def setup_handlers(server_app):
    global jupyterDrive
    global jupyterHome
    global userHome
    global jupyter_log

    jupyter_log = server_app.log

    if dev_version: 
        jupyter_log.info(optumi_format_and_log(None, 'Optumi extension started'))
    else:
        optumi_format_and_log(None, 'Optumi extension started')

    web_app = server_app.web_app
    base_url = web_app.settings['base_url']
    jupyterDrive, jupyterHome = extract_drive_and_fix_path(os.path.expanduser(web_app.settings['server_root_dir']))
    userHome = extract_drive_and_fix_path(os.path.expanduser('~'))[1]
    host_pattern = '.*$'
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/version'), VersionHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/login'), LoginHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/check-login'), CheckLoginHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/oauth-callback'), OauthCallbackHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/oauth-login'), OauthLoginHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/sign-agreement'), SignAgreementHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/get-user-information'), GetUserInformationHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/set-user-information'), SetUserInformationHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/logout'), LogoutHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/preview-notebook'), PreviewNotebookHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/setup-notebook'), SetupNotebookHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/launch-notebook'), LaunchNotebookHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/get-login-progress'), GetLoginProgressHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/get-launch-status'), GetLaunchStatusHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/get-compression-progress'), GetCompressionProgressHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/get-upload-progress'), GetUploadProgressHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/stop-notebook'), StopNotebookHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/teardown-notebook'), TeardownNotebookHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/get-machines'), GetMachinesHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/get-notebook-config'), GetNotebookConfigHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/set-notebook-config'), SetNotebookConfigHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/pull-package-update'), PullPackageUpdateHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/push-package-update'), PushPackageUpdateHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/get-integrations'), GetIntegrationsHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/add-integration'), AddIntegrationHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/remove-integration'), RemoveIntegrationHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/push-workload-initializing-update'), PushWorkloadInitializingUpdateHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/pull-workload-status-updates'), PullWorkloadStatusUpdatesHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/pull-workload-config'), PullWorkloadConfigHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/push-workload-config'), PushWorkloadConfigHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/pull-module-status-updates'), PullModuleStatusUpdateHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/upload-files'), UploadFilesHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/cancel-progress'), CancelProgressHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/delete-files'), DeleteFilesHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/list-files'), ListFilesHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/download-files'), DownloadFilesHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/get-notebook-output-files'), GetNotebookOutputFilesHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/get-download-progress'), GetDownloadProgressHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/get-balance'), GetBalanceHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/get-detailed-billing'), GetDetailedBillingHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/delete-machine'), DeleteMachineHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/create-portal'), CreatePortalHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/create-checkout'), CreateCheckoutHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/cancel-subscription'), CancelSubscriptionHandler)])

###############################################################################################
####    Login
####

def install_auth_opener(login_domain, token):
    policy = DefaultCookiePolicy(allowed_domains=[login_domain])
    cj = CookieJar(policy)
    ctx = ssl.create_default_context()
    ## If we want to move back to devserver certificate we need to disable the hostname check
    # ctx.check_hostname = False
    opener = request.build_opener(request.HTTPCookieProcessor(cj), request.HTTPSHandler(context=ctx))
    request.install_opener(opener)
    info = urlencode({'login_type': 'oauth', "username": '', "password": token}).encode('utf8')
    return info

def login_rest_server(login_domain, login_port, token, start_time=None, last_domain_and_port=None):
    global loginProgress
    try:
        while True:
            if start_time == None:
                start_time = time.time()
            elif time.time() - start_time > 600:  # 10 minute timeout
                return -1, "Timed out"
            ## If we want to move back to devserver certificate we need to check for devserver.optumi.com explicitly
            # Since we are bypassing the hostname check for the SSL context, we manually check it here
            # cert = ssl.get_server_certificate((DOMAIN, 8443))
            # cert = x509.load_pem_x509_certificate(cert.encode(), default_backend())
            # name = cert.subject.get_attributes_for_oid(x509.oid.NameOID.COMMON_NAME)[0].value
            # if name != 'devserver.optumi.com':
            #     raise ssl.SSLCertVerificationError("SSL domain check failed (" + name + " is not devserver.optumi.com)")

            login_domain_and_port = login_domain + ':' + str(login_port)

            URL = get_path(login_domain_and_port) + '/login'
            errorURL = URL + '?error'

            # We only want to print to the log when we try to contact somewhere new
            if login_domain_and_port != last_domain_and_port: 
                if dev_version: 
                    jupyter_log.info(optumi_format_and_log(None, 'Contacting ' + URL))
                else:
                    optumi_format_and_log(None, 'Contacting ' + URL)

            req = request.Request(URL, data=install_auth_opener(login_domain, token))
            
            # since it can take a long time to log in to actually log in to the station, set a longer timeout for that request
            timeout = 30 if login_domain_and_port == PORTAL_DOMAIN_AND_PORT or login_domain_and_port == "portal.optumi.net:" + str(PORTAL_PORT) else 120

            try:
                response = request.urlopen(req, timeout=timeout)
            except URLError as err:
                if isinstance(err.reason, socket.timeout):
                    return -1, "Timed out"
                if isinstance(err.reason, socket.gaierror):
                    if login_domain_and_port == PORTAL_DOMAIN_AND_PORT or login_domain_and_port == "portal.optumi.net:" + str(PORTAL_PORT):
                        # If we failed trying to access portalAB.optumi.net or portal.optumi.net, redirect to the top level portal.optumi.net
                        login_domain = "portal.optumi.net"
                        login_port = PORTAL_PORT
                        last_domain_and_port = login_domain_and_port
                        continue
                    else:
                        # If we were trying to access a station, redirect to portalAB.optumi.net
                        login_domain = PORTAL
                        login_port = PORTAL_PORT
                        last_domain_and_port = login_domain_and_port
                        continue
                if (isinstance(err.reason, ConnectionRefusedError)):
                    time.sleep(2)
                    login_domain = login_domain
                    login_port = login_port
                    last_domain_and_port = login_domain_and_port
                    continue
                raise err

            if response.geturl() == errorURL:
                # Parse the error message to pass on to the user
                raw_html = response.read().decode()
                try:
                    message = raw_html.split('<div class="alert alert-danger" role="alert">')[1].split('</div>')[0]
                except:
                    message = "Invalid username/password"

                if message.startswith('Redirect to: '):
                    raw  = message.replace('Redirect to: ', '', 1)
                    redirect = json.loads(html.unescape(raw))
                    if redirect['dnsName'] == 'unknown':
                        loginProgress = 'Allocating...'
                        time.sleep(2)
                        login_domain = login_domain
                        login_port = login_port
                        last_domain_and_port = login_domain_and_port
                        continue
                    elif redirect['dnsName'] == 'no more stations' or redirect['dnsName'] == 'no more trial stations':
                        return -1, redirect['dnsName']
                    else:
                        loginProgress = 'Restoring context...'
                        login_domain = redirect['dnsName']
                        login_port = redirect['port']
                        last_domain_and_port = login_domain_and_port
                        continue
                return -1, message
            # On success return the status value 1 and the domain that we logged in to
            return 1, login_domain_and_port
    except Exception as err:
        jupyter_log.error(optumi_format_and_log(None, str(err)))
        traceback.print_exc()
        return -2, ""

def logout():
    URL = get_path() + '/logout'
    try:
        try:
            lock.acquire()
            # These maps are no longer relevant
            compressionProgress = {}
            uploadProgress = {}
            launchStatus = {}
            downloadProgress = {}
        except:
            pass
        finally:
            lock.release()
        req = request.Request(URL)
        return request.urlopen(req, timeout=120)
    except HTTPError as e:
        return e

###############################################################################################
####    Optumi REST Interface
####

def sign_agreement(timeOfSigning, hashOfSignedAgreement):
    URL = get_path() + '/exp/jupyterlab/sign-agreement'
    try:
        form = MultiPartForm()
        form.add_field('timeOfSigning', timeOfSigning)
        form.add_field('hashOfSignedAgreement', hashOfSignedAgreement)
        data = bytes(form)
        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req, timeout=120)
    except HTTPError as e:
        return e

def get_new_agreement():
    URL = get_path() + '/exp/jupyterlab/get-new-agreement'
    try:
        req = request.Request(URL)
        return request.urlopen(req, timeout=120)
    except HTTPError as e:
        return e

def exchange_versions(version):
    URL = get_path() + '/exp/jupyterlab/exchange-versions'
    try:
        form = MultiPartForm()
        form.add_field('version', version)
        data = bytes(form)
        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req, timeout=120)
    except HTTPError as e:
        return e

def get_user_information(includeAll):
    URL = get_path() + '/exp/jupyterlab/get-user-information'
    try:
        form = MultiPartForm()
        form.add_field('includeAll', str(includeAll))
        data = bytes(form)
        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req, timeout=120)
    except HTTPError as e:
        return e

def set_user_information(param, value):
    URL = get_path() + '/exp/jupyterlab/set-user-information'
    try:
        form = MultiPartForm()
        form.add_field('param', param)
        form.add_field('value', str(value))
        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req, timeout=120)
    except HTTPError as e:
        return e

def preview_notebook(nbConfig, includeExisting):
    URL = get_path() + '/exp/jupyterlab/preview-notebook'
    try:
        form = MultiPartForm()
        ## Send this string as a file since it can have arbitrary length and cause issues for the REST Interface if sent as a string
        form.add_file('nbConfig', 'nbConfig', fileHandle=io.BytesIO(nbConfig.encode('utf-8')))
        form.add_field('includeExisting', str(includeExisting))

        # Build the request, including the byte-string
        # for the data to be posted.
        data = bytes(form)
        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req, timeout=120)
    except HTTPError as e:
        return e

def setup_notebook(name, timestamp, notebook, nbConfig):
    URL = get_path() + '/exp/jupyterlab/setup-notebook'
    try:
        form = MultiPartForm()
        form.add_field('name', name)
        form.add_field('timestamp', timestamp)
        form.add_file('notebook', notebook['path'], fileHandle=io.BytesIO(notebook['content'].encode('utf-8')))
        ## Send this string as a file since it can have arbitrary length and cause issues for the REST Interface if sent as a string
        form.add_file('nbConfig', 'nbConfig', fileHandle=io.BytesIO(nbConfig.encode('utf-8')))
        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req, timeout=120)
    except HTTPError as e:
        return e

def launch_notebook(requirementsFile, hashes, paths, creationTimes, lastModificationTimes, sizes, uuid, timestamp):
    URL = get_path() + '/exp/jupyterlab/launch-notebook'
    try:
        form = MultiPartForm()
        form.add_field('uuid', uuid)
        ## Send this list as a file since it can have arbitrary length and cause issues for the REST Interface if sent as an array
        form.add_file('hashes', 'hashes', fileHandle=io.BytesIO(','.join(hashes).encode('utf-8')))
        form.add_file('paths', 'paths', fileHandle=io.BytesIO(','.join(paths).encode('utf-8')))
        form.add_file('creationTimes', 'creationTimes', fileHandle=io.BytesIO(','.join(creationTimes).encode('utf-8')))
        form.add_file('lastModificationTimes', 'lastModificationTimes', fileHandle=io.BytesIO(','.join(lastModificationTimes).encode('utf-8')))
        form.add_file('sizes', 'sizes', fileHandle=io.BytesIO(','.join(sizes).encode('utf-8')))
        form.add_field('timestamp', timestamp)
        form.add_field('jupyterDrive', jupyterDrive)
        form.add_field('jupyterHome', jupyterHome)
        form.add_field('userHome', userHome)

        try:
            lock.acquire()
            if uuid in launchStatus and 'status' in launchStatus[uuid] and launchStatus[uuid]['status'] == "Failed":
                raise CanceledError("Job canceled")
            launchStatus[uuid] = {'status': 'Started'}
        except CanceledError:
            raise
        except:
            pass
        finally:
            lock.release()
        if requirementsFile != None:
            form.add_file('requirementsFile', 'requirements.txt', fileHandle=io.BytesIO(requirementsFile.encode('utf-8')))

        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        response = request.urlopen(req, timeout=120)
        try:
            lock.acquire()
            if response.getcode() == 200:
                launchStatus[uuid] = json.loads(response.read())
                launchStatus[uuid]['status'] = "Finished"
        except:
            pass
        finally:
            lock.release()
    except:
        try:
            lock.acquire()
            launchStatus[uuid]['status'] = "Failed"
        except:
            pass
        finally:
            lock.release()
        raise

def stop_notebook(workload, module):
    URL = get_path() + '/exp/jupyterlab/stop-notebook'
    try:
        form = MultiPartForm()
        form.add_field('workload', workload)
        form.add_field('module', module)
        data = bytes(form)

        try:
            lock.acquire()
            launchStatus[uuid]['status'] = "Failed"
        except:
            pass
        finally:
            lock.release()

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req, timeout=120)
    except HTTPError as e:
        return e

def teardown_notebook(workload, module):
    URL = get_path() + '/exp/jupyterlab/teardown-notebook'
    try:
        form = MultiPartForm()
        form.add_field('workload', workload)
        form.add_field('module', module)
        data = bytes(form)

        try:
            lock.acquire()
            launchStatus[uuid]['status'] = "Failed"
        except:
            pass
        finally:
            lock.release()

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req, timeout=120)
    except HTTPError as e:
        return e

def upload_cleanup(key, pairs):
    for response, path in pairs:
        response.read()
        try:
            lock.acquire()
            uploadProgress[key]['progress'] = -1
        except:
            pass
        finally:
            lock.release()
        if path != None:
            try:
                os.remove(path)
            except Exception as e:
                jupyter_log.error(optumi_format_and_log(self, str(e)))

def upload_files(key, paths, compress, storageTotal, storageLimit, autoAddOnsEnabled):
    URL = get_path() + '/exp/jupyterlab/upload-files'
    try: 
        filesToUpload = []
        ## Check for files in chunks of 1000
        while len(paths) > 1000:
            chunk = paths[:1000]
            for exists, file in zip(json.load(check_if_files_exist(chunk))['exists'], chunk):
                if not exists:
                    stat = os.stat(file)
                    created = datetime.datetime.utcfromtimestamp(stat.st_ctime).isoformat() + 'Z'
                    lastModified = datetime.datetime.utcfromtimestamp(stat.st_mtime).isoformat() + 'Z'
                    filesToUpload.append((file, os.path.getsize(file), created, lastModified))
            paths = paths[1000:]
        ## Check last chunk
        for exists, file in zip(json.load(check_if_files_exist(paths))['exists'], paths):
            if not exists:
                stat = os.stat(file)
                created = datetime.datetime.utcfromtimestamp(stat.st_ctime).isoformat() + 'Z'
                lastModified = datetime.datetime.utcfromtimestamp(stat.st_mtime).isoformat() + 'Z'
                filesToUpload.append((file, os.path.getsize(file), created, lastModified))
        
        # Check if the user aborted while we were getting file sizes, setting things up
        try:
            lock.acquire()
            if key in compressionProgress:
                # Handle the case where compression was canceled
                if compressionProgress[key]['progress'] == -1:
                    raise CanceledError("Compression canceled")
        except CanceledError as e:
            raise e
        except Exception as e:
            pass
        finally:
            lock.release()

        if len(filesToUpload) > 0:
            # Check if the user has enough space left in his storage account to upload the file
            uploadTotal = sum([x[1] for x in filesToUpload])

            if (not autoAddOnsEnabled) and (uploadTotal + storageTotal > storageLimit):
                try:
                    lock.acquire()
                    # See FileTracker.ts for error values (look at UploadStatus)
                    compressionProgress[key] = { 'progress': -2 }
                    uploadProgress[key] = { 'progress': -1 }
                except Exception as e:
                    pass
                finally:
                    lock.release()
                # We want to bail out of this upload
                return

            # Sort by file size
            filesToUpload.sort(key=lambda x:x[1], reverse=True)

            if compress:
                try:
                    lock.acquire()
                    compressionProgress[key] = {'progress': 0, 'total': len(filesToUpload)}
                except Exception as e:
                    pass
                finally:
                    lock.release()

            MAX_SIZE = 5 * 1024 * 1024 * 1024

            fileChunks = [[]]
            metadataChunks = [{}]
            totalSize = 0
            for file, size, created, lastModified in filesToUpload:
                # Check if the user aborted before we process and potentially compress a new file
                try:
                    lock.acquire()
                    if key in compressionProgress:
                        # Handle the case where compression was canceled
                        if compressionProgress[key]['progress'] == -1:
                            raise CanceledError("Compression canceled")
                except CanceledError as e:
                    raise e
                except Exception as e:
                    pass
                finally:
                    lock.release()

                if size > MAX_SIZE:
                    jupyter_log.error(optumi_format_and_log(self, 'Skipping upload of files ' + str(paths) + ", file " + file + " exceeds " + str(MAX_SIZE) + " limit"))
                    try:
                        lock.acquire()
                        # See FileTracker.ts for error values (look at UploadStatus)
                        compressionProgress[key] = { 'progress': -3 }
                        uploadProgress[key] = { 'progress': -1 }
                    except Exception as e:
                        pass
                    finally:
                        lock.release()
                    # We want to bail out of this upload
                    return
                elif totalSize + size > MAX_SIZE:
                    # If the next file takes us over 5GB, this is the end of the chunk
                    if compress:
                        zipFile = zip_files(key, str(len(fileChunks)), fileChunks[-1])
                        fileChunks[-1] = [zipFile]
                        
                    # Reset variables for the next chunk of files
                    fileChunks.append([])
                    metadataChunks.append({})
                    totalSize = 0
                else: 
                    fileChunks[-1].append(file if compress else extract_drive_and_fix_path(file)[1])
                    metadataChunks[-1][extract_drive_and_fix_path(file)[1]] = { 'created': created, 'lastModified': lastModified }
                    totalSize += size

            # Compress the last chunk if necessary
            if compress:
                zipFile = zip_files(key, str(len(fileChunks)), fileChunks[-1])
                fileChunks[-1] = [zipFile]

            # We need to add up the total upload size before we start uploading
            totalSize = 0
            for chunk in fileChunks:
                for file in chunk:
                    totalSize += os.path.getsize(file)
            try:
                lock.acquire()
                if key in compressionProgress:
                    # Handle the case where compression was canceled
                    if compressionProgress[key]['progress'] == -1:
                        raise CanceledError("Compression canceled")
                    compressionProgress[key]['progress'] = -1
                uploadProgress[key] = { 'progress': 0, 'total': totalSize }
            except CanceledError as e:
                raise e
            except Exception as e:
                pass
            finally:
                lock.release()

            responses = []
            for chunk, metadata in zip(fileChunks, metadataChunks):
                form = MultiPartForm()
                for file in chunk:
                    form.add_file('files', file, fileHandle=open(file, 'rb'))
                
                form.add_file('metadata', 'metadata', fileHandle=io.BytesIO(json.dumps(metadata).encode('utf-8')))

                form.add_field('jupyterHome', jupyterHome)
                form.add_field('userHome', userHome)
                form.add_field('compressed', str(compress))

                b = bytes(form)
                data = UploadProgressOpener(b, key)

                req = request.Request(URL, data=data)
                req.add_header('Content-type', form.get_content_type())
                req.add_header('Content-length', len(data))
                res = request.urlopen(req, timeout=14400) # 4 hour timeout
                if compress:
                    responses.append((res, chunk[0]))
                else:
                    responses.append((res, None))

                # This thread will set the upload state to none when it is finished
                Thread(target=upload_cleanup, args = (key, responses, )).start()
        else:
            # We want to record the no files need to be uploaded, otherwise the extension will keep asking
            try:
                lock.acquire()
                if compress:
                    compressionProgress[key] = {'progress': -1, 'total': 0 }
                uploadProgress[key] = {'progress': -1, 'total': 0 }
            except Exception as e:
                pass
            finally:
                lock.release()
    except CanceledError as e:
        cleanup_progress(e, compress)
        if e.pathToRemove and os.path.exists(e.pathToRemove):
            os.remove(e.pathToRemove)
        return e
    except HTTPError as e:
        cleanup_progress(e, compress)
        return e

def cleanup_progress(e, compress):
    # Clean up ongoing progress in the case of a failure
    try:
        lock.acquire()
        if compress:
            # Cancel compression progress
            if key in compressionProgress:
                compressionProgress[key] = {'progress': -1, 'total': 0 }
        # Cancel upload progress
        if key in uploadProgress:
            uploadProgress[key] = {'progress': -1, 'total': 0 }
    except Exception:
        pass
    finally:
        lock.release()

def check_if_files_exist(paths):
    URL = get_path() + '/exp/jupyterlab/check-if-files-exist'
    try:
        form = MultiPartForm()
        ## Send this list as a file since it can have arbitrary length and cause issues for the REST Interface if sent as an array
        form.add_file('paths', 'paths', fileHandle=io.BytesIO(','.join([extract_drive_and_fix_path(file)[1] for file in paths]).encode('utf-8')))
        form.add_file('hashes', 'hashes', fileHandle=io.BytesIO(','.join([hash_file(f) for f in paths]).encode('utf-8')))
        form.add_file('sizes', 'sizes', fileHandle=io.BytesIO(','.join([str(os.path.getsize(f)) for f in paths]).encode('utf-8')))
        stats = [os.stat(f) if os.path.isfile(f) else None for f in paths]
        creationTimes = [datetime.datetime.utcfromtimestamp(stat.st_ctime).isoformat() + 'Z' if stat != None else str(None) for stat in stats]
        lastModificationTimes = [datetime.datetime.utcfromtimestamp(stat.st_mtime).isoformat() + 'Z' if stat != None else str(None) for stat in stats]
        form.add_file('creationTimes', 'creationTimes', fileHandle=io.BytesIO(','.join(creationTimes).encode('utf-8')))
        form.add_file('lastModificationTimes', 'lastModificationTimes', fileHandle=io.BytesIO(','.join(lastModificationTimes).encode('utf-8')))
        form.add_field('userHome', jupyterHome)
        form.add_field('jupyterHome', jupyterHome)
        form.add_field('autoAdd', str(True))
        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req, timeout=120)
    except HTTPError as e:
        return e

def get_machines():
    URL = get_path() + '/exp/jupyterlab/get-machines'
    try:
        req = request.Request(URL)
        return request.urlopen(req, timeout=120)
    except HTTPError as e:
        return e

def pull_workload_config(workload):
    URL = get_path() + '/exp/jupyterlab/pull-workload-config'
    try:
        form = MultiPartForm()
        form.add_field('workload', workload)
        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req, timeout=120)
    except HTTPError as e:
        return e

def push_workload_config(workload, nbConfig):
    URL = get_path() + '/exp/jupyterlab/push-workload-config'
    try:
        form = MultiPartForm()
        form.add_field('workload', workload)
        form.add_field('nbConfig', nbConfig)
        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req, timeout=120)
    except HTTPError as e:
        return e

def get_notebook_config(nbKey):
    URL = get_path() + '/exp/jupyterlab/get-notebook-config'
    try:
        form = MultiPartForm()
        form.add_field('nbKey', nbKey)
        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req, timeout=120)
    except HTTPError as e:
        return e

def set_notebook_config(nbKey, nbConfig):
    URL = get_path() + '/exp/jupyterlab/set-notebook-config'
    try:
        form = MultiPartForm()
        form.add_field('nbKey', nbKey)
        form.add_field('nbConfig', nbConfig)
        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req, timeout=120)
    except HTTPError as e:
        return e

def pull_package_update(nbKeys):
    URL = get_path() + '/exp/jupyterlab/pull-package-update'
    try:
        form = MultiPartForm()
        # We need to send something in the body of this message otherwise the POST will fail
        if len(nbKeys) == 0:
            form.add_field('empty', str(True))
        for nbKey in nbKeys:
            form.add_field('nbKeys', nbKey)
        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req, timeout=120)
    except HTTPError as e:
        return e

def push_package_update(nbKey, label, hashes, paths, update):
    URL = get_path() + '/exp/jupyterlab/push-package-update'
    try:
        form = MultiPartForm()
        form.add_field('nbKey', nbKey)
        if label != None: form.add_field('label', label)
        if paths != None:
            form.add_file('hashes', 'hashes', fileHandle=io.BytesIO(','.join(hashes).encode('utf-8')))
            form.add_file('paths', 'paths', fileHandle=io.BytesIO(','.join(paths).encode('utf-8')))
        form.add_file('update', 'update', fileHandle=io.BytesIO(update.encode('utf-8')))
        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req, timeout=120)
    except HTTPError as e:
        return e

def get_integrations():
    URL = get_path() + '/exp/jupyterlab/get-integrations'
    try:
        req = request.Request(URL)
        return request.urlopen(req, timeout=120)
    except HTTPError as e:
        return e

def add_integration(name, info):
    URL = get_path() + '/exp/jupyterlab/add-integration'
    try:
        form = MultiPartForm()
        form.add_field('name', name)
        form.add_field('info', info)
        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req, timeout=120)
    except HTTPError as e:
        return e

def remove_integration(name):
    URL = get_path() + '/exp/jupyterlab/remove-integration'
    try:
        form = MultiPartForm()
        form.add_field('name', name)
        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req, timeout=120)
    except HTTPError as e:
        return e

def push_workload_initializing_update(uuid, update):
    URL = get_path() + '/exp/jupyterlab/push-workload-initializing-update'
    try:
        form = MultiPartForm()
        form.add_field('uuid', uuid)
        form.add_field('update', update)
        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req, timeout=120)
    except HTTPError as e:
        return e

def pull_workload_status_updates(uuids, lastInitializingLines, lastPreparingLines, lastRunningLines):
    URL = get_path() + '/exp/jupyterlab/pull-workload-status-updates'
    try:
        form = MultiPartForm()
        for uuid in uuids:
            form.add_field('uuids', uuid)
        for lastInitializingLine in lastInitializingLines:
            form.add_field('lastInitializingLines', str(lastInitializingLine))
        for lastPreparingLine in lastPreparingLines:
            form.add_field('lastPreparingLines', str(lastPreparingLine))
        for lastRunningLine in lastRunningLines:
            form.add_field('lastRunningLines', str(lastRunningLine))
        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req, timeout=120)
    except HTTPError as e:
        return e

def pull_module_status_updates(workloadUUIDs, moduleUUIDs, lastUpdateLines, lastOutputLines, lastMonitorings, lastPatches):
    URL = get_path() + '/exp/jupyterlab/pull-module-status-updates'
    try:
        form = MultiPartForm()
        for workloadUUID in workloadUUIDs:
            form.add_field('workloadUUIDs', workloadUUID)
        for moduleUUID in moduleUUIDs:
            form.add_field('moduleUUIDs', moduleUUID)
        for lastUpdateLine in lastUpdateLines:
            form.add_field('lastUpdateLines', str(lastUpdateLine))
        for lastOutputLine in lastOutputLines:
            form.add_field('lastOutputLines', str(lastOutputLine))
        if lastMonitorings != None:
            for lastMonitoring in lastMonitorings:
                form.add_field('lastMonitorings', str(lastMonitoring))
        for lastPatch in lastPatches:
            form.add_field('lastPatches', str(lastPatch))
        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req, timeout=120)
    except HTTPError as e:
        return e

def list_files():
    URL = get_path() + '/exp/jupyterlab/list-files'
    try:
        req = request.Request(URL)
        return request.urlopen(req, timeout=120)
    except HTTPError as e:
        return e

def delete_files(hashes, paths, creationTimes, directory):
    URL = get_path() + '/exp/jupyterlab/delete-files'
    try:
        form = MultiPartForm()
        form.add_file('hashes', 'hashes', fileHandle=io.BytesIO(','.join(hashes).encode('utf-8')))
        form.add_file('paths', 'paths', fileHandle=io.BytesIO(','.join(paths).encode('utf-8')))
        form.add_file('creationTimes', 'creationTimes', fileHandle=io.BytesIO(','.join(creationTimes).encode('utf-8')))
        form.add_field('directory', directory)
        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req, timeout=120)
    except HTTPError as e:
        return e

def save_file(fileName, content, overwrite):
    file = os.path.expanduser(fileName)
    if not overwrite:
        newName = file
        num = 1
        while os.path.exists(newName) and os.path.isfile(newName):
            f, ext = os.path.splitext(file)
            newName = f + '(' + str(num) + ')' + ext
            num += 1
        file = newName
    dirs = os.path.dirname(file)
    if dirs != "":
        os.makedirs(dirs, exist_ok=True)
    with open(file, "wb") as f:
        f.write(base64.decodebytes(content.getvalue()))

def add_content(content, decoded):
    # Remove starting or ending " so we can look at only , when splitting the string
    if decoded != '' and decoded[0] == '"':
        decoded = decoded[1:]
    if decoded != '' and decoded[-1] == '"':
        decoded = decoded[:-1]
    encoded = decoded.encode('ascii')
    content.write(encoded)

def download_files_helper(URL, formHashes, fileNames, savePaths, overwrite):
    form = MultiPartForm()
    form.add_file('hashes', 'hashes', fileHandle=io.BytesIO(','.join(formHashes).encode('utf-8')))
    form.add_file('paths', 'paths', fileHandle=io.BytesIO(','.join(fileNames).encode('utf-8')))

    data = bytes(form)

    req = request.Request(URL, data=data)
    req.add_header('Content-type', form.get_content_type())
    req.add_header('Content-length', len(data))

    response = request.urlopen(req, timeout=120)

    blocksize = 4096
    
    content = io.BytesIO()
    while True:
        read = response.read(blocksize)
        if not read:
            break
        decoded = read.decode("ascii")
        if decoded != '' and decoded[0] == '[':
            # Remove the opening ["
            decoded = decoded[1:]
        if decoded != '' and decoded[-1] == ']':
            # Remove the ending "]"
            decoded = decoded[:-1]
        if ',' in decoded:
            split = decoded.split(',')
            for chunk in split[:-1]:
                add_content(content, chunk)
                save_file(savePaths.pop(0), content, overwrite)
                content = io.BytesIO()
            # Handle the last chunk like the else case below
            add_content(content, split[-1])
        else:
            add_content(content, decoded)

    # Save the last file
    save_file(savePaths.pop(0), content, overwrite)

def download_file_chunk_helper(hash, fileName, savePath, size, overwrite):
    URL = get_path() + '/exp/jupyterlab/download-file-chunk'

    # Start with chunk thats 1 percent of the total size
    CHUNK_SIZE = size // 100
    # Round to the nearest megabyte for cleanliness
    CHUNK_SIZE = math.ceil(CHUNK_SIZE / (1024 * 1024)) * (1024 * 1024)
    # Apply min and max
    if CHUNK_SIZE < MIN_CHUNK_SIZE: CHUNK_SIZE = MIN_CHUNK_SIZE
    if CHUNK_SIZE > MAX_CHUNK_SIZE: CHUNK_SIZE = MAX_CHUNK_SIZE

    # Set up file
    file = os.path.expanduser(savePath)
    if not overwrite:
        newName = file
        num = 1
        while os.path.exists(newName) and os.path.isfile(newName):
            f, ext = os.path.splitext(file)
            newName = f + '(' + str(num) + ')' + ext
            num += 1
        file = newName
    dirs = os.path.dirname(file)
    if dirs != "":
        os.makedirs(dirs, exist_ok=True)
    f = open(file, "wb")

    offset = 0

    while True:
        form = MultiPartForm()
        form.add_field('hash', hash)
        form.add_field('offset', str(offset))
        form.add_field('chunkSize', str(CHUNK_SIZE))

        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))

        response = request.urlopen(req, timeout=120)
        chunk = response.read()
        
        offset += len(chunk)

        if not chunk:
            break
            
        f.write(chunk)

    f.close()

def download_files(key, hashes, paths, sizes, overwrite, directory):
    URL = get_path() + '/exp/jupyterlab/download-files'

    try:
        total = sum(sizes)
        try:
            lock.acquire()
            downloadProgress[key] = { 'progress': 0, 'total': total }
        except:
            pass
        finally:
            lock.release()

        savePaths = paths

        if directory != None:
            dirs = os.path.expanduser(directory)
            if not overwrite:
                newName = dirs
                num = 0
                while os.path.exists(newName) and os.path.isdir(newName):
                    num += 1
                    newName = dirs + '(' + str(num) + ')'
            if num > 0:
                savePaths = [path.replace(directory, directory + '(' + str(num) + ')', 1) for path in savePaths]

        filesToDownload = zip(hashes, paths, savePaths, sizes)
        # Sort by file size
        filesToDownload = sorted(filesToDownload, key=lambda x:x[3])

        # These files will be aggregated in a group with a max size of CUTOFF_SIZE, and downloaded as a group
        groupFiles = [x for x in filesToDownload if x[3] < CUTOFF_SIZE]
        # These files will be download individually in chunks of CHUNK_SIZE
        chunkFiles = [x for x in filesToDownload if x[3] >= CUTOFF_SIZE]

        # download group files
        totalSize = 0
        formHashes = []
        fileNames = []
        saveNames = []
        for hash, file, savePath, size in groupFiles:
            if totalSize + size > CUTOFF_SIZE:
                download_files_helper(URL, formHashes, fileNames, saveNames, overwrite)

                # Reset variables for the next chunk of files
                totalSize = 0
                formHashes = []
                fileNames = []
                saveNames = []
            totalSize += size
            formHashes.append(hash)
            fileNames.append(file)
            saveNames.append(savePath)

        if len(saveNames) > 0:
            # Download the remaining files
            download_files_helper(URL, formHashes, fileNames, saveNames, overwrite)

        for hash, file, savePath, size in chunkFiles:
            download_file_chunk_helper(hash, file, savePath, size, overwrite)

        # Make sure we mark the download as completed
        try:
            lock.acquire()
            downloadProgress[key] = { 'progress': -1, 'total': total }
        except:
            pass
        finally:
            lock.release()

        return
    except HTTPError as e:
        return e

def get_notebook_output_files(workloadUUID, moduleUUID, key, paths, sizes, overwrite, directory):
    URL = get_path() + '/exp/jupyterlab/get-notebook-output-file'

    try:
        # Tell the controller to put the files in blob storage early, this will return the hashes, which we need to download the files
        form = MultiPartForm()
        form.add_field('workloadUUID', workloadUUID)
        form.add_field('moduleUUID', moduleUUID)
        form.add_file('paths', 'paths', fileHandle=io.BytesIO(','.join(paths).encode('utf-8')))

        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))

        response = request.urlopen(req, timeout=600)
        hashes = json.loads(response.read())

        # Download the files
        return download_files(key, hashes, paths, sizes, overwrite, directory)
    except HTTPError as e:
        return e

def get_balance(startTime, endTime):
    URL = get_path() + '/exp/jupyterlab/get-balance'
    try:
        form = MultiPartForm()
        form.add_field('startTime', startTime)
        form.add_field('endTime', endTime)
        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req, timeout=120)
    except HTTPError as e:
        return e

def get_detailed_billing(startTime, endTime):
    URL = get_path() + '/exp/jupyterlab/get-detailed-billing'
    try:
        form = MultiPartForm()
        form.add_field('startTime', startTime)
        form.add_field('endTime', endTime)
        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req, timeout=120)
    except HTTPError as e:
        return e

def delete_machine(uuid):
    URL = get_path() + '/exp/jupyterlab/release-machine'
    try:
        form = MultiPartForm()
        form.add_field('uuid', uuid)
        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req, timeout=120)
    except HTTPError as e:
        return e

def change_password(loginName, oldPassword, newPassword):
    URL = get_path() + '/exp/jupyterlab/change-password'
    try:
        form = MultiPartForm()
        form.add_field('loginName', loginName)
        form.add_field('oldPassword', oldPassword)
        form.add_field('newPassword', newPassword)
        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req, timeout=120)
    except HTTPError as e:
        return e

def create_portal(redirect):
    URL = get_path() + '/exp/jupyterlab/create-portal'
    try:
        form = MultiPartForm()
        form.add_field('redirect', redirect)
        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req, timeout=120)
    except HTTPError as e:
        return e

def create_checkout(items, redirect):
    URL = get_path() + '/exp/jupyterlab/create-checkout'
    try:
        form = MultiPartForm()
        for item in items:
            form.add_field('items', item)
        form.add_field('redirect', redirect)
        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req, timeout=120)
    except HTTPError as e:
        return e

def cancel_subscription():
    URL = get_path() + '/exp/jupyterlab/cancel-subscription'
    try:
        req = request.Request(URL)
        return request.urlopen(req, timeout=120)
    except HTTPError as e:
        return e

###############################################################################################
####    Hash files
####

def hash_file(fileName):
    if os.path.isfile(fileName):
        BLOCKSIZE = 65536
        hasher = hashlib.md5()
        with open(fileName, 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)
        return hasher.hexdigest().upper()
    return str(None)

###############################################################################################
####    Zip files
####

def zip_files(key, inc, files):
    # make the path safe for Linux and windows, while being unique
    path = '.' + re.sub(r'\W+', '', key + inc) + '.zip'
    # put the pack in the temp dir
    path = TEMP_DIR + '/' + path
    files.sort(key=lambda x: os.path.getsize(x))
    # make sure the Optumi temp dir exists
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    # writing files to a zipfile 
    with ZipFile(path, 'w', ZIP_DEFLATED) as zip:
        # writing each file one by one 
        for file in files:
            zip.write(file)
            try:
                lock.acquire()
                if compressionProgress[key]['progress'] == -1:
                    raise CanceledError("Compression canceled", path)
                compressionProgress[key]['progress'] = compressionProgress[key]['progress'] + 1
            except CanceledError:
                raise
            except:
                pass
            finally:
                lock.release()
    return path

###############################################################################################
####    Upload progress
####

class CanceledError(Exception):
    def __init__(self, message, pathToRemove=None):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        self.message = message
        self.pathToRemove = pathToRemove

class UploadProgressOpener:
    def __init__ (self, _bytes, key):
        self._f = io.BytesIO(_bytes)
        self._key = key
        self._total = len(_bytes)

    def __len__(self):
        return self._total

    def __enter__ (self):
        return self._f

    def __exit__ (self, exc_type, exc_value, traceback):
        self.f.close()

    def read(self, n_bytes=-1):
        data = self._f.read(n_bytes)
        try:
            lock.acquire()
            if uploadProgress[self._key]['progress'] == -1:
                raise CanceledError("Upload canceled")
            uploadProgress[self._key]['progress'] = uploadProgress[self._key]['progress'] + len(data)
        except CanceledError:
            raise
        except:
            pass
        finally:
            lock.release()
        return data

###############################################################################################
####    FormData
####

class MultiPartForm:
    """Accumulate the data to be used when posting a form."""

    def __init__(self):
        self.form_fields = []
        self.files = []
        # Use a large random byte string to separate
        # parts of the MIME data.
        self.boundary = uuid.uuid4().hex.encode('utf-8')
        return

    def get_content_type(self):
        return 'multipart/form-data; boundary={}'.format(
            self.boundary.decode('utf-8'))

    def add_field(self, name, value):
        """Add a simple field to the form data."""
        self.form_fields.append((name, value))

    def add_file(self, fieldname, filename, fileHandle,
                 mimetype=None):
        """Add a file to be uploaded."""
        body = fileHandle.read()
        if mimetype is None:
            mimetype = (
                mimetypes.guess_type(filename)[0] or
                'application/octet-stream'
            )
        self.files.append((fieldname, filename, mimetype, body))
        return

    @staticmethod
    def _form_data(name):
        return ('Content-Disposition: form-data; '
                'name="{}"\r\n').format(name).encode('utf-8')

    @staticmethod
    def _attached_file(name, filename):
        return ('Content-Disposition: form-data; '
                'name="{}"; filename="{}"\r\n').format(
                    name, filename).encode('utf-8')

    @staticmethod
    def _content_type(ct):
        return 'Content-Type: {}\r\n'.format(ct).encode('utf-8')

    def __bytes__(self):
        """Return a byte-string representing the form data,
        including attached files.
        """
        buffer = io.BytesIO()
        boundary = b'--' + self.boundary + b'\r\n'

        # Add the form fields
        for name, value in self.form_fields:
            buffer.write(boundary)
            buffer.write(self._form_data(name))
            buffer.write(b'\r\n')
            buffer.write(value.encode('utf-8'))
            buffer.write(b'\r\n')

        # Add the files to upload
        for f_name, filename, f_content_type, body in self.files:
            buffer.write(boundary)
            buffer.write(self._attached_file(f_name, filename))
            buffer.write(self._content_type(f_content_type))
            buffer.write(b'\r\n')
            buffer.write(body)
            buffer.write(b'\r\n')

        buffer.write(b'--' + self.boundary + b'--\r\n')
        return buffer.getvalue()
