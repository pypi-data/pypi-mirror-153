/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global } from '../Global';

import { SxProps, Theme } from '@mui/system';
import {
    Slider as OtherSlider,
    darken,
    Paper,
    OutlinedInput,
    InputLabel,
    FormControl,
    lighten,
    InputAdornment,
} from '@mui/material';
import { withStyles } from '@mui/styles';

interface IProps {
    minValue: number
    maxValue: number
    getValue: () => number
    saveValue: (value: number) => void
    color: string
    sx?: SxProps<Theme>

    // Labeling
    label?: string
    labelWidth?: string
    styledUnit?: (value: number) => string
    styledValue?: (value: number) => string
    // If we have different units, we need to be able to convert text back to the correct value
    unstyledValue?: (value: number, unit: string) => number
    showUnit?: boolean

    // Resource Cap Slider
    scale?: (x: number) => number
    unscale?: (x: number) => number
    marks?: any[]
    step?: any
    alwaysDisplayUnit?: boolean
}

interface IState {
    value: number,
    typing: boolean,
    hovered: boolean,
    weGotADot: string,
}

const enableThumbText = false;
const alwaysShowValue = false;

var retrievingPreview: boolean = false;
var updatePreviewAgain: boolean = false;
var latestValue: number;

export class Slider extends React.Component<IProps, IState> {
    _isMounted = false;
    textField: React.RefObject<HTMLInputElement>

    StyledSlider: any;
    StyledValueLabel: any;
    StyledOutlinedInput: any;
    StyledInputLabel: any;

    min: number;
    max: number;

    static defaultProps: Partial<IProps> = {
        styledUnit: (value: number) => { return '' },
        styledValue: (value: number) => { return value == -1 ? 'unsp' : value.toFixed() },
        scale: (value: number) => { return value },
        unscale: (value: number) => { return value },
    }

    public constructor(props: IProps) {
        super (props);
        this.textField = React.createRef();
        this.StyledSlider = this.getStyledSlider();
        this.StyledValueLabel = this.getStyledValueLabel();
        this.StyledOutlinedInput = this.getStyledOutlinedInput();
        this.StyledInputLabel = this.getStyledInputLabel();
        this.state = {
            value: this.props.getValue(),
            typing: false,
            hovered: false,
            weGotADot: '',
        }
        this.min = this.props.marks ? this.props.marks[0].value : this.props.minValue;
        this.max = this.props.marks ? this.props.marks[this.props.marks.length-1].value : this.props.maxValue;
    }

    private getStyledSlider = () => {
        const isLightMode: boolean = Global.themeManager == undefined || Global.themeManager.isLight(Global.themeManager.theme)
        return withStyles({
            root: {
                height: '12px',
                width: '100%',
                margin: '0px 6px',
                padding: '6px 0px',
                overflow: 'hidden', // Specifically for double width thumb
            },
            thumb: { // hidden
                height: '12px',
                width: '200%', // So we show the label any time the slider is hovered
                transform: 'translate(-50%, calc(25% + 2px))',
                backgroundColor: 'transparent',
                padding: '0px',
                '&:focus, &:hover, &:active': {
                    boxShadow: 'none',
                },
                '&::after': {
                    left: -6,
                    top: -6,
                    right: -6,
                    bottom: -6,
                },
            },
            track: { // left side
                height: '12px',
                color: this.props.color,
                boxSizing: 'border-box',
                border: "1px solid " + darken(this.props.color, 0.25),
                borderRadius: '4px',
            },
            rail: { // right side
                height: '12px',
                width: '100%',
                opacity: 1,
                color: (isLightMode ? '#eeeeee' : '#424242'),
                boxSizing: 'border-box',
                border: '1px solid ' + (isLightMode ? darken('#eeeeee', 0.25) : lighten('#424242', 0.25)),
                borderRadius: '4px',
            },
            mark: {
                marginLeft: 0,
                height: 4,
                width: 1,
                backgroundColor: 'currentColor',
                opacity: 0,
            },
            markActive: {
                marginLeft: -1,
                height: 4,
                width: 2,
                backgroundColor: 'currentColor',
                opacity: 0,
            },
        }) (OtherSlider);
    }

    private getStyledValueLabel = () => {
        return withStyles({
            root: {
                padding: '0px 3px',
                position: 'absolute',
                color: '#ffffff',
                whiteSpace: 'nowrap',
                fontWeight: 'bold',
                backgroundColor: this.props.color,
                border: "1px solid " + darken(this.props.color, 0.25),
            },
        }) (Paper);
    }

