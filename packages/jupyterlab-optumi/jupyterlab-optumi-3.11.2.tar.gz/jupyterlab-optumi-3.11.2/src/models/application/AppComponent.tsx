/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../../Global';

import { darken, lighten } from '@mui/system';
import { IconButton, CircularProgress } from '@mui/material';
import { Clear, Check, Delete, Stop, WarningRounded } from '@mui/icons-material';

import { ServerConnection } from '@jupyterlab/services';

import { Status } from '../Module';
import { InfoSkirt } from '../../components/InfoSkirt';
import { StatusWrapper } from '../../components/StatusWrapper';
import { Tag } from '../../components/Tag';
import WarningPopup from '../../core/WarningPopup';
import ExtraInfo from '../../utils/ExtraInfo';
import { App } from './App';
import { Colors } from '../../Colors';

interface IProps {
	app: App,
}

interface IState {
	opened: boolean;
	waiting: boolean;
	spinning: boolean;
	showDeleteJobPopup: boolean;
	showStopJobPopup: boolean;
}

export class AppComponent extends React.Component<IProps, IState> {
	_isMounted = false;

    constructor(props: IProps) {
        super(props);
        this.state = {
			opened: false,
			waiting: false,
			spinning: false,
			showDeleteJobPopup: false,
			showStopJobPopup: false,
        };
    }

	private getDeleteJobPreventValue = (): boolean => {
		return Global.user.deleteJobPreventEnabled;
	}

	private saveDeleteJobPreventValue = (prevent: boolean) => {
		Global.user.deleteJobPreventEnabled = prevent;
	}

