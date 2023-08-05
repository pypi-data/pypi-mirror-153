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
//     InputAdornment,
//     OutlinedInput,
//     Radio,
//     Step,
//     StepContent,
//     StepLabel,
//     Stepper,
// } from '@mui/material';
// import { withStyles } from '@mui/styles';
// import { Close as CloseIcon } from '@mui/icons-material';

// import { ServerConnection } from '@jupyterlab/services';

// import { Package, PackageState } from '../../models/Package';
// import { OptumiConfig } from '../../models/OptumiConfig';
// import { Machine, NoMachine } from '../../models/machine/Machine';
// import { Dropdown, Header } from '../../core';
// import FileServerUtils from '../../utils/FileServerUtils';
// import WarningPopup from '../../core/WarningPopup';
// // import { PhoneTextBox } from '../../core/PhoneTextBox';
// import { Packages } from '../deploy/Packages';
// import { Files } from '../deploy/Files';
// import { OptumiMetadataTracker } from '../../models/OptumiMetadataTracker';
// import { KaggleAccelerator, Platform } from '../../models/PackageConfig';

// import { createPatch } from 'diff';
// import { html } from 'diff2html';
// import 'diff2html/bundles/css/diff2html.min.css';
// import { PhoneNumberFormat, PhoneNumberUtil } from 'google-libphonenumber';

// function capitalizeFirstLetter(value: string) {
//     if (value === null || value.length == 0) return value
//     return value.charAt(0).toUpperCase() + value.slice(1);
// }

// const StyledDialog = withStyles({
//     paper: {
//         width: '80%',
//         height: '80%',
//         overflowY: 'visible',
//         maxWidth: 'inherit',
//     },
// })(Dialog);

// const StyledOutlinedInput = withStyles({
//     root: {
//         padding: '0px',
//         margin: '0px 3px',
//         height: '21px',
//     },
//     input: {
//         fontSize: '12px',
//         padding: '3px 6px 3px 6px',
//     },
//     adornedEnd: {
//         paddingRight: '0px',
//     },
// }) (OutlinedInput)

// enum SubmitStep {
//     DOES_YOUR_NOTEBOOK_RUN = 0,
//     WHERE_ARE_YOU_RUNNING = 1,
//     PACKAGES = 2,
//     FILES = 3,
//     HOW_DO_YOU_WANT_TO_BE_NOTIFIED = 4,
//     SUBMIT = 5,
//     WAIT = 6,
//     OPEN = 7,
// }

// interface IProps {
//     sx?: SxProps<Theme>,

//     openDeployPage: () => any
// }

// interface IState {
//     open: boolean,
//     originalMachines: Machine[],
//     optimizedMachines: Machine[],
//     diffHTML: string,
//     showNoFileUploadsPopup: boolean,

//     steps: string[],
//     activeStep: number,

//     buttonKey: number,
// }

// export class PackageStepper extends React.Component<IProps, IState> {
//     private _isMounted = false;

//     constructor(props: IProps) {
//         super(props)
//         this.state = Object.assign({
//             open: false,
//             originalMachines: [],
//             optimizedMachines: [],
//             diffHTML: '',
//             showNoFileUploadsPopup: false,

//             steps: this.getSteps(),
//             activeStep: this.getInitialStep(),

//             buttonKey: 0,
//         }, this.getState());
//     }

//     private getInitialStep() : number {
//         const optumi = Global.metadata.getMetadata().config;

//         if (optumi.package.notebookRuns === null || (optumi.package.notebookRuns && optumi.package.runHours === 0 && optumi.package.runMinutes === 0)) return SubmitStep.DOES_YOUR_NOTEBOOK_RUN;
//         if (optumi.package.runPlatform === null || optumi.package.runPlatform == '' || (optumi.package.runPlatform === Platform.KAGGLE && optumi.package.kaggleAccelerator === null)) return SubmitStep.WHERE_ARE_YOU_RUNNING;
//         if (optumi.notifications.packageReadySMSEnabled && Global.user.phoneNumber === '') return SubmitStep.HOW_DO_YOU_WANT_TO_BE_NOTIFIED;
//         return SubmitStep.SUBMIT;
//     }

