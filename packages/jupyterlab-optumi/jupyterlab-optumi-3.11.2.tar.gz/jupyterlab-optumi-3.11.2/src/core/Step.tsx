/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { DIV, Global, SPAN } from '../Global'

import { SxProps, Theme } from '@mui/system';
import {
    Step as OtherStep,
    StepContent,
    StepButton,
    Button,
    StepIcon,
    SvgIcon,
    StepConnector,
    useTheme,
    OutlinedInput,
} from '@mui/material';
import { withStyles } from '@mui/styles';

import { StepperCallbacks } from './Stepper';

export const StepOutlinedInput = withStyles({
    root: {
        padding: '0px',
        margin: '0px 3px',
        height: '21px',
    },
    input: {
        fontSize: '12px',
        padding: '3px 6px 3px 6px',
    },
    adornedEnd: {
        paddingRight: '0px',
    },
}) (OutlinedInput)

interface IProps {
    header: string | (() => string)
    preview?: undefined | string | (() => undefined | string)

    overrideSelected?: undefined | boolean | (() => boolean)
    overrideDisabled?: undefined | boolean | (() => boolean)
    overrideCompleted?: undefined | boolean | (() => boolean)
    overrideError?: undefined | boolean | (() => boolean)
    overrideExpanded?: undefined | boolean | (() => boolean)

    overrideBackButton?: undefined | string | JSX.Element
    overrideNextButton?: undefined | string | JSX.Element
}

interface HiddenProps {
    step?: number
    stepperCallbacks?: StepperCallbacks
    sx?: SxProps<Theme>
    children?: undefined | JSX.Element | JSX.Element[]

    active?: boolean
    disabled?: boolean
    completed?: boolean
    expanded?: boolean
}

const StyledConnector = withStyles({
    line: {
        // this is a fantastic trick we should try to remember for dynamically changing
        // values based on props of child classes only accessible by styles
        minHeight: 'inherit',
    },
})(StepConnector)

/**
 * Target behavior:
 * - expanded if always expanded or both selected and not disabled
 * - gray (disabled) blue (enabled default) red (enabled error)
 * - number (default) check (completed) exclamation mark (error)
 */
