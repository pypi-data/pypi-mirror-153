// /*
// **  Copyright (C) Optumi Inc - All rights reserved.
// **
// **  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
// **  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
// **/

// import * as React from 'react'
// import { Global } from '../../Global'

// import { Button } from '@mui/material';

// import Step from '../../core/Step';
// import { Files } from '../deploy/Files';
// import { StepperCallbacks } from '../../core/Stepper';

// interface IProps {
//     step: number
//     stepperCallbacks: StepperCallbacks
// }

// export default function WhatFilesStep(props: any) {
//     const {step, stepperCallbacks} = props as IProps
//     const optumi = Global.metadata.getMetadata().config;
//     const files = optumi.upload.files;
//     const dataConnectors = optumi.upload.dataConnectors;

//     if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
//     return (
//         <Step {...props}
//             header={`What files does your notebook need?`}
//             preview={() => {
//                 let preview = ''
//                 if (files.length > 0) preview += files.length + ' upload'
//                 if (files.length > 1) preview += 's'
//                 if (files.length > 0 && dataConnectors.length > 0) preview += ', '
//                 if (dataConnectors.length > 0) preview += dataConnectors.length + ' connector'
//                 if (dataConnectors.length > 1) preview += 's'
//                 return preview
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
//             <Files />
//         </Step>
//     )
// }