//     private getSteps() {
//         return [
//             "What's the problem with your notebook?"", 
//             'Where are you currently running it?',
//             'What packages does your notebook use?',
//             'What files does your notebook need?',
//             "How would you like to be notified when it's done?"", 
//             'Submit your notebook',
//             'Wait for your optimized notebook',
//             'Review and accept the changes',
//         ];
//     }

//     private saveNotebookRunsValue(value: boolean) {
//         const tracker: OptumiMetadataTracker = Global.metadata;
//         const optumi = tracker.getMetadata();
//         optumi.config.package.notebookRuns = value
//         tracker.setMetadata(optumi);
//     }

//     private saveRunHoursValue(value: number) {
//         const tracker: OptumiMetadataTracker = Global.metadata;
//         const optumi = tracker.getMetadata();
//         optumi.config.package.runHours = value;
//         tracker.setMetadata(optumi);
//     }

//     private saveRunMinutesValue(value: number) {
//         const tracker: OptumiMetadataTracker = Global.metadata;
//         const optumi = tracker.getMetadata();
//         optumi.config.package.runMinutes = value;
//         tracker.setMetadata(optumi);
//     }

//     private saveRunPlatformValue(value: string) {
//         const tracker: OptumiMetadataTracker = Global.metadata;
//         const optumi = tracker.getMetadata();
//         optumi.config.package.runPlatform = value;
//         tracker.setMetadata(optumi);
//     }

//     private saveKaggleAcceleratorValue(value: string) {
//         const tracker: OptumiMetadataTracker = Global.metadata;
//         const optumi = tracker.getMetadata();
//         optumi.config.package.kaggleAccelerator = value as KaggleAccelerator;
//         tracker.setMetadata(optumi);
//     }

//     private savePackageReadySMSEnabledValue(value: boolean) {
//         const tracker: OptumiMetadataTracker = Global.metadata;
//         const optumi = tracker.getMetadata();
//         optumi.config.notifications.packageReadySMSEnabled = value;
//         tracker.setMetadata(optumi);
//     }

//     private getStepContent(step: number) {
//         const optumi = Global.metadata.getMetadata().config;

