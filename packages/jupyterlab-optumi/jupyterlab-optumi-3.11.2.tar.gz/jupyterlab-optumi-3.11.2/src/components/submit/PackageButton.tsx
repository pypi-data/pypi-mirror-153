// /*
// **  Copyright (C) Optumi Inc - All rights reserved.
// **
// **  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
// **  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
// **/

// import * as React from 'react';
// import { DIV, Global } from '../../Global';

// import { SxProps, Theme } from '@mui/system';
// import {
//     Button,
//     Dialog,
//     DialogContent,
//     DialogTitle,
//     IconButton,
//     Paper,
// } from '@mui/material';
// import { withStyles } from '@mui/styles';
// import { Close as CloseIcon } from '@mui/icons-material';

// import { ServerConnection } from '@jupyterlab/services';

// import { Package, PackageState } from '../../models/Package';
// import { StatusWrapper } from '../StatusWrapper';
// import { OptumiConfig } from '../../models/OptumiConfig';
// import { Machine, NoMachine } from '../../models/machine/Machine';
// import { Header } from '../../core';
// import FileServerUtils from '../../utils/FileServerUtils';
// import WarningPopup from '../../core/WarningPopup';

// import { html } from 'diff2html';
// import 'diff2html/bundles/css/diff2html.min.css';
// import { createPatch } from 'diff';

// const StyledDialog = withStyles({
//     paper: {
//         width: '80%',
//         height: '80%',
//         overflowY: 'visible',
//         maxWidth: 'inherit',
//     },
// })(Dialog);

// enum ButtonState {
//     SUBMIT = 0,
//     CANCEL = 1,
//     VIEW = 2,
// }

// interface IProps {
//     sx?: SxProps<Theme>,
// }

// interface IState {
//     buttonState: ButtonState,
//     open: boolean,
//     originalMachines: Machine[],
//     optimizedMachines: Machine[],
//     diffHTML: string,
//     showNoFileUploadsPopup: boolean
// }

// export class PackageButton extends React.Component<IProps, IState> {    
// 	private _isMounted = false;

//     constructor(props: IProps) {
//         super(props)
//         this.state = Object.assign(this.getState(), {
//             open: false,
//             originalMachines: [],
//             optimizedMachines: [],
//             diffHTML: '',
//             showNoFileUploadsPopup: false,
//         });
//     }

//     public handleClick = (bypassWarning = false) => {
//         if (this.state.buttonState == ButtonState.SUBMIT) {
//             const optumi = Global.metadata.getMetadata();
//             if (!bypassWarning && optumi.config.upload.files.length == 0) {
//                 this.safeSetState({ showNoFileUploadsPopup: true })
//             } else {
//                 Global.metadata.submitPackage();
//             }
//         } else if (this.state.buttonState == ButtonState.CANCEL) {
//             Global.metadata.cancelPackage();
//         } else if (this.state.buttonState == ButtonState.VIEW) {
//             this.safeSetState({ open: true })
//         }
//     }

