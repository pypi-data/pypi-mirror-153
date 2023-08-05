// /*
// **  Copyright (C) Optumi Inc - All rights reserved.
// **
// **  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
// **  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
// **/

// import * as React from 'react';
// import { DIV, Global } from '../Global';

// import { SxProps, Theme } from '@mui/system';

// import { NotebookPanel } from '@jupyterlab/notebook';

// import { PackageStepper } from './submit/PackageStepper';

// interface IProps {
// 	sx?: SxProps<Theme>
// 	openDeployPage?: () => any
// }

// interface IState {
// 	isFlipped:boolean
// }

// export class SubmitPage extends React.Component<IProps, IState> {
// 	// We need to know if the component is mounted to change state
// 	_isMounted = false;

// 	constructor(props: IProps) {
// 		super(props)
// 		if (Global.tracker.currentWidget != null) {
// 			Global.tracker.currentWidget.context.ready.then(() => {if (this._isMounted) this.forceUpdate()})
// 		}
// 		this.state = {
// 			isFlipped: Global.expertModeSelected,
// 		}
// 	}

// 	// The contents of the component
// 	public render = (): JSX.Element => {
// 		return (
// 			<DIV sx={Object.assign({overflow: 'auto'}, this.props.sx)}>
// 				{((Global.labShell.currentWidget instanceof NotebookPanel) && (Global.tracker.currentWidget != null) && (Global.tracker.currentWidget.context.isReady)) ? (
// 					<>
// 						{Global.metadata.getMetadata() == undefined ? (
// 							<DIV sx={Object.assign({display: 'flex', flexFlow: 'column', overflow: 'hidden'}, this.props.sx)}>
// 								<DIV sx={{flexGrow: 1, overflowY: 'auto', padding: '6px'}}>
// 									<DIV sx={{ textAlign: 'center', margin: '12px'}}>
// 										Fetching configuration...
// 									</DIV>
// 								</DIV>
// 							</DIV>
// 						) : (
// 							<>
// 								<DIV sx={{padding: '6px 10px'}}>
//                                     <PackageStepper openDeployPage={this.props.openDeployPage}/>
// 									{/* <Stepper>
// 										<WhatsTheProblemStep />
// 										<WheresItRunningStep />
// 										<WhatPackagesStep />
// 										<WhatFilesStep />
// 										<HowToNotifyStep />
// 										<SubmitNotebookStep overrideExpanded={true} />
// 										<WaitForChangesStep />
// 										<AcceptChangesStep openDeployPage={this.props.openDeployPage} />
// 									</Stepper> */}
// 								</DIV>
// 							</>
// 						)}
// 					</>
// 				) : (
// 					<DIV sx={{ textAlign: 'center', padding: "16px" }}>
// 						Open a notebook to get started...
// 					</DIV>
// 				)}
// 			</DIV>
// 		);
// 	}

// 	handleLabShellChange = () => this.forceUpdate()
//     handleTrackerChange = () => this.forceUpdate()
//     handlePackagesChange = () => this.forceUpdate()
// 	handleUserChange = () => {
// 		this.forceUpdate()
// 	}

// 	// Will be called automatically when the component is mounted
// 	public componentDidMount = () => {
// 		this._isMounted = true;
//         Global.labShell.currentChanged.connect(this.handleLabShellChange);
// 		Global.tracker.currentChanged.connect(this.handleTrackerChange);
//         Global.tracker.selectionChanged.connect(this.handleTrackerChange);
//         Global.metadata.getPackageChanged().connect(this.handlePackagesChange);
// 		Global.onUserChange.connect(this.handleUserChange)
// 		this.handleUserChange()
// 	}

// 	// Will be called automatically when the component is unmounted
// 	public componentWillUnmount = () => {
// 		Global.labShell.currentChanged.disconnect(this.handleLabShellChange);
// 		Global.tracker.currentChanged.disconnect(this.handleTrackerChange);
//         Global.tracker.selectionChanged.disconnect(this.handleTrackerChange);
// 		Global.metadata.getPackageChanged().disconnect(this.handlePackagesChange);
// 		Global.onUserChange.disconnect(this.handleUserChange)
// 		this._isMounted = false;
// 	}

// 	// private safeSetState = (map: any) => {
// 	// 	if (this._isMounted) {
// 	// 		let update = false
// 	// 		try {
// 	// 			for (const key of Object.keys(map)) {
// 	// 				if (JSON.stringify(map[key]) !== JSON.stringify((this.state as any)[key])) {
// 	// 					update = true
// 	// 					break
// 	// 				}
// 	// 			}
// 	// 		} catch (error) {
// 	// 			update = true
// 	// 		}
// 	// 		if (update) {
// 	// 			if (Global.shouldLogOnSafeSetState) console.log('SafeSetState (' + new Date().getSeconds() + ')');
// 	// 			this.setState(map)
// 	// 		} else {
// 	// 			if (Global.shouldLogOnSafeSetState) console.log('SuppressedSetState (' + new Date().getSeconds() + ')');
// 	// 		}
// 	// 	}
// 	// }

// 	public shouldComponentUpdate = (nextProps: IProps, nextState: IState): boolean => {
//         try {
//             if (JSON.stringify(this.props) != JSON.stringify(nextProps)) return true;
//             if (JSON.stringify(this.state) != JSON.stringify(nextState)) return true;
//             if (Global.shouldLogOnRender) console.log('SuppressedRender (' + new Date().getSeconds() + ')');
//             return false;
//         } catch (error) {
//             return true;
//         }
//     }
// }