    private getStyledOutlinedInput = () => {
        return withStyles({
            input: {
                fontSize: '12px',
                padding: '6px 0px 3px 6px',
            },
            adornedEnd: {
                paddingRight: '6px',
            },
        }) (OutlinedInput);
    }

    private getStyledInputLabel = () => {
        return withStyles({
            root: {
                fontSize: '12px',
            },
            outlined: {
                transform: 'translate(6px, 6px) scale(1)',
                '&$shrink': {
                    transform: 'translate(10px, -4.5px) scale(0.8)',
                }
            },
            formControl: {
                transform: 'translate(6px, 6px) scale(1)',
            },
            shrink: {
                transform: 'translate(10px, -4.5px) scale(0.8)',
            },
        }) (InputLabel);
    }

    private ValueLabelComponent = (props: any) => {
        var value = this.props.scale != undefined ? this.props.scale(props.value) : props.value;
        var fromLeft = 100 * props.value / this.max;
        return (
            <>
                <this.StyledValueLabel sx={{
                    display: props.open && this.props.showUnit ? 'inline-block' : 'none',
                    left: fromLeft + '%',
                    transform: 'translate(-' + fromLeft + '%, -25%)',
                }}>
                    {value}
                </this.StyledValueLabel>
                {props.children}
            </>
        );
    }

    private handleTextBoxChange = async (event: any) => {
        var value: string = event.target.value;
        var unit = this.props.styledUnit(this.state.value);
        /// Do special character checks upfront before length checks
        if ( value.length == 5 && value.startsWith('unsp')) {
            // If the value is unsp and the user types a number, change it to the number
            value = value.replace('unsp', '');
        } else if (value.includes('u')) {
            // Handle character change to unspecified
            this.safeSetState({ value: this.min, weGotADot: '' });
            this.slowDownSaveValue(this.min);
            return; // We are done here, do not go on
        } else if (value != '' && value.search(/[a-z]/i) != -1) {
            for (let c of value) {
                if (c.match(/[a-z]/i)) {
                    unit = c;
                    value = value.replace(c, '');
                    break;
                }
            }
        }
        
        if (value.endsWith('.') || value.endsWith('.0')/* || value.endsWith('.00')*/) {
            this.safeSetState({ weGotADot: value });
            return; // We do not want to save this value
        }
        this.parseTextAndSetValue(value, unit);
    }

    private handleChange = async (event: React.ChangeEvent<{}>, newValue: number | number[]) => {
		if (newValue instanceof Array) {
			// This is invalid
		} else {
            var cappedValue = Math.min(Math.max(this.min, newValue), this.max);
            this.safeSetState({ value: cappedValue, weGotADot: '' });
            this.slowDownSaveValue(cappedValue);
        }
    }

    private handleChangeCommitted = async (event: React.ChangeEvent<{}>, newValue: number | number[]) => {
		if (newValue instanceof Array) {
			// This is invalid
		} else {
            var cappedValue = Math.min(Math.max(this.min, newValue), this.max);
            this.safeSetState({ value: cappedValue, weGotADot: '' });
            this.props.saveValue(cappedValue);
        }
    }

    private formatTextForSmallBox(value: string): string {
        var ret = value;
        // Turn 1234 into 123, turn 1.234 into 1.23
        if (ret != 'unsp' && ret.length > length) ret = ret.substr(0, value.includes('.') ? 4 : 3);
        // turn 1.00 into 1. 1.50 into 1.5, 15.0 into 15.
        while (ret.includes('.') && ret.endsWith('0')) ret = ret.substr(0, ret.length-1)
        // Turn 1. into 1
        if (ret.endsWith('.')) ret = ret.substr(0, ret.length-1)
        return ret;
    }

    private delay = (ms: number) => { return new Promise(resolve => setTimeout(resolve, ms)) }
    private slowDownSaveValue = (newValue: number, bypassLimiter?: boolean) => {
        if (newValue != null) latestValue = newValue;
        if (bypassLimiter || !retrievingPreview) {
            retrievingPreview = true;
            this.delay(100).then(() => {
                this.props.saveValue(latestValue);
                if (updatePreviewAgain) {
                    updatePreviewAgain = false;
                    this.slowDownSaveValue(null, true);
                } else {
                    retrievingPreview = false;
                }
            }, () => {
                retrievingPreview = false;
            });
        } else {
            updatePreviewAgain = true;
        }
	}
 
