/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global } from '../../../Global';

import { SxProps, Theme } from '@mui/system';
import { Divider } from '@mui/material';

import { ResourceSelector } from './ResourceSelector';
import { OptumiMetadataTracker } from '../../../models/OptumiMetadataTracker';
import { GraphicsBasic } from './GraphicsBasic';
import { GraphicsRating } from './GraphicsRating';
import { GraphicsEquipment } from './GraphicsEquipment';
import { GraphicsComponent } from './GraphicsComponent';
import { ComputeBasic } from './ComputeBasic';
import { ComputeRating } from './ComputeRating';
import { ComputeComponent } from './ComputeComponent';
import { ComputeSimplified } from './ComputeSimplified';
import { MemoryBasic } from './MemoryBasic';
import { MemoryRating } from './MemoryRating';
import { MemoryComponent } from './MemoryComponent';
import { StorageBasic } from './StorageBasic';
import { StorageComponent } from './StorageComponent';
import { StorageRating } from './StorageRating';
import { StorageConfig } from '../../../models/StorageConfig';
import { Expertise } from '../../../models/OptumiConfig';
import { ComputeConfig } from '../../../models/ComputeConfig';
import { GraphicsConfig } from '../../../models/GraphicsConfig';
import { MemoryConfig } from '../../../models/MemoryConfig';
import { Simplified } from './Simplified';

interface IProps {
    sx?: SxProps<Theme>,
}

interface IState {}

export class ResourcesPanel extends React.Component<IProps, IState> {

    private getGraphicsLevel(tracker: OptumiMetadataTracker): Expertise {
        const optumi = tracker.getMetadata();
        const graphics: GraphicsConfig = optumi.config.graphics;
        return graphics.expertise;
    }

    private async saveGraphicsLevel(tracker: OptumiMetadataTracker, expertise: Expertise) {
        const optumi = tracker.getMetadata();
        const graphics: GraphicsConfig = optumi.config.graphics;
        graphics.expertise = expertise;
        tracker.setMetadata(optumi);
    }

    private getComputeLevel(tracker: OptumiMetadataTracker): Expertise {
        const optumi = tracker.getMetadata();
        const compute: ComputeConfig = optumi.config.compute;
        return compute.expertise;
    }

    private async saveComputeLevel(tracker: OptumiMetadataTracker, expertise: Expertise) {
        const optumi = tracker.getMetadata();
        const compute: ComputeConfig = optumi.config.compute;
        compute.expertise = expertise;
        tracker.setMetadata(optumi);
    }

    private getMemoryLevel(tracker: OptumiMetadataTracker): Expertise {
        const optumi = tracker.getMetadata();
        const memory: MemoryConfig = optumi.config.memory;
        return memory.expertise;
    }

    private async saveMemoryLevel(tracker: OptumiMetadataTracker, expertise: Expertise) {
        const optumi = tracker.getMetadata();
        const memory: MemoryConfig = optumi.config.memory;
        memory.expertise = expertise;
        tracker.setMetadata(optumi);
    }

    private getStorageLevel(tracker: OptumiMetadataTracker): Expertise {
        const optumi = tracker.getMetadata();
        const storage: StorageConfig = optumi.config.storage;
        return storage.expertise;
    }

    private async saveStorageLevel(tracker: OptumiMetadataTracker, expertise: Expertise) {
        const optumi = tracker.getMetadata();
        const storage: StorageConfig = optumi.config.storage;
        storage.expertise = expertise;
        tracker.setMetadata(optumi);
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        // For non-experimental users, we only need to look at one resource to decide what mode they are in
        // const basic: boolean = Global.metadata.getMetadata().metadata.graphics.expertise == Expertise.BASIC;
        return (
            <DIV sx={this.props.sx}>
                {Global.user.userExpertise >= 2 ? (
                    <>
                        <ResourceSelector title='GPU' getValue={this.getGraphicsLevel} saveValue={this.saveGraphicsLevel} childrenLabels={[Expertise.BASIC, Expertise.RATING, Expertise.EQUIPMENT, Expertise.COMPONENT]}>
                            <GraphicsBasic />
                            <GraphicsRating />
                            <GraphicsEquipment />
                            {Global.user.userExpertise >= 2 && <GraphicsComponent />}
                        </ResourceSelector>
                        <Divider variant='middle' />
                        <ResourceSelector title='CPU' getValue={this.getComputeLevel} saveValue={this.saveComputeLevel} childrenLabels={[Expertise.BASIC, Expertise.RATING, Expertise.SIMPLIFIED, Expertise.COMPONENT]}>
                            <ComputeBasic />
                            <ComputeRating />
                            {Global.user.userExpertise >= 2 && <ComputeSimplified />}
                            {Global.user.userExpertise >= 2 && <ComputeComponent />}
                        </ResourceSelector>
                        <Divider variant='middle' />
                        <ResourceSelector title='RAM' getValue={this.getMemoryLevel} saveValue={this.saveMemoryLevel} childrenLabels={[Expertise.BASIC, Expertise.RATING, Expertise.COMPONENT]}>
                            <MemoryBasic />
                            <MemoryRating />
                            {Global.user.userExpertise >= 2 && <MemoryComponent />}
                        </ResourceSelector>
                        <Divider variant='middle' />
                        <ResourceSelector title='DSK' getValue={this.getStorageLevel} saveValue={this.saveStorageLevel} childrenLabels={[Expertise.BASIC, Expertise.RATING, Expertise.COMPONENT]}>
                            <StorageBasic />
                            <StorageRating />
                            {Global.user.userExpertise >= 2 && <StorageComponent />}
                        </ResourceSelector>
                    </>
                ) : (
                    <>
                        <Simplified />
                    </>
                )}
                
            </DIV>
        );
    }

    private handleMetadataChange = () => { this.forceUpdate() }

    // Will be called automatically when the component is mounted
	public componentDidMount = () => {
        // This will cause the display to change when we change to a new notebook with a different level specified
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
