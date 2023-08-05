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
import DataConnectorDirListing from './DataConnectorDirListing'
import { DataService } from './DataConnectorDirListingItemIcon';
// import DataConnectorFilterBox from './DataConnectorFilterBox';

export interface DataConnectorMetadata extends FileMetadata {
    dataService: DataService,
}

interface IProps {
    sx?: SxProps<Theme>
    getSelected?: (getSelected: () => DataConnectorMetadata[]) => void
    onAdd?: () => void
    handleDelete?: (dataConnectorMetadata: DataConnectorMetadata) => void
}

interface IState {
    dataConnectors: DataConnectorMetadata[],
    filter: string,
}

export default class DataConnectorBrowser extends React.Component<IProps, IState> {
    private _isMounted = false
    private oldOpen: (event: MouseEvent) => boolean

    private getSelected = (): DataConnectorMetadata[] => {
        return this.getSelected();
    }

    constructor(props: IProps) {
        super(props)
        if (this.props.getSelected) this.props.getSelected(this.getSelected);
        this.state = {
            dataConnectors: Global.lastDataConnectors,
            filter: '',
        }
    }

    public request = async () => {
        const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + 'optumi/get-data-connectors'
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
                <DataConnectorDirListing
                    filter={this.state.filter}
                    dataConnectors={this.state.dataConnectors}
                    onOpen={this.handleOpen}
                    getSelected={this.props.getSelected && (getSelected => this.getSelected = getSelected)}
                    handleDelete={this.props.handleDelete}
                />
            </DIV>
        )
    }

    public componentDidMount = () => {
        this._isMounted = true
        this.request().then(json => {
            this.safeSetState({dataConnectors: json.connectors});
            Global.lastDataConnectors = json.connectors;
        })
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
