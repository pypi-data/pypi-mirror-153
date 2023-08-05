/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global } from '../../Global';

import { Dialog, DialogContent, DialogTitle, IconButton, Tab, Tabs } from '@mui/material';
import { CSSProperties, withStyles } from '@mui/styles';
import { MoreVert as PopupIcon, Close as CloseIcon } from '@mui/icons-material';

import { Machine, NoMachine } from './Machine';
import { ShadowedDivider } from '../../core';
import { MachineCapability } from './MachineCapabilities';
import FormatUtils from '../../utils/FormatUtils';
import { App } from '../application/App';

const StyledDialog = withStyles({
    paper: {
        width: 'calc(min(80%, 600px + 150px + 2px))',
        height: '80%',
        overflowY: 'visible',
        maxWidth: 'inherit',
    },
})(Dialog);

const enum Page {
    CAPABILITY = 0,
    STATUS = 1,
    COST = 2,
}

interface IProps {
    style?: CSSProperties
    machine: Machine
    onOpen?: () => void
	onClose?: () => void
    onMouseOver?: (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => void
    onMouseOut?: (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => void
}

interface IState {
    open: boolean,
    selectedPanel: number
}

// TODO:Beck The popup needs to be abstracted out, there is too much going on to reproduce it in more than one file
export class PopupMachineComponent extends React.Component<IProps, IState> {
    private _isMounted = false

    constructor(props: IProps) {
        super(props);
		this.state = {
            open: false,
            selectedPanel: Page.CAPABILITY,
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

    private handleMouseOver = (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
        if (this.props.onMouseOver) this.props.onMouseOver(event);
    }

    private handleMouseOut = (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
        if (this.props.onMouseOut) this.props.onMouseOut(event);
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const machine = this.props.machine
        var placedApp: App;
        if (machine.app) {
            for (var app of Global.user.appTracker.activeJobsOrSessions) {
                if (app.uuid == machine.app) {
                    placedApp = app;
                }
            }
        }
        return <>
            <IconButton
                size='large'
                disabled={machine instanceof NoMachine}
                onClick={this.handleClickOpen}
                sx={{
                    display: 'inline-block',
                    width: '36px',
                    height: '36px',
                    padding: '3px',
                }}
                onMouseOver={this.handleMouseOver}
                onMouseOut={this.handleMouseOut}
            >
                <PopupIcon
                    sx={{
                        width: '30px',
                        height: '30px',
                        padding: '3px',
                    }}
                />
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
                        minWidth: '150px',
                        fontSize: '16px',
                        fontWeight: 'bold',
                        paddingRight: '12px', // this is 6px counteracting the DialogTitle padding and 6px aligning the padding to the right of the tabs
                    }}>
                        <DIV sx={{margin: 'auto'}}>
                            Machine
                        </DIV>
                    </DIV>
                    <DIV sx={{
                        width: '100%',
                        display: 'inline-flex',
                        fontSize: '16px',
                        fontWeight: 'bold',
                        padding: '10px',
                    }}>
                    </DIV>
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
                        <CloseIcon
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
                    display: 'flex', 
                    height: 'calc(100% - 60px - 2px)',
                    fontSize: 'var(--jp-ui-font-size1)',
                }}>
                    <DIV sx={{width: '150px'}}>
                        <DialogContent sx={{padding: '0px'}}>
                            <DIV sx={{padding: '6px'}}>
                                <Tabs
                                    value={this.state.selectedPanel}
                                    onChange={(event, newValue) => this.safeSetState({selectedPanel: newValue})}
                                    orientation='vertical'
                                    variant='fullWidth'
                                    indicatorColor='primary'
                                    textColor='primary'
                                    sx={{minHeight: '24px'}}
                                >
                                    <Tab
                                        disableRipple
                                        label='Capability'
                                        sx={{
                                            padding: '0px',
                                            minWidth: 'auto',
                                            minHeight: '36px',
                                        }}
                                    />
                                    <Tab
                                        disableRipple
                                        label='Status'
                                        sx={{
                                            padding: '0px',
                                            minWidth: 'auto',
                                            minHeight: '36px',
                                        }}
                                    />
                                    <Tab
                                        disableRipple
                                        label='Cost'
                                        sx={{
                                            padding: '0px',
                                            minWidth: 'auto',
                                            minHeight: '36px',
                                        }}
                                    />
                                </Tabs>
                            </DIV>
                        </DialogContent>
                    </DIV>
                    <ShadowedDivider orientation='vertical' />
                    <DIV sx={{display: 'flex', flexFlow: 'column', overflow: 'hidden', width: 'calc(100% - 150px)', height: '100%'}}>
                        <DialogContent sx={{ padding: '0px', flexGrow: 1, overflowY: 'auto' }}>
                            {this.state.selectedPanel == Page.CAPABILITY ? (
                                <MachineCapability machine={machine}/>
                            ) : this.state.selectedPanel == Page.STATUS ? (
                                <>
                                    <DIV sx={{ margin: '6px' }}>
                                        {this.props.machine.getStateMessage() == '' ? 'Machine currently has no status' : 'Machine is currently ' + this.props.machine.getStateMessage().toLowerCase()}
                                    </DIV>
                                    {placedApp && (
                                        <DIV sx={{ margin: '6px' }}>
                                            {(placedApp.interactive ? 'Session' : 'Job') + " '" + placedApp.name + "' (" + placedApp.annotationOrRunNum + ") is " + (((placedApp.preparing.completed && !placedApp.preparing.error) && !placedApp.running.completed) ? 'running on' : 'waiting for') + ' this machine'}
                                        </DIV>
                                    )}
                                </>
                            ) : this.state.selectedPanel == Page.COST && (
                                <DIV sx={{ margin: '6px' }}>
                                    Machine costs {FormatUtils.styleRateUnitValue()(machine.rate) + (machine.promo ? ' (promotional price)' : '')}
                                </DIV>
                            )}
                        </DialogContent>
                    </DIV>
                </DIV>
            </StyledDialog>
        </>;
    }

    public componentDidMount = () => {
        this._isMounted = true
    }

    public componentWillUnmount = () => {
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