//         switch (step) {
//             case SubmitStep.DOES_YOUR_NOTEBOOK_RUN:
//                 return <>
//                     <DIV sx={{width: '100%', display: 'inline-flex'}}>
//                         <Radio sx={{padding: '3px'}} color='primary' checked={optumi.package.notebookRuns === false} onChange={() => this.saveNotebookRunsValue(false)}/>
//                         <DIV sx={{margin: 'auto 0px'}}>
//                             It does not run at all
//                         </DIV>
//                     </DIV>
//                     <DIV sx={{width: '100%', display: 'inline-flex'}}>
//                         <Radio sx={{padding: '3px'}} color='primary' checked={optumi.package.notebookRuns === true} onChange={() => this.saveNotebookRunsValue(true)}/>
//                         <DIV sx={{margin: 'auto 0px'}}>
//                             It runs too slow
//                         </DIV>
//                     </DIV>
//                     {optumi.package.notebookRuns && (
//                         <DIV sx={{display: 'inline-flex'}}>
//                             <StyledOutlinedInput
//                                 sx={{width: '75px'}}
//                                 value={optumi.package.runHours}
//                                 onChange={(event: React.ChangeEvent<HTMLInputElement>) => this.saveRunHoursValue( +(event.target.value.replace(/\D/g,'')))}
//                                 endAdornment={
//                                     <InputAdornment position="end" sx={{height: '20px', margin: '0px 3px 0px 0px'}}>
//                                         <SPAN sx={{fontSize: '12px'}}>
//                                             hours
//                                         </SPAN>
//                                     </InputAdornment>
//                                 }                                
//                             />
//                             <StyledOutlinedInput
//                                 sx={{width: '75px'}}
//                                 value={optumi.package.runMinutes}
//                                 onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
//                                     var value = +(event.target.value.replace(/\D/g,''))
//                                     if (value < 0) value = 0
//                                     if (value > 59) value = 59
//                                     this.saveRunMinutesValue(value)
//                                 }}
//                                 endAdornment={
//                                     <InputAdornment position="end" sx={{height: '20px', margin: '0px 3px 0px 0px'}}>
//                                         <SPAN sx={{fontSize: '12px'}}>
//                                             minutes
//                                         </SPAN>
//                                     </InputAdornment>
//                                 }
//                             />
//                         </DIV>
//                     )}
//                     <DIV sx={{display: 'inline-flex'}}>
//                         <Button
//                             disabled
//                             sx={{margin: '6px'}}
//                         >
//                             Back
//                         </Button>
//                         <Button
//                             variant="contained"
//                             color="primary"
//                             onClick={() => this.setState({ activeStep: SubmitStep.WHERE_ARE_YOU_RUNNING })}
//                             sx={{margin: '6px'}}
//                             disabled={optumi.package.notebookRuns === null || (optumi.package.notebookRuns && optumi.package.runHours === 0 && optumi.package.runMinutes === 0)}
//                         >
//                             Next
//                         </Button>
//                     </DIV>
//                 </>;
//             case SubmitStep.WHERE_ARE_YOU_RUNNING:
//                 return (
//                     <>
//                         <DIV sx={{width: '100%', display: 'inline-flex'}}>
//                             <Radio sx={{padding: '3px'}} color='primary' checked={optumi.package.runPlatform === Platform.LAPTOP} onChange={() => this.saveRunPlatformValue(Platform.LAPTOP)}/>
//                             <DIV sx={{margin: 'auto 0px'}}>
//                                 {capitalizeFirstLetter(Platform.LAPTOP)}
//                             </DIV>
//                         </DIV>
//                         <DIV sx={{width: '100%', display: 'inline-flex'}}>
//                             <Radio sx={{padding: '3px'}} color='primary' checked={optumi.package.runPlatform === Platform.COLAB} onChange={() => this.saveRunPlatformValue(Platform.COLAB)}/>
//                             <DIV sx={{margin: 'auto 0px'}}>
//                                 {capitalizeFirstLetter(Platform.COLAB)}
//                             </DIV>
//                         </DIV>
//                         <DIV sx={{width: '100%', display: 'inline-flex'}}>
//                             <Radio sx={{padding: '3px'}} color='primary' checked={optumi.package.runPlatform === Platform.KAGGLE} onChange={() => this.saveRunPlatformValue(Platform.KAGGLE)}/>
//                             <DIV sx={{margin: 'auto 0px'}}>
//                                 {capitalizeFirstLetter(Platform.KAGGLE)}
//                             </DIV>
//                             {optumi.package.runPlatform === Platform.KAGGLE && (
//                                 <Dropdown
//                                     sx={{padding: '3px 0px'}}
//                                     getValue={() => optumi.package.kaggleAccelerator === null ? "Pick accelerator" : optumi.package.kaggleAccelerator }
//                                     saveValue={(value: string) => this.saveKaggleAcceleratorValue(value)}
//                                     values={["Pick accelerator", KaggleAccelerator.NONE, KaggleAccelerator.GPU, KaggleAccelerator.TPU].map(x => { return { value: x, description: '', disabled: x === "Pick accelerator"} })}
//                                 />
//                             )}
//                         </DIV>
//                         <DIV sx={{width: '100%', display: 'inline-flex'}}>
//                             <Radio sx={{padding: '3px'}} color='primary' checked={optumi.package.runPlatform !== null && !([Platform.LAPTOP, Platform.KAGGLE, Platform.COLAB] as string[]).includes(optumi.package.runPlatform)} onChange={() => this.saveRunPlatformValue('')}/>
//                             <DIV sx={{margin: 'auto 0px'}}>
//                                 Other
//                             </DIV>
//                             {optumi.package.runPlatform !== null && !([Platform.LAPTOP, Platform.KAGGLE, Platform.COLAB] as string[]).includes(optumi.package.runPlatform) && (
//                                 <StyledOutlinedInput
//                                     placeholder={'ex. AWS instance'}
//                                     sx={{ margin: 'auto 6px' }}
//                                     value={optumi.package.runPlatform !== null && !([Platform.LAPTOP, Platform.KAGGLE, Platform.COLAB] as string[]).includes(optumi.package.runPlatform) ? optumi.package.runPlatform : ''}
//                                     onChange={(event: React.ChangeEvent<HTMLInputElement>) => this.saveRunPlatformValue(event.target.value)}
//                                 />
//                             )}
//                         </DIV>
//                         <DIV sx={{display: 'inline-flex'}}>
//                             <Button
//                                 onClick={() => this.setState({ activeStep: SubmitStep.DOES_YOUR_NOTEBOOK_RUN })}
//                                 sx={{margin: '6px'}}
//                             >
//                                 Back
//                             </Button>
//                             <Button
//                                 variant="contained"
//                                 color="primary"
//                                 onClick={() => this.setState({ activeStep: SubmitStep.PACKAGES })}
//                                 sx={{margin: '6px'}}
//                                 disabled={optumi.package.runPlatform === null || optumi.package.runPlatform == '' || (optumi.package.runPlatform === Platform.KAGGLE && optumi.package.kaggleAccelerator === null)}
//                             >
//                                 Next
//                             </Button>
//                         </DIV>
//                     </>
//                 )
//             case SubmitStep.PACKAGES:
//                 return (
//                     <>
//                         <Packages />
//                         <DIV sx={{display: 'inline-flex'}}>
//                             <Button
//                                 onClick={() => this.setState({ activeStep: SubmitStep.WHERE_ARE_YOU_RUNNING })}
//                                 sx={{margin: '6px'}}
//                             >
//                                 Back
//                             </Button>
//                             <Button
//                                 variant="contained"
//                                 color="primary"
//                                 onClick={() => this.setState({ activeStep: SubmitStep.FILES })}
//                                 sx={{margin: '6px'}}
//                             >
//                                 Next
//                             </Button>
//                         </DIV>
//                     </>
//                 );
//             case SubmitStep.FILES:
//                 return (
//                     <>
//                         <Files />
//                         <DIV sx={{display: 'inline-flex'}}>
//                             <Button
//                                 onClick={() => this.setState({ activeStep: SubmitStep.PACKAGES })}
//                                 sx={{margin: '6px'}}
//                             >
//                                 Back
//                             </Button>
//                             <Button
//                                 variant="contained"
//                                 color="primary"
//                                 onClick={() => this.setState({ activeStep: SubmitStep.HOW_DO_YOU_WANT_TO_BE_NOTIFIED })}
//                                 sx={{margin: '6px'}}
//                             >
//                                 Next
//                             </Button>
//                         </DIV>
//                     </>
//                 );
//             case SubmitStep.HOW_DO_YOU_WANT_TO_BE_NOTIFIED:
//                 const phoneUtil = PhoneNumberUtil.getInstance();
//                 return (
//                     <>
//                         {/* <DIV sx={{width: '100%', display: 'inline-flex'}}>
//                             <Radio sx={{padding: '3px'}} color='primary' checked={optumi.notifyVia === NotifyVia.EMAIL} onChange={() => this.saveNotifyViaValue(NotifyVia.EMAIL)}/>
//                             <DIV sx={{margin: 'auto 0px'}}>
//                                 Email
//                             </DIV>
//                         </DIV>
//                         {optumi.notifyVia === NotifyVia.EMAIL && (
//                             <StyledOutlinedInput
//                                 placeholder={'example@gmail.com'}
//                                 fullWidth
//                                 value={optumi.email}
//                                 onChange={(event: React.ChangeEvent<HTMLInputElement>) => this.saveEmailValue(event.target.value)}
//                             />
//                         )} */}
//                         <DIV sx={{width: '100%', display: 'inline-flex'}}>
//                             <Radio sx={{padding: '3px'}} color='primary' checked={optumi.notifications.packageReadySMSEnabled} onChange={() => this.savePackageReadySMSEnabledValue(true)}/>
//                             <DIV sx={{margin: 'auto 0px'}}>
//                             {'Text to ' + phoneUtil.format(phoneUtil.parse(Global.user.phoneNumber, 'US'), PhoneNumberFormat.INTERNATIONAL)}                            </DIV>
//                         </DIV>
//                         {/* {optumi.notifications.packageReadySMSEnabled && (
//                             <PhoneTextBox
//                                 getValue={() => Global.user.phoneNumber}
//                                 saveValue={(phoneNumber: string) => {
//                                     if (phoneNumber == '') Global.user.notificationsEnabled = false;
//                                     // We will automatically turn on notification if the user enters their phone number
//                                     if (phoneNumber != '') Global.user.notificationsEnabled = true;
//                                     Global.user.phoneNumber = phoneNumber;
//                                     // We need to update so the button below will be updated properly
//                                     this.setState({ buttonKey: this.state.buttonKey+1 });
//                                 }}
//                             />
//                         )} */}
//                         <DIV sx={{width: '100%', display: 'inline-flex'}}>
//                             <Radio sx={{padding: '3px'}} color='primary' checked={!optumi.notifications.packageReadySMSEnabled} onChange={() => this.savePackageReadySMSEnabledValue(false)}/>
//                             <DIV sx={{margin: 'auto 0px'}}>
//                                 Don't notify me
//                             </DIV>
//                         </DIV>
//                         <DIV sx={{display: 'inline-flex'}}>
//                             <Button
//                                 key={this.state.buttonKey}
//                                 onClick={() => this.setState({ activeStep: SubmitStep.FILES })}
//                                 sx={{margin: '6px'}}
//                             >
//                                 Back
//                             </Button>
//                             <Button
//                                 variant="contained"
//                                 color="primary"
//                                 onClick={() => this.setState({ activeStep: SubmitStep.SUBMIT })}
//                                 sx={{margin: '6px'}}
//                                 // disabled={optumi.notifications.packageReadySMSEnabled && Global.user.phoneNumber === ''}
//                             >
//                                 Next
//                             </Button>
//                         </DIV>
//                     </>
//                 )
//             case SubmitStep.SUBMIT:
//                 return (
//                     <DIV sx={{display: 'inline-flex'}}>
//                         <Button
//                             onClick={() => this.setState({ activeStep: SubmitStep.HOW_DO_YOU_WANT_TO_BE_NOTIFIED })}
//                             sx={{margin: '6px'}}
//                         >
//                             Back
//                         </Button>
//                         <Button
//                             variant="contained"
//                             color="primary"
//                             onClick={() => {
//                                 this.handleSubmitClick()
//                                 this.setState({ activeStep: SubmitStep.WAIT })
//                             }}
//                             sx={{margin: '6px'}}
//                         >
//                             Submit
//                         </Button>
//                     </DIV>
//                 )
//             case SubmitStep.WAIT:
//                 return (
//                     <DIV sx={{display: 'inline-flex'}}>
//                         <Button
//                             color="error"
//                             onClick={() => {
//                                 Global.metadata.cancelPackage();
//                                 this.setState({ activeStep: SubmitStep.SUBMIT })
//                             }}
//                             sx={{margin: '6px'}}
//                         >
//                             Cancel
//                         </Button>
//                         <Button
//                             variant="contained"
//                             color="primary"
//                             sx={{margin: '6px'}}
//                             disabled
//                         >
//                             Next
//                         </Button>
//                     </DIV>
//                 );
//             case SubmitStep.OPEN:
//                 return (
//                     <DIV sx={{display: 'inline-flex'}}>
//                         <Button
//                             sx={{margin: '6px'}}
//                             disabled
//                         >
//                             Back
//                         </Button>
//                         <Button
//                             variant="contained"
//                             color="success"
//                             onClick={() => {
//                                 this.safeSetState({ open: true })
//                             }}
//                             sx={{margin: '6px'}}
//                         >
//                             View
//                         </Button>
//                     </DIV>
//                 );
//             default:
//                 return (<></>)
//         }
//     }

