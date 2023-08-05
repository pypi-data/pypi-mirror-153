// /*
// **  Copyright (C) Optumi Inc - All rights reserved.
// **
// **  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
// **  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
// **/

// import * as React from 'react';
// import { DIV, Global, SPAN } from '../../Global';

// import { SxProps, Theme } from '@mui/system';
// import {
//     Button,
//     Dialog,
//     DialogContent,
//     DialogTitle,
//     IconButton,
// } from '@mui/material';
// import { withStyles } from '@mui/styles';
// import { Close as CloseIcon, CheckCircle } from '@mui/icons-material';

// import { ServerConnection } from '@jupyterlab/services';

// import { Package, PackageState } from '../../models/Package';
// import { OptumiConfig } from '../../models/OptumiConfig';
// import { Machine, NoMachine } from '../../models/machine/Machine';
// import { Header } from '../../core';

// import { createPatch } from 'diff';
// import { html } from 'diff2html';
// import 'diff2html/bundles/css/diff2html.min.css';

// const StyledDialog = withStyles({
//     paper: {
//         width: '80%',
//         height: '80%',
//         overflowY: 'visible',
//         maxWidth: 'inherit',
//     },
// })(Dialog);

// interface IProps {
//     sx?: SxProps<Theme>,
// }

// interface IState {
//     open: boolean,

//     packageReady: boolean,

//     originalMachines: Machine[],
//     optimizedMachines: Machine[],
//     diffHTML: string,
//     showNoFileUploadsPopup: boolean,
// }

// export class PackageNotification extends React.Component<IProps, IState> {
//     private _isMounted = false;

//     constructor(props: IProps) {
//         super(props)
//         this.state = Object.assign({
//             open: false,
//             originalMachines: [],
//             optimizedMachines: [],
//             diffHTML: '',
//             showNoFileUploadsPopup: false,
//             packageReady: false,
//         }, this.getState());
//     }

//     public handleSubmitClick = (bypassWarning = false) => {
//         const optumi = Global.metadata.getMetadata();
//         if (!bypassWarning && optumi.config.upload.files.length == 0) {
//             this.safeSetState({ showNoFileUploadsPopup: true })
//         } else {
//             Global.metadata.submitPackage();
//         }
//     }

//     public formatOptimizedRuntime(pack: Package) {
//         if (pack && pack.optimizedConfig) {
//             const packConfig = pack.optimizedConfig.package;
//             var ret = ''
//             if (packConfig.runHours > 0) {
//                 ret += packConfig.runHours + ' hour'
//                 if (packConfig.runHours > 1) ret += 's'
//                 ret += ' '
//             }
//             ret += packConfig.runMinutes + ' minute'
//             if (packConfig.runMinutes > 1) ret += 's'
//             return ret
//         }
//     }

//     public getOptimizedCost(pack: Package) {
//         if (pack && pack.optimizedConfig) {
//             const machine = this.state.optimizedMachines[0]
//             const packConfig = pack.optimizedConfig.package;
//             if (machine) return '$' + ((machine.rate * packConfig.runHours) + ((machine.rate / 60) * packConfig.runMinutes)).toFixed(2)
//         }
//     }

//     public render = (): JSX.Element => {
//         if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
//         const pack = Global.metadata.getPackage(true);
//         return (
//             <DIV sx={Object.assign({ margin: '6px', }, this.props.sx)}>
//                 {this.state.packageReady && (
//                     <>
//                         <Button
//                             fullWidth
//                             variant='contained'
//                             color='success'
//                             sx={{color: 'white', padding: '3px 3px'}}
//                             onClick={()=> {
//                                 this.setState({ open: true })
//                                 Global.snackbarClose.emit(pack.label)
//                             }}
//                         >
//                             <DIV sx={{display: 'inline-flex', width: '100%'}}>
//                                 <CheckCircle sx={{fill: 'white', margin: '6px'}}/>
//                                 <SPAN sx={{flexGrow: 1, margin: 'auto'}}>View new notebook optimization</SPAN>
//                             </DIV>
//                         </Button>
//                         <StyledDialog
//                             open={this.state.open}
//                             onClose={() => {
//                                 this.safeSetState({open: false})
//                             }}
//                             scroll='paper'
//                         >
//                             <DialogTitle sx={{
//                                 display: 'inline-flex',
//                                 height: '60px',
//                                 padding: '6px',
//                             }}>
//                                 <DIV sx={{
//                                     display: 'inline-flex',
//                                     minWidth: '150px',
//                                     fontSize: '16px',
//                                     fontWeight: 'bold',
//                                     paddingRight: '12px', // this is 6px counteracting the DialogTitle padding and 6px aligning the padding to the right of the tabs
//                                 }}>
//                                     <DIV sx={{margin: '12px'}}>
//                                     Optimizations
//                                     </DIV>
//                                 </DIV>
//                                 <DIV sx={{width: '100%', display: 'inline-flex', overflowX: 'hidden', fontSize: '16px', paddingLeft: '8px'}}>
//                                     <DIV sx={{flexGrow: 1}} />
//                                     <Button
//                                         disableElevation
//                                         sx={{
//                                             height: '36px',
//                                             margin: '6px',
//                                         }}
//                                         onClick={() => {
//                                             Global.metadata.openPackage(true, true)

