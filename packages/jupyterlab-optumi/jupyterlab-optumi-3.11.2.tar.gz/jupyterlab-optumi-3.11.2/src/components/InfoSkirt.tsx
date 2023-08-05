/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global } from '../Global';

import { SxProps, Theme } from '@mui/system';
import { Paper } from '@mui/material';

interface IProps {
    sx?: SxProps<Theme>
    children: JSX.Element
    leftButton?: JSX.Element
    rightButton?: JSX.Element
    tags: JSX.Element[]
    onMouseOver?: (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => void
    onMouseOut?: (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => void
}

interface IState {}

export class InfoSkirt extends React.Component<IProps, IState> {

    private handleMouseOver = (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => {
        if (this.props.onMouseOver) this.props.onMouseOver(event);
    }

    private handleMouseOut = (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => {
        if (this.props.onMouseOut) this.props.onMouseOut(event);
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');

        return (
            <Paper
                elevation={1}
                sx={Object.assign({
                    width: '100%',
                    padding: '3px',
                    backgroundColor: 'var(--jp-layout-color2)',
                    borderRadius: '3px',
                }, this.props.sx)}
                onMouseOver={this.handleMouseOver}
                onMouseOut={this.handleMouseOut}
            >
                <DIV sx={{
                    display: 'inline-flex',
                    width: '100%',
                }}>
                    <DIV sx={{
                        width: '100%',
                        margin: '3px 0px 3px 3px',
                        overflow: 'hidden',
                    }}>
                        {this.props.children}
                    </DIV>
                    <DIV sx={{
                        display: 'inline-flex',
                        minWidth: this.props.leftButton && this.props.rightButton? '82px' : '50px',
                        margin: '10px 3px 0px 0px',
                    }}>
                        {this.props.leftButton && (
                            <DIV sx={{margin: this.props.rightButton ? 'auto 0 auto auto' : '0px 10px 0px 4px'}}>
                                {this.props.leftButton}
                            </DIV>
                        )}
                        {this.props.rightButton && (
                            <DIV sx={{margin: this.props.leftButton ? 'auto auto auto 0' : '0px 4px 0px 10px'}}>
                                {this.props.rightButton}
                            </DIV>
                        )}
                    </DIV>
                </DIV>
                <DIV sx={{
                    display: 'inline-flex',
                    flexWrap: 'wrap',
                    width: '100%',
                }}>
                    <DIV sx={{
                        display: 'inline-flex',
                        flexGrow: 1,
                    }}>
                        {this.props.tags.length == 0 ? (
                            <DIV sx={{
                                minWidth: '74px',
                                height: '20px',
                            }}/>
                        ) : (
                            this.props.tags
                        )}
                    </DIV>
                </DIV>
            </Paper>
        );
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
