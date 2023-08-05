/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { DIV, Global } from '../Global'

import { Radio } from '@mui/material';

import Step from './Step';
import { StepperCallbacks } from './Stepper';

/* example Stepper:

    <Stepper>
        <WhatsTheProblemStep />
        <WheresItRunningStep />
        <WhatPackagesStep />
        <WhatFilesStep />
        <HowToNotifyStep />
        <SubmitNotebookStep overrideExpanded={!notebookSubmitted} />
        <WaitForChangesStep />
        <AcceptChangesStep />
    </Stepper>
*/

interface IProps {
    // I snagged these out of the props to use them here. All props
    // (both IProps and HiddenProps) in Step.tsx pass through this object,
    // so feel free to grab any of them. Note: the props type this object officially
    // takes is any since we don't want to require props that will be passed
    // from Stepper.tsx to Step.tsx since that will just throw errors for missing props
    // when we define the stepper
    step: number
    stepperCallbacks: StepperCallbacks
}

/**
 * THIS IS JUST FOR EXAMPLE
 * 
 * The logic for increasing the focusMax is reasonable if you want
 * things to unlock one at a time and allow clicking around previously
 * answered items, but could totally be handled differently
 * 
 * Also, the implementation of the internals was as it was before.
 * I did not do any optimization to reduce complexity there
 */
export default function WhatsTheProblemStep(props: any) {
    const {step, stepperCallbacks} = props as IProps
    const [notebookRuns, setNotebookRuns] = React.useState<boolean>(undefined)

    const handleChange = (checked: boolean) => {
        setNotebookRuns(checked)
        if (stepperCallbacks.getFocusMax() <= step) stepperCallbacks.setFocusMax(step + 1)
        stepperCallbacks.setStepComplete(step, checked)
    }

    if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
    return (
        <Step {...props}
            // You can define things here or in the implementation of the stepper.
            // If you wanted this step to always be expanded for example, you could either add
            // overrideExpanded={true} here or in <WhatsTheProblemStep overrideExpanded={true} />
            header={`What's the problem with your notebook?`}
            preview={`It does not run at all`}
        >
            <DIV sx={{width: '100%', display: 'inline-flex'}}>
                <Radio sx={{padding: '3px'}} color='primary' checked={notebookRuns === false} onChange={() => handleChange(false)}/>
                <DIV sx={{margin: 'auto 0px'}}>
                    It does not run at all
                </DIV>
            </DIV>
            <DIV sx={{width: '100%', display: 'inline-flex'}}>
                <Radio sx={{padding: '3px'}} color='primary' checked={notebookRuns === true} onChange={() => handleChange(true)}/>
                <DIV sx={{margin: 'auto 0px'}}>
                    It runs too slow
                </DIV>
            </DIV>
        </Step>
    )
}
