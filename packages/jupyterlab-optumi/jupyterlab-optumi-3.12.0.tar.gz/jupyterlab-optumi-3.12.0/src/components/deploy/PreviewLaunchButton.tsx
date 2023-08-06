/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global } from '../../Global';

import { SxProps, Theme } from '@mui/system';

import { Machine } from '../../models/machine/Machine';
import { App } from '../../models/application/App';
import { LightweightApp } from '../../models/application/LightweightApp';
import { StatusWrapper } from '../StatusWrapper';
import { ComputeConfig } from '../../models/ComputeConfig';
import { StorageConfig } from '../../models/StorageConfig';
import { GraphicsConfig } from '../../models/GraphicsConfig';
import { MemoryConfig } from '../../models/MemoryConfig';

// Properties from parent
interface IProps {
	sx?: SxProps<Theme>
	balance: number
}

// Properties for this component
interface IState {
	machine: Machine[]
}

var retrievingPreview: boolean = false;
var updatePreviewAgain: boolean = false;

export class PreviewLaunchButton extends React.Component<IProps, IState> {
	// We need to know if the component is mounted to change state
	_isMounted = false;
	polling = false;
	timeout: NodeJS.Timeout = null

	constructor(props: IProps) {
		super(props);
		this.state = {
			machine: [Global.lastMachine]
		}
	}

	private poll = () => {
		// We will poll for a new preview every 10 seconds
		if (this.polling) {
			if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
			this.timeout = setTimeout(() => this.poll(), 10000);
		}
		this.handlePreviewClick(false);
	}

	// To understand whats going on, look at the commented out functions below
	private handlePreviewClick = (printRecommendations: boolean, bypassLimiter?: boolean) => {
		// For basic mode, we do not need to retrieve a preview, since we know the exact machine
		if (!Global.expertModeSelected) return;
		const current = Global.tracker.currentWidget;
		if (current != null) {
			const config = Global.metadata.getMetadata().config;
			// await current.context.ready;
			// current.context.save();
            // Make sure the notebook has the correct metadata.
			if (bypassLimiter || !retrievingPreview) {
				try {
					retrievingPreview = true;
					const app = new App(current.context.path, current.model.toJSON(), config);
					app.previewNotebook(printRecommendations).then((machines: Machine[]) => {
						this.safeSetState({
							machine: machines,
						});
						Global.lastMachine = machines[0]
						if (updatePreviewAgain) {
							updatePreviewAgain = false;
							this.handlePreviewClick(false, true);
						} else {
							retrievingPreview = false;
						}
					}, () => {
						retrievingPreview = false;
					});
				} catch (err) {
					console.error(err);
					retrievingPreview = false;
				}
			} else {
				updatePreviewAgain = true;
			}
		}
	}

	// This is the logic of the function above incase we want to understand what it is doing easier
	// This function uses two flags, one flag keeps track of when we are actively getting an update, and one keeps track if we need to get another at the end.
	// We do this to not lose any requests that would be dropped between when we last started an update and the last request to update
	// private newHandlePreviewClick = (printRecommendations: boolean, bypassLimiter?: boolean) => {
	// 	if (bypassLimiter || !retrievingPreview) {
	// 		retrievingPreview = true;
	//		try {
	// 			// do the update
	//			...
	//			// after the update completed
	// 			if (updatePreviewAgain) {
	// 				updatePreviewAgain = false;
	// 				this.newHandlePreviewClick(false, true);
	// 			} else {
	// 				retrievingPreview = false;
	// 			}
	//		} catch (exception) {
	//			retrievingPreview = false;
	//		}
	// 	} else {
	// 		updatePreviewAgain = true;
	// 	}
	// }

	// This is the old handle code that was combined with the function above for the current handlePreviewClick
	// private oldHandlePreviewClick = (printRecommendations: boolean) => {
	// 	const current = Global.tracker.currentWidget;
	// 	if (current != null) {
	// 		const app = new App(current.context.path, current.model.toJSON(), "");
	// 		app.previewNotebook(printRecommendations).then((machine: Machine) => {
	// 			this.safeSetState({
	// 				machine: machine,
	// 			});
	// 		});
	// 	}
	// }

