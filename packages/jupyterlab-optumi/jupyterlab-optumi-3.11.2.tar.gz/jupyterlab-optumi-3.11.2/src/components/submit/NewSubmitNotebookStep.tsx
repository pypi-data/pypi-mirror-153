// /*
// **  Copyright (C) Optumi Inc - All rights reserved.
// **
// **  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
// **  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
// **/

// import * as React from 'react'
// import { Global } from '../../Global'

// import { Button } from '@mui/material';

// import { StepperCallbacks } from '../../core/Stepper';
// import Step from '../../core/Step';
// import WarningPopup from '../../core/WarningPopup';

// interface IProps {
//     step: number
//     stepperCallbacks: StepperCallbacks
// }

// export default function SubmitNotebookStep(props: any) {
//     const {step, stepperCallbacks} = props as IProps
//     const [open, setOpen] = React.useState<boolean>(false)

//     const handleSubmitClick = (bypassWarning: boolean) => {
//         const optumi = Global.metadata.getMetadata();
//         if (!bypassWarning && optumi.config.upload.files.length === 0) {
//             setOpen(true)
//         } else {
//             Global.metadata.submitPackage();
//             stepperCallbacks.completeAndIncrement(step)
//         }
//     }

//     if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
//     return (
//         <Step {...props}
//             header={`Submit your notebook`}
//             overrideNextButton={
//                 <Button
//                     onClick={() => handleSubmitClick(false)}
//                     disabled={stepperCallbacks.isStepDisabled(step)}
//                     sx={{margin: '6px'}}
//                     variant='contained'
//                     color='primary'
//                 >
//                     Submit
//                 </Button>
//             }
//         >
//             <WarningPopup
//                 open={open}
//                 headerText='Heads up!'
//                 bodyText={`You didn't add any files. If your notebook reads local data files or Optumi data connectors you can hit "Cancel" and revisit the "Files" section.`}
//                 cancel={{
//                     text: 'Cancel',
//                     onCancel: () => {
//                         setOpen(false)
//                     },
//                 }}
//                 continue={{
//                     text: 'Submit anyway',
//                     onContinue: () => {
//                         setOpen(false)
//                         handleSubmitClick(true)
//                     },
//                     color: 'primary',
//                 }}
//             />
//         </Step>
//     )
// }