//                                             const current = Global.tracker.currentWidget;

//                                             // Update the code
//                                             const originalNotebook = pack.originalNotebook;
//                                             const currentNotebook = current.content.model.toJSON();
//                                             const optimizedNotebook = pack.optimizedNotebook;
                                            
//                                             const settings = ServerConnection.makeSettings();
//                                             const url = settings.baseUrl + "optumi/merge-notebooks";
//                                             const init: RequestInit = {
//                                                 method: 'POST',
//                                                 body: JSON.stringify({
//                                                     base: originalNotebook,
//                                                     local: currentNotebook,
//                                                     remote: optimizedNotebook,
//                                                 }),
//                                             };
//                                             return ServerConnection.makeRequest(
//                                                 url,
//                                                 init, 
//                                                 settings
//                                             ).then((response: Response) => {
//                                                 Global.handleResponse(response);
//                                                 return response.json();
//                                             }).then((body: any) => {
                                                
//                                                 for (let cell of body.cells) {
//                                                     var src: string[] = []
//                                                     for (let line of cell.source) {
//                                                         src.push(line.replace('<<<<<<< local', '<<<<<<< Your modifications:').replace('=======', '======= Optumi modifications:').replace('>>>>>>> remote', '>>>>>>>'));
//                                                     }
//                                                     cell.source = src;
//                                                 }

//                                                 current.content.model.fromJSON(body)

//                                                 // // Update the metadata
//                                                 const metadata = Global.metadata.getMetadata();
//                                                 metadata.config = pack.optimizedConfig;
//                                                 Global.metadata.setMetadata(metadata);

//                                                 this.safeSetState({ open: false, packageReady: false })
//                                             });
//                                         }}
//                                         variant='contained'
//                                         color='primary'
//                                     >
//                                         Accept
//                                     </Button>
//                                 </DIV>
//                                 <IconButton
//                                     size='large'
//                                     onClick={() => this.safeSetState({ open: false })}
//                                     sx={{
//                                         display: 'inline-block',
//                                         width: '36px',
//                                         height: '36px',
//                                         padding: '3px',
//                                         margin: '6px',
//                                     }}
//                                 >
//                                     <CloseIcon
//                                         sx={{
//                                             width: '30px',
//                                             height: '30px',
//                                             padding: '3px',
//                                         }}
//                                     />
//                                 </IconButton>
//                             </DialogTitle>
//                             <DialogContent sx={{
//                                 flexGrow: 1, 
//                                 width: '100%',
//                                 height: '100%',
//                                 padding: '0px',
//                                 marginBottom: '0px', // This is because MuiDialogContentText-root is erroneously setting the bottom to 12
//                                 // lineHeight: 'var(--jp-code-line-height)',
//                                 fontSize: 'var(--jp-ui-font-size1)',
//                                 fontFamily: 'var(--jp-ui-font-family)',
//                             }}>
//                                 <DIV sx={{height: '100%', overflow: 'auto', padding: '20px'}}>
//                                     <DIV sx={{}}>
//                                         <Header title="Estimates" />
//                                         <DIV sx={{margin: '6px'}}>Runtime: <SPAN sx={{fontWeight: 'bold'}}>{this.formatOptimizedRuntime(pack)}</SPAN></DIV>
//                                         <DIV sx={{margin: '6px'}}>Cost: <SPAN sx={{fontWeight: 'bold'}}>{this.getOptimizedCost(pack)}</SPAN></DIV>
//                                     </DIV>
//                                     <DIV sx={{display: 'inline-flex', width: '50%'}}>
//                                         {/* <DIV sx={{flexGrow: 1}}>
//                                             <Header title="Original Resource Selection" />
//                                             {this.state.originalMachines.map(m => m.getPreviewComponent())}
//                                         </DIV> */}
//                                         <DIV sx={{flexGrow: 1, paddingTop: '6px'}}>
//                                             <Header title="Resource Optimization" />
//                                             {this.state.optimizedMachines.map(m => m.getPreviewComponent())}
//                                         </DIV>
//                                     </DIV>
//                                     <DIV sx={{flexGrow: 1, paddingTop: '6px'}}>
//                                         <Header title="Notebook Optimization" />
//                                         {/* position: relative is needed here otherwise the line numbers for the diff do not scroll with the rest of the page*/}
//                                         <DIV sx={{position: 'relative'}} dangerouslySetInnerHTML={{ __html: this.state.diffHTML }} />
//                                     </DIV>
//                                 </DIV>
//                             </DialogContent>
//                         </StyledDialog>
//                     </>
//                 )}
//             </DIV>
//         );
//     }

