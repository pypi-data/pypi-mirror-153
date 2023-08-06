/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global, SPAN } from '../Global';

import { SxProps, Theme } from '@mui/system';
import { Button, OutlinedInput, FormControl, InputLabel, InputAdornment, IconButton, FormHelperText } from '@mui/material';
import { withStyles } from '@mui/styles';
import { Close as CloseIcon, Done as DoneIcon, Visibility as VisibilityIcon, VisibilityOff as VisibilityOffIcon, Lock as LockIcon } from '@mui/icons-material';

import ExtraInfo from '../utils/ExtraInfo';

interface IProps<T> {
    sx?: SxProps<Theme>
    label?: string
    labelWidth?: string
    getValue: () => T
    saveValue: (value: T) => string | void
    editPressRequired?: boolean
    editPopup?: JSX.Element
    disabled?: boolean
    disabledMessage?: string
    password?: boolean
    placeholder?: string
    styledUnitValue?: (value: T) => string
    unstyleUnitValue?: (value: string) => T
    minValue?: T
    maxValue?: T
    helperText?: string
    helperLink?: {link: string, text: string}
    onFocus?: (event: React.FocusEvent<HTMLInputElement>) => void
    onBlur?: (event: React.FocusEvent<HTMLInputElement>) => void
    multiline?: boolean
    minLines?: number
    required?: boolean
}

interface IState<T> {
    value: T
    textValue: string
    editing: boolean
    invalidTextMessage: string
    hovered: boolean
    hidePassword: boolean
}

export class TextBox<T> extends React.Component<IProps<T>, IState<T>> {
    private _isMounted = false

    StyledOutlinedInput: any
    StyledInputLabel: any;
    textField: React.RefObject<HTMLInputElement>

    static defaultProps: Partial<IProps<any>> = {
        styledUnitValue: (value: any) => { return value.toString() },
    }

    constructor(props: IProps<T>) {
        super(props);
        this.StyledOutlinedInput = this.getStyledOutlinedInput();
        this.StyledInputLabel = this.getStyledInputLabel();
        this.textField = React.createRef();
        const value: any = this.props.getValue();
        this.state = {
            value: value,
            textValue: this.props.styledUnitValue(value),
            editing: false,
            hovered: false,
            invalidTextMessage: '',
            hidePassword: true,
        }
    }

    private getStyledOutlinedInput = () => {
        return withStyles({
            root: {
                padding: '0px',
            },
            input: {
                lineHeight: '14px',
                fontSize: '12px',
                padding: '3px 6px 3px 6px',
                height: '1.1876em',
            },
            adornedEnd: {
                paddingRight: '0px',
            },
        }) (OutlinedInput);
    }

    private getStyledInputLabel = () => {
        return withStyles({
            root: {
                fontSize: '12px',
                backgroundColor: 'var(--jp-layout-color1)',
                padding: '1px 2px',
            },
            outlined: {
                transform: 'translate(6px, 6px) scale(1)',
                '&$shrink': {
                    transform: 'translate(9px, -6px) scale(0.8)',
                }
            },
            formControl: {
                transform: 'translate(6px, 6px) scale(1)',
            },
            shrink: {
                transform: 'translate(9px, -6px) scale(0.8)',
            },
        }) (InputLabel);
    }

    // This turns the textbox red if it is not a valid value determined by the unstyle function
    private handleChange = async (event: React.FormEvent<HTMLInputElement>) => {
        const value = event.currentTarget.value
        this.safeSetState({ textValue: value });
        if (this.props.unstyleUnitValue == undefined) {
            if (typeof value === 'number') {
                if (this.props.minValue !== undefined && value < this.props.minValue) {
                    this.safeSetState({ invalidTextMessage: 'Minimum value is ' + this.props.styledUnitValue(this.props.minValue) })
                } else if (this.props.maxValue !== undefined && value > this.props.maxValue) {
                    this.safeSetState({ invalidTextMessage: 'Maximum value is ' + this.props.styledUnitValue(this.props.maxValue) })
                } else {
                    if (!this.props.editPressRequired) this.safeSetState({ value: value as unknown as T, invalidTextMessage: '' });
                }
            } else {
                if (!this.props.editPressRequired) this.safeSetState({ value: value as unknown as T, invalidTextMessage: '' });
            }
        } else {
            var unstyledValue: any = this.props.unstyleUnitValue(value);
            if (!isNaN(unstyledValue)) {
                if (this.props.minValue !== undefined && unstyledValue < this.props.minValue) {
                    this.safeSetState({ invalidTextMessage: 'Minimum value is ' + this.props.styledUnitValue(this.props.minValue) })
                } else if (this.props.maxValue !== undefined && unstyledValue > this.props.maxValue) {
                    this.safeSetState({ invalidTextMessage: 'Maximum value is ' + this.props.styledUnitValue(this.props.maxValue) })
                } else {
                    if (!this.props.editPressRequired) this.safeSetState({ value: unstyledValue as unknown as T, invalidTextMessage: '' });
                }
            } else {
                this.safeSetState({ invalidTextMessage: 'Invalid format' })
            }
        }
    }

