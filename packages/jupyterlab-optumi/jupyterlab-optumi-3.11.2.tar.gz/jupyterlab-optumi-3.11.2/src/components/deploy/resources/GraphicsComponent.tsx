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
import { GraphicsConfig } from '../../../models/GraphicsConfig';
import { User } from '../../../models/User';
import { OptumiMetadataTracker } from '../../../models/OptumiMetadataTracker';
import FormatUtils from '../../../utils/FormatUtils';
import { Colors } from '../../../Colors';

interface IProps {
    sx?: SxProps<Theme>,
}

interface IState {}

export class GraphicsComponent extends React.Component<IProps, IState> {
        
    private getCoresValue(): number {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const graphics: GraphicsConfig = optumi.config.graphics;
        return graphics.cores[1];
    }

    private async saveCoresValue(cores: number) {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const graphics: GraphicsConfig = optumi.config.graphics;
        graphics.cores = [-1, cores, -1];
        tracker.setMetadata(optumi);
    }

    private getScoreValue(): number {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const graphics: GraphicsConfig = optumi.config.graphics;
        return graphics.score[1];
    }
    
    private async saveScoreValue(score: number) {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const graphics: GraphicsConfig = optumi.config.graphics;
        graphics.score = [-1, score, -1];
        tracker.setMetadata(optumi);
    }

    private getFrequencyValue(): number {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const graphics: GraphicsConfig = optumi.config.graphics;
        return graphics.frequency[1];
    }
    
    private async saveFrequencyValue(frequency: number) {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const graphics: GraphicsConfig = optumi.config.graphics;
        graphics.frequency = [-1, frequency, -1];
        tracker.setMetadata(optumi);
    }

    private getMemoryValue(): number {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const graphics: GraphicsConfig = optumi.config.graphics;
        return graphics.memory[1];
    }
    
    private async saveMemoryValue(memory: number) {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const graphics: GraphicsConfig = optumi.config.graphics;
        graphics.memory = [-1, memory, -1];
        tracker.setMetadata(optumi);
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        var user: User = Global.user;
        return (
            <DIV sx={this.props.sx}>
                <Slider
                    getValue={this.getCoresValue}
                    saveValue={this.saveCoresValue}
                    minValue={-1}
                    maxValue={user.machines.graphicsCoresMax}
                    label={'Cores'}
                    color={Colors.GPU}
                    showUnit
                />
                <Slider
                    getValue={this.getScoreValue}
                    saveValue={this.saveScoreValue}
                    minValue={-1}
                    maxValue={user.machines.graphicsScoreMax}
                    label={'Score'}
                    color={Colors.GPU}
                    showUnit
                />
                <Slider
                    getValue={this.getFrequencyValue}
                    saveValue={this.saveFrequencyValue}
                    minValue={-1}
                    step={1000000}
                    maxValue={user.machines.graphicsFrequencyMax}
                    label={'Frequency'}
                    color={Colors.GPU}
                    showUnit
                    styledUnit={FormatUtils.styleFrequencyUnit()}
                    styledValue={FormatUtils.styleFrequencyValue()}
                    unstyledValue={FormatUtils.unstyleFrequencyValue()}
                />
                <Slider
                    getValue={this.getMemoryValue}
                    saveValue={this.saveMemoryValue}
                    minValue={-1}
                    step={1048576}
                    maxValue={user.machines.graphicsMemoryMax}
                    label={'Memory'}
                    color={Colors.GPU}
                    showUnit
                    styledUnit={FormatUtils.styleCapacityUnit()}
                    styledValue={FormatUtils.styleCapacityValue()}
                    unstyledValue={FormatUtils.unstyleCapacityValue()}
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