//     private getStepPreview(step: number) {
//         const optumi = Global.metadata.getMetadata().config;
        
//         switch (step) {
//             case SubmitStep.DOES_YOUR_NOTEBOOK_RUN:
//                 return (
//                     <>
//                         {optumi.package.notebookRuns === true && (
//                             <>
//                                 {'It runs too slow: ' + optumi.package.runHours + 'h' + optumi.package.runMinutes + 'm'}
//                             </>
//                         )}
//                         {optumi.package.notebookRuns === false && (
//                             <>
//                                 It doesn't run at all
//                             </>
//                         )}
//                     </>
//                 )
//             case SubmitStep.WHERE_ARE_YOU_RUNNING:
//                 return (
//                     <>
//                         {optumi.package.runPlatform !== null && (
//                             <>
//                                 {capitalizeFirstLetter(optumi.package.runPlatform)}
//                                 {optumi.package.runPlatform === Platform.KAGGLE && (
//                                     <>
//                                         {': ' + optumi.package.kaggleAccelerator}
//                                     </>
//                                 )}
//                             </>
//                         )}
//                     </>
//                 )
//             case SubmitStep.PACKAGES:
//                 const requirements = optumi.upload.requirements
//                 const numRequirements = requirements === '' ? 0 : requirements.split('\n').filter(line => line !== '').length
//                 return (
//                     <>
//                         {numRequirements > 0 && (
//                             <>
//                                 {numRequirements + ' requirement' + (numRequirements > 1 ? 's' : '')}
//                             </>
//                         )}
//                     </>
//                 )
//             case SubmitStep.FILES:
//                 const files = optumi.upload.files;
//                 const dataConnectors = optumi.upload.dataConnectors;
//                 return (
//                     <>
//                         {files.length > 0 && (files.length + ' upload' + (files.length > 1 ? 's' : ''))}{files.length > 0 && dataConnectors.length > 0 ? ', ' : ''}
//                         {dataConnectors.length > 0 && (dataConnectors.length + ' connector' + (dataConnectors.length > 1 ? 's' : ''))}
//                     </>
//                 )
//             case SubmitStep.HOW_DO_YOU_WANT_TO_BE_NOTIFIED:
//                 const phoneUtil = PhoneNumberUtil.getInstance();
//                 return (
//                     <>
//                         {optumi.package.runPlatform !== null && (
//                             <>
//                                 {/* {capitalizeFirstLetter(optumi.notifyVia)}
//                                 {optumi.notifyVia === NotifyVia.EMAIL && (
//                                     <>
//                                         {': ' + optumi.email}
//                                     </>
//                                 )} */}
//                                 {optumi.notifications.packageReadySMSEnabled && (
//                                     <>
//                                         {'Text: ' + phoneUtil.format(phoneUtil.parse(Global.user.phoneNumber, 'US'), PhoneNumberFormat.INTERNATIONAL)}
//                                     </>
//                                 )}
//                                 {!optumi.notifications.packageReadySMSEnabled && (
//                                     <>
//                                         Don't notify me
//                                     </>
//                                 )}
//                             </>
//                         )}
//                     </>
//                 )
//             default:
//                 return (<></>)
//         }
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
//         const pack = Global.metadata.getPackage();
//         return (
//             <DIV sx={Object.assign({}, this.props.sx)}>
//                 {this.state.activeStep != -1 && (
//                     <Stepper 
//                         sx={{
//                             padding: '12px',
//                         }}
//                         activeStep={this.state.activeStep} 
//                         orientation="vertical"
//                     >
//                         {this.state.steps.map((label, index) => (
//                             <Step key={label}>
//                                 <StepLabel sx={{position: 'relative'}}>
//                                     {label}
//                                     {this.state.activeStep != index && (
//                                         <DIV sx={{position: 'absolute', bottom: '-22px', color: 'gray'}}>
//                                             {this.getStepPreview(index)}
//                                         </DIV>
//                                     )}
//                                 </StepLabel>
//                                 <StepContent>
//                                     {this.getStepContent(this.state.activeStep)}
//                                 </StepContent>
//                             </Step>
//                         ))}
//                     </Stepper>
//                 )}
//                 <WarningPopup
//                     open={this.state.showNoFileUploadsPopup}
//                     headerText="Heads up!"
//                     bodyText={`You didn't add any files. If your notebook reads local data files or Optumi data connectors you can hit "Cancel" and revisit the "Files" section.`}
//                     cancel={{
//                         text: `Cancel`,
//                         onCancel: (prevent: boolean) => {
//                             this.safeSetState({ showNoFileUploadsPopup: false })
//                         },
//                     }}
//                     continue={{
//                         text: `Submit anyway`,
//                         onContinue: (prevent: boolean) => {
//                             this.safeSetState({ showNoFileUploadsPopup: false })
//                             this.handleSubmitClick(true);
//                         },
//                         color: `primary`,
//                     }}
//                 />
//                 {this.state.activeStep == SubmitStep.OPEN && (
//                     <StyledDialog
//                         open={this.state.open}
//                         onClose={() => {
//                             this.safeSetState({open: false})
//                         }}
//                         scroll='paper'
//                     >
//                         <DialogTitle sx={{
//                             display: 'inline-flex',
//                             height: '60px',
//                             padding: '6px',
//                         }}>
//                             <DIV sx={{
//                                 display: 'inline-flex',
//                                 minWidth: '150px',
//                                 fontSize: '16px',
//                                 fontWeight: 'bold',
//                                 paddingRight: '12px', // this is 6px counteracting the DialogTitle padding and 6px aligning the padding to the right of the tabs
//                             }}>
//                                 <DIV sx={{margin: '12px'}}>
//                                 Optimizations
//                                 </DIV>
//                             </DIV>
//                             <DIV sx={{width: '100%', display: 'inline-flex', overflowX: 'hidden', fontSize: '16px', paddingLeft: '8px'}}>
//                                 <DIV sx={{flexGrow: 1}} />
//                                 <Button
//                                     disableElevation
//                                     sx={{
//                                         height: '36px',
//                                         margin: '6px',
//                                     }}
//                                     onClick={() => {
//                                         const pack = Global.metadata.getPackage();
//                                         Global.metadata.openPackage(true, true)

