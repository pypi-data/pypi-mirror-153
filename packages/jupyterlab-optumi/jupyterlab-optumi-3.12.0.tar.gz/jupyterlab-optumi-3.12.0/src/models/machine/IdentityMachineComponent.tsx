/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global } from '../../Global';

import { Slider } from '@mui/material';
import { withStyles } from '@mui/styles';

import ExtraInfo from '../../utils/ExtraInfo';
import FormatUtils from '../../utils/FormatUtils';
import { Machine, NoMachine } from './Machine';
import { Colors } from '../../Colors';

const corners = '4px'
const rounding = '5px'

const topTrackRadius = corners + ' ' + rounding + ' ' + rounding + ' 0px'
const topRailRadius = corners + ' ' + corners + ' 0px 0px';

const middleTrackRadius = '0px ' + rounding + ' ' + rounding + ' 0px';
const middleRailRadius = '0px';

const bottomTrackRadius = '0px ' + rounding + ' ' + rounding + ' ' + corners;
const bottomRailRadius = '0px 0px ' + corners + ' ' + corners; 

const BAR_HEIGHT = '16px'

function forBar(type: string, empty: boolean, expert: boolean): any {
    var color: string
    var trackRadius: string, railRadius: string

    // if (type == 'Compute') {
    //     color = '#ba9fd1';
    //     if (expert) {
    //         trackRadius = middleTrackRadius
    //         railRadius = middleRailRadius
    //     } else {
    //         trackRadius = topTrackRadius
    //         railRadius = topRailRadius
    //     }
    // } else if (type == 'Graphics') {
    //     color = '#ffba7d';
    //     trackRadius = topTrackRadius
    //     railRadius = topRailRadius
    // } else if (type == 'GraphicsMemory') {
    //     color = '#B5C6E3';
    //     trackRadius = middleTrackRadius
    //     railRadius = middleRailRadius
    // } else if (type == 'Memory') {
    //     color = '#f48f8d';
    //     if (expert) {
    //         trackRadius = middleTrackRadius
    //         railRadius = middleRailRadius
    //     } else {
    //         trackRadius = bottomTrackRadius
    //         railRadius = bottomRailRadius
    //     }
    // } else if (type == 'Disk') {
    //     color = '#00c650'
    //     trackRadius = bottomTrackRadius
    //     railRadius = bottomRailRadius
    // }

    if (type == 'Compute') {
        color = Colors.CPU;
        if (expert) {
            trackRadius = middleTrackRadius
            railRadius = middleRailRadius
        } else {
            trackRadius = topTrackRadius
            railRadius = topRailRadius
        }
    } else if (type == 'Graphics') {
        color = Colors.GPU;
        trackRadius = topTrackRadius
        railRadius = topRailRadius
    } else if (type == 'GraphicsMemory') {
        color = Colors.VRAM;
        trackRadius = middleTrackRadius
        railRadius = middleRailRadius
    } else if (type == 'Memory') {
        color = Colors.RAM;
        if (expert) {
            trackRadius = middleTrackRadius
            railRadius = middleRailRadius
        } else {
            trackRadius = bottomTrackRadius
            railRadius = bottomRailRadius
        }
    } else if (type == 'Disk') {
        color = Colors.DISK
        trackRadius = bottomTrackRadius
        railRadius = bottomRailRadius
    }

    return {
        root: {
            marginRight: '8px',
            height: BAR_HEIGHT,
            width: '100%',
            padding: '0px',
            lineHeight: 1,
            fontSize: '14px',
        },
        thumb: { // hidden
            height: BAR_HEIGHT,
            top: '6px',
            backgroundColor: 'transparent',
            padding: '0px',
            '&:focus, &:hover, &:active': {
                boxShadow: 'none',
            },
            '&::before': {
                boxShadow: 'none',
            },
            '&::after': {
                left: -6,
                top: -6,
                right: -6,
                bottom: -6,
            },
        },
        track: { // left side
            height: BAR_HEIGHT,
            color: color,
            boxSizing: 'border-box',
            // border: "1px solid " + darken(color, 0.25),
            borderRadius: trackRadius,
            opacity: empty ? 0 : 1,
            '-webkit-transition': 'none',
            transition: 'none',
        },
        rail: { // right side
            // display: 'none',
            height: BAR_HEIGHT,
            color: color,
            borderRadius: railRadius,
        },
    };
}

interface IProps {
    machine: Machine
}

interface IState {}

const FONT_SIZE = '12px'
const COLUMN_WIDTH_1 = '105px'
const COLUMN_MARGIN = 'auto'

export class IdentityMachineComponent extends React.Component<IProps, IState> {

    private ComputeBar = withStyles(forBar('Compute', false, false)) (Slider);
    private GraphicsBar = withStyles(forBar('Graphics', false, false)) (Slider);
    private GraphicsMemoryBar = withStyles(forBar('GraphicsMemory', false, false)) (Slider);
    private MemoryBar = withStyles(forBar('Memory', false, false)) (Slider);
    
