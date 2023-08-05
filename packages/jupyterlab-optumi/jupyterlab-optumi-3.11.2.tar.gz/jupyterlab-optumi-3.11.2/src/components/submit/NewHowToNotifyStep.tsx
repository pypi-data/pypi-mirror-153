// /*
// **  Copyright (C) Optumi Inc - All rights reserved.
// **
// **  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
// **  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
// **/

// import * as React from 'react'
// import { DIV, Global } from '../../Global'

// import { Button, Radio } from '@mui/material';

// import Step from '../../core/Step';
// import { OptumiMetadataTracker } from '../../models/OptumiMetadataTracker';
// import { StepperCallbacks } from '../../core/Stepper';

// import { PhoneNumberFormat, PhoneNumberUtil } from 'google-libphonenumber';

// interface IProps {
//     step: number
//     stepperCallbacks: StepperCallbacks
// }

// export default function HowToNotifyStep(props: any) {
//     const {step, stepperCallbacks} = props as IProps
//     const optumi = Global.metadata.getMetadata().config;
//     const phoneUtil = PhoneNumberUtil.getInstance();

//     const savePackageReadySMSEnabledValue = (value: boolean): void => {
//         const tracker: OptumiMetadataTracker = Global.metadata;
//         const optumi = tracker.getMetadata();
//         optumi.config.notifications.packageReadySMSEnabled = value;
//         tracker.setMetadata(optumi);
//     }

//     if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
//     return (
//         <Step {...props}
//             header={`How would you like to be notified when it's done?`}
//             preview={() => {
//                 if (optumi.package.runPlatform !== null) {
//                     // if (optumi.notifyVia === NotifyVia.EMAIL) {
//                     //     return `Email: ${optumi.email}`
//                     // } else {
//                         if (optumi.notifications.packageReadySMSEnabled) {
//                             return `Text: ${phoneUtil.format(phoneUtil.parse(Global.user.phoneNumber, 'US'), PhoneNumberFormat.INTERNATIONAL)}`
//                         } else {
//                             return `Don't notify me`
//                         }
//                     // }
//                 }
//             }}
//             overrideNextButton={
//                 <Button
//                     onClick={() => stepperCallbacks.completeAndIncrement(step)}
//                     sx={{margin: '6px'}}
//                     variant='contained'
//                     color='primary'
//                 >
//                     Next
//                 </Button>
//             }
//         >
//             {/* <DIV sx={{width: '100%', display: 'inline-flex'}}>
//                 <Radio
//                     sx={{padding: '3px'}}
//                     color='primary'
//                     checked={optumi.notifyVia === NotifyVia.EMAIL}
//                     onChange={() => this.saveNotifyViaValue(NotifyVia.EMAIL)}
//                 />
//                 <DIV sx={{margin: 'auto 0px'}}>
//                     Email
//                 </DIV>
//             </DIV>
//             {optumi.notifyVia === NotifyVia.EMAIL && (
//                 <StyledOutlinedInput
//                     placeholder={'example@gmail.com'}
//                     fullWidth
//                     value={optumi.email}
//                     onChange={(event: React.ChangeEvent<HTMLInputElement>) => this.saveEmailValue(event.target.value)}
//                 />
//             )} */}
//             <DIV sx={{width: '100%', display: 'inline-flex'}}>
//                 <Radio
//                     sx={{padding: '3px'}}
//                     color='primary'
//                     checked={optumi.notifications.packageReadySMSEnabled}
//                     onChange={() => savePackageReadySMSEnabledValue(true)}
//                 />
//                 <DIV sx={{margin: 'auto 0px'}}>
//                     {'Text to ' + phoneUtil.format(phoneUtil.parse(Global.user.phoneNumber, 'US'), PhoneNumberFormat.INTERNATIONAL)}
//                 </DIV>
//             </DIV>
//             {/* {optumi.notifications.packageReadySMSEnabled && (
//                 <PhoneTextBox
//                     getValue={() => Global.user.phoneNumber}
//                     saveValue={(phoneNumber: string) => {
//                         if (phoneNumber == '') Global.user.notificationsEnabled = false;
//                         // We will automatically turn on notification if the user enters their phone number
//                         if (phoneNumber != '') Global.user.notificationsEnabled = true;
//                         Global.user.phoneNumber = phoneNumber;
//                         // We need to update so the button below will be updated properly
//                         this.setState({ buttonKey: this.state.buttonKey+1 });
//                     }}
//                 />
//             )} */}
//             <DIV sx={{width: '100%', display: 'inline-flex'}}>
//                 <Radio
//                     sx={{padding: '3px'}}
//                     color='primary'
//                     checked={!optumi.notifications.packageReadySMSEnabled}
//                     onChange={() => savePackageReadySMSEnabledValue(false)}
//                 />
//                 <DIV sx={{margin: 'auto 0px'}}>
//                     Don't notify me
//                 </DIV>
//             </DIV>
//         </Step>
//     )
// }
