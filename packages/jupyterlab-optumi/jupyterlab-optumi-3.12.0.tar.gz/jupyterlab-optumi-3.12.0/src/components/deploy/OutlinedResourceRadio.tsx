/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global, SPAN } from '../../Global';

import { SxProps, Theme } from '@mui/system';
import { Button } from '@mui/material';
import { withStyles } from '@mui/styles';
import { RadioButtonUnchecked as RadioButtonUncheckedIcon, CheckCircle as CheckCircleIcon } from '@mui/icons-material';

interface IProps {
    sx?: SxProps<Theme>
    label: string
    selected: boolean
    color: string
    beta?: boolean
    handleClick: () => string | void
    onMouseOver?: (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => void
    onMouseOut?: (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => void
}

interface IState {}

export class OutlinedResourceRadio extends React.Component<IProps, IState> {
    textField: React.RefObject<HTMLInputElement>

    StyledButton: any

    constructor(props: IProps) {
        super(props);
        this.StyledButton = this.getStyledButton(this.props.color);
    }

    private handleMouseOver = (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => {
        if (this.props.onMouseOver) this.props.onMouseOver(event);
    }

    private handleMouseOut = (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => {
        if (this.props.onMouseOut) this.props.onMouseOut(event);
    }

    private getStyledButton = (color: string) => {
        return withStyles({
            root: {
                textAlign: 'center',
                fontWeight: 'normal',
                display: 'inline-flex',
                padding: '0px 6px',
                height: '28px',
                border: '1px solid ' + color + '80',
                borderRadius: '6px',
                margin: '1px 6px 6px 6px',
                width: 'calc(100% - 12px)',
                transition: 'background-color 250ms cubic-bezier(0.4, 0, 0.2, 1) 0ms',
                overflow: 'hidden',
                position: 'relative',
                color: 'var(--jp-ui-font-color1)'
            },
        }) (Button)
    }
    
    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <this.StyledButton
                style={{border: this.props.selected ? '1px solid ' + this.props.color : ''}}
                sx={Object.assign({
                    backgroundColor: this.props.selected ? this.props.color + '40' : '',
                }, this.props.sx)}
                onClick={() => this.props.handleClick()}
                onMouseOver={this.handleMouseOver}
                onMouseOut={this.handleMouseOut}
            >
                <SPAN sx={{
                    flexGrow: 1,
                    lineHeight: '14px',
                    margin: 'auto auto auto 6px',
                    textAlign: 'center',
                    whiteSpace: 'pre-wrap',
                }}>
                    {(this.props.beta ? ' ' : '' /* This extra space is explicitly for 'Session' launch mode so we dont forget to remove the space when we remove the beta label */) + this.props.label}
                </SPAN>
                {this.props.selected ? (
                    <CheckCircleIcon
                        fontSize='small'
                        sx={{
                            fill: this.props.color,
                            margin: 'auto',
                        }}
                    />
                ) : (
                    <RadioButtonUncheckedIcon
                        fontSize='small'
                        sx={{
                            fill: this.props.color + '80',
                            margin: 'auto',
                        }}
                    />
                )}
                {this.props.beta && (
                    <DIV sx={{
                        position: 'absolute',
                        left: '-22px',
                        top: '3px',
                        transform: 'rotate(-45deg)',
                        background: this.props.selected ? this.props.color : this.props.color + '80',
                        color: '#ffffff',
                        fontSize: '9px',
                        lineHeight: '14px',
                        fontWeight: 'bold',
                        padding: '0px 20px',
                    }}>
                        BETA
                    </DIV>
                )}
            </this.StyledButton>
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
