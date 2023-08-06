/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../../Global';

import { Button, CircularProgress, SvgIcon } from '@mui/material';

import WarningPopup from '../../core/WarningPopup';
import ExtraInfo from '../../utils/ExtraInfo';
import { App } from './App';
import { OptumiConfig } from '../OptumiConfig';
import { LaunchSkirt } from '../../components/LaunchSkirt';
import { LightweightApp } from './LightweightApp';
import { Tag } from '../../components/Tag';
import { OptumiMetadataTracker } from '../OptumiMetadataTracker';
import { CustomerState } from '../../core/CustomerState';
import { Machine, NoMachine } from '../machine/Machine';

interface IProps {
    lightweightApp: LightweightApp
    machine: Machine
    balance: number    
}

interface IState {
    numApps: number;
    displayNumApps: number;
    showNoRequirementsPopup: boolean;
    showNoFileUploadsPopup: boolean;
    showStartSessionPopup: boolean;
    waiting: boolean;
    spinning: boolean;
}

export class AppLaunchComponent extends React.Component<IProps, IState> {
    _isMounted = false

    constructor(props: IProps) {
        super(props);
        this.state = {
            numApps: Global.user.appTracker.getNum(),
            displayNumApps: Global.user.appTracker.getDisplayNum(),
            waiting: false,
            spinning: false,
            showNoRequirementsPopup: false,
            showNoFileUploadsPopup: false,
            showStartSessionPopup: false,
        };
    }

    private handleLaunchClick = async () => {
		const current = Global.tracker.currentWidget;
		if (current != null) {
            this.safeSetState({ waiting: true, spinning: false });
            setTimeout(() => this.safeSetState({ spinning: true }), 1000);
            const notebook: any = current.model.toJSON();
            // Clear any cell outputs and execution counts
            const optumi = Global.metadata.getMetadata();
            const config: OptumiConfig = optumi.config;
            if (!config.interactive) {
                for (var cell of notebook.cells) {
                    if (cell.cell_type === 'code') {
                        cell.outputs = [];
                        cell.execution_count = null;
                    }
                }
            }
            // Remove papermill timing cells if they exist
            if (notebook.metadata.papermill) delete notebook.metadata.papermill;
            for (var cell of notebook.cells) {
                if (cell.metadata.papermill) delete cell.metadata.papermill;
            }
            // If the requirements are empty, we will auto add packages
            if (!config.upload.requirements) {
                const newRequirements = OptumiMetadataTracker.autoAddPackages(config.upload.requirements, current.content.model);
                if (newRequirements) {
                    config.upload.requirements = newRequirements;
                    Global.metadata.setMetadata(optumi)
                }
            }
            // Save the notebook before transferring
            await current.context.save();
            const app = new App(current.context.path, notebook, config);
            app.setupNotebook(Global.user.appTracker).then(
                // on success or error, we stop waiting
                () => this.safeSetState({ waiting: false }),
                () => this.safeSetState({ waiting: false })
            );
		}
	}

    // This allows us to queue multiple warning messages
    private actions: (() => any)[] = []

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        var tags: JSX.Element[] = [];
        var left: string = null
        var disabled = false
        const user = Global.user;

