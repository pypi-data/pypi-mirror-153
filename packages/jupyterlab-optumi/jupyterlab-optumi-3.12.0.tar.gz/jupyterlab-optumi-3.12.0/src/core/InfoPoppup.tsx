/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { DIV, Global } from '../Global';

import { Dialog, DialogTitle, IconButton } from '@mui/material';
import { withStyles } from '@mui/styles';
import { Close, InfoOutlined } from '@mui/icons-material';

import { ShadowedDivider } from '.';
import { SxProps, Theme } from '@mui/system';

const StyledDialog = withStyles({
    paper: {
        width: 'calc(min(80%, 600px + 2px))',
        // width: '100%',
        // height: '80%',
        overflowY: 'visible',
        maxWidth: 'inherit',
    },
})(Dialog);

interface IProps {
    sx?: SxProps<Theme>
    title: string
    popup: JSX.Element
}

interface IState {
    hovered: boolean
    open: boolean
}

export class InfoPopup extends React.Component<IProps, IState> {
    _isMounted = false;

    public constructor(props: IProps) {
        super(props)
        this.state = {
            hovered: false,
            open: false,
        }
    }
    
    private handleClickOpen = () => {
		this.safeSetState({ open: true });
	}

	private handleClose = () => {
        this.safeSetState({ open: false });
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
		return <>
            <IconButton
                size='large'
                onClick={this.handleClickOpen}
                sx={Object.assign({padding: 0, marginY: 'auto', marginRight: -0.25, marginLeft: 0}, this.props.sx)}
                onMouseOver={() => this.safeSetState({hovered: true})}
                onMouseOut={() => this.safeSetState({hovered: false})}
            >
                <InfoOutlined sx={{width: '14px', height: '14px', color: this.state.hovered || this.state.open ? 'primary.light' : 'text.disabled'}}/>
            </IconButton>
            <StyledDialog
                open={this.state.open}
                onClose={this.handleClose}
                scroll='paper'
            >
                <DialogTitle
                    sx={{
                        display: 'inline-flex',
                        height: '60px',
                        padding: '6px',
                    }}>
                    <DIV sx={{
                        display: 'inline-flex',
                        minWidth: '225px',
                        fontSize: '16px',
                        fontWeight: 'bold',
                        paddingRight: 1, // this is 0.5 counteracting the DialogTitle padding and 0.5 aligning the padding to the right of the tabs
                    }}>
                        <DIV sx={{marginY: 'auto', marginX: 0.5, paddingLeft: 1}}>
                            {this.props.title}
                        </DIV>
                    </DIV>
                    <DIV sx={{flexGrow: 1}} />
                    <IconButton
                        size='large'
                        onClick={this.handleClose}
                        sx={{
                            display: 'inline-block',
                            width: '36px',
                            height: '36px',
                            padding: 0.25,
                            margin: 0.5,
                        }}
                    >
                        <Close
                            sx={{
                                width: '30px',
                                height: '30px',
                                padding: 0.25,
                            }}
                        />
                    </IconButton>
                </DialogTitle>
                <ShadowedDivider />
                <DIV sx={{
                    padding: 1,
                    fontSize: 'var(--jp-ui-font-size1)',
                }}>
                    {this.props.popup}
                </DIV>
            </StyledDialog>
        </>;
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
