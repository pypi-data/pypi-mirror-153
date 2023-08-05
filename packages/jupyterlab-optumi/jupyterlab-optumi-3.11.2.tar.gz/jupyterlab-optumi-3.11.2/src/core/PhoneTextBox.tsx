/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global, SPAN } from '../Global';

import { SxProps, Theme } from '@mui/system';

// import ExtraInfo from '../utils/ExtraInfo';

import ReactPhoneInput from 'react-phone-input-2';
import 'react-phone-input-2/lib/style.css';
import libphonenumber from 'google-libphonenumber';

interface IProps {
    sx?: SxProps<Theme>
    label?: string
    labelWidth?: string
    getValue: () => string
    saveValue: (value: string) => string | void
    disabled?: boolean
    disabledMessage?: string
    onFocus?: (event: React.FocusEvent<HTMLInputElement>) => void
    onBlur?: (event: React.FocusEvent<HTMLInputElement>) => void
    validOnBlur?: (valid: boolean) =>  void
}

interface IState {
    value: string
    invalidTextMessage: string
    editing: boolean
    hovered: boolean
    hidePassword: boolean
}

export class PhoneTextBox extends React.Component<IProps, IState> {
    private _isMounted = false

    constructor(props: IProps) {
        super(props);
        const value: any = this.props.getValue().replace('+', '');
        this.state = {
            value: value == '' ? '1' : value,
            invalidTextMessage: '',
            editing: false,
            hovered: false,
            hidePassword: true,
        }
    }

    // This turns the textbox red if it is not a valid value determined by the unstyle function
    private handleChange = async (value: string, data: any, event: React.ChangeEvent<HTMLInputElement>, formattedValue: string) => {
        this.safeSetState({ value: value, invalidTextMessage: '' });
    }

    // Saves value if it is a valid value
    private saveChanges = () => {
        var value = this.state.value;
        var invalid = false;
        if (value == "" || value == "1") {
            this.props.saveValue("")
        } else {
            try {
                const phoneUtil = libphonenumber.PhoneNumberUtil.getInstance();
                if (phoneUtil.isValidNumber(phoneUtil.parse('+' + value, 'US'))) {
                    this.safeSetState({editing: false, value: value})
                    this.props.saveValue('+' + value)
                } else {
                    invalid = true;
                }
            } catch (err) {
                invalid = true;
            }
        }
        if (invalid) {
            this.safeSetState({invalidTextMessage: 'Invalid phone number'});
        }
        if (this.props.validOnBlur) {
            this.props.validOnBlur(!invalid);
        }
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
        if (this.state.value == '') this.setState({ value: '1' })
        this.saveChanges()
    }
    
    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <DIV
                sx={Object.assign({display: 'inline-flex', width: '100%', padding: '6px 0px'}, this.props.sx)}
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
                        <SPAN sx={{display: 'inline', width: '100%', color: !(this.props.disabledMessage == undefined || this.props.disabledMessage == '') ? 'var(--jp-ui-font-color3)' : 'var(--jp-ui-font-color1)'}}>
                            {this.props.label}
                        </SPAN>
                    </DIV>
                )}
                {/* <ExtraInfo reminder={this.state.invalidTextMessage}> */}
                    <ReactPhoneInput
                        disabled={this.props.disabled}
                        value={'+' + this.state.value}
                        country={'us'}
                        onChange={this.handleChange}
                        preferredCountries={['us']}
                        containerStyle={{margin: 'auto 0px auto 6px'}}
                        inputStyle={{height:'20.25px', width: '100%', background: 'var(--jp-layout-color1)', color: 'var(--jp-ui-font-color0)'}}
                        buttonStyle={{height: '20.25px', background: 'var(--jp-layout-color1)', color: 'var(--jp-ui-font-color0)'}}
                        dropdownStyle={{background: 'var(--jp-layout-color1)', color: 'var(--jp-ui-font-color0)'}}
                        searchStyle={{background: 'var(--jp-layout-color1)', color: 'var(--jp-ui-font-color0)'}}
                        onFocus={this.handleFocus}
                        onBlur={this.handleBlur}
                        isValid={this.state.invalidTextMessage == ''}
                    />
                {/* </ExtraInfo> */}
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