//                                         // Update the code
//                                         const current = Global.tracker.currentWidget;
//                                         current.content.model.fromJSON(pack.optimizedNotebook)

//                                         // Update the metadata
//                                         const metadata = Global.metadata.getMetadata();
//                                         metadata.config = pack.optimizedConfig;
//                                         Global.metadata.setMetadata(metadata);

//                                         this.safeSetState({ open: false, activeStep: SubmitStep.SUBMIT })

//                                         this.props.openDeployPage();
//                                     }}
//                                     variant='contained'
//                                     color='primary'
//                                 >
//                                     Replace existing notebook
//                                 </Button>
//                                 <Button
//                                     disableElevation
//                                     sx={{
//                                         height: '36px',
//                                         margin: '6px',
//                                     }}
//                                     onClick={async () => {
//                                         const pack = Global.metadata.getPackage();
//                                         Global.metadata.openPackage(true, true)

//                                         // Open the code in a new notebook
//                                         var path = Global.tracker.currentWidget.context.path;
                                        
//                                         var inc = 0;
//                                         var newPath = path;
//                                         while ((await FileServerUtils.checkIfPathExists(newPath))[0]) {
//                                             inc++;
//                                             newPath = inc == 0 ? path : path.replace('.', '(' + inc + ').');
//                                         }

