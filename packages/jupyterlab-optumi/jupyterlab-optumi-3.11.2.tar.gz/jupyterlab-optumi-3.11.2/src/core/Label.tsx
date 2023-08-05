/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global } from '../Global';

import { SxProps, Theme } from '@mui/system';

interface IProps<T> {
    sx?: SxProps<Theme>
    label: string
    labelWidth?: string
    getValue: () => T
    styledUnitValue?: (value: T) => string
    align?: 'left' | 'center' | 'right'
    valueAlign?: 'left' | 'center' | 'right'
    lineHeight?: string
    info?: JSX.Element
    infoRight: JSX.Element
}

interface IState<T> {}

export class Label<T> extends React.Component<IProps<T>, IState<T>> {

    static defaultProps: Partial<IProps<any>> = {
        styledUnitValue: (value: any) => { return value.toString() },
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <DIV
                sx={Object.assign({display: 'inline-flex', width: '100%', padding: '3px 0px', position: 'relative'}, this.props.sx)}
            >
                <DIV sx={{
                    minWidth: this.props.labelWidth || '68px',
                    maxWidth: this.props.labelWidth || '68px',
                    height: this.props.lineHeight || '24px',
                    margin: '0px 12px',
                    lineHeight: this.props.lineHeight || '24px',
                    textAlign: this.props.align || 'center',
                    whiteSpace: 'pre',
                }}>
                    {this.props.label}
                    {this.props.info}
                </DIV>
                <DIV sx={{
                    width: '100%',
                    height: this.props.lineHeight || '24px',
                    margin: '0px 6px',
                    lineHeight: this.props.lineHeight || '24px',
                    textAlign: this.props.valueAlign || 'left',
                }}>
                    <DIV sx={{padding: '0px 6px', fontSize: '12px'}}>
                        {this.props.styledUnitValue(this.props.getValue())}
                    </DIV>
                </DIV>
                {this.props.infoRight && (
                    <DIV sx={{position: 'absolute', right: '-6px'}}>
                        {this.props.infoRight}
                    </DIV>
                )}
            </DIV>
        )
    }

    // public shouldComponentUpdate = (nextProps: IProps<any>, nextState: IState<any>): boolean => {
    //     try {
    //         if (JSON.stringify(this.props) != JSON.stringify(nextProps)) return true;
    //         if (JSON.stringify(this.state) != JSON.stringify(nextState)) return true;
    //         if (Global.shouldLogOnRender) console.log('SuppressedRender (' + new Date().getSeconds() + ')');
    //         return false;
    //     } catch (error) {
    //         return true;
    //     }
    // }
}
