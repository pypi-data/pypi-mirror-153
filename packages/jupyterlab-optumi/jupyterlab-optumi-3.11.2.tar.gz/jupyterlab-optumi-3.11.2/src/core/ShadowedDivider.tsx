/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { DIV, Global } from '../Global'

import { Divider, lighten } from '@mui/material'

interface IProps {
    orientation?: 'vertical' | 'horizontal'
}

interface IState {}

export class ShadowedDivider extends React.Component<IProps, IState> {
    isLightMode: boolean = Global.themeManager == undefined || Global.themeManager.isLight(Global.themeManager.theme)
    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const darkColor = this.isLightMode ? '#bbbbbb' : 'rgba(255, 255, 255, 0.18)'
        const lightColor = this.isLightMode ? lighten(darkColor, 2/3) : 'rgba(255, 255, 255, 0.12)'
        return this.props.orientation === undefined || this.props.orientation === 'horizontal' ? (
            <>
                <Divider variant='fullWidth' sx={{backgroundColor: darkColor}} />
                <Divider variant='fullWidth' sx={{backgroundColor: lightColor}} />
            </>
        ) : this.props.orientation === 'vertical' && (
            <DIV sx={{display: 'flex', height: '100%'}}>
                <Divider orientation='vertical' variant='fullWidth' sx={{backgroundColor: darkColor}} />
                <Divider orientation='vertical' variant='fullWidth' sx={{backgroundColor: lightColor}} />
            </DIV>
        )
    }

    private handleThemeChange = () => {this.isLightMode = Global.themeManager == undefined || Global.themeManager.isLight(Global.themeManager.theme); this.forceUpdate()}

    public componentDidMount = () => {
        Global.themeManager.themeChanged.connect(this.handleThemeChange)
    }

    public componentWillUnmount = () => {
        Global.themeManager.themeChanged.disconnect(this.handleThemeChange)
    }
}
