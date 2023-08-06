/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { DIV, Global } from '../../Global';

import { IconButton } from '@mui/material';
import { Close as CloseIcon } from '@mui/icons-material';

import DataConnectorDirListingItemIcon from './IntegrationBrowser/IntegrationDirListingItemIcon';
import { Colors } from '../../Colors';
import { DataConnectorConfig } from '../../models/IntegrationConfig';

interface RDCProps {
    dataConnector: DataConnectorConfig,
    handleFileDelete: () => void,
    noLongerExists?: boolean,
}

interface RDCState {
    hovering: boolean,
}

export class ResourceDataConnector extends React.Component<RDCProps, RDCState> {
    _isMounted: boolean = false

    constructor(props: RDCProps) {
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
                        <CloseIcon sx={{position: 'relative', width: '16px', height: '16px'}} />
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
                    <DataConnectorDirListingItemIcon
                        dataService={this.props.dataConnector.dataService}
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
                        {this.props.dataConnector.name + (this.props.noLongerExists ? ' (no longer exists)' : '')}
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

    public shouldComponentUpdate = (nextProps: RDCProps, nextState: RDCState): boolean => {
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
