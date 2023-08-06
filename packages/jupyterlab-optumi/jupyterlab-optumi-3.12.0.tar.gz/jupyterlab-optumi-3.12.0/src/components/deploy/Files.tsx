/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { DIV, Global } from '../../Global';

import { SxProps, Theme } from '@mui/system';

import WarningPopup from '../../core/WarningPopup';
import { FileUploadConfig } from '../../models/FileUploadConfig';
import { OptumiMetadataTracker } from '../../models/OptumiMetadataTracker';
import { UploadConfig } from '../../models/UploadConfig';
import FormatUtils from '../../utils/FormatUtils';
import { FileMetadata } from './fileBrowser/FileBrowser';
import { AddFilesPopup } from './AddFilesPopup';
import FileServerUtils from '../../utils/FileServerUtils';
import { AddDataConnectorsPopup } from './AddDataConnectorsPopup';
import { DataConnectorMetadata, IntegrationMetadata } from './IntegrationBrowser/IntegrationBrowser';
import { ResourceFile } from './ResourceFile';
import { ResourceDataConnector } from './ResourceDataConnector';
import { FileChecker } from '../../models/FileChecker';
import { DataConnectorConfig } from '../../models/IntegrationConfig';

interface IProps {
    sx?: SxProps<Theme>
}

interface IState {
    filePath: string
    filesTooBig: FileMetadata[]
}

export class DataSources extends React.Component<IProps, IState> {
    _isMounted = false;

    fileChecker: FileChecker

    public constructor(props: IProps) {
        super(props)
        this.state = {
            filePath: '',
            filesTooBig: [],
        }

        this.fileChecker = Global.user.fileChecker;
    }

    private pathHasError = (path: string): boolean => {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const upload: UploadConfig = optumi.config.upload;
        const files = upload.files;
        for (var i = 0; i < files.length; i++) {
            if (files[i].path === path) return true;
        }
        return false;
    }

    private nameHasError = (name: string): boolean => {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const integrations = optumi.config.integrations;
        for (var i = 0; i < integrations.length; i++) {
            if (integrations[i].name === name) return true;
        }
        return false;
    }

