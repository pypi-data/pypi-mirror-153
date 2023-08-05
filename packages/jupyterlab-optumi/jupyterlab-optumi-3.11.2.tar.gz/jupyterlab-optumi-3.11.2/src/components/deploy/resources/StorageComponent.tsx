/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global } from '../../../Global';

import { SxProps, Theme } from '@mui/system';

import { Slider } from '../../../core';
import { OptumiMetadataTracker } from '../../../models/OptumiMetadataTracker';
import { StorageConfig } from '../../../models/StorageConfig';
import { User } from '../../../models/User';
import FormatUtils from '../../../utils/FormatUtils';
import { Colors } from '../../../Colors';

interface IProps {
    sx?: SxProps<Theme>,
}

interface IState {}

export class StorageComponent extends React.Component<IProps, IState> {
    
    private getSizeValue(): number {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const storage: StorageConfig = optumi.config.storage;
        return storage.size[1];
        return 20
    }
    
    private async saveSizeValue(size: number) {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const storage: StorageConfig = optumi.config.storage;
        storage.size = [-1, size, -1];
        tracker.setMetadata(optumi);
    }

    private getIopsValue(): number {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const storage: StorageConfig = optumi.config.storage;
        return storage.iops[1];
        return 20
    }
    
    private async saveIopsValue(iops: number) {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const storage: StorageConfig = optumi.config.storage;
        storage.iops = [-1, iops, -1];
        tracker.setMetadata(optumi);
    }

    private getThroughputValue(): number {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const storage: StorageConfig = optumi.config.storage;
        return storage.throughput[1];
        return 20
    }
    
    private async saveThroughputValue(throughput: number) {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const storage: StorageConfig = optumi.config.storage;
        storage.throughput = [-1, throughput, -1];
        tracker.setMetadata(optumi);
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        var user: User = Global.user;
        return (
            <DIV sx={this.props.sx}>
                <Slider
                    getValue={this.getSizeValue}
                    saveValue={this.saveSizeValue}
                    minValue={-1}
                    step={1048576}
                    maxValue={user.machines.storageSizeMax}
                    label={'Size'}
                    color={Colors.DISK}
                    showUnit
                    styledUnit={FormatUtils.styleCapacityUnit()}
                    styledValue={FormatUtils.styleCapacityValue()}
                    unstyledValue={FormatUtils.unstyleCapacityValue()}
                />
                <Slider
                    getValue={this.getIopsValue}
                    saveValue={this.saveIopsValue}
                    minValue={-1}
                    maxValue={user.machines.storageIopsMax}
                    label={'IOPS'}
                    color={Colors.DISK}
                    showUnit
                />
                <Slider
                    getValue={this.getThroughputValue}
                    saveValue={this.saveThroughputValue}
                    minValue={-1}
                    step={1000000}
                    maxValue={user.machines.storageThroughputMax}
                    label={'Throughput'}
                    color={Colors.DISK}
                    showUnit
                    styledUnit={FormatUtils.styleThroughputUnit()}
                    styledValue={FormatUtils.styleThroughputValue()}
                    unstyledValue={FormatUtils.unstyleThroughputValue()}
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