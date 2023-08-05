/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global, StyledSelect } from '../Global';

import { SxProps, Theme } from '@mui/system';
import { OutlinedInput, FormControl, FormHelperText, MenuItem, SelectChangeEvent } from '@mui/material';
import { withStyles } from '@mui/styles';

import ExtraInfo from '../utils/ExtraInfo';

const StyledMenuItem = withStyles({
    root: {
        fontSize: 'var(--jp-ui-font-size1)',
        padding: '3px 3px 3px 6px',
        justifyContent: 'center',
    }
}) (MenuItem)

const StyledOutlinedInput = withStyles({
    input: {
        fontSize: '12px',
        padding: '3px 6px 3px 6px',
        height: '1.1876em',
    },
    adornedEnd: {
        paddingRight: '0px',
    },
}) (OutlinedInput);

interface IProps {
    sx?: SxProps<Theme>
    label: string
    labelWidth?: string
    getValue: () => number
    saveValue: (value: number) => string | void
    unitValues: {unit: string, value: number}[]
    placeholder?: string
    helperText?: string
    minValue?: number
    maxValue?: number
    onFocus?: (event: React.FocusEvent<HTMLInputElement>) => void
    onBlur?: (event: React.FocusEvent<HTMLInputElement>) => void
}

interface IState {
    unit: string
    value: number
    errorMessage: string
}

export class TextBoxDropdown extends React.Component<IProps, IState> {
    private _isMounted = false

    textField: React.RefObject<HTMLInputElement>

    constructor(props: IProps) {
        super(props);
        this.textField = React.createRef();
        const [unit, value] = this.normalize(this.props.getValue());
        this.state = {
            unit: unit,
            value: value,
            errorMessage: '',
        }
    }

    private normalize(value: number): [string, number] {
        let largestSmallerUnit = this.props.unitValues[0].unit
        let largestSmallerValue = this.props.unitValues[0].value
        for (let unitValue of this.props.unitValues) {
            if (unitValue.value <= value && unitValue.value > largestSmallerValue) {
                largestSmallerUnit = unitValue.unit
                largestSmallerValue = unitValue.value
            }
        }
        return [largestSmallerUnit, Number.parseFloat((value / largestSmallerValue).toPrecision(3))]
    }

    private denormalize(unit: string, value: number): number {
        for (let unitValue of this.props.unitValues) {
            if (unitValue.unit === unit) {
                return unitValue.value * value
            }
        }
        return value
    }

