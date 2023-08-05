/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { Global } from '../Global'

import { SxProps, Theme } from '@mui/system';
import { Stepper as OtherStepper } from '@mui/material';

interface IProps {
    sx?: SxProps<Theme>,
    children?: JSX.Element[],
}

interface IState {
    focusMin: number
    focusMax: number

    selectedStep: number
    stepsDisabled: boolean[]
    stepsCompleted: boolean[]
    stepsErrored: boolean[]
}

export interface StepperCallbacks {
    setFocusMin: (step: number) => void
    setFocusMax: (step: number) => void
    getFocusMin: () => number
    getFocusMax: () => number
    isLastStep: (step: number) => boolean
    incrementFocusMax: (step: number, count?: number) => void
    completeAndIncrement: (step: number) => void

    setStepSelected: (step: number) => void
    setStepDisabled: (step: number, disabled: boolean) => void
    setStepComplete: (step: number, complete: boolean) => void
    setStepError: (step: number, error: boolean) => void

    isStepSelected: (step: number) => boolean
    isStepDisabled: (step: number) => boolean
    isStepCompleted: (step: number) => boolean
    isStepError: (step: number) => boolean
}

export class Stepper extends React.Component<IProps, IState> {
    private _isMounted = false;

    constructor(props: IProps) {
        super(props)
        this.state = {
            focusMin: -1,
            focusMax: 0,

            selectedStep: -1,
            stepsDisabled: [],
            stepsCompleted: [],
            stepsErrored: [],
        }
    }

    private setFocusMin = (step: number): void => {
        this.safeSetState({focusMin: step})
    }

    private setFocusMax = (step: number): void => {
        this.safeSetState({focusMax: step})
    }

    private getFocusMin = (): number => {
        return this.state.focusMin
    }

    private getFocusMax = (): number => {
        return this.state.focusMax
    }

    private isLastStep = (step: number): boolean => {
        return this.props.children.length === (step + 1)
    }

    private incrementFocusMax = (step: number, count?: number): void => {
        if (count === undefined || count < 1) count = 1
        if (this.getFocusMax() <= step) this.setFocusMax(step + count)
    }

    private completeAndIncrement = (step: number): void => {
        let newStepsCompleted = this.state.stepsCompleted;
        newStepsCompleted[step] = true
        let newFocusMax = this.state.focusMax
        if (this.getFocusMax() <= step) newFocusMax = step + 1
        let newSelectedStep = this.state.selectedStep
        if (!this.isStepDisabled(step)) newSelectedStep = step + 1;
        this.safeSetState({stepsCompleted: newStepsCompleted, focusMax: newFocusMax, selectedStep: newSelectedStep}, true)
    }

    private setStepSelected = (step: number): void => {
        if (!this.isStepDisabled(step)) this.safeSetState({selectedStep: step});
    }

    private setStepDisabled = (step: number, disabled: boolean): void => {
        let newStepsDisabled = this.state.stepsDisabled;
        newStepsDisabled[step] = disabled
        this.safeSetState({stepsDisabled: newStepsDisabled}, true)
    }

    private setStepComplete = (step: number, complete: boolean): void => {
        let newStepsCompleted = this.state.stepsCompleted;
        newStepsCompleted[step] = complete
        this.safeSetState({stepsCompleted: newStepsCompleted}, true)
    }

    private setStepError = (step: number, error: boolean): void => {
        let newStepsErrored = this.state.stepsErrored;
        newStepsErrored[step] = error
        this.safeSetState({stepsErrored: newStepsErrored}, true)
    }

    private isStepSelected = (step: number) : boolean => {
        return step === this.state.selectedStep
    }
    private isStepDisabled = (step: number): boolean => {
        if (!(step >= this.state.focusMin && step <= this.state.focusMax)) return true;
        return this.state.stepsDisabled[step] === true
    }
    private isStepCompleted = (step: number): boolean => {
        return this.state.stepsCompleted[step] === true
    }
    private isStepError = (step: number): boolean => {
        return this.state.stepsErrored[step] === true
    }

    private stepperCallbacks: StepperCallbacks = {
        setFocusMin: this.setFocusMin,
        setFocusMax: this.setFocusMax,
        getFocusMin: this.getFocusMin,
        getFocusMax: this.getFocusMax,
        isLastStep: this.isLastStep,
        incrementFocusMax: this.incrementFocusMax,
        completeAndIncrement: this.completeAndIncrement,

        setStepSelected: this.setStepSelected,
        setStepDisabled: this.setStepDisabled,
        setStepComplete: this.setStepComplete,
        setStepError: this.setStepError,

        isStepSelected: this.isStepSelected,
        isStepDisabled: this.isStepDisabled,
        isStepCompleted: this.isStepCompleted,
        isStepError: this.isStepError,
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <OtherStepper
                sx={Object.assign({padding: '12px'}, this.props.sx)}
                orientation='vertical'
                nonLinear
                activeStep={this.state.selectedStep}
                connector={<></>}
            >
                {this.props.children.map((child, step) => React.cloneElement(child, {
                    key: step,
                    step: step,
                    stepperCallbacks: this.stepperCallbacks,
                }))}
            </OtherStepper>
        )
    }

    public componentDidMount = () => {
        this._isMounted = true;
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
        this._isMounted = false;
	}

    private safeSetState = (map: any, forceUpdate?: boolean) => {
		if (this._isMounted) {
			let update = forceUpdate === true
			try {
                if (!update) {
                    for (const key of Object.keys(map)) {
                        if (JSON.stringify(map[key]) !== JSON.stringify((this.state as any)[key])) {
                            update = true
                            break
                        }
                    }
                }
			} catch (error) {
				update = true
			}
			if (update) {
				if (Global.shouldLogOnSafeSetState) console.log('SafeSetState (' + new Date().getSeconds() + ')');
				this.setState(map)
			} else {
				if (Global.shouldLogOnSafeSetState) console.log('SuppressedSetState (' + new Date().getSeconds() + ')');
			}
		}
	}

    public shouldComponentUpdate = (nextProps: IProps, nextState: IState): boolean => {
        try {
            if (JSON.stringify(this.props) != JSON.stringify(nextProps)) return true;
            if (JSON.stringify(this.state) != JSON.stringify(nextState)) return true;
            if (Global.shouldLogOnRender) console.log('SuppressedRender (' + new Date().getSeconds() + ')');
            return false;
        } catch (error) {
            return true;
        }
    }
}
