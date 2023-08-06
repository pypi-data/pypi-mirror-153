/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global } from '../../Global';

import { SxProps, Theme } from '@mui/system';
import { Input } from '@mui/material';
import { withStyles } from '@mui/styles';
import { Edit } from '@mui/icons-material';

const StyledInput = withStyles({
    root: {
        fontSize: 'var(--jp-ui-font-size1)', 
        lineHeight: '1', 
        fontWeight: 'normal', 
        width: '200px',
    },
    input: {
        padding: '2px 0px',
    },
    underline: {
        '&:hover:before': {
            borderBottomWidth: '1px !important',
        },
        '&:before': {
            borderBottomWidth: '0px',
        },
    },
})(Input);

interface IProps {
    getValue: () => string
    saveValue: (value: string) => void
    placeholder: string
    sx?: SxProps<Theme>,
}

interface IState {
    value: string
    editing: boolean
}

export class AnnotationInput extends React.Component<IProps, IState> {
    private _isMounted = false;
    textField: React.RefObject<HTMLInputElement>

    constructor(props: IProps) {
        super(props);
        this.textField = React.createRef();
        this.state = {
            value: this.props.getValue(),
            editing: false,
        }
    }
    
    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const fontSize = getComputedStyle(document.documentElement).getPropertyValue('--jp-ui-font-size1').trim()
        const fontFamily = getComputedStyle(document.documentElement).getPropertyValue('--jp-ui-font-family').trim()
        return (
            <DIV sx={{position: 'relative', display: 'inline-flex'}}>
                <StyledInput
                    inputRef={this.textField}
                    value={this.state.value}
                    onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                        const value = event.target.value;
                        this.safeSetState({ value: value })
                    }}
                    onKeyDown={(e: React.KeyboardEvent<HTMLInputElement>) => {
                        if (e.key === 'Enter') {
                            this.textField.current.blur();
                        }
                    }}
                    onBlur={() => this.props.saveValue(this.state.value)}
                    placeholder={this.props.placeholder}
                />
                 <Edit sx={{opacity: this.state.value == '' ? 0.5 : 0, height: '12px', width: '12px', margin: '4px', position: 'absolute', left: Math.min(Global.getStringWidth(this.state.value == "" ? this.props.placeholder : this.state.value, fontSize + " " + fontFamily), 200) + 'px' }} />
            </DIV>
        )
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
}