	public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        // var order = 1;
		const metadata = Global.metadata.getMetadata();
		const machine = (Global.expertModeSelected ? this.state.machine[0] : Global.user.machines.getMachine(Global.metadata.getMetadata().config.machineAssortment[0]));
		return (
			<DIV sx={Object.assign({width: '100%'}, this.props.sx)}>
				{React.cloneElement(machine.getPreviewComponent(), {style: {}})}
				<DIV sx={{margin: '6px'}}>
					<StatusWrapper statusColor={'var(--jp-layout-color2)'}>
						{new LightweightApp(metadata.metadata.nbKey, Global.tracker.currentWidget.context.path, metadata.config).getLaunchComponent(machine, this.props.balance)}
					</StatusWrapper>
				</DIV>
				{/* {Global.user.userExpertise < 2 ? (<></>) : (this.state.machine.splice(1).map(x => (<DIV sx={{marginTop: '12px'}}>{x.getLaunchComponent(order++)}</DIV>)))} */} {/* Not sure how this is supposed to translate to the new method of launching */}
			</DIV>
		);
	}

	// We need to force update in case the preview doesn't change but the metadata does
	private handleMetadataChange = () => {
		try {
			const optumi = Global.metadata.getMetadata();
			var changed:boolean = false
			if (Global.expertModeSelected) {
				// In expert mode, we do not want any specified VM sizes
				if (optumi.config.machineAssortment.length > 0) {
					optumi.config.machineAssortment = []
					changed = true
				}
			} else {
				// In basic mode, we do not want any config except vm sizes
				if (JSON.stringify(optumi.config.compute) != JSON.stringify(new ComputeConfig())) {
					optumi.config.compute = new ComputeConfig();
					changed = true;
				}
				if (JSON.stringify(optumi.config.graphics) != JSON.stringify(new GraphicsConfig())) {
					optumi.config.graphics = new GraphicsConfig();
					changed = true;
				}
				if (JSON.stringify(optumi.config.memory) != JSON.stringify(new MemoryConfig())) {
					optumi.config.memory = new MemoryConfig();
					changed = true;
				}
				if (JSON.stringify(optumi.config.storage) != JSON.stringify(new StorageConfig())) {
					optumi.config.storage = new StorageConfig();
					changed = true;
				}
				if (optumi.config.intent != 0.5) {
					optumi.config.intent = 0.5;
					changed = true;
				}
				// We need one VM size for basic mode
				if (optumi.config.machineAssortment.length == 0) {
					optumi.config.machineAssortment = ['Azure:Standard_NC4as_T4_v3']
					changed = true;
				}
			}
			if (changed) {
				Global.metadata.setMetadata(optumi);
			}
		} catch (err) {
			console.error(err);
		}

		this.forceUpdate()
		this.handlePreviewClick(false)
	}

	// Will be called automatically when the component is mounted
	public componentDidMount = () => {
		this._isMounted = true;

		this.handleMetadataChange();

		this.polling = true;
		this.poll();
		Global.metadata.getMetadataChanged().connect(this.handleMetadataChange);
		Global.user.userInformationChanged.connect(() => this.forceUpdate())
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
		this.polling = false;
		if (this.timeout != null) {
			clearTimeout(this.timeout);
			retrievingPreview = false;
		}
		Global.metadata.getMetadataChanged().disconnect(this.handleMetadataChange);
		Global.user.userInformationChanged.disconnect(() => this.forceUpdate())
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

	// public shouldComponentUpdate = (nextProps: IProps, nextState: IState): boolean => {
    //     try {
    //         if (JSON.stringify(this.props) != JSON.stringify(nextProps)) return true;
    //         if (JSON.stringify(this.state) != JSON.stringify(nextState)) return true;
    //         if (Global.shouldLogOnRender) console.log('SuppressedRender (' + new Date().getSeconds() + ')');
    //         return false;
    //     } catch (error) {
    //         return true;
    //     }
    // }
}