    private startEdit = () => {
        this.safeSetState({editing: true})
        this.textField.current.disabled = false
        this.textField.current.focus()
    }

    private discardChanges = () => {
        this.safeSetState({
            editing: false,
            textValue: this.props.styledUnitValue(this.state.value),
            invalidTextMessage: '',
        })
    }

    // If save clicked, or if unfocused if save not required. Saves value if it is a valid value determined by the unstyle function or lack thereof
    private saveChanges = () => {
        var invalidTextMessage: string = '';
        var unstyledValue: any = this.state.textValue;
        if (this.props.unstyleUnitValue != undefined) {
            unstyledValue = this.props.unstyleUnitValue(this.state.textValue);
            if (isNaN(unstyledValue)) {
                invalidTextMessage = 'Invalid format'
            } else if (this.props.minValue !== undefined && unstyledValue < this.props.minValue) {
                invalidTextMessage = 'Minimum value is ' + this.props.styledUnitValue(this.props.minValue)
            } else if (this.props.maxValue !== undefined && unstyledValue > this.props.maxValue) {
                invalidTextMessage = 'Maximum value is ' + this.props.styledUnitValue(this.props.maxValue)
            }
        }
        this.safeSetState({invalidTextMessage: invalidTextMessage});
        if (invalidTextMessage == '') {
            this.safeSetState({editing: false, value: unstyledValue, textValue: this.props.styledUnitValue(unstyledValue)})
            var saveReturn = this.props.saveValue(unstyledValue)
            this.safeSetState({invalidTextMessage: saveReturn == undefined ? '' : saveReturn as string})
        }
    }

    private startHover = () => {
        this.safeSetState({hovered: true})
    }

    private stopHover = () => {
        this.safeSetState({hovered: false})
    }

    private renderPopupButton = (render: boolean): JSX.Element => {
        return this.props.editPopup !== undefined ? React.cloneElement(this.props.editPopup, {
            style: {
                display: render ? 'flex' : 'none',
            },
            onOpen: () => {
                this.safeSetState({editing: true})
            },
            onClose: () => {
                this.safeSetState({hovered: false, editing: false})
            }
        }) : <></>
    }

    private renderEditButton = (render: boolean): JSX.Element => {
        return (
            <Button
                onClick={this.startEdit}
                sx={{
                    display: render ? 'flex' : 'none',
                    width: '100%',
                    minWidth: '0px',
                    paddingTop: '6px',
                }}
                variant="outlined"
                color='secondary'
            >
                Edit
            </Button>
        )
    }

    private renderConfirmCancelButtons = (render: boolean): JSX.Element => {
        return (
            <>
                <Button
                    onClick={this.discardChanges}
                    variant="outlined"
                    color="primary"
                    sx={{
                        display: render ? 'flex' : 'none',
                        width: '50%',
                        minWidth: '0px',
                        paddingTop: '6px',
                        borderTopRightRadius: '0px',
                        borderBottomRightRadius: '0px',
                        borderRight: '0px',
                    }}
                >
                    <CloseIcon sx={{width: '20px', height: '20px'}} />
                </Button>
                <Button
                    onClick={this.saveChanges}
                    variant="outlined"
                    color="primary"
                    sx={{
                        display: render ? 'flex' : 'none',
                        width: '50%',
                        minWidth: '0px',
                        paddingTop: '6px',
                        borderTopLeftRadius: '0px',
                        borderBottomLeftRadius: '0px',
                    }}
                >
                    <DoneIcon sx={{width: '20px', height: '20px'}} />
                </Button>
            </>
        )
    }

    private renderLabelOverButton = (render: boolean): JSX.Element => {
        return (
            <this.StyledInputLabel shrink={true} sx={{display: render ? 'flex' : 'none', position: 'absolute'}}>
                {this.props.label}
            </this.StyledInputLabel>
        )
    }

    private renderLabel = (render: boolean): JSX.Element => {
        return (
            <SPAN sx={{display: render ? 'inline' : 'none', width: '100%', color: !(this.props.disabledMessage == undefined || this.props.disabledMessage == '') ? 'var(--jp-ui-font-color3)' : 'var(--jp-ui-font-color1)'}}>
                {this.props.label + (this.props.required ? '*' : '')}
            </SPAN>
        )
    }

    private handleFocus = (event: React.FocusEvent<HTMLInputElement>) => {
        if (this.props.onFocus) {
            this.props.onFocus(event)
        }
    }