    private parseTextAndSetValue(value: string, unit: string) {
        if (!isNaN(+value)) {
            // Only allow the user to specify up to 2 decimal points
            if (value.includes('.') && value.split('.')[1].length > 2) {
                return;
            }
            var unscaledValue = this.props.unscale(this.props.unstyledValue ? this.props.unstyledValue(+value, unit) : +value)
            if (unscaledValue < this.min) {
                this.safeSetState({ value: this.min, weGotADot: '' });
                this.slowDownSaveValue(this.min);
            } else if (unscaledValue > this.max) {
                this.safeSetState({ value: this.max, weGotADot: '' });
                this.slowDownSaveValue(this.max);
            } else {
                this.safeSetState({ value: unscaledValue, weGotADot: '' });
                this.slowDownSaveValue(unscaledValue);
            }
        }
    }

    private startTyping = () => {
        this.safeSetState({typing: true})
    }

    private stopTyping = () => {
        if (this.state.weGotADot != '') {
            // Save the value with a dot, since the user is no longer typing
            this.parseTextAndSetValue(this.state.weGotADot, this.props.styledUnit(this.state.value));
            
        }
        this.safeSetState({typing: false})
    }

    private startHover = () => {
        this.safeSetState({hovered: true})
    }

    private stopHover = () => {
        this.safeSetState({hovered: false})
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        var showValue: boolean = alwaysShowValue || this.state.hovered || this.state.typing || this.props.alwaysDisplayUnit;
        const fontFamily = getComputedStyle(document.body).getPropertyValue('--jp-ui-font-family').trim()
        return this.max == 0 ? (<></>) : (
            <DIV
                sx={Object.assign({display: 'inline-flex', width: '100%'}, this.props.sx)}
                onMouseOver={this.startHover}
                onMouseOut={this.stopHover}
            >
                <this.StyledSlider
                    sx={{position: 'relative'}}
                    onChange={this.handleChange}
                    onChangeCommitted={this.handleChangeCommitted}
                    min={0}
                    max={this.max}
                    value={this.state.value}
                    ValueLabelComponent={enableThumbText && (this.props.alwaysDisplayUnit || this.state.hovered) ? this.ValueLabelComponent : undefined}
                    valueLabelDisplay={enableThumbText && (this.props.alwaysDisplayUnit || this.state.hovered) ? 'on' : 'off'}
                    marks={this.props.marks}
                    step={this.props.step}
                />
                <FormControl
                    variant='outlined'
                    sx={{maxWidth: this.props.labelWidth || '68px', minWidth: this.props.labelWidth || '68px', margin: '0px 6px', display: showValue ? 'block' : 'none'}}
                >
                    <this.StyledInputLabel>
                        {this.props.label}
                    </this.StyledInputLabel>
                    <this.StyledOutlinedInput
                        inputRef={this.textField}
                        value={this.state.weGotADot != '' ? this.state.weGotADot : this.formatTextForSmallBox(this.props.styledValue(this.props.scale(this.state.value)))}
                        labelWidth={Global.getStringWidth(this.props.label, '12px ' + fontFamily) - 8}
                        onChange={this.handleTextBoxChange}
                        onFocus={this.startTyping}
                        onBlur={this.stopTyping}
                        onKeyDown={(event: React.KeyboardEvent) => { if (event.key == 'Enter' || event.key == 'Escape') this.textField.current.blur() }}
                        endAdornment={<InputAdornment position="end" disableTypography sx={{fontSize: '12px', margin: '0px', height: '12px', paddingTop: '3px'}}>{this.props.styledUnit(this.state.value)}</InputAdornment>}
                    />
                </FormControl>
                <DIV sx={{
                    minWidth: this.props.labelWidth || '68px',
                    lineHeight: '24px',
                    textAlign: 'center',
                    margin: '0px 6px',
                    display: !showValue ? 'block' : 'none'
                }}>
                    {this.props.label}
                </DIV>
            </DIV>
        )
    }

    private handleMetadataChange = () => this.safeSetState({ value: this.props.getValue(), weGotADot: '' })
    private handleThemeChange = () => {
        this.StyledSlider = this.getStyledSlider();
        this.StyledValueLabel = this.getStyledValueLabel();
        this.StyledOutlinedInput = this.getStyledOutlinedInput();
        this.StyledInputLabel = this.getStyledInputLabel();
        if (this._isMounted) this.forceUpdate();
    }

    // Will be called automatically when the component is mounted
	public componentDidMount = () => {
		this._isMounted = true;
        Global.metadata.getMetadataChanged().connect(this.handleMetadataChange);
        Global.themeManager.themeChanged.connect(this.handleThemeChange);
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
		Global.metadata.getMetadataChanged().disconnect(this.handleMetadataChange);
        Global.themeManager.themeChanged.disconnect(this.handleThemeChange);
		this._isMounted = false;
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
}
