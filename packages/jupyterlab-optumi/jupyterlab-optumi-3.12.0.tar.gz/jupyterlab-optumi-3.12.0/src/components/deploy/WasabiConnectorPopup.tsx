/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { Global } from '../../Global';

import { CSSProperties } from '@mui/styles';

import { Dropdown, TextBox } from '../../core';
import { DataService } from './IntegrationBrowser/IntegrationDirListingItemIcon';
import { BaseConnectorPopup } from '../../core/BaseConnectorPopup';
import { WasabiRegions } from '../../models/WasabiRegions';

interface IProps {
    // This close action will allow us to get a new set of connectors when a new one is created
    onClose?: () => any
    style?: CSSProperties
}

interface IState {
    region: string
    bucketName: string
    objectKey: string
    accessKeyID: string
    secretAccessKey: string
}

const defaultState = {
    region: WasabiRegions.US_EAST_1.region,
    bucketName: '',
    objectKey: '',
    accessKeyID: '',
    secretAccessKey: '',
}

export class WasabiConnectorPopup extends React.Component<IProps, IState> {
    private _isMounted = false

    constructor(props: IProps) {
        super(props);
		this.state = defaultState
    }

	private handleClose = () => {
        if (this.props.onClose) this.props.onClose();
        this.safeSetState(defaultState);
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <BaseConnectorPopup
                dataService={DataService.WASABI}
                description='Access a Wasabi bucket'
                header='Connect to a Wasabi bucket or object.'
                downloadPath=''
                onClose={this.handleClose}
                getInfo={() => this.state }
                getContents={(waiting: boolean) => (
                    <>
                        <Dropdown
                            getValue={() => this.state.region}
                            saveValue={(value: string) => this.safeSetState({ region: value })}
                            label='Region'
                            labelWidth={BaseConnectorPopup.LABEL_WIDTH}
                            values={WasabiRegions.values.map(x => { return { value: x.region, description: x.description} })}
                            helperText='The service region as specified in Wasabi (or S3) documentation.'
                        />
                        <TextBox<string>
                            getValue={() => this.state.bucketName}
                            saveValue={(value: string) => this.safeSetState({ bucketName: value })}
                            label='Bucket Name'
                            helperText='The Bucket Name as specified in Wasabi (or S3) documentation.'
                            labelWidth={BaseConnectorPopup.LABEL_WIDTH}
                            disabled={waiting}
                            required
                        />
                        <TextBox<string>
                            getValue={() => this.state.objectKey}
                            saveValue={(value: string) => this.safeSetState({ objectKey: value })}
                            label='Object Key'
                            helperText='If you leave this blank, we will transfer the entire bucket.'
                            labelWidth={BaseConnectorPopup.LABEL_WIDTH}
                            disabled={waiting}
                        />
                        <TextBox<string>
                            getValue={() => this.state.accessKeyID}
                            saveValue={(value: string) => this.safeSetState({ accessKeyID: value })}
                            label='Access Key ID'
                            helperText='The Access Key ID as specified in Wasabi (or S3) documentation.'
                            labelWidth={BaseConnectorPopup.LABEL_WIDTH}
                            disabled={waiting}
                            required
                        />
                        <TextBox<string>
                            getValue={() => this.state.secretAccessKey}
                            saveValue={(value: string) => this.safeSetState({ secretAccessKey: value })}
                            label='Secret Access Key'
                            helperText='The Secret Access Key as specified in Wasabi (or S3) documentation.'
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