    private EmptyComputeBar = withStyles(forBar('Compute', true, false)) (Slider);
    private EmptyGraphicsBar = withStyles(forBar('Graphics', true, false)) (Slider);
    private EmptyGraphicsMemoryBar = withStyles(forBar('GraphicsMemory', true, false)) (Slider);
    private EmptyMemoryBar = withStyles(forBar('Memory', true, false)) (Slider);
    
    private ExpertGraphicsBar = withStyles(forBar('Graphics', false, true)) (Slider);
    private ExpertComputeBar = withStyles(forBar('Compute', false, true)) (Slider);
    private ExpertMemoryBar = withStyles(forBar('Memory', false, true)) (Slider);
    private ExpertDiskBar = withStyles(forBar('Disk', false, true)) (Slider);
    
    private ExpertEmptyGraphicsBar = withStyles(forBar('Graphics', true, true)) (Slider);
    private ExpertEmptyComputeBar = withStyles(forBar('Compute', true, true)) (Slider);
    private ExpertEmptyMemoryBar = withStyles(forBar('Memory', true, true)) (Slider);
    private ExpertEmptyDiskBar = withStyles(forBar('Disk', true, true)) (Slider);

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const machine = this.props.machine
        const machines = Global.user.machines
        const title = machine instanceof NoMachine ? 'No matching machines' : '';
        return (
            <ExtraInfo reminder={title}>
                <DIV
                    sx={{display: 'inline-flex', width: '262px', }}
                    title={machine.getDetails()}
                >
                    <DIV sx={{width: '100%', lineHeight: '9px', textAlign: 'left'}}>
                        {Global.expertModeSelected ? (
                            <>
                                <DIV sx={{width: '100%', display: 'inline-flex'}}>
                                    {machine.graphicsRating > 0 ? (
                                        <this.ExpertGraphicsBar
                                            id={machine.name + '-graphics'}
                                            value={machine.graphicsScore}
                                            max={machines.graphicsScoreMax}
                                            step={100}
                                            disabled
                                        />
                                    ) : (
                                        <this.ExpertEmptyGraphicsBar disabled />
                                    )}
                                    <DIV sx={{zIndex: 1, minWidth: COLUMN_WIDTH_1, margin: COLUMN_MARGIN, fontSize: FONT_SIZE, lineHeight: FONT_SIZE}}>
                                        GPU: {(machine.graphicsNumCards > 0 ? (machine.graphicsNumCards + ' ' + machine.graphicsCardType) : 'None')}
                                    </DIV>
                                </DIV>
                                <DIV sx={{width: '100%', display: 'inline-flex'}}>
                                    {machine.memoryRating > 0 ? (
                                        <this.ExpertComputeBar
                                            id={machine.name + '-compute'}
                                            value={machine.computeScore[1]}
                                            max={machines.computeScoreMax}
                                            step={100}
                                            disabled
                                        />
                                    ) : (
                                        <this.ExpertEmptyComputeBar disabled />
                                    )}
                                    <DIV sx={{zIndex: 1, minWidth: COLUMN_WIDTH_1, margin: COLUMN_MARGIN, fontSize: FONT_SIZE, lineHeight: FONT_SIZE}}>
                                        CPU: {(machine.computeCores[1] == machine.computeCores[2] ? Math.round(machine.computeCores[1] * 100) / 100 : Math.round(machine.computeCores[1] * 100) / 100 + `-` + Math.round(machine.computeCores[2] * 100) / 100)} cores
                                    </DIV>
                                </DIV>
                                <DIV sx={{width: '100%', display: 'inline-flex'}}>                
                                    {machine.memoryRating > 0 ? (
                                        <this.ExpertMemoryBar
                                            id={machine.name + '-memory'}
                                            value={machine.memorySize}
                                            max={machines.memorySizeMax}
                                            step={1024}
                                            disabled
                                        />
                                    ) : (
                                        <this.ExpertEmptyMemoryBar disabled />
                                    )}
                                    <DIV sx={{zIndex: 1,minWidth: COLUMN_WIDTH_1, margin: COLUMN_MARGIN, fontSize: FONT_SIZE, lineHeight: FONT_SIZE}}>
                                        RAM: {FormatUtils.styleCapacityUnitValue()(machine.memorySize)}
                                    </DIV>
                                </DIV>
                                <DIV sx={{width: '100%', display: 'inline-flex'}}>                
                                    {machine.memoryRating > 0 ? (
                                        <this.ExpertDiskBar
                                            id={machine.name + '-disk'}
                                            value={machine.storageSize}
                                            max={machines.storageSizeMax}
                                            step={1024}
                                            disabled
                                        />
                                    ) : (
                                        <this.ExpertEmptyDiskBar disabled />
                                    )}
                                    <DIV sx={{zIndex: 1,minWidth: COLUMN_WIDTH_1, margin: COLUMN_MARGIN, fontSize: FONT_SIZE, lineHeight: FONT_SIZE}}>
                                        Disk: {FormatUtils.styleCapacityUnitValue()(machine.storageSize)}
                                    </DIV>
                                </DIV>
                            </>
                        ) : (machine.graphicsNumCards > 0 ? (
                            <>
                                <DIV sx={{width: '100%', display: 'inline-flex'}}>
                                    {machine.graphicsRating > 0 ? (
                                        <this.GraphicsBar
                                            id={machine.name + '-graphics'}
                                            value={machine.graphicsScore}
                                            max={machines.graphicsScoreMax}
                                            step={100}
                                            disabled
                                        />
                                    ) : (
                                        <this.EmptyGraphicsBar disabled />
                                    )}
                                    <DIV sx={{zIndex: 1, minWidth: COLUMN_WIDTH_1, margin: COLUMN_MARGIN, fontSize: FONT_SIZE, lineHeight: FONT_SIZE}}>
                                        GPU: {(machine.graphicsNumCards > 0 ? (machine.graphicsNumCards + ' ' + machine.graphicsCardType) : 'None')}
                                    </DIV>
                                </DIV>
                                <DIV sx={{width: '100%', display: 'inline-flex'}}>
                                    {machine.memoryRating > 0 ? (
                                        <this.GraphicsMemoryBar
                                            id={machine.name + '-graphicsmemory'}
                                            value={machine.graphicsMemory}
                                            max={machines.graphicsMemoryMax}
                                            step={1024}
                                            disabled
                                        />
                                    ) : (
                                        <this.EmptyGraphicsMemoryBar disabled />
                                    )}
                                    <DIV sx={{zIndex: 1, minWidth: COLUMN_WIDTH_1, margin: COLUMN_MARGIN, fontSize: FONT_SIZE, lineHeight: FONT_SIZE}}>
                                        vRAM: {FormatUtils.styleCapacityUnitValue()(machine.graphicsMemory)}
                                    </DIV>
                                </DIV>
                                <DIV sx={{width: '100%', display: 'inline-flex'}}>                
                                    {machine.memoryRating > 0 ? (
                                        <this.MemoryBar
                                            id={machine.name + '-memory'}
                                            value={machine.memorySize}
                                            max={machines.memorySizeMax}
                                            step={1024}
                                            disabled
                                        />
                                    ) : (
                                        <this.EmptyMemoryBar disabled />
                                    )}
                                    <DIV sx={{zIndex: 1,minWidth: COLUMN_WIDTH_1, margin: COLUMN_MARGIN, fontSize: FONT_SIZE, lineHeight: FONT_SIZE}}>
                                        RAM: {FormatUtils.styleCapacityUnitValue()(machine.memorySize)}
                                    </DIV>
                                </DIV>
                            </>
                        ) : (
                            <>
                                <DIV sx={{width: '100%', display: 'inline-flex'}}>
                                    {machine.memoryRating > 0 ? (
                                        <this.ComputeBar
                                            id={machine.name + '-compute'}
                                            value={machine.computeScore}
                                            max={machines.computeScoreMax}
                                            step={100}
                                            disabled
                                        />
                                    ) : (
                                        <this.EmptyComputeBar disabled />
                                    )}
                                    <DIV sx={{zIndex: 1, minWidth: COLUMN_WIDTH_1, margin: COLUMN_MARGIN, fontSize: FONT_SIZE, lineHeight: FONT_SIZE}}>
                                        CPU: {(machine.computeCores[1] == machine.computeCores[2] ? Math.round(machine.computeCores[1] * 100) / 100 : Math.round(machine.computeCores[1] * 100) / 100 + `-` + Math.round(machine.computeCores[2] * 100) / 100)} cores
                                    </DIV>
                                </DIV>
                                <DIV sx={{width: '100%', display: 'inline-flex'}}>                
                                    {machine.memoryRating > 0 ? (
                                        <this.MemoryBar
                                            id={machine.name + '-memory'}
                                            value={machine.memorySize}
                                            max={machines.memorySizeMax}
                                            step={1024}
                                            disabled
                                        />
                                    ) : (
                                        <this.EmptyMemoryBar disabled />
                                    )}
                                    <DIV sx={{zIndex: 1,minWidth: COLUMN_WIDTH_1, margin: COLUMN_MARGIN, fontSize: FONT_SIZE, lineHeight: FONT_SIZE}}>
                                        RAM: {FormatUtils.styleCapacityUnitValue()(machine.memorySize)}
                                    </DIV>
                                </DIV>
                            </>
                        ))}
                    </DIV>
                </DIV>
            </ExtraInfo>
        )
    }
}
