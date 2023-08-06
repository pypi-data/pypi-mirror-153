/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { Global } from '../../Global';

import { SxProps, Theme } from '@mui/system';

import { TextBox } from '../../core';
import { DataService } from './IntegrationBrowser/IntegrationDirListingItemIcon';
import { BaseConnectorPopup } from '../../core/BaseConnectorPopup';

interface IProps {
    // This close action will allow us to get a new set of connectors when a new one is created
    onClose?: () => any
    sx?: SxProps<Theme>
}

interface IState {
    containerName: string
    blobName: string
    connectionString: string
}

const defaultState = {
    containerName: '',
    blobName: '',
    connectionString: '',
}

export class AzureBlobStorageConnectorPopup extends React.Component<IProps, IState> {
    private _isMounted = false

    constructor(props: IProps) {
        super(props);
		this.state = defaultState;
    }

	private handleClose = () => {
        if (this.props.onClose) this.props.onClose();
        this.safeSetState(defaultState);
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <BaseConnectorPopup
                dataService={DataService.AZURE_BLOB_STORAGE}
                description='Access an Azure Blob Storage container'
                header='Connect to an Azure Blob Storage container or blob.'
                downloadPath=''
                onClose={this.handleClose}
                getInfo={() => this.state }
                getContents={(waiting: boolean) => (
                    <>
                        <TextBox<string>
                            getValue={() => this.state.containerName}
                            saveValue={(value: string) => this.safeSetState({ containerName: value })}
                            label='Container Name'
                            helperText='The Container Name as specified in Azure documentation.'
                            labelWidth={BaseConnectorPopup.LABEL_WIDTH}
                            disabled={waiting}
                            required
                        />
                        <TextBox<string>
                            getValue={() => this.state.blobName}
                            saveValue={(value: string) => this.safeSetState({ blobName: value })}
                            label='Blob Name'
                            helperText='If you leave this blank, we will transfer the entire container.'
                            labelWidth={BaseConnectorPopup.LABEL_WIDTH}
                            disabled={waiting}
                        />
                        <TextBox<string>
                            getValue={() => this.state.connectionString}
                            saveValue={(value: string) => this.safeSetState({ connectionString: value })}
                            label='Connection String'
                            helperText='The Connection String as specified in Azure documentation.'
                            labelWidth={BaseConnectorPopup.LABEL_WIDTH}
                            disabled={waiting}
                            required
                        />
                    </>
                )}
            />
        )
    }

    public componentDidMount = () => {
        this._isMounted = true
    }

    public componentWillUnmount = () => {
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
