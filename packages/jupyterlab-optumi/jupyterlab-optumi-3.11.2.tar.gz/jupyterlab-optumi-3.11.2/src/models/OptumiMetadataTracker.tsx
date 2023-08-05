/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { Global } from '../Global'

import { ServerConnection } from '@jupyterlab/services';
import { INotebookModel, NotebookPanel, NotebookTracker } from '@jupyterlab/notebook';
import { ISignal, Signal } from '@lumino/signaling';

import { OptumiConfig } from './OptumiConfig';
import { OptumiMetadata } from './OptumiMetadata';
import { NoMachine } from './machine/Machine';
import { FileMetadata } from '../components/deploy/fileBrowser/FileBrowser';

const PYTHON_STANDARD_IMPORTS = ['doctest', 'array', 'binhex', 'zlib', 'zipimport', 'code', 'tokenize', 'pickletools', 'struct', 'msilib', 'glob', 'wave', 'runpy', 'shlex', 'atexit', 'fileinput', 'poplib', 'ftplib', 'distutils', 'textwrap', 'gc', 'types', 'selectors', 'pprint', 'timeit', 'imghdr', 'dataclasses', 'imp', 'bisect', 'base64', 'xdrlib', 'pwd', 'pty', 'formatter', 'codecs', 'hashlib', 'ensurepip', 'chunk', 'winreg', 'zoneinfo', 'configparser', 'crypt', 'sched', 'sunau', 'dbm', 'tarfile', 'uu', '_thread', 'mmap', 'marshal', 'unicodedata', 'spwd', 'trace', 'symbol', 'functools', 'resource', 'sys', 'quopri', 'sysconfig', 'bdb', 'winsound', 'gzip', 'webbrowser', 'wsgiref', 'tkinter', 'zipapp', 'hmac', 'getpass', 'site', 'posix', 'html', 'filecmp', 'email', 'heapq', 'tabnanny', 'colorsys', 'smtplib', 'pkgutil', 'fcntl', 'parser', 'argparse', 'csv', 'audioop', 'venv', 'errno', 'ipaddress', 'socket', 'gettext', 'math', 'copy', 'tracemalloc', 'select', 'traceback', 'tty', 'getopt', 'xmlrpc', 'contextvars', 'binascii', 'builtins', 'numbers', 'cmd', 'threading', 'json', 'urllib', 'weakref', 'asyncore', 'rlcompleter', 'queue', 'token', 'reprlib', 'compileall', 'imaplib', 'ossaudiodev', 'operator', 'subprocess', 'asyncio', 'shelve', 'mimetypes', 'ast', 'locale', 'grp', 'decimal', 'difflib', 'concurrent', 'pathlib', 'io', 'nntplib', '__future__', 'pickle', 'sqlite3', 're', 'stringprep', 'abc', 'nis', 'tempfile', 'secrets', 'readline', 'smtpd', 'cmath', 'time', 'string', 'unittest', 'warnings', 'stat', 'faulthandler', 'signal', 'random', 'os', 'optparse', 'test', 'inspect', 'pdb', 'contextlib', 'calendar', 'plistlib', 'cgi', 'turtle', 'pipes', 'importlib', 'lzma', 'pydoc', 'sndhdr', 'typing', 'msvcrt', 'statistics', 'keyword', 'termios', 'ssl', '__main__', 'linecache', 'uuid', 'collections', 'logging', 'codeop', 'fnmatch', 'http', 'graphlib', 'ctypes', 'curses', 'datetime', 'mailbox', 'cgitb', 'xml', 'aifc', 'fractions', 'telnetlib', 'itertools', 'mailcap', 'netrc', 'symtable', 'socketserver', 'multiprocessing', 'pyclbr', 'asynchat', 'dis', 'py_compile', 'bz2', 'zipfile', 'syslog', 'enum', 'shutil', 'copyreg', 'platform', 'modulefinder']
const PYTHON_PACKAGE_TRANSLATIONS = new Map()
PYTHON_PACKAGE_TRANSLATIONS.set('cv2', 'opencv-python')
PYTHON_PACKAGE_TRANSLATIONS.set('mpl_toolkits', 'matplotlib')
PYTHON_PACKAGE_TRANSLATIONS.set('PIL', 'Pillow')
PYTHON_PACKAGE_TRANSLATIONS.set('pytorch_lightning', 'pytorch-lightning')
PYTHON_PACKAGE_TRANSLATIONS.set('scikitplot', 'scikit-plot')
PYTHON_PACKAGE_TRANSLATIONS.set('sklearn', 'scikit-learn')
PYTHON_PACKAGE_TRANSLATIONS.set('skopt', 'scikit-optimize')
PYTHON_PACKAGE_TRANSLATIONS.set('sherpa', 'parameter-sherpa')