        if (user.customerState == CustomerState.FREE_TRIAL_ENDED) {
            left = 'Free trial ended'
            disabled = true
        } else if (user.customerState == CustomerState.FREE_TRIAL && this.props.balance > 0) {
            left = 'No remaining credit'
            disabled = true
        } else if (user.customerState == CustomerState.FREE_TRIAL && user.egressTotal > user.egressLimit) {
            left = 'Egress limit exceeded'
            disabled = true
        } else if (user.customerState == CustomerState.SUBSCRIPTION_CANCELED) {
            left = 'Subscription canceled'
            disabled = true
        } else if (user.isSubscribed() && !user.autoAddOnsEnabled && user.egressTotal > user.egressLimit) {
            left = 'Egress limit exceeded'
            disabled = true
        } else if (this.state.numApps >= Global.user.runHistoryLength) {
            left = 'Workload history exceeded'
            disabled = true
        } else if (this.props.machine instanceof NoMachine) {
            left = 'No matching machines'
            disabled = true
        } else if (this.state.displayNumApps < Global.user.maxJobs) {
            left = 'Concurrent launches: ' + this.state.displayNumApps.toString() + ' of ' + Global.user.maxJobs.toString()
        } else if (this.state.displayNumApps == 0) {
            left = 'Concurrent launches: Max ' + Global.user.maxJobs.toString()
        } else {
            left = 'Concurrent launches exceeded'
            disabled = true
        }
        tags.push(<Tag key={'left'} label={left} />);
        return (
            <LaunchSkirt
                launchButton={
                    <>
                        <WarningPopup
                            open={this.state.showNoRequirementsPopup}
                            headerText="Heads up!"
                            bodyText={(() => {
                                const optumi = Global.metadata.getMetadata().config;
                                const newRequirements = OptumiMetadataTracker.autoAddPackages(optumi.upload.requirements, Global.tracker.currentWidget.content.model).split('\n').map(s => '    • ' + s).join('\n');
                                return `You didn't add any Python packages but it looks like your notebook is using the following:\n\n` + newRequirements + `\n\nWe'll add these packages for you, but if we missed any you can hit "Cancel" and revisit the "Packages" section.`;
                            })()}
                            preventText="Don't warn me again"
                            cancel={{
                                text: `Cancel`,
                                onCancel: (prevent: boolean) => {
                                    this.safeSetState({ showNoRequirementsPopup: false })
                                    this.actions = []
                                },
                            }}
                            continue={{
                                text: `Add and launch it`,
                                onContinue: (prevent: boolean) => {
                                    this.safeSetState({ showNoRequirementsPopup: false })
                                    Global.user.noRequirementsPreventEnabled = prevent
                                    this.actions.shift()();
                                },
                                color: `primary`,
                            }}
                        />
                        <WarningPopup
                            open={this.state.showNoFileUploadsPopup}
                            headerText="Heads up!"
                            bodyText={`You didn't add any files. If your notebook reads local data files or Optumi data connectors you can hit "Cancel" and revisit the "Files" section.`}
                            preventText="Don't warn me again"
                            cancel={{
                                text: `Cancel`,
                                onCancel: (prevent: boolean) => {
                                    this.safeSetState({ showNoFileUploadsPopup: false })
                                    this.actions = []
                                },
                            }}
                            continue={{
                                text: `Launch it`,
                                onContinue: (prevent: boolean) => {
                                    this.safeSetState({ showNoFileUploadsPopup: false })
                                    Global.user.noFileUploadsPreventEnabled = prevent
                                    this.actions.shift()();
                                },
                                color: `primary`,
                            }}
                        />
                        <WarningPopup
                            open={this.state.showStartSessionPopup}
                            headerText="Heads up!"
                            bodyText={`You are about to launch a session that will remain active until you manually close it. In case you forget, the session will automatically close after 4 hours of idle time (no cells running).`}
                            preventText="Don't warn me again"
                            cancel={{
                                text: `Cancel`,
                                onCancel: (prevent: boolean) => {
                                    this.safeSetState({ showStartSessionPopup: false })
                                    this.actions = []
                                },
                            }}
                            continue={{
                                text: `Launch it`,
                                onContinue: (prevent: boolean) => {
                                    this.safeSetState({ showStartSessionPopup: false })
                                    Global.user.startSessionPreventEnabled = prevent
                                    this.actions.shift()();
                                },
                                color: `primary`,
                            }}
                        />
                        <ExtraInfo reminder='Launch'>
                            <Button
                                variant='contained'
                                color='primary'
                                disabled={disabled || this.state.waiting}
                                onClick={() => {
                                    const optumi = Global.metadata.getMetadata().config;
                                    // Check upfront if the user needs any packages specified
                                    const newRequirements = OptumiMetadataTracker.autoAddPackages(optumi.upload.requirements, Global.tracker.currentWidget.content.model);
                                    const requirementsEmpty = (optumi.upload.requirements == null || optumi.upload.requirements == "") && (optumi.upload.requirements != newRequirements);
                                    const fileUploadsEmpty = optumi.upload.files.length == 0 && optumi.dataConnectors.length == 0;
                                    const user = Global.user;

                                    var showStartSessionPopup = false;
                                    var showNoFileUploadsPopup = false;
                                    var showNoRequirementsPopup = false;

                                    if (optumi.interactive) {
                                        if (!user.startSessionPreventEnabled) {
                                            showStartSessionPopup = true;
                                        }
                                    }
                                    if (requirementsEmpty) {
                                        if (!user.noRequirementsPreventEnabled) {
                                            showNoRequirementsPopup = true;
                                        }
                                    }
                                    if (fileUploadsEmpty) {
                                        if (!user.noFileUploadsPreventEnabled) {
                                            showNoFileUploadsPopup = true;
                                        }
                                    }
                                    if (showStartSessionPopup || showNoFileUploadsPopup || showNoRequirementsPopup) {
                                        if (showStartSessionPopup) this.actions.push(() => this.safeSetState({ showStartSessionPopup: true }))
                                        if (showNoFileUploadsPopup) this.actions.push(() => this.safeSetState({ showNoFileUploadsPopup: true }))
                                        if (showNoRequirementsPopup) this.actions.push(() => this.safeSetState({ showNoRequirementsPopup: true }))
                                    }
                                    this.actions.push(this.handleLaunchClick);
                                    // Run the first action
                                    this.actions.shift()();
                                }}
                                sx={{
                                    position: 'relative',
                                    minWidth: '0px',
                                    minHeight: '0px',
                                    width: '52px',
                                    height: '52px',
                                    borderRadius: '26px',
                                    color: 'var(--jp-layout-color2)',
                                }}
                            >
                                <SvgIcon viewBox="0, 0, 400,446" sx={{position: 'relative', width: '36px', height: '36px'}}>
                                    <path d="M348.000 58.232 C 324.618 61.984,306.000 66.674,306.000 68.813 C 306.000 71.851,369.545 135.122,371.067 133.599 C 372.905 131.761,382.000 74.336,382.000 64.567 L 382.000 56.000 370.500 56.234 C 364.175 56.362,354.050 57.262,348.000 58.232 M261.029 86.235 C 214.374 111.539,184.827 137.455,151.438 182.354 C 131.859 208.683,134.247 207.280,105.973 209.077 C 77.646 210.877,78.107 210.586,46.111 246.944 C 14.709 282.628,13.657 285.006,24.595 295.608 C 33.914 304.640,38.535 303.841,62.774 289.000 C 74.453 281.850,85.356 276.000,87.004 276.000 C 90.397 276.000,91.021 279.133,88.000 281.000 C 80.966 285.347,86.211 293.260,115.524 322.525 C 145.290 352.241,154.153 357.842,159.000 350.000 C 161.093 346.613,163.948 347.791,162.638 351.500 C 161.957 353.425,155.685 364.580,148.700 376.288 C 133.629 401.551,133.207 405.011,144.006 414.767 C 155.049 424.744,153.659 425.401,190.701 392.696 C 227.821 359.922,227.156 360.976,229.004 332.000 C 230.748 304.673,229.916 306.203,252.454 288.864 C 308.578 245.687,341.585 206.858,361.005 161.165 C 368.325 143.941,367.373 141.488,347.134 125.396 C 330.680 112.314,319.724 100.874,305.577 82.000 C 295.803 68.959,292.260 69.296,261.029 86.235 M281.518 145.989 C 295.397 154.451,299.651 169.944,291.460 182.204 C 279.075 200.744,254.612 198.973,245.060 178.845 C 234.650 156.906,260.788 133.350,281.518 145.989 M65.116 318.984 C 41.834 327.278,33.655 343.820,22.828 404.507 C 19.046 425.702,19.740 429.180,26.337 422.099 C 32.573 415.406,48.022 408.969,72.496 402.867 C 109.336 393.683,120.097 382.787,119.904 354.869 L 119.808 341.000 116.404 347.823 C 111.679 357.294,105.398 361.342,88.000 366.125 C 79.750 368.394,70.975 371.564,68.500 373.171 C 63.012 376.734,63.005 376.424,68.070 354.701 C 73.737 330.396,81.234 320.000,93.094 320.000 C 94.692 320.000,96.000 319.100,96.000 318.000 C 96.000 315.041,74.239 315.734,65.116 318.984 " />
                                </SvgIcon>
                                {this.state.waiting && this.state.spinning && <CircularProgress size='54px' sx={{position: 'absolute'}}/>}
                            </Button>
                        </ExtraInfo>
                    </>
                }
                tags={tags}
            >
                {this.props.lightweightApp.getIdentityComponent()}
            </LaunchSkirt>
        )
    }

    handleAppsChanged = () => {
        this.setState({numApps: Global.user.appTracker.getNum(), displayNumApps: Global.user.appTracker.getDisplayNum()})
    }

	public componentDidMount = () => {
		this._isMounted = true;
        Global.user.appTracker.appsChanged.connect(this.handleAppsChanged);
	}

	public componentWillUnmount = () => {
        Global.user.appTracker.appsChanged.disconnect(this.handleAppsChanged);
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
