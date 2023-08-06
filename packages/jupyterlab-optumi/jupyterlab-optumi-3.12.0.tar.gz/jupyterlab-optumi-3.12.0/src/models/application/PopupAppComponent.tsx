/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global } from '../../Global';

import { Button, Dialog, DialogContent, DialogTitle, IconButton, Tab, Tabs } from '@mui/material';
import { CSSProperties, withStyles } from '@mui/styles';
import { MoreVert, Close, OpenInNew, WarningRounded, GetApp } from '@mui/icons-material';

import { App } from './App';
import { ScrollableDiv } from '../../components/monitor/ScrollableDiv';
import { FileList } from '../../components/deploy/FileList';
import { Status } from '../Module';
import { MachineCapability } from '../machine/MachineCapabilities';
import { ShadowedDivider } from '../../core';
import Notebook from '../../core/notebook/Notebook';
import FileServerUtils from '../../utils/FileServerUtils';
import { NotificationContent } from '../../core/NotificationContent';
import { OptumiConfig } from '../OptumiConfig';
import { ResourceGraph } from '../../core/ResourceGraph';
import { Colors } from '../../Colors';
import { Snackbar } from '../Snackbar';
import ExtraInfo from '../../utils/ExtraInfo';

const StyledDialog = withStyles({
    paper: {
        width: '80%',
        height: '80%',
        overflowY: 'visible',
        maxWidth: 'inherit',
    },
})(Dialog);

const enum Page {
    SUMMARY = 0,
    NOTIFICATIONS = 1,
    NOTEBOOK = 2,
    FILES = 3,
    MACHINE = 4,
    LOG = 5,
    GRAPH = 6,
}