export default function Step(props: IProps) {
    const {
        header, preview,
        overrideSelected, overrideDisabled, overrideCompleted, overrideError, overrideExpanded,
        overrideBackButton, overrideNextButton,
        step, stepperCallbacks, children, sx,
        active, disabled, completed, expanded, ...other
    } = props as IProps & HiddenProps
    const theme = useTheme()

    let actualHeader: string = (() => {
        switch(typeof(header)) {
            case 'string': return header
            case 'function': return header()
        }
    })()

    let actualPreview: string = (() => {
        switch(typeof(preview)) {
            case 'string': return preview
            case 'function': return preview()
        }
    })()

    let actuallySelected: boolean = (() => {
        switch(typeof(overrideSelected)) {
            case 'undefined': return stepperCallbacks.isStepSelected(step)
            case 'boolean': return overrideSelected
            case 'function': return overrideSelected()
        }
    })()

    let actuallyDisabled: boolean = (() => {
        switch(typeof(overrideDisabled)) {
            case 'undefined': return stepperCallbacks.isStepDisabled(step)
            case 'boolean': return overrideDisabled
            case 'function': return overrideDisabled()
        }
    })()

    let actuallyCompleted: boolean = (() => {
        switch(typeof(overrideCompleted)) {
            case 'undefined': return stepperCallbacks.isStepCompleted(step)
            case 'boolean': return overrideCompleted
            case 'function': return overrideCompleted()
        }
    })()

    let actuallyError: boolean = (() => {
        switch(typeof(overrideError)) {
            case 'undefined': return stepperCallbacks.isStepError(step)
            case 'boolean': return overrideError
            case 'function': return overrideError()
        }
    })()

    let actuallyExpanded: boolean = (() => {
        switch(typeof(overrideExpanded)) {
            case 'undefined': return actuallySelected
            case 'boolean': return overrideExpanded
            case 'function': return overrideExpanded()
        }
    })()

    const getIcon = () => {
        const className = (
            'MuiStepIcon-root'
            + (!actuallyDisabled ? (
                ' MuiStepIcon-active'
                + (actuallyError ? ' Mui-error' : '')
                + (actuallyCompleted ? ' MuiStepIcon-completed' : '')
            ) : '')
        )
        if (actuallyError) {
            return (
                <SvgIcon className={className}>
                    <path d='M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z' />
                </SvgIcon>
            )
        } else if (actuallyCompleted) {
            return (
                <SvgIcon className={className}>
                    <path d='M12 0a12 12 0 1 0 0 24 12 12 0 0 0 0-24zm-2 17l-5-5 1.4-1.4 3.6 3.6 7.6-7.6L19 8l-9 9z' />
                </SvgIcon>
            )
        } else {
            return (
                <SvgIcon className={className}>
                    <circle cx='12' cy='12' r='12' />
                    <text className='MuiStepIcon-text' x='12' y='16' textAnchor='middle'>
                        {step + 1}
                    </text>
                </SvgIcon>
            )
        }
    }

    if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
    return (
        <OtherStep
            {...other}
            sx={Object.assign({}, sx)}
            active={actuallySelected}
            completed={actuallyCompleted}
            disabled={actuallyDisabled}
            expanded={actuallyExpanded}
        >
            <StepButton
                sx={{
                    position: 'relative',
                    textAlign: 'left',
                    margin: '-4px',
                    padding: '4px',
                }}
                onClick={() => stepperCallbacks.setStepSelected(step)}
                icon={<StepIcon icon={getIcon()} />}
            >
                <SPAN sx={{
                    color: !actuallyDisabled && actuallyError ? theme.palette.error.main : undefined,
                }}>
                    {actualHeader}
                </SPAN>
                <DIV sx={{
                    position: 'absolute',
                    bottom: 'calc(-30px + 8px)',
                    color: 'gray',
                    opacity: actuallyExpanded ? 0 : 1,
                    transitionDelay: actuallyExpanded ? '0ms' : '245ms',
                    transitionDuration: actuallyExpanded ? '0ms' : '245ms',
                }}>
                    {actualPreview}
                </DIV>
            </StepButton>
            <StepContent sx={{marginTop: '4px'}}>
                {children}
                {(!actuallyDisabled || actuallyExpanded) && (
                    <DIV sx={{display: 'inline-flex'}}>
                        {typeof(overrideBackButton) === 'object' ? (
                            overrideBackButton
                        ) : (
                            <Button
                                onClick={() => stepperCallbacks.setStepSelected(step - 1)}
                                disabled={stepperCallbacks.isStepDisabled(step - 1)}
                                sx={{margin: '6px'}}
                            >
                                {typeof(overrideBackButton) === 'string' ? (
                                    overrideBackButton
                                ) : (
                                    'Back'
                                )}
                            </Button>
                        )}
                        {typeof(overrideNextButton) === 'object' ? (
                            overrideNextButton
                        ) : (
                            <Button
                                onClick={() => stepperCallbacks.setStepSelected(step + 1)}
                                disabled={stepperCallbacks.isStepDisabled(step + 1)}
                                sx={{margin: '6px'}}
                                variant='contained'
                                color='primary'
                            >
                                {typeof(overrideNextButton) === 'string' ? (
                                    overrideNextButton
                                ) : (
                                    'Next'
                                )}
                            </Button>
                        )}
                    </DIV>
                )}
            </StepContent>
            <StyledConnector sx={{
                minHeight: !actuallyExpanded && (!stepperCallbacks.isLastStep(step) || actualPreview !== undefined) ? '24px' : '0px',
                transitionDuration: '245ms',
                paddingBottom: '0 0 4px',
            }} />
        </OtherStep>
    )
}