//                                         Global.metadata.setMetadataAfterOpen(newPath, pack.optimizedConfig);

//                                         FileServerUtils.saveNotebook(newPath, pack.optimizedNotebook).then((success: boolean) => {
//                                             Global.docManager.open(newPath);
//                                         });

//                                         this.safeSetState({ open: false, activeStep: SubmitStep.SUBMIT })

//                                         this.props.openDeployPage();
//                                     }}
//                                     variant='contained'
//                                     color='primary'
//                                 >
//                                     Open as a new notebook
//                                 </Button>
//                             </DIV>
//                             <IconButton
//                                 size='large'
//                                 onClick={() => this.safeSetState({ open: false })}
//                                 sx={{
//                                     display: 'inline-block',
//                                     width: '36px',
//                                     height: '36px',
//                                     padding: '3px',
//                                     margin: '6px',
//                                 }}
//                             >
//                                 <CloseIcon
//                                     sx={{
//                                         width: '30px',
//                                         height: '30px',
//                                         padding: '3px',
//                                     }}
//                                 />
//                             </IconButton>
//                         </DialogTitle>
//                         <DialogContent sx={{
//                             flexGrow: 1, 
//                             width: '100%',
//                             height: '100%',
//                             padding: '0px',
//                             marginBottom: '0px', // This is because MuiDialogContentText-root is erroneously setting the bottom to 12
//                             // lineHeight: 'var(--jp-code-line-height)',
//                             fontSize: 'var(--jp-ui-font-size1)',
//                             fontFamily: 'var(--jp-ui-font-family)',
//                         }}>
//                             <DIV sx={{height: '100%', overflow: 'auto', padding: '20px'}}>
//                                 <DIV sx={{}}>
//                                     <Header title="Estimates" />
//                                     <DIV sx={{margin: '6px'}}>Runtime: <SPAN sx={{fontWeight: 'bold'}}>{this.formatOptimizedRuntime(pack)}</SPAN></DIV>
//                                     <DIV sx={{margin: '6px'}}>Cost: <SPAN sx={{fontWeight: 'bold'}}>{this.getOptimizedCost(pack)}</SPAN></DIV>
//                                 </DIV>
//                                 <DIV sx={{display: 'inline-flex', width: '50%'}}>
//                                     {/* <DIV sx={{flexGrow: 1}}>
//                                         <Header title="Original Resource Selection" />
//                                         {this.state.originalMachines.map(m => m.getPreviewComponent())}
//                                     </DIV> */}
//                                     <DIV sx={{flexGrow: 1, paddingTop: '6px'}}>
//                                         <Header title="Resource Optimization" />
//                                         {this.state.optimizedMachines.map(m => m.getPreviewComponent())}
//                                     </DIV>
//                                 </DIV>
//                                 <DIV sx={{flexGrow: 1, paddingTop: '6px'}}>
//                                     <Header title="Notebook Optimization" />
//                                     {/* position: relative is needed here otherwise the line numbers for the diff do not scroll with the rest of the page*/}
//                                     <DIV sx={{position: 'relative'}} dangerouslySetInnerHTML={{ __html: this.state.diffHTML }} />
//                                 </DIV>
//                             </DIV>
//                         </DialogContent>
//                     </StyledDialog>
//                 )}
// 			</DIV>
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
//         const pack = Global.metadata.getPackage();
//         if (pack == null) {
//             return { };
//         } else if (pack.packageState == PackageState.SHIPPED) {
//             this.previewNotebook(pack.originalConfig).then(machines => this.safeSetState({ originalMachines: [machines[0]] }))
//             this.previewNotebook(pack.optimizedConfig).then(machines => this.safeSetState({ optimizedMachines: [machines[0]] }))
//             return { 
//                 activeStep: SubmitStep.OPEN, 
//                 diffHTML: this.getDiff(pack.originalNotebook, pack.optimizedNotebook),
//             };
//         } else {
//             return { activeStep: SubmitStep.WAIT };
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
// 	}

// 	// Will be called automatically when the component is unmounted
// 	public componentWillUnmount = () => {
//         Global.metadata.getPackageChanged().disconnect(this.handleUpdate);
//         Global.metadata.getMetadataChanged().disconnect(this.handleMetadataChange)
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
