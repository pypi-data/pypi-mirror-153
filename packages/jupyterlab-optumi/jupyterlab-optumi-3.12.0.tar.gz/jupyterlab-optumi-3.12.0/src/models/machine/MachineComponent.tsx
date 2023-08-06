/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../../Global';

import { CircularProgress, IconButton } from '@mui/material';
import { Delete as DeleteIcon } from '@mui/icons-material';

import { ServerConnection } from '@jupyterlab/services';

import { Machine } from './Machine';
import { Tag } from '../../components/Tag';
import { InfoSkirt } from '../../components/InfoSkirt';
import { User } from '../User';
import WarningPopup from '../../core/WarningPopup';
import FormatUtils from '../../utils/FormatUtils';
import ExtraInfo from '../../utils/ExtraInfo';
import { App } from '../application/App';

interface IProps {
    machine: Machine
}

interface IState {
    showDeleteMachinePopup: boolean;
    waiting: boolean;
    spinning: boolean;
    deleting: boolean;  // Extra variable to avoid flickering trash can 
}

export class MachineComponent extends React.Component<IProps, IState> {
    _isMounted = false;

    constructor(props: IProps) {
        super(props);
        this.state = {
            showDeleteMachinePopup: false,
            waiting: false,
            spinning: false,
            deleting: false,
        };
    }