	private handleDeleteClicked = () => {
		this.safeSetState({ waiting: true, spinning: false });
		setTimeout(() => this.safeSetState({ spinning: true }), 1000);
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/teardown-notebook";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				workload: this.props.app.uuid,
				module: this.props.app.modules[0].uuid,
			}),
		};
		ServerConnection.makeRequest(
			url,
			init,
			settings
		).then((response: Response) => {
			this.safeSetState({ waiting: false });
			Global.handleResponse(response);
			Global.user.appTracker.removeApp(this.props.app.uuid);
		});
    }
	
	private getStopJobPreventValue = (): boolean => {
		return Global.user.stopJobPreventEnabled;
	}

	private saveStopJobPreventValue = (prevent: boolean) => {
		Global.user.stopJobPreventEnabled = prevent;
	}

    private handleStopClicked = () => {
		this.safeSetState({ waiting: true, spinning: false });
		setTimeout(() => this.safeSetState({ spinning: true }), 1000);
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/stop-notebook";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				workload: this.props.app.uuid,
				module: this.props.app.modules[0].uuid,
			}),
		};
		ServerConnection.makeRequest(
			url,
			init,
			settings
		).then((response: Response) => {
			this.safeSetState({ waiting: false })
			Global.handleResponse(response);
		});
	}

	private getStatusColor = (): string => {
		if (this.props.app.error) {
			return Colors.ERROR;
		} else {
			const appStatus = this.props.app.getAppStatus();
			if (appStatus == Status.INITIALIZING) {
				return Colors.PRIMARY;
			} else {
				return Colors.SUCCESS;
			}
		}
	}

	private getChipColor = (): string => {
		const message = this.props.app.getAppMessage()
		if (this.props.app.error) {
			return Colors.ERROR
		} else if (message == 'Completed') {
			return Colors.SUCCESS
		}
		return undefined
	}

	public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
		var tags: JSX.Element[] = []
		var app: App = this.props.app

		// Get the right progress message...
		var appMessage = app.getAppMessage();
		tags.push(
			<ExtraInfo key={'appMessageInfo'} reminder={app.error ? app.getDetailedAppMessage() : ''}>
				<Tag key={'appMessage'}
					id={app.uuid + appMessage}
					icon={
						app.getAppStatus() == Status.COMPLETED ? (
							app.getAppMessage() == 'Closed' || app.getAppMessage() == 'Terminated' ? (
								<Clear sx={{
									height: '14px',
									width: '14px',
									fill: Global.themeManager == undefined || Global.themeManager.isLight(Global.themeManager.theme) ? darken(Colors.CHIP_GREY, 0.35) : lighten(Colors.CHIP_GREY, 0.35),
								}} />
							) : (
							(app.error ? (
								<Clear sx={{
									height: '14px',
									width: '14px',
									fill: Global.themeManager == undefined || Global.themeManager.isLight(Global.themeManager.theme) ? darken(Colors.ERROR, 0.35) : lighten(Colors.ERROR, 0.35),
								}} />
							) : (
								<Check sx={{
									height: '14px',
									width: '14px',
									fill: Global.themeManager == undefined || Global.themeManager.isLight(Global.themeManager.theme) ? darken(Colors.SUCCESS, 0.35) : lighten(Colors.SUCCESS, 0.35),
								}} />
							))
						)) : undefined}
					label={appMessage}
					color={this.getChipColor()}
					showLoading={app.getShowLoading()}
					percentLoaded={undefined}
				/>
			</ExtraInfo>
		)
		if (app.warning) {
			tags.push(
				<ExtraInfo key={'appWarningInfo'} reminder={app.getAppWarningMessage()}>
					<Tag key={'appWarning'}
						icon={
							<WarningRounded sx={{
								height: '14px',
								width: '14px',
								fill: Global.themeManager == undefined || Global.themeManager.isLight(Global.themeManager.theme) ? darken(Colors.WARNING, 0.35) : lighten(Colors.WARNING, 0.35),
							}} />
						}
						label={'Warning'}
						color={Colors.WARNING}
					/>
				</ExtraInfo>
			);
		}

        var appElapsed = app.getTimeElapsed();
		tags.push(
			<Tag
				key={'appElapsed'}
				label={appElapsed}
			/>
		)
		// var appCost = app.getCost();
		// if (appCost) {
		// 	tags.push(
		// 		<ExtraInfo key={'appCost'} reminder='Approximate machine cost'>
		// 			<Tag key={'appCost'} label={appCost} />
		// 		</ExtraInfo>
		// 	)
		// }
        return (
            <StatusWrapper key={app.uuid} statusColor={app.getAppStatus() == Status.COMPLETED ? 'var(--jp-layout-color2)' : this.getStatusColor()} opened={this.state.opened}>
                <InfoSkirt
                    leftButton={
                        <ExtraInfo reminder='See details'>
                            {app.getPopupComponent(() => this.safeSetState({ opened: true }), () => this.safeSetState({ opened: false }))}
                        </ExtraInfo>
                    }
                    rightButton={(app.preparing.completed && !app.preparing.error) && !app.running.completed ? (
                        <>
                            <WarningPopup
                                open={this.state.showStopJobPopup}
                                headerText="Are you sure?"
                                bodyText={(() => {
                                    if (app.interactive) {
                                        return "This session is active. If you close it, the session cannot be resumed."
                                    } else {
                                        return "This job is running. If you terminate it, the job cannot be resumed."
                                    }
                                })()}
                                preventText="Don't ask me again"
                                cancel={{
                                    text: `Cancel`,
                                    onCancel: (prevent: boolean) => {
                                        // this.saveStopJobPreventValue(prevent)
                                        this.safeSetState({ showStopJobPopup: false })
                                    },
                                }}
                                continue={{
                                    text: (() => {
                                        if (app.interactive) {
                                            return "Close it"
                                        } else {
                                            return "Terminate it"
                                        }
                                    })(),
                                    onContinue: (prevent: boolean) => {
                                        this.safeSetState({ showStopJobPopup: false })
                                        this.saveStopJobPreventValue(prevent)
                                        this.handleStopClicked()
                                    },
                                    color: `error`,
                                }}
                            />
                            <IconButton
                                size='large'
                                disabled={this.state.waiting}
                                onClick={() => {
                                    if (this.getStopJobPreventValue()) {
                                        this.handleStopClicked()
                                    } else {
                                        this.safeSetState({ showStopJobPopup: true })
                                    }
                                }}
                                sx={{
                                    position: 'relative',
                                    display: 'inline-block',
                                    width: '36px',
                                    height: '36px',
                                    padding: '3px',
                                }}
                            >
                                <ExtraInfo reminder={app.interactive ? 'Stop' : 'Terminate'}>
                                    <Stop sx={{
                                        position: 'relative',
                                        width: '30px',
                                        height: '30px',
                                        padding: '3px',
                                    }} />
                                </ExtraInfo>
                                {this.state.waiting && this.state.spinning && <CircularProgress size='30px' sx={{position: 'absolute', left: '3px', top: '3px'}} />}
                            </IconButton>
                        </>
                    ) : (
                        <>
                            <WarningPopup
                                open={this.state.showDeleteJobPopup}
                                headerText="Are you sure?"
                                bodyText={(() => {
                                    if (app.interactive) {
                                        return "You will lose all session information and output files that have not been downloaded. This cannot be undone."
                                    } else {
                                        return "You will lose all job information and output files that have not been downloaded. This cannot be undone."
                                    }
                                })()}
                                preventText="Don't ask me again"
                                cancel={{
                                    text: `Cancel`,
                                    onCancel: (prevent: boolean) => {
                                        // this.saveDeleteJobPreventValue(prevent)
                                        this.safeSetState({ showDeleteJobPopup: false })
                                    },
                                }}
                                continue={{
                                    text: `Delete it`,
                                    onContinue: (prevent: boolean) => {
                                        this.safeSetState({ showDeleteJobPopup: false })
                                        this.saveDeleteJobPreventValue(prevent)
                                        this.handleDeleteClicked()
                                    },
                                    color: `error`,
                                }}
                            />
                            <ExtraInfo reminder='Delete'>
                                <IconButton
                                    size='large'
                                    disabled={this.state.waiting || !app.initializing.completed}
                                    onClick={() => {
                                        if (this.getDeleteJobPreventValue() || !app.running.started) {
                                            this.handleDeleteClicked()
                                        } else {
                                            this.safeSetState({ showDeleteJobPopup: true })
                                        }
                                    }}
                                    sx={{position: 'relative', display: 'inline-block', width: '36px', height: '36px', padding: '3px'}}
                                >
                                    <Delete sx={{position: 'relative', width: '30px', height: '30px', padding: '3px'}} />
                                    {this.state.waiting && this.state.spinning && <CircularProgress size='30px' sx={{position: 'absolute', left: '3px', top: '3px'}} />}
                                </IconButton>
                            </ExtraInfo>
                        </>
                    )}
                    tags={tags}
                >
                    {app.getIdentityComponent()}
                </InfoSkirt>
            </StatusWrapper>
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

	private handleThemeChange = () => {
        this.forceUpdate()
    }

	private handleAppChange = () => {
		this.forceUpdate()
	}

	private handleRefreshWhileRunning = () => {
		if (this.props.app.getAppStatus() !== Status.COMPLETED) {
			this.forceUpdate()
		}
	}

	private forceUpdateIntervalId: NodeJS.Timeout

	// Will be called automatically when the component is mounted
	public componentDidMount = () => {
        this._isMounted = true;
		Global.themeManager.themeChanged.connect(this.handleThemeChange)
		this.props.app.changed.connect(this.handleAppChange)
		this.forceUpdateIntervalId = setInterval(() => this.handleRefreshWhileRunning(), 500)
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
		this._isMounted = false;
		Global.themeManager.themeChanged.disconnect(this.handleThemeChange)
		this.props.app.changed.disconnect(this.handleAppChange)
		clearInterval(this.forceUpdateIntervalId)
	}
}