    key = 0
    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const optumi = Global.metadata.getMetadata().config;
        const files = optumi.upload.files;
        const dataConnectors = optumi.dataConnectors
		return (
            <>
                <DIV sx={{width: '100%', display: 'inline-flex'}}>
                    <WarningPopup
                        open={this.state.filesTooBig.length > 0}
                        headerText="Warning"
                        bodyText={(() => {
                            const problems = this.state.filesTooBig.map(x => x.path + ' (' + FormatUtils.styleCapacityUnitValue()(x.size) + ')').join('\n')
                            return `The following files exceed the maximum upload size (${FormatUtils.styleCapacityUnitValue()(Global.MAX_UPLOAD_SIZE)}):\n\n` + problems + `\n\nTo access larger data, use data connectors.`
                        })()}
                        continue={{
                            text: `OK`,
                            onContinue: (prevent: boolean) => {
                                this.safeSetState({ filesTooBig: [] })
                            },
                            color: `error`,
                        }}
                    />
                    <AddFilesPopup onFilesAdded={async (metadatas: FileMetadata[]) => {
                        const filesTooBig = [];
                        for (let fileModel of metadatas) {
                            fileModel.path = Global.convertJupyterPathToOptumiPath(fileModel.path)
                            // Don't try to add the same file/directory more than once
                            if (this.pathHasError(fileModel.path)) continue;
                            const tracker = Global.metadata
                            const optumi = tracker.getMetadata()
                            var files = optumi.config.upload.files
                            if (fileModel.type != 'directory') {
                                if (fileModel.size > Global.MAX_UPLOAD_SIZE) {
                                    filesTooBig.push(fileModel);
                                } else {
                                    files.push(new FileUploadConfig({
                                        hash: fileModel.hash,
                                        path: fileModel.path,
                                        size: fileModel.size,
                                        created: fileModel.created,
                                        lastModified: fileModel.last_modified,
                                        type: fileModel.type,
                                        mimetype: fileModel.mimetype,
                                        enabled: true,
                                    }))
                                }
                            } else {
                                const directoryContents = (await FileServerUtils.getRecursiveTree(Global.convertOptumiPathToJupyterPath(fileModel.path)))
                                const directoryPaths = []
                                for (let metadata of directoryContents) {
                                    if (metadata.size > Global.MAX_UPLOAD_SIZE) {
                                        filesTooBig.push(metadata);
                                    } else {
                                        directoryPaths.push(metadata.path);
                                    }
                                }
                                if (directoryPaths.length > 0) {
                                    files.push(new FileUploadConfig({
                                        hash: fileModel.hash,
                                        path: fileModel.path,
                                        size: fileModel.size,
                                        created: fileModel.created,
                                        lastModified: fileModel.last_modified,
                                        type: fileModel.type,
                                        mimetype: fileModel.mimetype,
                                        enabled: true,
                                    }))
                                }
                            }
                            tracker.setMetadata(optumi)
                            Global.user.fileTracker.uploadFiles(fileModel)
                        }
                        if (filesTooBig.length > 0) {
                            this.safeSetState({ filesTooBig: filesTooBig })
                        }
                    }} />
                    <AddDataConnectorsPopup
                        onDataConnectorsAdded={async (metadatas: IntegrationMetadata[]) => {
                            for (let dataConnectorModel of metadatas) {
                                // Don't try to add the same file/directory more than once
                                if (this.nameHasError(dataConnectorModel.name)) continue;
                                const tracker = Global.metadata
                                const optumi = tracker.getMetadata()
                                var integrations = optumi.config.integrations
                                integrations.push(new DataConnectorConfig({
                                    name: dataConnectorModel.name,
                                    dataService: (dataConnectorModel as DataConnectorMetadata).dataService,
                                }))
                                tracker.setMetadata(optumi)
                            }
                        }
                    } />
                </DIV>
                
                {files.length == 0 && dataConnectors.length == 0 ? (
                    <DIV
                        sx={{
                        fontSize: '12px',
                        lineHeight: '14px',
                        padding: '3px 6px 3px 6px',
                    }}>
                        None
                    </DIV>
                ) : (
                    <>
                        {files.map(
                            (value: FileUploadConfig) => (
                                <ResourceFile
                                    key={value.path + this.key++}
                                    file={value}
                                    handleFileDelete={() => {
                                        // Cancel the upload
                                        const progress = Global.user.fileTracker.get(value.path);
                                        const compression = progress.filter(x => x.type == 'compression');
                                        const upload = progress.filter(x => x.type == 'upload');
                                        if (compression.length > 0) compression[0].cancel();
                                        if (upload.length > 0) upload[0].cancel();

                                        // Remove the file from metadata
                                        const tracker: OptumiMetadataTracker = Global.metadata;
                                        const optumi = tracker.getMetadata();
                                        const files = optumi.config.upload.files
                                        for (var i = 0; i < files.length; i++) {
                                            if (files[i].path === value.path) {
                                                files.splice(i, 1)
                                                break
                                            }
                                        }
                                        // optumi.upload.files = (optumi.upload.files as UploadVarMetadata[]).filter(x => x.path !== (event.currentTarget as HTMLButtonElement).id.replace('-delete', ''));
                                        tracker.setMetadata(optumi);
                                        this.fileChecker.removeFile(value.path);    
                                    }}
                                    handleFileEnabledChange={(enabled: boolean) => {
                                        const tracker: OptumiMetadataTracker = Global.metadata;
                                        const optumi = tracker.getMetadata();
                                        const upload: UploadConfig = optumi.config.upload;
                                        const files = upload.files;
                                        for (var i = 0; i < files.length; i++) {
                                            const file = files[i];
                                            if (file.path === value.path) {
                                                file.enabled = enabled;
                                                break;
                                            }
                                        }
                                        tracker.setMetadata(optumi);
                                    }}
                                    missingLocally={this.fileChecker.fileMissingLocally(value.path)}
                                    missingInCloud={this.fileChecker.fileMissingInCloud(value.path)}
                                />
                            )
                        )}
                        {dataConnectors.map(
                            (value: DataConnectorConfig) => (
                                <ResourceDataConnector
                                    key={value.name + this.key++}
                                    dataConnector={value}
                                    handleFileDelete={() => {
                                        const tracker: OptumiMetadataTracker = Global.metadata;
                                        const optumi = tracker.getMetadata();
                                        const integrations = optumi.config.integrations
                                        for (var i = 0; i < integrations.length; i++) {
                                            if (integrations[i].name === value.name) {
                                                integrations.splice(i, 1)
                                                break
                                            }
                                        }
                                        // optumi.upload.files = (optumi.upload.files as UploadVarMetadata[]).filter(x => x.path !== (event.currentTarget as HTMLButtonElement).id.replace('-delete', ''));
                                        tracker.setMetadata(optumi);
                                        this.fileChecker.removeDataConnector(value.name);
                                    }}
                                    noLongerExists={this.fileChecker.dataConnectorMissing(value.name)}
                                />
                            )
                        )}
                    </>
                )}
            </>
		);
	}

    

    private handleThemeChange = () => this.forceUpdate()

    private handleMetadataChange = () => {
        this.fileChecker.refreshIntegrations(false)
        this.fileChecker.refreshFiles(false)
        this.forceUpdate()
    }

    private handleDataConnectorChange = () => {
        this.fileChecker.refreshIntegrations(false)
    }

    public componentDidMount = () => {
        this._isMounted = true;
        Global.themeManager.themeChanged.connect(this.handleThemeChange);
        Global.metadata.getMetadataChanged().connect(this.handleMetadataChange);
        Global.dataConnectorChange.connect(this.handleDataConnectorChange);
        Global.labShell.currentChanged.connect(this.handleMetadataChange)
	}

	public componentWillUnmount = () => {
        Global.themeManager.themeChanged.disconnect(this.handleThemeChange);
        Global.metadata.getMetadataChanged().disconnect(this.handleMetadataChange);
        Global.dataConnectorChange.disconnect(this.handleDataConnectorChange);
        Global.labShell.currentChanged.disconnect(this.handleMetadataChange)
		this._isMounted = false;
	}

    private safeSetState = (map: any) => {
		if (this._isMounted) {
			let update = false
			try {
				for (const key of Object.keys(map)) {
					if (JSON.stringify(map[key]) !== JSON.stringify((this.state as any)[key])) {
						update = true
						break
					}
				}
			} catch (error) {
				update = true
			}
			if (update) {
				if (Global.shouldLogOnSafeSetState) console.log('SafeSetState (' + new Date().getSeconds() + ')');
				this.setState(map)
			} else {
				if (Global.shouldLogOnSafeSetState) console.log('SuppressedSetState (' + new Date().getSeconds() + ')');
			}
		}
	}

	public shouldComponentUpdate = (nextProps: IProps, nextState: IState): boolean => {
        try {
            if (JSON.stringify(this.props) != JSON.stringify(nextProps)) return true;
            if (JSON.stringify(this.state) != JSON.stringify(nextState)) return true;
            if (Global.shouldLogOnRender) console.log('SuppressedRender (' + new Date().getSeconds() + ')');
            return false;
        } catch (error) {
            return true;
        }
    }
}
