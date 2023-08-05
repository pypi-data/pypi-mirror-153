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
// import { Packages } from '../deploy/Packages';
// import { StepperCallbacks } from '../../core/Stepper';

// interface IProps {
//     step: number
//     stepperCallbacks: StepperCallbacks
// }

// export default function WhatPackagesStep(props: any) {
//     const {step, stepperCallbacks} = props as IProps
//     const requirements = Global.metadata.getMetadata().config.upload.requirements
//     const numRequirements = requirements === '' ? 0 : requirements.split('\n').filter(line => line !== '').length

//     if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
//     return (
//         <Step {...props}
//             header={`What packages does your notebook use?`}
//             preview={() => {
//                 let preview = ''
//                 if (numRequirements > 0) preview += numRequirements + ' requirement'
//                 if (numRequirements > 1) preview += 's'
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
//             <Packages />
//         </Step>
//     )
// }
