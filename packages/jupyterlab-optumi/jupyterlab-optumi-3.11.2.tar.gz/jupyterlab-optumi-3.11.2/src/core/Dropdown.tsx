/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global, StyledSelect } from '../Global';

import { SxProps, Theme } from '@mui/system';
import { FormControl, FormHelperText, MenuItem, SelectChangeEvent } from '@mui/material';
import { withStyles } from '@mui/styles';

const StyledMenuItem = withStyles({
    root: {
        fontSize: 'var(--jp-ui-font-size1)',
        padding: '3px 3px 3px 6px',
        textAlign: 'start',
    }
}) (MenuItem)

interface IProps {
    sx?: SxProps<Theme>
    label?: string
    labelWidth?: string
    getValue: () => string
    saveValue: (value: string) => string | void
    values: {value: string, description: string, disabled?: boolean}[]
    helperText?: string
    onFocus?: (event: React.FocusEvent<HTMLInputElement>) => void
    onBlur?: (event: React.FocusEvent<HTMLInputElement>) => void
    disabled?: boolean
}

interface IState {
    value: string
}

export class Dropdown extends React.Component<IProps, IState> {
    private _isMounted = false

    constructor(props: IProps) {
        super(props);
        this.state = {
            value: this.props.getValue(),
        }
    }

    private handleValueChange = (event: SelectChangeEvent<unknown>) => {
        const value = event.target.value as string
        this.safeSetState({value: value})
        this.props.saveValue(value);
    }
    
    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <DIV sx={Object.assign({
                display: 'inline-flex',
                width: '100%',
                padding: '6px 0px',
                // textAlign: 'center',
                // justifyContent: 'center'
            }, this.props.sx)}>
                {this.props.label && <DIV sx={{
                    minWidth: this.props.labelWidth || '68px',
                    margin: '0px 12px',
                    lineHeight: '24px',
                }}>
                    {this.props.label}
                </DIV>}
                <FormControl
                    variant='outlined'
                    sx={{width: '100%', margin: '2px 6px', height: this.props.helperText ? '32px' : '20px'}}
                >
                    <StyledSelect
                        value={this.state.value}
                        onChange={this.handleValueChange}
                        SelectDisplayProps={{style: {padding: '1px 20px 1px 6px'}}}
                        MenuProps={{MenuListProps: {style: {paddingTop: '6px', paddingBottom: '6px'}}}}
                        sx={{width: '100%'}}
                        disabled={this.props.disabled}
                    >
                        {this.props.values.map(value =>
                            <StyledMenuItem key={value.value} value={value.value} disabled={value.disabled}>
                                {value.value + (value.description ? (': ' + value.description) : '')}
                            </StyledMenuItem>
                        )}
                    </StyledSelect>
                    {this.props.helperText && 
                        <FormHelperText sx={{fontSize: '10px', lineHeight: '10px', margin: '4px 6px', whiteSpace: 'nowrap'}}>
                            {this.props.helperText}
                        </FormHelperText>
                    }
                </FormControl>
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
