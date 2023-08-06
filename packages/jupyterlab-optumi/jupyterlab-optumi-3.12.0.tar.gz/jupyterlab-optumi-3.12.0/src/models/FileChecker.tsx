/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { Global } from "../Global"

import { ServerConnection } from '@jupyterlab/services';

import { DataConnectorMetadata } from '../components/deploy/IntegrationBrowser/IntegrationBrowser';
import { FileMetadata } from "../components/deploy/fileBrowser/FileBrowser"
import FileServerUtils from "../utils/FileServerUtils"
import { FileUploadConfig } from './FileUploadConfig';
import { DataConnectorConfig } from "./IntegrationConfig";

export class FileChecker {
    // Here is where we will keep a list of the file paths that were entered successfully but no longer exist on the disk
    private localProblemFiles: string[] = []
    private cloudProblemFiles: string[] = []
    private problemDataConnectors: string[] = []
    private problemEnvironmentVariables: string[] = []

    refreshing: boolean = false
    filesTimeout: NodeJS.Timeout = null
    dataConnectorsTimeout: NodeJS.Timeout = null

    public start() {
        if (!this.refreshing) {
            this.refreshing = true

            this.refreshFiles(true)
            this.refreshIntegrations(true)
        }
    }

    public stop() {
        this.refreshing = false
        if (this.filesTimeout != null) clearTimeout(this.filesTimeout)
        if (this.dataConnectorsTimeout != null) clearTimeout(this.dataConnectorsTimeout)
    }

    public getTriangle(files: FileUploadConfig[], dataConnectors: DataConnectorConfig[]): [boolean, boolean] {
        var yellowTriangle = false
        var redTriangle = false
        for (let file of files) {
            if (file.enabled) {
                if (this.localProblemFiles.includes(file.path)) {
                    yellowTriangle = true
                    if (this.cloudProblemFiles.includes(file.path)) {
                        redTriangle = true
                    }
                }
            }
        }
        for (let dataConnector of dataConnectors) {
            if (dataConnector.enabled) {
                if (this.problemDataConnectors.includes(dataConnector.name)) {
                    redTriangle = true
                }
            }
        }
        return [yellowTriangle, redTriangle]
    }

    public fileMissingLocally(path: string): boolean {
        return this.localProblemFiles.includes(path);
    }

    public fileMissingInCloud(path: string): boolean {
        return this.cloudProblemFiles.includes(path);
    }
    
    public dataConnectorMissing(name: string): boolean {
        return this.problemDataConnectors.includes(name);
    }

    public environmentVariableMissing(name: string): boolean {
        return this.problemEnvironmentVariables.includes(name);
    }

    public removeFile(path: string) {
        if (this.localProblemFiles.includes(path)) this.localProblemFiles = this.localProblemFiles.filter(x => x != path);
        if (this.cloudProblemFiles.includes(path)) this.cloudProblemFiles = this.cloudProblemFiles.filter(x => x != path);
    }

    public removeDataConnector(name: string) {
        if (this.problemDataConnectors.includes(name)) this.problemDataConnectors = this.problemDataConnectors.filter(x => x != name);
    }

    public removeEnvironmentVariable(name: string) {
        if (this.problemEnvironmentVariables.includes(name)) this.problemEnvironmentVariables = this.problemEnvironmentVariables.filter(x => x != name);
    }

    public refreshFiles = async (poll: boolean = true) => {
        if (this.refreshing) {
            try {
                var newLocalProblemFiles = [];
                var newCloudProblemFiles = [];
                const optumi = Global.metadata.getMetadata().config;
                const files = optumi.upload.files;
                const fileTracker = Global.user.fileTracker;
                for (var file of files) {
                    if (!this.refreshing) break;
                    // Check local
                    const barr = await FileServerUtils.checkIfPathExists(Global.convertOptumiPathToJupyterPath(file.path));
                    if (!barr[0]) {
                        newLocalProblemFiles.push(file.path);
                    } else {
                        // This upload call will 'sync' the file if necessary
                        // We don't want to re-upload disabled files
                        if (file.enabled) Global.user.fileTracker.uploadFiles({ path: file.path, type: file.type } as FileMetadata);
                    }
                    // Check cloud
                    const exists = file.type === 'directory' ? fileTracker.directoryExists(file.path) : fileTracker.pathExists(file.path)
                    if (!exists) {
                        newCloudProblemFiles.push(file.path)
                    }
                }
                
                this.localProblemFiles = newLocalProblemFiles;
                this.cloudProblemFiles = newCloudProblemFiles;
            } catch (err) {
                console.error(err)
            }
            if (poll) {
                if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
                this.filesTimeout = setTimeout(this.refreshFiles, 60000);
            }
        }
    }

    public refreshIntegrations = async (poll: boolean = true) => {
        if (this.refreshing) {
            try {
                const optumi = Global.metadata.getMetadata().config;
                const dataConnectors = optumi.dataConnectors
                
                const settings = ServerConnection.makeSettings();
                const url = settings.baseUrl + "optumi/get-integrations";
                const dataConnectorsFromController: DataConnectorMetadata[] = await (ServerConnection.makeRequest(url, {}, settings).then(response => {
                    if (response.status !== 200) throw new ServerConnection.ResponseError(response);
                    return response.json();
                }).then((json: any) => json.integrations));

                for (var dataConnector of dataConnectors) {
                    if (!this.refreshing) break;
                    if (!this.problemDataConnectors.includes(dataConnector.name)) {
                        const exists = dataConnectorsFromController.map(x => x.name).includes(dataConnector.name);
                        if (!exists) {
                            this.problemDataConnectors = this.problemDataConnectors.concat([dataConnector.name]);
                        }
                    }
                }
            } catch (err) {
                console.error(err)
            }
            if (poll) {
                if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
                this.dataConnectorsTimeout = setTimeout(this.refreshIntegrations, 60000);
            }
        }
    }
}