interface IProps {
    style?: CSSProperties
    app: App
    onOpen?: () => void
	onClose?: () => void
    onMouseOver?: (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => void
    onMouseOut?: (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => void
}

interface IState {
    open: boolean,
	selectedPanel: number,
	inputLine: string
}

// TODO:Beck The popup needs to be abstracted out, there is too much going on to reproduce it in more than one file
export class PopupAppComponent extends React.Component<IProps, IState> {
    private _isMounted = false

    constructor(props: IProps) {
        super(props);
		this.state = {
            open: false,
			selectedPanel: Page.SUMMARY,
			inputLine: ''
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

    private openSession = () => {
        window.open('https://' + this.props.app.machine.dnsName + ':54321?token=' + this.props.app.sessionToken, '_blank');
    }

    private openAsNewNotebook = async () => {
        const app = this.props.app;
        var path = app.path.replace('.ipynb', '-' + (app.annotationOrRunNum.replace(/\W/g, '')) + '.ipynb');
        
        var inc = 0;
        var newPath = path;
        while ((await FileServerUtils.checkIfPathExists(newPath))[0]) {
            inc++;
            newPath = inc == 0 ? path : path.replace('.', '(' + inc + ').');
        }

        var notebook: any = app.notebook;
        FileServerUtils.saveNotebook(newPath, notebook).then((success: boolean) => { Global.docManager.open(newPath) });
        
        // Close the dialog
        this.handleClose();
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        var i = 0;
        const app = this.props.app;
        return <>
            <IconButton
                size='large'
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
                <MoreVert
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
                        <DIV sx={{margin: 'auto', paddingLeft: '12px'}}>
                            {app.interactive ? "Session" : "Job"}
                        </DIV>
                    </DIV>
                    <DIV sx={{width: '100%', display: 'inline-flex', overflowX: 'hidden', fontSize: '16px', paddingLeft: '8px'}}>
                        <DIV sx={{flexGrow: 1, margin: 'auto 0px'}}>
                            {app.path}
                        </DIV>
                        {app.interactive && (
                            <Button
                                sx={{margin: '6px'}}
                                disableElevation
                                variant='contained'
                                color='primary'
                                onClick={this.openSession}
                                disabled={app.getAppStatus() == Status.COMPLETED || !(app.modules.length > 0 && app.modules[0].sessionReady)}
                                endIcon={<OpenInNew />}
                            >
                                Open session
                            </Button>
                        )}
                        <Button
                            sx={{margin: '6px'}}
                            disableElevation
                            variant='contained'
                            color='primary'
                            onClick={this.openAsNewNotebook}
                            disabled={app.getAppStatus() != Status.COMPLETED}
                            endIcon={<OpenInNew />}
                        >
                            Open as a new notebook
                        </Button>
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
                <DIV sx={{display: 'flex', height: 'calc(100% - 60px - 2px)'}}>
                    <DIV sx={{width: '150px'}}>
                        <DialogContent sx={{padding: '0px'}}>
                            <DIV sx={{padding: '12px 6px'}}>
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
                                        label='Summary'
                                        sx={{
                                            padding: '0px',
                                            minWidth: 'auto',
                                            minHeight: '36px',
                                        }}
                                        value={Page.SUMMARY}
                                    />
                                    {!app.interactive && <Tab
                                        disableRipple
                                        label='Notifications'
                                        sx={{
                                            padding: '0px',
                                            minWidth: 'auto',
                                            minHeight: '36px',
                                        }}
                                        value={Page.NOTIFICATIONS}
                                    />}
                                    {!app.interactive && <Tab
                                        disableRipple
                                        label='Notebook'
                                        sx={{
                                            padding: '0px',
                                            minWidth: 'auto',
                                            minHeight: '36px',
                                        }}
                                        value={Page.NOTEBOOK}
                                    />}
                                    <Tab
                                        disableRipple
                                        label='Files'
                                        sx={{
                                            padding: '0px',
                                            minWidth: 'auto',
                                            minHeight: '36px',
                                        }}
                                        value={Page.FILES}
                                    />
                                    {/* <Tab
                                        disableRipple
                                        label='NEW_FILES'
                                        sx={{
                                            padding: '0px',
                                            minWidth: 'auto',
                                            minHeight: '36px',
                                        }}
                                        value={Page.NEW_FILES}
                                    /> */}
                                    <Tab
                                        disableRipple
                                        label='Machine'
                                        sx={{
                                            padding: '0px',
                                            minWidth: 'auto',
                                            minHeight: '36px',
                                        }}
                                        value={Page.MACHINE}
                                    />
                                    {app.modules.length > 0 && /*app.interactive &&*/ <Tab
                                        disableRipple
                                        label='Log'
                                        sx={{
                                            padding: '0px',
                                            minWidth: 'auto',
                                            minHeight: '36px',
                                        }}
                                        value={Page.LOG}
                                    />}
                                    {Global.user.showMonitoringEnabled && <Tab
                                        disableRipple
                                        label='Graph'
                                        sx={{
                                            padding: '0px',
                                            minWidth: 'auto',
                                            minHeight: '36px',
                                        }}
                                        value={Page.GRAPH}
                                    />}
                                </Tabs>
                            </DIV>
                        </DialogContent>
                    </DIV>
                    <ShadowedDivider orientation='vertical' />
                    <DIV sx={{display: 'flex', flexFlow: 'column', overflow: 'hidden', width: 'calc(100% - 150px)', height: '100%'}}>
                        <DialogContent sx={{
                            flexGrow: 1, 
                            overflowY: 'auto',
                            width: '100%',
                            height: '100%',
                            padding: '0px',
                            marginBottom: '0px', // This is because MuiDialogContentText-root is erroneously setting the bottom to 12
                            // lineHeight: 'var(--jp-code-line-height)',
                            fontSize: 'var(--jp-ui-font-size1)',
                            // fontFamily: 'var(--jp-code-font-family)',
                        }}>
                            {this.state.selectedPanel == Page.SUMMARY ? (
                                <DIV sx={{padding: '20px'}}>
                                    {app.interactive ? 'Session' : 'Job'} launched at {app.timestamp.toLocaleTimeString('en-US', { 
                                        hour: 'numeric', minute: 'numeric',
                                    })} on {app.timestamp.toLocaleDateString('en-US', { 
                                        weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' 
                                    })}
                                    <br/>
                                    {app.runNum ? (
                                        <>
                                            Run #{app.runNum + (app.config.annotation != '' ? ': ' + app.config.annotation : '')}<br/>
                                        </>
                                    ) : (
                                        <></>
                                    )}
                                    {app.getTimeElapsed() ? (
                                        <>
                                            Duration: {app.getTimeElapsed()}<br/>
                                        </>
                                    ) : (
                                        <></>
                                    )}
                                    {app.getCost() ? (
                                        <>
                                            Approximate machine cost: {app.getCost()}<br/>
                                        </>
                                    ) : (
                                        <></>
                                    )}
                                    <br/>
                                    {/* The must have unique key error apparently applies to fragments as well, despite not being able to hold keys */}
                                    {app.initializing.messages.concat(app.preparing.messages).concat(app.running.messages).filter(value => value[0].trim().length > 0).map((value: [string, string, boolean]) => (
                                        <>
                                            <DIV sx={{display: 'inline-flex', whiteSpace: 'pre'}} key={value[0] + i++}>
                                                {value[2] && (
                                                    <>
                                                        {value[1] == 'error' ? (
                                                            <WarningRounded sx={{color: Colors.ERROR, height: '16px', width: '24px'}}/>
                                                        ) : (value[1] == 'warning' ? (
                                                            <WarningRounded sx={{color: Colors.WARNING, height: '16px', width: '24px'}}/>
                                                        ) : (
                                                            <DIV sx={{width: '24px'}} />
                                                        ))}
                                                    </>
                                                )}
                                                <DIV sx={{margin: 'auto'}}>
                                                    {app.adjustMessage(value[0])}
                                                    {/* {value[0] + " " + value[1] + " " + value[2]} */}
                                                </DIV>
                                            </DIV>
                                            <br />
                                        </>
                                    ))}
                                </DIV>
                            ) : this.state.selectedPanel == Page.NOTIFICATIONS ? (
                                <DIV sx={{padding: '20px'}}>
                                    <NotificationContent 
                                        getValue={() => app.config}
                                        saveValue={(config: OptumiConfig) => app.config = config}
                                        disabled={app.getAppStatus() == Status.COMPLETED}
                                        handleClose={this.handleClose}
                                    />
                                </DIV>
                            ) : this.state.selectedPanel == Page.NOTEBOOK ? (
                                <DIV sx={{overflow: 'auto', width: '100%', height: '100%'}}>
                                    <Notebook notebook={app.notebook} />
                                </DIV>
                            ) : this.state.selectedPanel == Page.FILES ? (
                                <DIV sx={{padding: '8px'}}>
                                    {app.interactive && app.getAppStatus() != Status.COMPLETED ? (
                                        <DIV sx={{padding: '12px'}}>
                                            For active sessions, upload/download files directly from the session tab using the JupyterLab browser.
                                            <br />
                                            Files will appear here when the session has finished.
                                        </DIV>
                                    ) : (
                                        <FileList app={app} />
                                    )}
                                </DIV>
                            ) : this.state.selectedPanel == Page.MACHINE ? (
                                <DIV sx={{padding: '14px 8px'}}>
                                     {app.machine ? (
                                        <MachineCapability machine={app.machine} />
                                    ) : (
                                        <DIV sx={{padding: '6px 12px'}}>
                                            Machine information will appear when the {app.interactive ? ' session ' : ' job '} starts.
                                        </DIV>
                                    )}
                                </DIV>
                                
                            ) : this.state.selectedPanel == Page.LOG ? (
                                <DIV sx={{overflow: 'hidden', display: 'flex', flexDirection: 'column', height: '100%'}}>
                                    <ScrollableDiv
                                        key='output'
                                        source={Object.assign([], app.modules[0].output.filter(x => !x.line.startsWith('  warnings.warn(')))}
                                        autoScroll={true}
                                    />
                                    {app.modules[0].output.length > 0 && (
                                        <ExtraInfo reminder={'Download to ~/' + app.path.replace('.ipynb', '-' + (app.annotationOrRunNum.replace(/\W/g, '')) + '.log')}>
                                            <Button
                                                sx={{margin: '12px'}}
                                                onClick={async () => {
                                                    var path = app.path.replace('.ipynb', '-' + (app.annotationOrRunNum.replace(/\W/g, '')) + '.log');
                                                    var inc = 0;

                                                    var newPath = path;
                                                    while ((await FileServerUtils.checkIfPathExists(newPath))[0]) {
                                                        inc++;
                                                        newPath = inc == 0 ? path : path.replace('.', '(' + inc + ').');
                                                    }

                                                    if (Global.shouldLogOnEmit) console.log('SignalEmit (' + new Date().getSeconds() + ')');
                                                    Global.snackbarEnqueue.emit(new Snackbar(
                                                        "Downloading ~/" + newPath,
                                                        { variant: 'success', key: new Date().toISOString() }
                                                    ));

                                                    FileServerUtils.saveFile(newPath, app.modules[0].output.filter(x => !x.line.startsWith('  warnings.warn(')).map(x => x.line).join(''))
                                                }}
                                                endIcon={<GetApp />}
                                            >
                                                Download log file
                                            </Button>
                                        </ExtraInfo>
                                    )}
                                </DIV>
                            ) : this.state.selectedPanel == Page.GRAPH && (
                                <DIV sx={{overflow: 'hidden', width: '100%', height: '100%'}}>
                                    {app.modules.map(module => <ResourceGraph key={module.uuid} app={app} />)}
                                </DIV>
                            )}
                        </DialogContent>
                    </DIV>
                </DIV>
            </StyledDialog>
        </>;
    }

	private handleAppChange = () => {
		this.forceUpdate()
	}

    public componentDidMount = () => {
        this._isMounted = true
		this.props.app.changed.connect(this.handleAppChange)
    }

    public componentWillUnmount = () => {
		this.props.app.changed.disconnect(this.handleAppChange)
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