//     public render = (): JSX.Element => {
//         if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
//         // const optumi = Global.metadata.getMetadata();
//         // const pack = Global.user.packageTracker.getPackageByNotebook(optumi.metadata.nbKey);
//         const buttonState = this.state.buttonState;
//         return (
//             <DIV sx={Object.assign({margin: '12px 0px 6px 6px'}, this.props.sx)}>
//                 <StatusWrapper statusColor={'var(--jp-layout-color2)'}>
//                     <Paper
//                         elevation={1}
//                         sx={{
//                             width: '100%',
//                             padding: '3px',
//                             backgroundColor: 'var(--jp-layout-color2)',
//                             borderRadius: '3px',
//                         }}
//                     >
//                         <DIV sx={{width: '100%', display: 'flex'}}>
//                             <WarningPopup
//                                 open={this.state.showNoFileUploadsPopup}
//                                 headerText="Heads up!"
//                                 bodyText={`You didn't add any files. If your notebook reads local data files or Optumi data connectors you can hit "Cancel" and revisit the "Files" section.`}
//                                 cancel={{
//                                     text: `Cancel`,
//                                     onCancel: (prevent: boolean) => {
//                                         this.safeSetState({ showNoFileUploadsPopup: false })
//                                     },
//                                 }}
//                                 continue={{
//                                     text: `Submit anyway`,
//                                     onContinue: (prevent: boolean) => {
//                                         this.safeSetState({ showNoFileUploadsPopup: false })
//                                         this.handleClick(true);
//                                     },
//                                     color: `primary`,
//                                 }}
//                             />
//                             <Button
//                                 variant='contained'
//                                 color={buttonState == ButtonState.SUBMIT ? 'primary' : (buttonState == ButtonState.CANCEL ? 'inherit' : 'success')}
//                                 onClick={() => this.handleClick()}
//                                 sx={{
//                                     minHeight: '0px',
//                                     minWidth: '95px',
//                                     color: 'var(--jp-layout-color2)',
//                                     margin: '9px',
//                                     transition: 'left 500ms ease-in-out 0s, background-color 250ms ease-in-out 0s'
//                                 }}
//                             >
//                                 {this.state.buttonState == ButtonState.SUBMIT ? 
//                                     'submit' 
//                                 : (this.state.buttonState == ButtonState.CANCEL ? 
//                                     'cancel'
//                                 : 
//                                     'view'
//                                 )}
//                             </Button>
//                             <DIV sx={{margin: 'auto 6px', flexGrow: 1}}>
//                                 {this.state.buttonState == ButtonState.SUBMIT ? 
//                                     'Ask optumi to optimize your notebook' 
//                                 : (this.state.buttonState == ButtonState.CANCEL ? 
//                                     'Notebook optimization in progress'
//                                 : 
//                                     'Notebook optimization is ready'
//                                 )}
//                             </DIV>
//                             {buttonState == ButtonState.VIEW && (
//                                 <StyledDialog
//                                     open={this.state.open}
//                                     onClose={() => {
//                                         this.safeSetState({open: false})
//                                     }}
//                                     scroll='paper'
//                                 >
//                                     <DialogTitle sx={{
//                                         display: 'inline-flex',
//                                         height: '60px',
//                                         padding: '6px',
//                                     }}>
//                                         <DIV sx={{
//                                             display: 'inline-flex',
//                                             minWidth: '150px',
//                                             fontSize: '16px',
//                                             fontWeight: 'bold',
//                                             paddingRight: '12px', // this is 6px counteracting the DialogTitle padding and 6px aligning the padding to the right of the tabs
//                                         }}>
//                                             <DIV sx={{margin: '12px'}}>
//                                             Optimizations
//                                             </DIV>
//                                         </DIV>
//                                         <DIV sx={{width: '100%', display: 'inline-flex', overflowX: 'hidden', fontSize: '16px', paddingLeft: '8px'}}>
//                                             <DIV sx={{flexGrow: 1}} />
//                                             <Button
//                                                 disableElevation
//                                                 sx={{
//                                                     height: '36px',
//                                                     margin: '6px',
//                                                 }}
//                                                 onClick={() => {
//                                                     const pack = Global.metadata.getPackage();
//                                                     Global.metadata.openPackage(true, true)

//                                                     // Update the code
//                                                     const current = Global.tracker.currentWidget;
//                                                     current.content.model.fromJSON(pack.optimizedNotebook)

//                                                     // Update the metadata
//                                                     const metadata = Global.metadata.getMetadata();
//                                                     metadata.config = pack.optimizedConfig;
//                                                     Global.metadata.setMetadata(metadata);

//                                                     this.safeSetState({ open: false })
//                                                 }}
//                                                 variant='contained'
//                                                 color='primary'
//                                             >
//                                                 Replace existing notebook
//                                             </Button>
//                                             <Button
//                                                 disableElevation
//                                                 sx={{
//                                                     height: '36px',
//                                                     margin: '6px',
//                                                 }}
//                                                 onClick={async () => {
//                                                     const pack = Global.metadata.getPackage();
//                                                     Global.metadata.openPackage(true, true)

//                                                     // Open the code in a new notebook
//                                                     var path = Global.tracker.currentWidget.context.path;
                                                    
//                                                     var inc = 0;
//                                                     var newPath = path;
//                                                     while ((await FileServerUtils.checkIfPathExists(newPath))[0]) {
//                                                         inc++;
//                                                         newPath = inc == 0 ? path : path.replace('.', '(' + inc + ').');
//                                                     }
                                                    
