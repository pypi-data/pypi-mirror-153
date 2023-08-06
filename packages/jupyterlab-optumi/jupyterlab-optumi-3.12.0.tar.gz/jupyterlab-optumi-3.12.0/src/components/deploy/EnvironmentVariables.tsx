/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { DIV, Global } from '../../Global';

import { SxProps, Theme } from '@mui/system';

import { OptumiMetadataTracker } from '../../models/OptumiMetadataTracker';

import { AddEnvironmentVariablesPopup } from './AddEnvironmentVariablesPopup';
import { ResourceEnvironmentVariable } from './ResourceEnvironmentVariable';
import { FileChecker } from '../../models/FileChecker';
import { IntegrationMetadata } from './IntegrationBrowser/IntegrationBrowser';
import { EnvironmentVariableConfig } from '../../models/IntegrationConfig';

interface IProps {
    sx?: SxProps<Theme>
}

interface IState {}

export class EnvironmentVariables extends React.Component<IProps, IState> {
    _isMounted = false;

    fileChecker: FileChecker

    public constructor(props: IProps) {
        super(props)
        this.state = {}

        this.fileChecker = Global.user.fileChecker;
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
        const environmentVariables = optumi.environmentVariables;
		return (
            <>
                <DIV sx={{width: '100%'}}>
                    <DIV sx={{width: '100%', display: 'inline-flex'}}>
                        <AddEnvironmentVariablesPopup
                            onEnvironmentVariablesAdded={async (metadatas: IntegrationMetadata[]) => {
                                for (let environmentVariableModel of metadatas) {
                                    // Don't try to add the same file/directory more than once
                                    if (this.nameHasError(environmentVariableModel.name)) continue;
                                    const tracker = Global.metadata
                                    const optumi = tracker.getMetadata()
                                    var integrations = optumi.config.integrations
                                    integrations.push(new EnvironmentVariableConfig({
                                        name: environmentVariableModel.name,
                                    }))
                                    console.log(optumi)
                                    tracker.setMetadata(optumi)
                                }
                            }
                        } />
                    </DIV>

                    {environmentVariables.length == 0 ? (
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
                            {environmentVariables.map(
                                (value: EnvironmentVariableConfig) => (
                                    <ResourceEnvironmentVariable
                                        key={value.name + this.key++}
                                        environmentVariable={value}
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
                                            this.fileChecker.removeEnvironmentVariable(value.name);
                                        }}
                                        noLongerExists={this.fileChecker.environmentVariableMissing(value.name)}
                                    />
                                )
                            )}
                        </>
                    )}
                </DIV>
            </>
		);
	}

    private handleThemeChange = () => this.forceUpdate()
    private handleMetadataChange = () => this.forceUpdate()

    public componentDidMount = () => {
		this._isMounted = true;
        Global.themeManager.themeChanged.connect(this.handleThemeChange);
        Global.metadata.getMetadataChanged().connect(this.handleMetadataChange);
        Global.labShell.currentChanged.connect(this.handleMetadataChange)
	}

	public componentWillUnmount = () => {
        Global.themeManager.themeChanged.disconnect(this.handleThemeChange);
        Global.metadata.getMetadataChanged().disconnect(this.handleMetadataChange);
        Global.labShell.currentChanged.disconnect(this.handleMetadataChange)
		this._isMounted = false;
	}

    // private safeSetState = (map: any) => {
	// 	if (this._isMounted) {
	// 		let update = false
	// 		try {
	// 			for (const key of Object.keys(map)) {
	// 				if (JSON.stringify(map[key]) !== JSON.stringify((this.state as any)[key])) {
	// 					update = true
	// 					break
	// 				}
	// 			}
	// 		} catch (error) {
	// 			update = true
	// 		}
	// 		if (update) {
	// 			if (Global.shouldLogOnSafeSetState) console.log('SafeSetState (' + new Date().getSeconds() + ')');
	// 			this.setState(map)
	// 		} else {
	// 			if (Global.shouldLogOnSafeSetState) console.log('SuppressedSetState (' + new Date().getSeconds() + ')');
	// 		}
	// 	}
	// }

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