// const UNOWNED_PACKAGES = 'other'

export class OptumiMetadataTracker {
    // Map of file path to metadata
    private _optumiMetadata = new Map<string, TrackedOptumiMetadata>();
    // // Map of notebook key to package
    // private _packages = new Map<string, Package[]>();

    private _configToSetAfterOpen = new Map<string, OptumiConfig>();

    private _tracker: NotebookTracker;

    constructor(tracker: NotebookTracker) {
        this._tracker = tracker;
        // We will have an entry ready for packages that we don't have a path for
        // this._packages.set(UNOWNED_PACKAGES, []);
        tracker.currentChanged.connect(() => {
            this.handleCurrentChanged(this._tracker.currentWidget);
        });
        this.handleCurrentChanged(this._tracker.currentWidget);
        // this.receiveUpdate();
	}

	private handleCurrentChanged = async (current: NotebookPanel) => {
        if (current == null) {
            if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
            setTimeout(() => this.handleCurrentChanged(this._tracker.currentWidget), 250);
            return;
        }
        Global.lastMachine  = new NoMachine();
        if (!current.context.isReady) await current.context.ready;
        // If the path changes we need to add a new entry into our map
        current.context.pathChanged.connect(() => this.handleCurrentChanged(current));
        const path = current.context.path;
        const rawMetadata = current.model.metadata;
        const oldMetadata = rawMetadata.get("optumi") || {}
        var metadata = new OptumiMetadata(oldMetadata);

        var trackedMetadata: TrackedOptumiMetadata;
        // Get the metadata from the controller, unless we have metadata that is waiting to be set
        var config = this._configToSetAfterOpen.get(path)
        if (!config) {
            config = (await this.fetchConfig(metadata));
        }

        // If this is a duplicated notebook, we want to give it a new uuid, but we will use the old uuid to pick up the config
        for (var entry of this._optumiMetadata) {
            if (entry[1].metadata.nbKey == metadata.nbKey && entry[0] != path) {
                metadata = new OptumiMetadata();
                metadata.nbKeyHistory.push(entry[1].metadata.nbKey);
            }
        }
        if (config) {
            trackedMetadata = new TrackedOptumiMetadata(path, metadata, config);

            trackedMetadata.metadata.version = Global.version;
            this._optumiMetadata.set(path, trackedMetadata);

            // // Initialize the packages if necessary
            // if (!this._packages.has(trackedMetadata.metadata.nbKey)) this._packages.set(trackedMetadata.metadata.nbKey, []);
            // for (let nbKey of trackedMetadata.metadata.nbKeyHistory) {
            //     if (!this._packages.has(nbKey)) this._packages.set(nbKey, []);
            // }

            // Save the metadata in the file to make sure all files have valid metadata
            rawMetadata.set("optumi", JSON.parse(JSON.stringify(metadata)));
            // Save the metadata to the controller, in case something was updated above
            this.setMetadata(trackedMetadata);

            // If we changed the metadata, save the notebook
            if (JSON.stringify(metadata) != JSON.stringify(oldMetadata)) current.context.save()
            // Once all of this is done, emit a signal that the metadata changed
            if (Global.shouldLogOnEmit) console.log('SignalEmit (' + new Date().getSeconds() + ')');
            this._metadataChanged.emit();
        }
	}