//                                                     FileServerUtils.saveNotebook(newPath, pack.optimizedNotebook).then((success: boolean) => {
//                                                         const widget = Global.docManager.open(newPath);
//                                                         // Wait until we have anew notebook with new metadata
//                                                         while (!widget.isVisible) {}
//                                                         setTimeout(() => this.setConfigAfterOpen(pack), 250);
//                                                     });

//                                                     this.safeSetState({ open: false })
//                                                 }}
//                                                 variant='contained'
//                                                 color='primary'
//                                             >
//                                                 Open as a new notebook
//                                             </Button>
//                                         </DIV>
//                                         <IconButton
//                                             size='large'
//                                             onClick={() => this.safeSetState({ open: false })}
//                                             sx={{
//                                                 display: 'inline-block',
//                                                 width: '36px',
//                                                 height: '36px',
//                                                 padding: '3px',
//                                                 margin: '6px',
//                                             }}
//                                         >
//                                             <CloseIcon
//                                                 sx={{
//                                                     width: '30px',
//                                                     height: '30px',
//                                                     padding: '3px',
//                                                 }}
//                                             />
//                                         </IconButton>
//                                     </DialogTitle>
//                                     <DialogContent sx={{
//                                         flexGrow: 1, 
//                                         width: '100%',
//                                         height: '100%',
//                                         padding: '0px',
//                                         marginBottom: '0px', // This is because MuiDialogContentText-root is erroneously setting the bottom to 12
//                                         // lineHeight: 'var(--jp-code-line-height)',
//                                         fontSize: 'var(--jp-ui-font-size1)',
//                                         fontFamily: 'var(--jp-ui-font-family)',
//                                     }}>
//                                         <DIV sx={{height: '100%', overflow: 'auto', padding: '20px'}}>
//                                             <DIV sx={{display: 'inline-flex', width: '50%'}}>
//                                                 {/* <DIV sx={{flexGrow: 1}}>
//                                                     <Header title="Original Resource Selection" />
//                                                     {this.state.originalMachines.map(m => m.getPreviewComponent())}
//                                                 </DIV> */}
//                                                 <DIV sx={{flexGrow: 1}}>
//                                                     <Header title="Resource Optimization" />
//                                                     {this.state.optimizedMachines.map(m => m.getPreviewComponent())}
//                                                 </DIV>
//                                             </DIV>
//                                             <Header title="Notebook Optimization" />
//                                             {/* position: relative is needed here otherwise the line numbers for the diff do not scroll with the rest of the page*/}
//                                             <DIV sx={{position: 'relative'}} dangerouslySetInnerHTML={{ __html: this.state.diffHTML }} />
//                                         </DIV>
//                                     </DialogContent>
//                                 </StyledDialog>
//                             )}
//                         </DIV>
//                     </Paper>
//                 </StatusWrapper>
// 			</DIV>
//         );
//     }

//     private setConfigAfterOpen = (pack: Package) => {
//         var metadata = Global.metadata.getMetadata();
//         if (!metadata) {
//             setTimeout(() => this.setConfigAfterOpen(pack), 250);
//             return;
//         }
//         // Update the metadata
//         metadata.config = pack.optimizedConfig;
//         Global.metadata.setMetadata(metadata);
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
//         const pack = Global.metadata.getPackage();
//         if (pack == null) {
//             return { buttonState: ButtonState.SUBMIT };
//         } else if (pack.packageState == PackageState.SHIPPED) {
//             this.previewNotebook(pack.originalConfig).then(machines => this.safeSetState({ originalMachines: [machines[0]] }))
//             this.previewNotebook(pack.optimizedConfig).then(machines => this.safeSetState({ optimizedMachines: [machines[0]] }))
//             return { 
//                 buttonState: ButtonState.VIEW, 
//                 diffHTML: this.getDiff(pack.originalNotebook, pack.optimizedNotebook),
//             };
//         } else {
//             return { buttonState: ButtonState.CANCEL };
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

//     public componentDidMount = () => {
//         this._isMounted = true;
//         Global.metadata.getPackageChanged().connect(this.handleUpdate);
//         Global.tracker.currentChanged.connect(this.handleUpdate);
// 	}

// 	// Will be called automatically when the component is unmounted
// 	public componentWillUnmount = () => {
//         Global.metadata.getPackageChanged().disconnect(this.handleUpdate);
//         Global.tracker.currentChanged.disconnect(this.handleUpdate);
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
