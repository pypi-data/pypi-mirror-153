/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global } from '../Global';

import { SxProps, Theme } from '@mui/system';

interface IProps {
    sx?: SxProps<Theme>
    title: string
    align?: 'left' | 'center' | 'right'
    grey?: boolean
}

interface IState {}

export class Header extends React.Component<IProps, IState> {
    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <DIV sx={Object.assign({
                textAlign: this.props.align || 'left',
                fontSize: '16px',
                fontWeight: 'bold',
                lineHeight: '18px',
                margin: '6px'
            }, this.props.sx)}>
                {this.props.title}
            </DIV>
        )
    }
}

export class SubHeader extends React.Component<IProps, IState> {
    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <DIV sx={Object.assign({
                textAlign: this.props.align || 'left',
                fontSize: '14px',
                fontWeight: 'bold',
                lineHeight: '18px',
                margin: '6px',
                opacity: this.props.grey ? 0.5 : 1,
            }, this.props.sx)}>
                {this.props.title}
            </DIV>
        )
    }
}


export class SubSubHeader extends React.Component<IProps, IState> {
    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <DIV sx={Object.assign({
                textAlign: this.props.align || 'left',
                fontSize: '13px',
                lineHeight: '18px',
                margin: '6px',
                color: 'var(--jp-ui-font-color2)',
            }, this.props.sx)}>
                {this.props.title}
            </DIV>
        )
    }
}