    private handleValueChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        try {
            let unit = this.state.unit
            const charTyped = event.currentTarget.value.replace(/[0-9\.]/g, '')
            if (charTyped.length > 0) {
                for (let unitValue of this.props.unitValues) {
                    if (unitValue.unit.charAt(0) === charTyped[0]) {
                        unit = unitValue.unit
                        break
                    }
                }
            }
            let value = event.currentTarget.value === '' ? 0 : Number.parseFloat(event.currentTarget.value.replace(/[^0-9\.]/g, ''))
            const denormalizedValue = this.denormalize(unit, value)
            let errorMessage = ''
            if (this.props.minValue && denormalizedValue < this.props.minValue) {
                const [minUnit, minValue] = this.normalize(this.props.minValue)
                errorMessage = `Minimum value is ${minValue}${minUnit}`
            } else if (this.props.maxValue && denormalizedValue > this.props.maxValue) {
                const [maxUnit, maxValue] = this.normalize(this.props.maxValue)
                errorMessage = `Maximum value is ${maxValue}${maxUnit}`
            }
            this.safeSetState({unit: unit, value: value === NaN ? this.state.value : value, errorMessage: errorMessage})
        } catch (error) {
            // If Number.parseFloat fails, we don't want to update the values
        }
    }

    private handleValueFocus = (event: React.FocusEvent<HTMLInputElement>) => {
        if (this.props.onFocus) {
            this.props.onFocus(event)
        }
    }

    private handleValueBlur = (event: React.FocusEvent<HTMLInputElement>) => {
        if (this.props.onBlur) {
            this.props.onBlur(event)
        }
        const [normalizedUnit, normalizedValue] = this.normalize(this.denormalize(this.state.unit, this.state.value))
        this.safeSetState({unit: normalizedUnit, value: normalizedValue})
        this.saveChanges()
    }

    private handleUnitChange = (event: SelectChangeEvent<unknown>) => {
        const unit = event.target.value as string
        const value = this.state.value
        const denormalizedValue = this.denormalize(unit, value)
        let errorMessage = ''
        if (this.props.minValue && denormalizedValue < this.props.minValue) {
            const [minUnit, minValue] = this.normalize(this.props.minValue)
            errorMessage = `Minimum value is ${minValue}${minUnit}`
        } else if (this.props.maxValue && denormalizedValue > this.props.maxValue) {
            const [maxUnit, maxValue] = this.normalize(this.props.maxValue)
            errorMessage = `Maximum value is ${maxValue}${maxUnit}`
        }
        this.safeSetState({unit: unit, errorMessage: errorMessage})
    }

    private handleUnitBlur = () => {
        const [normalizedUnit, normalizedValue] = this.normalize(this.denormalize(this.state.unit, this.state.value))
        this.safeSetState({unit: normalizedUnit, value: normalizedValue})
        this.saveChanges()
    }

    private saveChanges = () => {
        if (this.state.errorMessage === '') {
            var saveErrorMessage = this.props.saveValue(this.denormalize(this.state.unit, this.state.value))
            if (typeof saveErrorMessage === 'string' && saveErrorMessage !== '') {
                this.safeSetState({errorMessage: saveErrorMessage})
            }
        }
    }
    
    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <DIV sx={Object.assign({
                display: 'inline-flex',
                width: '100%',
                padding: '6px 0px',
                textAlign: 'center',
                justifyContent: 'center'
            }, this.props.sx)}>
                <DIV sx={{
                    minWidth: this.props.labelWidth || '68px',
                    margin: '0px 12px',
                    lineHeight: '24px',
                }}>
                    {this.props.label}
                </DIV>
                <ExtraInfo reminder={this.state.errorMessage}>
                    <FormControl
                        error={this.state.errorMessage != ''}
                        variant='outlined'
                        sx={{
                            width: '100%',
                            margin: '2px 3px 2px 6px',
                            height: this.props.helperText ? '32px' : '20px',
                        }}
                    >
                        <StyledOutlinedInput
                            notched={false}
                            label=''
                            inputRef={this.textField}
                            value={this.state.value}
                            placeholder={this.props.placeholder}
                            onChange={this.handleValueChange}
                            onFocus={this.handleValueFocus}
                            onBlur={this.handleValueBlur}
                            onKeyDown={(event: React.KeyboardEvent) => { if (event.key == 'Enter' || event.key == 'Escape') this.textField.current.blur() }}
                        />
                        {this.props.helperText && 
                            <FormHelperText sx={{fontSize: '10px', lineHeight: '10px', margin: '4px 6px', whiteSpace: 'nowrap'}}>
                                {this.props.helperText}
                            </FormHelperText>
                        }
                    </FormControl>
                </ExtraInfo>
                <StyledSelect
                    value={this.state.unit}
                    onChange={this.handleUnitChange}
                    onBlur={this.handleUnitBlur}
                    SelectDisplayProps={{style: {padding: '3px 20px 3px 6px', minHeight: 'unset'}}}
                    MenuProps={{MenuListProps: {style: {paddingTop: '6px', paddingBottom: '7px'}}}}
                    sx={{margin: '2px 6px 2px 3px', height: '20px'}}
                    disabled={this.props.unitValues.length == 1}
                >
                    {this.props.unitValues.map(unitValue =>
                        <StyledMenuItem key={unitValue.unit} value={unitValue.unit}>
                            {unitValue.unit}
                        </StyledMenuItem>
                    )}
                </StyledSelect>
            </DIV>
        )
    }

    public componentDidMount = () => {
        this._isMounted = true
    }

    public componentWillUnmount = () => {
        this._isMounted = false
    }

    private safeSetState = (map: any) => {
		if (this._isMounted) {
			let update = false
			try {
				for (const key of Object.keys(map)) {
					if (JSON.stringify(map[key]) !== JSON.stringify((this.state as any)[key])) {
						update = true
						break
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
