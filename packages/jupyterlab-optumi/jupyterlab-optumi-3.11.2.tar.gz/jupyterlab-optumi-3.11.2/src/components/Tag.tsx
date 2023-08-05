/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global } from '../Global';

import { alpha, darken, lighten, SxProps, Theme } from '@mui/system';
import { Chip, CircularProgress } from '@mui/material';
import { withStyles } from '@mui/styles';
import { Colors } from '../Colors';

interface IProps {
    id?: string
    label?: string
    color?: string
    showLoading?: boolean
    percentLoaded?: number
    icon? : JSX.Element;
    onMouseOver?: (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => void
    onMouseOut?: (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => void
    onClick?: () => void
    sx?: SxProps<Theme>
}

interface IState {}

const progressBorderSize: number = 1

export class Tag extends React.Component<IProps, IState> {
    StyledChip: any;
    StyledCircularProgress: any;

    public constructor(props: IProps) {
        super(props);
        this.StyledChip = this.getStyledChip();
        this.StyledCircularProgress = this.getStyledCircularProgress();
    }

    private getStyledCircularProgress = () => {
        return withStyles({
            root: {
                color: Global.themeManager == undefined || Global.themeManager.isLight(Global.themeManager.theme) ? darken(this.props.color || Colors.CHIP_GREY, 0.35) : lighten(this.props.color || Colors.CHIP_GREY, 0.35),
            },
        }) (CircularProgress);
    }

    private getStyledChip = () => {
        return withStyles({
            root: {
                position: 'relative',
                bottom: '0px',
                margin: `${progressBorderSize}px`,
                height: '18px',
                backgroundColor: alpha(this.props.color || Colors.CHIP_GREY, 0.25),
                fontSize: 'var(--jp-ui-font-size1)',
                color: Global.themeManager == undefined || Global.themeManager.isLight(Global.themeManager.theme) ? darken(this.props.color || Colors.CHIP_GREY, 0.35) : lighten(this.props.color || Colors.CHIP_GREY, 0.35),
                // fontWeight: 'bold',
            },
            label: {
                overflow: 'visible',
            },
            icon: {
                fontSize: '14px !important',
            },
        }) (Chip);
    }

    private handleMouseOver = (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => {
        if (this.props.onMouseOver) this.props.onMouseOver(event);
    }

    private handleMouseOut = (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => {
        if (this.props.onMouseOut) this.props.onMouseOut(event);
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const fontSize = getComputedStyle(document.documentElement).getPropertyValue('--jp-ui-font-size1').trim()
        const fontFamily = getComputedStyle(document.documentElement).getPropertyValue('--jp-ui-font-family').trim()
        return (
            <>
                {((this.props.label != "" && this.props.label != undefined) || (this.props.icon != undefined)) &&
                    <DIV
                        sx={Object.assign({
                            position: 'relative',
                            margin: '3px',
                        }, this.props.sx)}
                        onMouseOver={this.handleMouseOver}
                        onMouseOut={this.handleMouseOut}
                    >
                        <this.StyledChip
                            onClick={this.props.onClick}
                            key={this.props.label + this.props.color + this.props.icon}
                            id={this.props.id}
                            size='small'
                            label={this.props.label}
                            icon={this.props.showLoading ? (
                                <DIV sx={{height: '16px'}}>
                                    {
                                        this.props.percentLoaded === undefined ? (
                                            <this.StyledCircularProgress 
                                                size='14px'
                                                thickness={6}
                                            />
                                        ) : (
                                            <this.StyledCircularProgress
                                                size='14px'
                                                thickness={6}
                                                variant='determinate'
                                                value={this.props.percentLoaded * 100}
                                            />
                                        )
                                    }
                                </DIV>
                            ) : (
                                <DIV sx={{height: '14px'}}>
                                    {this.props.icon}
                                </DIV>
                            )}
                            sx={{
                                width: (this.props.label != "" && this.props.label != undefined) ? ((Global.getStringWidth(this.props.label, fontSize + " " + fontFamily) + 14) + (this.props.showLoading || this.props.icon ? 14 : 0)) + 'px' : '18px',
                            }}
                        />
                    </DIV>
                }
            </>
        )
    }

    private handleThemeChange = () => {
        this.StyledChip = this.getStyledChip();
        this.StyledCircularProgress = this.getStyledCircularProgress();
        this.forceUpdate()
    }

    public componentDidMount = () => {
        Global.themeManager.themeChanged.connect(this.handleThemeChange)
    }

    public componentWillUnmount = () => {
        Global.themeManager.themeChanged.disconnect(this.handleThemeChange)
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
