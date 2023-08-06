/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { DIV, Global } from '../../../Global';

import { SxProps, Theme } from '@mui/system';

import { ServerConnection } from '@jupyterlab/services';

import { FileMetadata } from '../fileBrowser/FileBrowser';
import IntegrationDirListing from './IntegrationDirListing'
import { DataService } from './IntegrationDirListingItemIcon';
import { IntegrationConfig } from '../../../models/IntegrationConfig';
// import DataConnectorFilterBox from './DataConnectorFilterBox';
export enum IntegrationType {
    DATA_CONNECTOR = 'data connector',
    ENVIRONMENT_VARIABLE = 'environment variable',
    NONE = '',
    ALL = 'all',
}

export interface IntegrationMetadata extends FileMetadata {
    integrationType: IntegrationType
}

export interface DataConnectorMetadata extends IntegrationMetadata {
    dataService: DataService,
}

export interface EnvironmentVariableMetadata extends IntegrationMetadata {
    key: string,
}

interface IProps {
    sx?: SxProps<Theme>
    getSelected?: (getSelected: () => IntegrationMetadata[]) => void
    onAdd?: () => void
    handleDelete?: (integrationMetadata: IntegrationMetadata) => void
    type: IntegrationType
}

interface IState {
    integrations: IntegrationMetadata[],
    filter: string,
}

export default class IntegrationBrowser extends React.Component<IProps, IState> {
    private _isMounted = false
    private oldOpen: (event: MouseEvent) => boolean

    private getSelected = (): IntegrationMetadata[] => {
        return this.getSelected();
    }

    constructor(props: IProps) {
        super(props)
        if (this.props.getSelected) this.props.getSelected(this.getSelected);
        this.state = {
            integrations: Global.lastIntegrations,
            filter: '',
        }
    }

    public request = async () => {
        const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + 'optumi/get-integrations'
		return ServerConnection.makeRequest(url, {}, settings).then(response => {
			if (response.status !== 200) throw new ServerConnection.ResponseError(response);
			return response.json()
		})
    }

    private handleOpen = (file: FileMetadata) => {
        if (this.props.onAdd) this.props.onAdd();
    }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <DIV className='jp-FileBrowser' sx={this.props.sx}>
                {/* <DataConnectorFilterBox sx={{marginBottom: '8px'}} onChange={(filter: string) => this.safeSetState({filter})} /> */}
                <IntegrationDirListing
                    filter={this.state.filter}
                    integrations={this.state.integrations}
                    onOpen={this.handleOpen}
                    getSelected={this.props.getSelected && (getSelected => this.getSelected = getSelected)}
                    handleDelete={this.props.handleDelete}
                    type={this.props.type}
                />
            </DIV>
        )
    }

    public componentDidMount = () => {
        this._isMounted = true
        this.request().then(json => {
            this.safeSetState({ integrations: 
                this.props.type == IntegrationType.DATA_CONNECTOR ? (
                    json.integrations.filter((x: IntegrationConfig) => x.integrationType == IntegrationType.DATA_CONNECTOR)
                ) : this.props.type == IntegrationType.ENVIRONMENT_VARIABLE ? (
                    json.integrations.filter((x: IntegrationConfig) => x.integrationType == IntegrationType.ENVIRONMENT_VARIABLE)
                ) : (
                    json.integrations
                )
            });
            Global.lastIntegrations = json.integrations;
        });
        // Override the JupyterLab context menu open (disable it)
        this.oldOpen = Global.lab.contextMenu.open
        Global.lab.contextMenu.open = () => false
    }

    // Add context menu items back
    public componentWillUnmount = () => {
        // Restore the old JupyterLab context menu open
        Global.lab.contextMenu.open = this.oldOpen
        this._isMounted = false
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
}
