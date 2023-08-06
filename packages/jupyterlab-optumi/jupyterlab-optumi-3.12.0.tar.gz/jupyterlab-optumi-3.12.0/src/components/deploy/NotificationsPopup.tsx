/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { DIV, Global } from '../../Global';

import { SxProps, Theme } from '@mui/system';
import { Dialog, DialogTitle, IconButton } from '@mui/material';
import { withStyles } from '@mui/styles';
import { AddAlert, Close } from '@mui/icons-material';

import { ShadowedDivider } from '../../core';
import { OptumiConfig } from '../../models/OptumiConfig';
import { NotificationContent } from '../../core/NotificationContent'

const StyledDialog = withStyles({
    paper: {
        width: 'calc(min(80%, 600px + 150px + 2px))',
        // width: '100%',
        height: '80%',
        overflowY: 'visible',
        maxWidth: 'inherit',
    },
})(Dialog);

interface IProps {
    sx?: SxProps<Theme>
    onOpen?: () => void
    onClose?: () => void
    disabled?: boolean
}

interface IState {
    open: boolean,
}

// TODO:Beck The popup needs to be abstracted out, there is too much going on to reproduce it in more than one file
export class NotificationsPopup extends React.Component<IProps, IState> {
    private _isMounted = false

    constructor(props: IProps) {
        super(props);
		this.state = {
            open: false,
		};
    }
    
    private handleClickOpen = () => {
        if (this.props.onOpen) this.props.onOpen()
		this.safeSetState({ open: true });
	}

	private handleClose = () => {
        this.safeSetState({ open: false });
        if (this.props.onClose) this.props.onClose()
    }

    private handleKeyDown = (event: KeyboardEvent) => {
        if (event.key === 'Escape') this.handleClose();
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <DIV sx={Object.assign({margin: 'auto'}, this.props.sx)}>
                <IconButton
                    size='large'
                    onClick={this.handleClickOpen}
                    sx={{padding: '0px', marginRight: '-3px', width: '30px', height: '30px'}}
                    disabled={this.props.disabled}
                >
                    <AddAlert sx={{height: '21px'}}/>
                </IconButton>
                <StyledDialog
					open={this.state.open}
					onClose={this.handleClose}
                    scroll='paper'
				>
					<DialogTitle sx={{
                        display: 'inline-flex',
                        height: '60px',
                        padding: '6px',
                    }}>
                        <DIV sx={{
                            display: 'inline-flex',
                            minWidth: '225px',
                            fontSize: '16px',
                            fontWeight: 'bold',
                            paddingRight: '12px', // this is 6px counteracting the DialogTitle padding and 6px aligning the padding to the right of the tabs
                        }}>
                            <DIV sx={{margin: 'auto', paddingLeft: '12px'}}>
            					Configure Notifications
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
                                padding: '3px',
                                margin: '6px',
                            }}
                        >
                            <Close
                                sx={{
                                    width: '30px',
                                    height: '30px',
                                    padding: '3px',
                                }}
                            />
                        </IconButton>
					</DialogTitle>
                    <ShadowedDivider />
                    <DIV sx={{
                        padding: '12px',
                        fontSize: 'var(--jp-ui-font-size1)',
                    }}>
                        <NotificationContent 
                            getValue={() => Global.metadata.getMetadata().config}
                            saveValue={(config: OptumiConfig) => {
                                const metadata = Global.metadata.getMetadata();
                                metadata.config = config;
                                Global.metadata.setMetadata(metadata);
                            }}
                            handleClose={this.handleClose}
                        />
                    </DIV>
				</StyledDialog>
            </DIV>
        );
    }

    public componentDidMount = () => {
        this._isMounted = true
        Global.setLink(Global.Target.DeployTab.NotificationsPopup, () => {
            if (!this.props.disabled) this.safeSetState({open: true});
        })
        document.addEventListener('keydown', this.handleKeyDown, false)
    }

    public componentWillUnmount = () => {
        document.removeEventListener('keydown', this.handleKeyDown, false)
        Global.deleteLink(Global.Target.DeployTab.NotificationsPopup)
        this._isMounted = false
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
}
