/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global, SPAN } from '../Global';

import { SxProps, Theme } from '@mui/system';
import { IconButton } from '@mui/material';
import { Flip as FlipIcon /*, FlipCameraAndroid as FlipCameraAndroidIcon*/ } from '@mui/icons-material';

import { NotebookPanel } from '@jupyterlab/notebook';

import { PreviewLaunchButton } from './deploy/PreviewLaunchButton';
import { OptumiMetadataTracker } from '../models/OptumiMetadataTracker';
import { IntentSlider, SubHeader } from '../core';
import { FilesPanel } from './deploy/FilesPanel';
import { ResourcesPanel } from './deploy/resources/ResourcesPanel';
import { LaunchMode } from './deploy/resources/LaunchMode';
// import { PackageNotification } from './submit/PackageNotification';

import ReactCardFlip from 'react-card-flip';
import { Colors } from '../Colors';

interface IProps {
	sx?: SxProps<Theme>
	balance: number
}

interface IState {
	isFlipped:boolean
}

export class DeployPage extends React.Component<IProps, IState> {
	// We need to know if the component is mounted to change state
	_isMounted = false;

	constructor(props: IProps) {
		super(props)
		if (Global.tracker.currentWidget != null) {
			Global.tracker.currentWidget.context.ready.then(() => {if (this._isMounted) this.forceUpdate()})
		}
		this.state = {
			isFlipped: Global.expertModeSelected,
		}
	}

	private getValue(): number {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
		return optumi.config.intent;
	}

	private async saveValue(intent: number) {
        const tracker: OptumiMetadataTracker = Global.metadata;
		const optumi = tracker.getMetadata();
		optumi.config.intent = intent;
		tracker.setMetadata(optumi);
	}

	// The contents of the component
	public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
		const flipCardHeader = (
			<DIV sx={{display: 'inline-flex', width: '100%'}}>
				<SubHeader title='Resource selection'/>
				<SPAN sx={{
					margin: 'auto 8px',
					flexGrow: 1,
					textAlign: 'end',
					opacity: 0.5,
					transitionDuration: '217ms',
					whiteSpace: 'nowrap',
					fontSize: '12px',
					fontStyle: 'italic',
				}}>
					{this.state.isFlipped ? 'expert' : 'basic'}
				</SPAN>
				<IconButton
                    size='large'
                    onClick={() => {
						// // We want to set the metadata back to the last history suggestion
						// // TODO:JJ This doesn't always work for some reason
						// setTimeout(() => {
						// 	const pack = Global.metadata.getLastPackage();
						// 	if (pack) {
						// 		const optumi = Global.metadata.getMetadata();
						// 		optumi.config = pack.optimizedConfig;
						// 		Global.metadata.setMetadata(optumi);
						// 	}
						// }, 250);
						Global.expertModeSelected = !this.state.isFlipped;
						this.safeSetState({ isFlipped: !this.state.isFlipped })
					}}
                    sx={{padding: '0px', marginRight: '-3px', width: '30px', height: '30px'}}
                >
					<FlipIcon sx={{height: '20px'}}/>
				</IconButton>
			</DIV>
		);
		return (
			<DIV sx={Object.assign({overflow: 'auto'}, this.props.sx)}>
				{((Global.labShell.currentWidget instanceof NotebookPanel) && (Global.tracker.currentWidget != null) && (Global.tracker.currentWidget.context.isReady)) ? (
					<>
						{Global.metadata == undefined || Global.metadata.getMetadata() == undefined ? (
							<DIV sx={Object.assign({display: 'flex', flexFlow: 'column', overflow: 'hidden'}, this.props.sx)}>
								<DIV sx={{flexGrow: 1, overflowY: 'auto', padding: '6px'}}>
									<DIV sx={{ textAlign: 'center', margin: '12px'}}>
										Fetching configuration...
									</DIV>
								</DIV>
							</DIV>
						) : (
							<>
								<DIV sx={{padding: '6px 10px'}}>
									<FilesPanel />
									<LaunchMode />

									<ReactCardFlip
										cardStyles={{front: {transformStyle: 'flat'}, back: {transformStyle: 'flat'}}}
										isFlipped={this.state.isFlipped}
										flipSpeedBackToFront={0.3}
										flipSpeedFrontToBack={0.3}
									>
										<DIV>
											{flipCardHeader}
											{!this.state.isFlipped && (
												<>
													<PreviewLaunchButton key={'preview-launch'} balance={this.props.balance}/>
													{/* <PackageNotification /> */}
												</>
											)}
										</DIV>

										<DIV>
											{flipCardHeader}
											<ResourcesPanel />
											<IntentSlider
												color={Colors.PRIMARY}
												getValue={this.getValue}
												saveValue={this.saveValue}
											/>
											{this.state.isFlipped && (
												<>
													<PreviewLaunchButton key={'preview-launch'} balance={this.props.balance}/>
													{/* <PackageNotification /> */}
												</>
											)}
										</DIV>
									</ReactCardFlip>

								</DIV>
							</>
						)}
					</>
				) : (
					<DIV sx={{ textAlign: 'center', padding: "16px" }}>
						Open a notebook to get started...
					</DIV>
				)}
			</DIV>
		);
	}

	handleLabShellChange = () => this.forceUpdate()
    handleTrackerChange = () => this.forceUpdate()
    handleMetadataChange = () => this.forceUpdate()
	handlePackageChange = () => this.forceUpdate()
	handleUserChange = () => {
		this.forceUpdate()
	}

	// Will be called automatically when the component is mounted
	public componentDidMount = () => {
		this._isMounted = true;
		Global.setLink(Global.Target.DeployTab.BasicMode, () => {
			this.safeSetState({isFlipped: false})
			Global.expertModeSelected = false
		})
		Global.setLink(Global.Target.DeployTab.ExpertMode, () => {
			this.safeSetState({isFlipped: true})
			Global.expertModeSelected = true
		})
        Global.labShell.currentChanged.connect(this.handleLabShellChange);
		Global.tracker.currentChanged.connect(this.handleTrackerChange);
        Global.tracker.selectionChanged.connect(this.handleTrackerChange);
        Global.metadata.getMetadataChanged().connect(this.handleMetadataChange);
        // Global.metadata.getPackageChanged().connect(this.handlePackageChange);
		Global.onUserChange.connect(this.handleUserChange)
		this.handleUserChange()
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
		Global.labShell.currentChanged.disconnect(this.handleLabShellChange);
		Global.tracker.currentChanged.disconnect(this.handleTrackerChange);
        Global.tracker.selectionChanged.disconnect(this.handleTrackerChange);
        Global.metadata.getMetadataChanged().disconnect(this.handleMetadataChange);
		// Global.metadata.getPackageChanged().disconnect(this.handlePackageChange);
		Global.onUserChange.disconnect(this.handleUserChange)
		Global.deleteLink(Global.Target.DeployTab.BasicMode)
		Global.deleteLink(Global.Target.DeployTab.ExpertMode)
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
