/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global } from '../Global';

import { SxProps, Theme } from '@mui/system';
import { darken, lighten, Paper } from '@mui/material';

interface IProps {
    sx?: SxProps<Theme>
    children?: JSX.Element | JSX.Element[]
    statusColor: string
    opened?: boolean,
}

interface IState {}

export class StatusWrapper extends React.Component<IProps, IState> {

    private isLightMode: boolean = false;

    constructor(props: IProps) {
        super(props);
        this.isLightMode = Global.themeManager == undefined || Global.themeManager.isLight(Global.themeManager.theme)
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        var color: string = this.props.statusColor;
        if (!color) color = 'var(--jp-layout-color2)';
        if (color.startsWith('var')) {
            color = getComputedStyle(document.documentElement).getPropertyValue(color.replace('var(', '').replace(')', '')).trim();
        }

        return (
            <DIV sx={this.props.sx}>
                <Paper elevation={0} sx={{
                    background: this.props.opened ? (this.isLightMode ? darken(color, 0.5) : lighten(color, 0.5)) : color,
                    transition: 'background 750ms cubic-bezier(0.4, 0, 0.2, 1) 0ms',
                }}>
                    <DIV sx={{marginLeft: '6px', padding: '2px'}}>
                        {this.props.children}
                    </DIV>
                </Paper>
            </DIV>
        );
    }

    private handleThemeChange = () => {
        this.isLightMode = Global.themeManager == undefined || Global.themeManager.isLight(Global.themeManager.theme)
        this.forceUpdate();
    }

    public componentDidMount = () => {
        Global.themeManager.themeChanged.connect(this.handleThemeChange);
    }

    public componentWillUnmount = () => {
        Global.themeManager.themeChanged.disconnect(this.handleThemeChange);
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
