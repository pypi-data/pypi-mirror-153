/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { Global } from '../Global';

import { Theme } from '@mui/system';
import { Popover } from '@mui/material';

interface IProps {
    button: JSX.Element
    popup: JSX.Element
    onOpen?: () => void
    onClose?: () => void
    close?: (close: () => void) => void
    stopPropagation?: (stopPropagation: () => void) => void
    color?: string
}

interface IState {
    open: boolean
    anchorEl: any
}

export class Popper extends React.Component<IProps, IState> {
    _isMounted = false;
    stopPropagation = false;

    public constructor(props: IProps) {
        super(props)
        if (props.close) props.close(this.handleClose)
        if (props.stopPropagation) props.stopPropagation(this.handleStopPropagation)
        this.state = {
            open: false,
            anchorEl: null,
        }
    }

    private handleClick = (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
        if (this.props.button.props.onClick) this.props.button.props.onClick();
        if (this.stopPropagation) {
            this.stopPropagation = false
            return
        }
        if (this.props.onOpen) this.props.onOpen();
        this.safeSetState({open: true, anchorEl: event.currentTarget})
    }

    private handleClose = () => {
        if (this.props.onClose) this.props.onClose();
        this.safeSetState({open: false, anchorEl: null})
    }

    private handleStopPropagation = () => {
        this.stopPropagation = true
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
		return (
            <>
                {React.cloneElement(this.props.button, {onClick: this.handleClick})}
                <Popover
                    sx={{top: (theme: Theme) => theme.spacing(0.5)}}
                    open={this.state.open}
                    anchorEl={this.state.anchorEl}
                    onClose={this.handleClose}
                    anchorOrigin={{
                        vertical: 'bottom',
                        horizontal: 'left',
                    }}
                    transformOrigin={{
                        vertical: 'top',
                        horizontal: 'left',
                    }}
                    PaperProps={{
                        style: {
                            border: this.props.color ? 'solid 1px ' + this.props.color : undefined
                        }
                    }}
                >
                    {React.cloneElement(this.props.popup, {sx: Object.assign({minWidth: 'var(--jp-sidebar-min-width)'}, this.props.popup.props.sx)})}
                </Popover>
            </>
		);
	}

    public componentDidMount = () => {
		this._isMounted = true;
	}

	public componentWillUnmount = () => {
		this._isMounted = false;
	}

    private safeSetState = (map: any) => {
		if (this._isMounted) {
			let update = false
			try {
				for (const key of Object.keys(map)) {
					if (JSON.stringify(map[key]) !== JSON.stringify((this.state as any)[key])) {
						update = true
						break
					}
				}
			} catch (error) {
				update = true
			}
			if (update) {
				if (Global.shouldLogOnSafeSetState) console.log('SafeSetState (' + new Date().getSeconds() + ')');
				this.setState(map)
			} else {
				if (Global.shouldLogOnSafeSetState) console.log('SuppressedSetState (' + new Date().getSeconds() + ')');
			}
		}
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