//     private getDiff = (originalNotebook: any, optimizedNotebook: any) => {
//         try {
//             // Convert to readable text
//             var originalText = ""
//             for (let cell of originalNotebook.cells) {
//                 if (cell.cell_type == 'code') {
//                     originalText += cell.source
//                 }
//                 originalText += '\n'
//             }

//             var optimizedText = ""
//             for (let cell of optimizedNotebook.cells) {
//                 if (cell.cell_type == 'code') {
//                     optimizedText += cell.source
//                 }
//                 optimizedText += '\n'
//             }

//             if (originalText == optimizedText) return '<DIV style="padding: 6px;">No suggested notebook changes</DIV>'

//             var diff = createPatch("notebook", originalText, optimizedText);
//             return html(diff, { outputFormat: 'side-by-side', drawFileList: false });
//         } catch (err) {
//             console.warn(err)
//         }
//     }

//     private getState = () => {
//         const pack = Global.metadata.getPackage(true);
//         if (pack == null) {
//             return { packageReady: false };
//         } else if (pack.packageState == PackageState.SHIPPED) {
//             this.previewNotebook(pack.originalConfig).then(machines => this.safeSetState({ originalMachines: [machines[0]] }))
//             this.previewNotebook(pack.optimizedConfig).then(machines => this.safeSetState({ optimizedMachines: [machines[0]] }))
//             var ret =  { 
//                 packageReady: true,
//                 diffHTML: this.getDiff(pack.originalNotebook, pack.optimizedNotebook),
//             }
//             if (!Global.lastForceCompleted) {
//                 Object.assign(ret, { open: true });
//                 Global.lastForceCompleted = true;
//             }
//             return ret;
//         } else {
//             return { packageReady: false };
//         }
//     }

//     public async previewNotebook(config: OptumiConfig): Promise<Machine[]> {
// 		const settings = ServerConnection.makeSettings();
// 		const url = settings.baseUrl + "optumi/preview-notebook";
// 		const init: RequestInit = {
// 			method: 'POST',
// 			body: JSON.stringify({
// 				nbConfig: JSON.stringify(config),
//                 includeExisting: false,
// 			}),
// 		};
// 		return ServerConnection.makeRequest(
// 			url,
// 			init, 
// 			settings
// 		).then((response: Response) => {
// 			Global.handleResponse(response);
// 			return response.json();
// 		}).then((body: any) => {
//             if (body.machines.length == 0) return [new NoMachine()]; // we have no recommendations
//             const machines: Machine[] = [];
//             for (let machine of body.machines) {
//                 machines.push(Machine.parse(machine));
//             }
// 			return machines;
// 		});
// 	}

//     public handleUpdate = () => {
//         this.safeSetState(this.getState())
//     };

//     public handleMetadataChange = () => {
//         this.forceUpdate();
//     }

//     public componentDidMount = () => {
//         this._isMounted = true;
//         Global.metadata.getPackageChanged().connect(this.handleUpdate);
//         Global.metadata.getMetadataChanged().connect(this.handleMetadataChange)
//         Global.tracker.currentChanged.connect(this.handleUpdate);
//         Global.forcePackageIntoView.connect(this.handleUpdate);
// 	}

// 	// Will be called automatically when the component is unmounted
// 	public componentWillUnmount = () => {
//         Global.metadata.getPackageChanged().disconnect(this.handleUpdate);
//         Global.metadata.getMetadataChanged().disconnect(this.handleMetadataChange)
//         Global.tracker.currentChanged.disconnect(this.handleUpdate);
//         Global.forcePackageIntoView.disconnect(this.handleUpdate);
//         this._isMounted = false;
// 	}

//     private safeSetState = (map: any) => {
// 		if (this._isMounted) {
// 			let update = false
// 			try {
// 				for (const key of Object.keys(map)) {
// 					if (JSON.stringify(map[key]) !== JSON.stringify((this.state as any)[key])) {
// 						update = true
// 						break
// 					}
// 				}
// 			} catch (error) {
// 				update = true
// 			}
// 			if (update) {
// 				if (Global.shouldLogOnSafeSetState) console.log('SafeSetState (' + new Date().getSeconds() + ')');
// 				this.setState(map)
// 			} else {
// 				if (Global.shouldLogOnSafeSetState) console.log('SuppressedSetState (' + new Date().getSeconds() + ')');
// 			}
// 		}
// 	}

//     public shouldComponentUpdate = (nextProps: IProps, nextState: IState): boolean => {
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