    private stopApp = (app: App): Promise<string> => {
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/stop-notebook";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				workload: app.uuid,
				module: app.modules[0].uuid,
			}),
		};
		return ServerConnection.makeRequest(
			url,
			init,
			settings
		).then((response: Response) => {
			Global.handleResponse(response);
            return response.text();
		});
    }

    private deleteApp = (workload: string, module: string): Promise<string> => {
        const settings = ServerConnection.makeSettings();
        const url = settings.baseUrl + "optumi/teardown-notebook";
        const init: RequestInit = {
            method: 'POST',
            body: JSON.stringify({
                workload: workload,
                module: module,
            }),
        };
        return ServerConnection.makeRequest(
            url,
            init,
            settings
        ).then((response: Response) => {
            Global.handleResponse(response);
            Global.user.appTracker.removeApp(workload);
            return response.text()
        });
    }

    private handleDeleteClicked = (tries = 0) => {
        const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/delete-machine";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				uuid: this.props.machine.uuid,
			}),
        };
		ServerConnection.makeRequest(
			url,
			init,
			settings
		).then((response: Response) => {
            Global.handleResponse(response);
            this.safeSetState({ waiting: false, deleting: true });
        }).then(() => {
            // Nothing to do on success
        }, () => {
            // We can hit an error here by asking too soon for a machines deletion, so we will wait a little and ask again
            // We will give up after 30 tries (30 seconds)
            if (tries < 30) {
                if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
                if (Global.user) setTimeout(() => this.handleDeleteClicked(tries++), 1000);
            }
        });
    }
    
    private showLoading = (machineState: string): boolean => {
        switch (machineState) {
        case 'Acquiring':
        case 'Releasing':
        case 'Configuring':
            return true
        default:
            return false
        }
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        var machine: Machine = this.props.machine
        var tags: JSX.Element[] = []
        var machineState: string = this.props.machine.getStateMessage();

        var appName = ''
        for (var app of Global.user.appTracker.activeJobsOrSessions) {
            if (app.uuid == machine.app) {
                appName = app.name + " (" + app.annotationOrRunNum + ")"
                break;
            }
        }

        if (machineState != '') {
            tags.push(
                <ExtraInfo reminder={appName}>
                    <Tag key={'machineState'} label={machineState} showLoading={this.showLoading(machineState)} />
                </ExtraInfo>
            );
        }
        if (machine.rate != undefined) {
            tags.push(
                <Tag key={'machineRate'} label={(machine.promo ? 'Promo: ' : '') + FormatUtils.styleRateUnitValue()(machine.rate)} />
            );
        }
        const user: User = Global.user;        
		return (
            <InfoSkirt
                rightButton={
                    <>
                        <WarningPopup
                            open={this.state.showDeleteMachinePopup}
                            headerText="Are you sure?"
                            bodyText={(() => {
                                if (this.state.showDeleteMachinePopup) {
                                    for (var app of user.appTracker.activeJobsOrSessions) {
                                        if (app.uuid == machine.app) {
                                            const appWord = app.interactive ? "session" : "job";
                                            const appAction = app.interactive ? "closed" : "terminated";
                                            // if (app is running) {
                                            if ((app.preparing.completed && !app.preparing.error) && !app.running.completed) {
                                                return "Your " + appWord + " '" +  app.name + "' (" + app.annotationOrRunNum + ") is active on this machine. It will be " + appAction + " if the machine is released."
                                            } else {
                                                return "Your " + appWord + " '" +  app.name + "' (" + app.annotationOrRunNum + ") is waiting for this machine. It will be deleted if the machine is released."
                                            }
                                        }
                                    }
                                    // TODO:JJ We want to patch a timing hole where the job completes while the popup is open. For now, we will show the stale information instead of an empty popup
                                    for (var app of user.appTracker.finishedJobsOrSessions) {
                                        if (app.uuid == machine.app) {
                                            const appWord = app.interactive ? "session" : "job";
                                            const appAction = app.interactive ? "closed" : "terminated";
                                            // if (app is running) {
                                            if ((app.preparing.completed && !app.preparing.error) && !app.running.completed) {
                                                return "Your " + appWord + " '" +  app.name + "' (" + app.annotationOrRunNum + ") is active on this machine. It will be " + appAction + " if the machine is released."
                                            } else {
                                                return "Your " + appWord + " '" +  app.name + "' (" + app.annotationOrRunNum + ") is waiting for this machine. It will be deleted if the machine is released."
                                            }
                                        }
                                    }
                                    setTimeout(() => this.safeSetState({ spinning: true }), 1000);
                                    this.handleDeleteClicked()
                                    this.safeSetState({ showDeleteMachinePopup: false })
                                } else {
                                    return '';
                                }
                            })()}
                            cancel={{
                                text: `Cancel`,
                                onCancel: () => {
                                    this.safeSetState({ showDeleteMachinePopup: false })
                                },
                            }}
                            continue={{
                                text: `Release it`,
                                onContinue: () => {
                                    if (user.appTracker.activeJobsOrSessions.length == 0) {
                                        // Workloads completed while this popup was open
                                        setTimeout(() => this.safeSetState({ spinning: true }), 1000);
                                        this.handleDeleteClicked()
                                    } else {
                                        for (var app of user.appTracker.activeJobsOrSessions) {
                                            if (app.uuid == machine.app) {
                                                // if (app is running) {
                                                if ((app.preparing.completed && !app.preparing.error) && !app.running.completed) {
                                                    // Only delete the machine after the job is stopped to avoid a race condition
                                                    // We set these outside so they will span the job stop/delete as well
                                                    this.safeSetState({ waiting: true, spinning: false });
                                                    setTimeout(() => this.safeSetState({ spinning: true }), 1000);
                                                    this.stopApp(app).then(() => this.handleDeleteClicked());
                                                } else {
                                                    // Only delete the machine after the job is deleted to avoid a race condition
                                                    // We set these outside so they will span the job stop/delete as well
                                                    this.safeSetState({ waiting: true, spinning: false });
                                                    setTimeout(() => this.safeSetState({ spinning: true }), 1000);
                                                    this.deleteApp(app.uuid, app.modules[0].uuid).then(() => this.handleDeleteClicked());
                                                }
                                                break;
                                            }
                                        }
                                    }
                                    this.safeSetState({ showDeleteMachinePopup: false })
                                },
                                color: `error`,
                            }}
                        />
                        <ExtraInfo reminder='Release'>
                            <IconButton
                                size='large'
                                onClick={() => {
                                    if (machine.app) {
                                        this.safeSetState({showDeleteMachinePopup: true})
                                    } else {
                                        this.safeSetState({ waiting: true, spinning: false });
                                        setTimeout(() => this.safeSetState({ spinning: true }), 1000);
                                        this.handleDeleteClicked()
                                    }
                                }}
                                disabled={this.state.deleting || this.state.waiting || this.props.machine.state.includes('sequestration')}
                                sx={{position: 'relative', display: 'inline-block', width: '36px', height: '36px', padding: '3px'}}
                            >
                                <DeleteIcon sx={{position: 'relative', width: '30px', height: '30px', padding: '3px'}} />
                                {(this.state.deleting || this.state.waiting) && this.state.spinning && <CircularProgress size='30px' sx={{position: 'absolute', left: '3px', top: '3px'}} />}
                            </IconButton>
                        </ExtraInfo>
                    </>
                }
                tags={tags}
            >
                {this.props.machine.getIdentityComponent()}
            </InfoSkirt>
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
