/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global } from '../../../Global';

import { SxProps, Theme } from '@mui/system';

import { OptumiMetadataTracker } from '../../../models/OptumiMetadataTracker';
import { StorageConfig } from '../../../models/StorageConfig';
import { Switch } from '../../../core';

interface IProps {
    sx?: SxProps<Theme>,
}

interface IState {}

export class StorageBasic extends React.Component<IProps, IState> {
    
    private getValue(): boolean {
        const tracker: OptumiMetadataTracker = Global.metadata;
		const optumi = tracker.getMetadata();
		const storage: StorageConfig = optumi.config.storage;
        return storage.required;
        return false
	}

	private async saveValue(checked: boolean) {
        const tracker: OptumiMetadataTracker = Global.metadata;
		const optumi = tracker.getMetadata();
        const storage: StorageConfig = optumi.config.storage;
        storage.required = checked;
        tracker.setMetadata(optumi);
	}

    handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const checked = event.target.checked;
        this.saveValue(checked);
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <DIV sx={this.props.sx}>
                <Switch
                    label='Required'
                    flip
                    getValue={this.getValue}
                    saveValue={this.saveValue}
                />
            </DIV>
        )
    }

    private handleMetadataChange = () => { this.forceUpdate() }

    // Will be called automatically when the component is mounted
	public componentDidMount = () => {
		Global.metadata.getMetadataChanged().connect(this.handleMetadataChange);
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
		Global.metadata.getMetadataChanged().disconnect(this.handleMetadataChange);
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
