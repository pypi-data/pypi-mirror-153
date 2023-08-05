/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global } from '../../../Global';

import { SxProps, Theme } from '@mui/system';

import { Switch } from '../../../core';
import { MemoryConfig } from '../../../models/MemoryConfig';
import { OptumiMetadataTracker } from '../../../models/OptumiMetadataTracker';

interface IProps {
    sx?: SxProps<Theme>,
}

interface IState {}

export class MemoryBasic extends React.Component<IProps, IState> {
    
    private getValue(): boolean {
        const tracker: OptumiMetadataTracker = Global.metadata;
		const optumi = tracker.getMetadata();
		const memory: MemoryConfig = optumi.config.memory;
		return memory.required;
	}

	private async saveValue(checked: boolean) {
        const tracker: OptumiMetadataTracker = Global.metadata;
		const optumi = tracker.getMetadata();
        const memory: MemoryConfig = optumi.config.memory;
        memory.required = checked;
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