    private handleBlur = (event: React.FocusEvent<HTMLInputElement>) => {
        if (this.props.onBlur) {
            this.props.onBlur(event)
        }
        if (!(this.props.editPressRequired || this.props.editPopup !== undefined)) {
            this.saveChanges()
        }
    }
    
    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        var showPopupButton = false, showEditButton = false, showConfirmCancelButtons = false, showLabel = false
        // There should never be an if without an else. That could lead to nothing being rendered to the left of the textbox
        if (this.props.editPopup === undefined && !this.props.editPressRequired) {
            showLabel = true
        } else if (!this.state.hovered && !this.state.editing) {
            showLabel = true
        } else {
            if (this.props.editPopup !== undefined) {
                showPopupButton = true
            } else {
                if (this.state.editing) {
                    showConfirmCancelButtons = true
                } else {
                    showEditButton = true
                }
            }
        }
        return (
            <DIV
                sx={Object.assign({display: 'inline-flex', width: '100%', padding: '6px 0px'}, this.props.sx)}
                onMouseOver={this.startHover}
                onMouseOut={this.stopHover}
            >
                {this.props.label && (
                    <DIV sx={{
                        display: 'flex',
                        position: 'relative',
                        minWidth: this.props.labelWidth || '68px',
                        maxWidth: this.props.labelWidth || '68px',
                        height: '24px',
                        margin: '0px 12px',
                        lineHeight: '24px',
                        // textAlign: 'center',
                    }}>
                        {this.renderLabel(showLabel)}
                        {this.renderPopupButton(showPopupButton)}
                        {this.renderEditButton(showEditButton)}
                        {this.renderConfirmCancelButtons(showConfirmCancelButtons)}
                        {this.renderLabelOverButton(!showLabel)}
                    </DIV>
                )}
                <ExtraInfo reminder={this.state.invalidTextMessage}>
                    <FormControl
                        error={this.state.invalidTextMessage != ''}
                        variant='outlined'
                        sx={{width: '100%', margin: '2px 6px', height: this.props.multiline ? '' : (this.props.helperText ? '32px' : '20px')}}
                    >
                        <this.StyledOutlinedInput
                            size='small'
                            notched={false}
                            label=''
                            inputRef={this.textField}
                            value={this.state.textValue}
                            placeholder={this.props.placeholder}
                            disabled={
                                this.props.disabled ||
                                (!(this.props.disabledMessage == undefined || this.props.disabledMessage == '') ||
                                (this.props.editPressRequired && !this.state.editing) ||
                                this.props.editPopup !== undefined)
                            }
                            onChange={this.handleChange}
                            onKeyDown={(event: React.KeyboardEvent) => { if ((!this.props.multiline && event.key == 'Enter') || event.key == 'Escape') this.textField.current.blur() }}
                            onFocus={this.handleFocus}
                            onBlur={this.handleBlur}
                            type={this.props.password && this.state.hidePassword ? 'password' : 'text'}
                            multiline={this.props.multiline}
                            required={this.props.required}
                            rows={(() => {
                                const lines = this.state.textValue.split('\n').length;
                                if (this.props.minLines && lines < this.props.minLines) return this.props.minLines;
                                return lines;
                            })()}
                            endAdornment={
                                (this.props.disabled || !(this.props.disabledMessage == undefined || this.props.disabledMessage == '')) ? (
                                    // <ExtraInfo reminder={this.props.disabledMessage}>
                                        <InputAdornment position="end" sx={{height: '20px', margin: '0px 3px 0px 0px'}}>
                                            <IconButton  size='large' disabled sx={{padding: '3px 3px 3px 0px'}}>
                                                <LockIcon sx={{width: '14px', height: '14px'}} />
                                            </IconButton>
                                        </InputAdornment>
                                    // </ExtraInfo>
                                ) : this.props.password && (
                                    // <ExtraInfo reminder={this.state.hidePassword ? 'Show Password' : 'Hide Password'}>
                                        <InputAdornment position="end" sx={{height: '20px', margin: '0px 3px 0px 0px'}}>
                                            <IconButton
                                                size='large'
                                                onClick={() => this.safeSetState({hidePassword: !this.state.hidePassword})}
                                                sx={{padding: '3px 3px 3px 0px'}}
                                            >
                                                {this.state.hidePassword ? (
                                                    <VisibilityOffIcon sx={{width: '14px', height: '14px'}} /> 
                                                ) : (
                                                    <VisibilityIcon sx={{width: '14px', height: '14px'}} />
                                                )}
                                            </IconButton>
                                        </InputAdornment>
                                    // </ExtraInfo>
                                )
                            }
                        />
                        {this.props.helperText && 
                            <FormHelperText sx={{fontSize: '10px', lineHeight: '10px', margin: '4px 6px', whiteSpace: 'nowrap', display: 'inline-flex'}}>
                                {this.props.helperText}
                                {this.props.helperLink && (
                                    <a href={this.props.helperLink.link} target="_blank" style={{flexGrow: 1, textAlign: 'end', fontStyle: 'italic'}}>
                                        {this.props.helperLink.text}
                                    </a>
                                )}
                            </FormHelperText>
                        }
                    </FormControl>
                </ExtraInfo>
            </DIV>
        );
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

    public shouldComponentUpdate = (nextProps: IProps<any>, nextState: IState<any>): boolean => {
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
