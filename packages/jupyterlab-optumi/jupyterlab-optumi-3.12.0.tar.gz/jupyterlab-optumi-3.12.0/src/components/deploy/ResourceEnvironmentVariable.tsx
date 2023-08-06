/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { DIV, Global } from '../../Global';

import { IconButton } from '@mui/material';

import { Colors } from '../../Colors';

import Terminal from '@mui/icons-material/Terminal';
import Close from '@mui/icons-material/Close';
import { EnvironmentVariableConfig } from '../../models/IntegrationConfig';

interface EVProps {
    environmentVariable: EnvironmentVariableConfig,
    handleFileDelete: () => void,
    noLongerExists?: boolean,
}

interface EVState {
    hovering: boolean,
}

export class ResourceEnvironmentVariable extends React.Component<EVProps, EVState> {
    _isMounted: boolean = false

    constructor(props: EVProps) {
        super(props)
        this.state = {
            hovering: false,
        }
    }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <DIV
                sx={{display: 'flex', width: '100%', position: 'relative'}}
                onMouseOver={() => {
                    this.safeSetState({hovering: true})
                }}
                onMouseOut={() => {
                    this.safeSetState({hovering: false})
                }}
            >
                <DIV sx={{
                    position: 'absolute',
                    right: '-10px',
                    display: 'inline-flex',
                    background: 'var(--jp-layout-color1)',
                    opacity: this.state.hovering ? '1' : '0',
                    transition: Global.easeAnimation,
                }}>
                    <IconButton
                        size='large'
                        onClick={this.props.handleFileDelete}
                        sx={{
                            width: '22px',
                            height: '22px',
                            padding: '0px',
                            position: 'relative',
                            display: 'inline-block',
                        }}
                    >
                        <Close sx={{position: 'relative', width: '16px', height: '16px'}} />
                    </IconButton>
                </DIV>
                <DIV
                    sx={{
                        width: '100%',
                        fontSize: '12px',
                        lineHeight: '14px',
                        padding: '3px 6px 3px 6px',
                        display: 'inline-flex'
                    }}
                >   
                    <Terminal
                        sx={Object.assign({
                            width: '16px',
                            height: '16px',
                            display: 'block',
                            margin: '0px 6px 0px 0px',
                        })}
                    />
                    <DIV
                        sx={{
                            margin: 'auto 0px',
                            overflow: 'hidden', 
                            textOverflow: 'ellipsis', 
                            whiteSpace: 'nowrap',
                            direction: 'rtl',
                            color: this.props.noLongerExists ? Colors.ERROR : ''
                        }}
                    >
                        {this.props.environmentVariable.name + (this.props.noLongerExists ? ' (no longer exists)' : '')}
                    </DIV>
                </DIV>
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

    public shouldComponentUpdate = (nextProps: EVProps, nextState: EVState): boolean => {
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