    private fetchConfig = (metadata: OptumiMetadata) : Promise<OptumiConfig> => {
        // If there is no user signed in, there is no config
        if (Global.user == null) return Promise.resolve(undefined);
        // Fetch the config for this user + notebook from the controller
        const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/get-notebook-config";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				nbKey: metadata.nbKey,
			}),
		};
		return ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response)
            return response.text();
		}).then((response: string) => {
            try {
                var map = {};
                map = JSON.parse(response);
                return new OptumiConfig(map, metadata.version);
            } catch (err) { if (response != '') console.error(err) }
            return new OptumiConfig();
        }, (error:any) => {
            console.error(error);
            return undefined;
        });
    }

    public refreshMetadata = async () : Promise<void> => {
        // When the user logs in, we need to refresh metadata for them
        this._tracker.forEach(tracker => {
            this.handleCurrentChanged(tracker);
        });
        return Promise.resolve();
    }

	public getMetadata = (): TrackedOptumiMetadata => {
        const path: string = this._tracker.currentWidget.context.path;
        if (!this._optumiMetadata.has(path)) {
            return undefined
        }
        return this._optumiMetadata.get(path);
	}

    public setMetadataAfterOpen = (path: string, config: OptumiConfig) => {
        this._configToSetAfterOpen.set(path, config);
    }

    public setMetadata = (optumi: TrackedOptumiMetadata, tries: number = 0) => {
        // We do not want to set config that is empty, on startup it will cause us to override requirements
        if (!optumi.config) return;
        const rawMetadata = this._tracker.find(x => x.context.path == optumi.path).model.metadata;
		rawMetadata.set("optumi", JSON.parse(JSON.stringify(optumi.metadata)));
        this._optumiMetadata.set(optumi.path, optumi);

        if (Global.shouldLogOnEmit) console.log('SignalEmit (' + new Date().getSeconds() + ')');
        this._metadataChanged.emit();

        if (Global.user == null) return;

        // Tell the controller about the change
        const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/set-notebook-config";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				nbKey: optumi.metadata.nbKey,
                nbConfig: JSON.stringify(optumi.config),
			}),
		};
        ServerConnection.makeRequest(
            url,
            init, 
            settings
        ).then((response: Response) => {
            Global.handleResponse(response)
        }).then(() => {
            // Do nothing on success
        }, () => {
            // Try again on failure
            if (tries < 15) this.setMetadata(this._optumiMetadata.get(optumi.path), tries + 1);
        });
	}

    private static removeVersion = (pack: string): string => {
        // ~=: Compatible release clause
        pack = pack.split('~=')[0];
        // ==: Version matching clause
        pack = pack.split('==')[0];
        // !=: Version exclusion clause
        pack = pack.split('!=')[0];
        // <=, >=: Inclusive ordered comparison clause
        pack = pack.split('<=')[0];
        pack = pack.split('>=')[0];
        // <, >: Exclusive ordered comparison clause
        pack = pack.split('<')[0];
        pack = pack.split('>')[0];
        // ===: Arbitrary equality clause.
        pack = pack.split('===')[0];
        // Also remove SomeProject[foo, bar]
        pack = pack.split('[')[0];
        return pack;
    }

    private static removeLeadingSpace = (pack: string): string => {
        while (pack.startsWith(' ')) {
            pack = pack.slice(1);
        }
        return pack;
    }

    public static autoAddPackages = (requirements: string, notebook: INotebookModel): string => {
        if (requirements == null) requirements = "";
        if (requirements.length > 0 && !requirements.endsWith('\n')) requirements = requirements + '\n';

        const alreadyAdded = requirements.split('\n').map(x => OptumiMetadataTracker.removeVersion(x));
        const cells = notebook.cells;
        for (let i = 0; i < cells.length; i++) {
            var cell = cells.get(i);
            if (cell.type == 'code') {
                var multiline = '';
                for (var line of cell.value.text.split('\n')) {
                    // Kepp track of multiline strings
                    line = line.replace(/""".*?"""/g,"");  // Hanlde multiline strings that are only on one line
                    line = line.replace(/'''.*?'''/g,"");  // Hanlde multiline strings that are only on once line
                    if (line.includes("'''")) {
                        if (multiline == '') {
                            // This is the start of a multiline
                            multiline = "'''"
                        } else if (multiline == "'''") {
                            // This is the end of a multiline
                            multiline = ''
                        } else {
                            // This is a multiline inside of a multiline of the other type, so ignore it
                        }
                    } else if (line.includes('"""')) {
                        if (multiline == '') {
                            // This is the start of a multiline
                            multiline = '"""'
                        } else if (multiline == '"""') {
                            // This is the end of a multiline
                            multiline = ''
                        } else {
                            // This is a multiline inside of a multiline of the other type, so ignore it
                        }
                    }
                    // Ignore content that is part of a multiline string
                    if (multiline != '') continue;
                    line = OptumiMetadataTracker.removeLeadingSpace(line);
                    // Ignore comments
                    line = line.replace(/#.*?$/,"");
                    // Ignore strings
                    line = line.replace(/".*?"/g,"");
                    line = line.replace(/'.*?'/g,"");

                    var ps: string[] = [];
                    if (line.includes('from ')) {
                        ps.push(line.split('from ')[1].split(' ')[0].split('.')[0]);
                    } else if (line.includes('import ')) {
                        ps = ps.concat(line.split('import ')[1].split(',').map(x => OptumiMetadataTracker.removeLeadingSpace(x).split(' ')[0].split('.')[0]));
                    }
                    for (let p of ps) {
                        if (!PYTHON_STANDARD_IMPORTS.includes(p)) {
                            if (PYTHON_PACKAGE_TRANSLATIONS.has(p)) {
                                p = PYTHON_PACKAGE_TRANSLATIONS.get(p);
                            }
                            if (!alreadyAdded.includes(p)) {
                                requirements += p + '\n';
                                alreadyAdded.push(p);
                            }
                        }
                    }
                }
            }
        }
        if (requirements.endsWith('\n')) requirements = requirements.slice(0, requirements.length-1);
        return requirements;
    }

    public disableDirectoryInAllConfigs = (path: string) => {
        for (let metadata of this._optumiMetadata.values()) {
            for (let file of metadata.config.upload.files) {
                if (file.path.startsWith(path)) {
                    file.enabled = false;
                }
            }
        }
    }

    public disableFileInAllConfigs = (files: FileMetadata[]) => {
        for (let metadata of this._optumiMetadata.values()) {
            for (let file of metadata.config.upload.files) {
                for (let toDisable of files) {
                    if (file.path == toDisable.path) {
                        file.enabled = false;
                    }
                }
            }
        }
    }

    // public submitPackage = async () => {
    //     const current = this._tracker.currentWidget;
    //     if (current != null) {
    //         const notebook: any = current.model.toJSON();
    //         const optumi = this._optumiMetadata.get(current.context.path);

    //         const uploadFiles: FileUploadConfig[] = optumi.config.upload.files;
    
    //         var paths = [];
    //         for (var uploadEntry of uploadFiles) {
    //             if (uploadEntry.enabled) {
    //                 if (uploadEntry.type == 'directory') {
    //                     for (var file of (await FileServerUtils.getRecursiveTree(Global.convertOptumiPathToJupyterPath(uploadEntry.path)))) {
    //                         paths.push(Global.convertJupyterPathToOptumiPath(file.path));
    //                     }
    //                 } else {
    //                     paths.push(uploadEntry.path);
    //                 }
    //             }
    //         }

    //         const settings = ServerConnection.makeSettings();
    //         const url = settings.baseUrl + "optumi/push-package-update";
    //         const init: RequestInit = {
    //             method: 'POST',
    //             body: JSON.stringify({
    //                 nbKey: optumi.metadata.nbKey,
    //                 paths: paths,
    //                 update: JSON.stringify({
    //                     name: current.context.path,
    //                     packageState: PackageState.ACCEPTED,
    //                     originalNotebook: JSON.stringify(notebook),
    //                     originalConfig: JSON.stringify(optumi.config),
    //                     auto: false,
    //                 }),
    //             }),
    //         };
    //         ServerConnection.makeRequest(
    //             url,
    //             init, 
    //             settings
    //         ).then((response: Response) => {
    //             Global.handleResponse(response, true);
    //             setTimeout(() => this.receiveUpdate(), this.pollDelay);
    //             if (response.status == 204) {
    //                 return;
    //             }
    //             return response.json();
    //         }).then((body: any) => {
    //             if (body) {
    //                 this._packages.get(optumi.metadata.nbKey).push(new Package(body.path, new Date(), optumi.metadata.nbKey, body.label, PackageState.ACCEPTED, notebook, optumi.config, null, null, body.auto))
    //                 this._packageChanged.emit();
    //             }
    //         });
    //     }
    // }

    // public cancelPackage = async () => {
    //     const current = this._tracker.currentWidget;
    //     if (current != null) {
    //         const optumi = this._optumiMetadata.get(current.context.path);
    //         var label: string = null
    //         for (let pack of this._packages.get(optumi.metadata.nbKey)) {
    //             if (pack.packageState != PackageState.OPENED) {
    //                 label = pack.label;
    //                 break;
    //             }
    //         }

    //         if (label != null) {
    //             const settings = ServerConnection.makeSettings();
    //             const url = settings.baseUrl + "optumi/push-package-update";
    //             const init: RequestInit = {
    //                 method: 'POST',
    //                 body: JSON.stringify({
    //                     nbKey: optumi.metadata.nbKey,
    //                     label: label,
    //                     update: JSON.stringify({
    //                         packageState: PackageState.CANCELED,
    //                     }),
    //                 }),
    //             };
    //             ServerConnection.makeRequest(
    //                 url,
    //                 init, 
    //                 settings
    //             ).then((response: Response) => {
    //                 Global.handleResponse(response, true);
    //                 setTimeout(() => this.receiveUpdate(), this.pollDelay);
    //                 if (response.status == 204) {
    //                     return;
    //                 }
    //                 return response.json();
    //             }).then((body: any) => {
    //                 if (body) {
    //                     this._packages.set(optumi.metadata.nbKey, this._packages.get(optumi.metadata.nbKey).filter(x => x.label != label));
    //                     this._packageChanged.emit();
    //                 }
    //             });
    //         }
    //     }
    // }

    // public openPackage = async (configAccepted: boolean, codeChangesAccepted: boolean) => {
    //     const current = this._tracker.currentWidget;
    //     if (current != null) {
    //         const optumi = this._optumiMetadata.get(current.context.path);
    //         for (let pack of this._packages.get(optumi.metadata.nbKey)) {
    //             if (pack.packageState != PackageState.OPENED) {
    //                 const settings = ServerConnection.makeSettings();
    //                 const url = settings.baseUrl + "optumi/push-package-update";
    //                 const init: RequestInit = {
    //                     method: 'POST',
    //                     body: JSON.stringify({
    //                         nbKey: pack.nbKey,
    //                         label: pack.label,
    //                         update: JSON.stringify({
    //                             packageState: PackageState.OPENED,
    //                             configAccepted: configAccepted,
    //                             codeChangesAccepted: codeChangesAccepted,
    //                         }),
    //                     }),
    //                 };
    //                 ServerConnection.makeRequest(
    //                     url,
    //                     init, 
    //                     settings
    //                 ).then((response: Response) => {
    //                     Global.handleResponse(response, true);
    //                     setTimeout(() => this.receiveUpdate(), this.pollDelay);
    //                     if (response.status == 204) {
    //                         return;
    //                     }
    //                     return response.json();
    //                 }).then((body: any) => {
    //                     // Do nothing here
    //                 });
    //                 break;
    //             }
    //         }
    //     }
    // }


    // // The polling mechanism for packages works slightly differently than for other polling
    // // We will pass as an argument the notebook keys for any notebooks that the user has open. We will get the all packages for this notebook, excluding canceled packages
    // // Regardless of what nbKeys we pass, the response will include a single entry for any notebooks that have a package that needs to be opened.
    // // This will allow us to show the user a history for notebooks he is working on, as well as notify him of a new package no matter what he has open, both without retrieveing the entire package history for all notebooks, which could be extrememly long
    // private pollDelay = 5000;
    // private receiveUpdate = async (empty: boolean = false) => {
    //     // If there is no logged in user, do not poll
    //     if (Global.user == null) {
    //         setTimeout(() => this.receiveUpdate(), this.pollDelay);
    //         return;
    //     }
    //     // If there is an unsigned agreement, do not poll
    //     if (Global.user != null && Global.user.unsignedAgreement) {
    //         setTimeout(() => this.receiveUpdate(), this.pollDelay);
    //         return;
    //     }

    //     const nbKeys: string[] = []
    //     for (let [key, _] of this._packages) {
    //         if (key != UNOWNED_PACKAGES) nbKeys.push(key)
    //     }

    //     const settings = ServerConnection.makeSettings();
    //     const url = settings.baseUrl + "optumi/pull-package-update";
    //     const init: RequestInit = {
    //         method: 'POST',
    //         body: JSON.stringify({
    //             nbKeys: nbKeys,
    //         }),
    //     };
    //     ServerConnection.makeRequest(
    //         url,
    //         init, 
    //         settings
    //     ).then((response: Response) => {
    //         Global.handleResponse(response, true);
    //         setTimeout(() => this.receiveUpdate(), this.pollDelay);
    //         if (response.status == 204) {
    //             return;
    //         }
    //         return response.json();
    //     }).then((body: any) => {
    //         if (body) {
    //             for (let newPack of body.packages) {
    //                 var key;
    //                 if (this._packages.get(newPack.nbKey)) {
    //                     key = newPack.nbKey;
    //                 } else {
    //                     key = UNOWNED_PACKAGES;
    //                 }
    //                 const packages = this._packages.get(key);
    //                 var found = false;
    //                 for (let pack of packages) {
    //                     if (pack.label == newPack.label) {
    //                         found = true;
    //                         const lastState = pack.packageState;
    //                         pack.update(Package.fromMap(newPack));
    //                         if (pack.packageState == PackageState.SHIPPED && lastState != PackageState.SHIPPED) {
    //                             this.packageSnackbar(pack);
    //                         }
    //                         break;
    //                     }
    //                 }
    //                 if (!found) {
    //                     // If package is shipped, we want a snackbar
    //                     if (newPack.packageState == PackageState.SHIPPED) {
    //                         this.packageSnackbar(newPack);
    //                     }
    //                     packages.push(Package.fromMap(newPack));
    //                 }
    //                 this._packages.set(key, packages);
    //             }
    //             this._packageChanged.emit();
    //         }
    //     }, (error: ServerConnection.ResponseError) => {
    //         setTimeout(() => this.receiveUpdate(), this.pollDelay);
    //     });
    // }

    // public packageSnackbar = (pack: Package) => {
    //     const action = (key: SnackbarKey) => (
    //         <>
    //             <Button sx={{color: 'white'}} onClick={() => {
    //                 Global.snackbarClose.emit(key)
    //                 Global.docManager.openOrReveal(pack.path).revealed.then(() => Global.forcePackageIntoView.emit());
    //             }}>
    //                 View
    //             </Button>
    //             <Button sx={{color: 'white'}} onClick={() => {
    //                 Global.snackbarClose.emit(key)
    //             }}>
    //                 Dismiss
    //             </Button>
    //             {/* <IconButton
    //                 onClick={() => { Global.snackbarClose.emit(key) }}
    //                 sx={{padding: '3px'}}
    //             >
    //                 <Close sx={{ color: 'white' }}/>
    //             </IconButton> */}
    //         </>
    //     );
    //     Global.snackbarEnqueue.emit(new Snackbar(
    //         'New optimization for notebook ' + pack.path,
    //         { variant: 'success', persist: true, key: pack.label, action }
    //     ));
    // }

    // public getLastPackage(): Package {
    //     const current = this._tracker.currentWidget;
    //     if (current != null) {
    //         const optumi = this._optumiMetadata.get(current.context.path);
    //         if (optumi) {
    //             for (let pack of (this._packages.get(optumi.metadata.nbKey) || []).sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime())) {
    //                 if (pack.packageState == PackageState.OPENED) return pack;
    //             }
    //         }
    //     }
    //     return null;
    // }

    // public getPackage(auto: boolean = false): Package {
    //     const current = this._tracker.currentWidget;
    //     if (current != null) {
    //         const optumi = this._optumiMetadata.get(current.context.path);
    //         if (optumi) {
    //             for (let pack of (this._packages.get(optumi.metadata.nbKey) || [])) {
    //                 if ((pack.packageState != PackageState.OPENED) && (pack.auto == auto)) return pack;
    //             }
    //         }
    //     }
    //     return null;
    // }

    // public isFirstPackage(): boolean {
    //     const current = this._tracker.currentWidget;
    //     if (current != null) {
    //         const optumi = this._optumiMetadata.get(current.context.path);
    //         for (let pack of (this._packages.get(optumi.metadata.nbKey) || [])) {
    //             if (pack.packageState == PackageState.OPENED) {
    //                 return false;
    //             }
    //         }
    //         for (let nbKey of (optumi.metadata.nbKeyHistory || [])) {
    //             for (let pack of (this._packages.get(nbKey) || [])) {
    //                 if (pack.packageState == PackageState.OPENED) {
    //                     return false;
    //                 }
    //             }
    //         }
    //     }
    //     return true;
    // }

	public getMetadataChanged = (): ISignal<this, void> => {
		return this._metadataChanged;
	}

    private _metadataChanged = new Signal<this, void>(this);

    // public getPackageChanged = (): ISignal<this, void> => {
	// 	return this._packageChanged;
	// }

    // private _packageChanged = new Signal<this, void>(this);
}

export class TrackedOptumiMetadata {
    public path: string;
    public metadata: OptumiMetadata;
    public config: OptumiConfig;

    constructor(path: string, metadata: OptumiMetadata, config: OptumiConfig) {
        this.path = path;
        this.metadata = metadata;
        this.config = config;
    }

    get uuid(): string {
        return this.metadata.nbKey;
    }
}
