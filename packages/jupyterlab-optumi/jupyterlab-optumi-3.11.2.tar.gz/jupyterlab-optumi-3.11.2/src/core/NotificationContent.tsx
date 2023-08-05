/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global } from '../Global';

import { IconButton } from '@mui/material';
import { CSSProperties } from '@mui/styles';
import { OpenInNew } from '@mui/icons-material';

import { OptumiConfig } from '../models/OptumiConfig';
import { Dropdown, Switch } from '.';


interface IProps {
    style?: CSSProperties
    getValue: () => OptumiConfig
    saveValue: (config: OptumiConfig) => void
    disabled?: boolean
    handleClose?: () => void
}

interface IState {
    value: string
}

const LABEL_WIDTH = '80px'
const VALUES = [{value: 'succeeds or fails', description: ''}, {value: 'fails', description: ''}];

export class NotificationContent extends React.Component<IProps, IState> {
    private _isMounted = false

    constructor(props: IProps) {
        super(props);
        const value = this.props.getValue();
        this.state = {
            value: !value.notifications.jobFailedSMSEnabled || (value.notifications.jobFailedSMSEnabled && value.notifications.jobCompletedSMSEnabled) ?  VALUES[0].value : VALUES[1].value,
        }
    }

    // private handleNotebookOptimizedSMSChange = (value: boolean) => {
    //     const config = this.props.getValue().copy()
    //     config.notifications.packageReadySMSEnabled = value;
    //     this.props.saveValue(config);
    // }

    private handleJobStartedSMSChange = (value: boolean) => {
        const config = this.props.getValue().copy()
        config.notifications.jobStartedSMSEnabled = value;
        this.props.saveValue(config);
    }

    private handleChange = (value: string, enabled: boolean) => {
        const config = this.props.getValue().copy()
        config.notifications.jobCompletedSMSEnabled = value == VALUES[0].value && enabled;
        config.notifications.jobFailedSMSEnabled = enabled;
        this.props.saveValue(config);
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const disabled = !Global.user.notificationsEnabled || Global.user.phoneNumber == null || Global.user.phoneNumber == ""
        return <>
            {/* <Switch
                getValue={() => (disabled && !this.props.disabled) ? false : this.props.getValue().notifications.packageReadySMSEnabled}
                saveValue={this.handleNotebookOptimizedSMSChange}
                label='Send a text when Optumi has a new optimization'
                labelWidth={LABEL_WIDTH}
                disabled={disabled || this.props.disabled || this.props.disabled}
            /> */}
            <Switch
                getValue={() => (disabled && !this.props.disabled) ? false : this.props.getValue().notifications.jobStartedSMSEnabled}
                saveValue={this.handleJobStartedSMSChange}
                label='Send a text when my job starts'
                labelWidth={LABEL_WIDTH}
                disabled={disabled || this.props.disabled || this.props.disabled}
            />
            <DIV sx={{display: 'inline-flex'}}>
                <Switch
                    getValue={() => (disabled && !this.props.disabled) ? false : this.props.getValue().notifications.jobFailedSMSEnabled}
                    saveValue={(enabled: boolean) => this.handleChange(this.state.value, enabled)}
                    label='Send a text when my job '
                    labelWidth={LABEL_WIDTH}
                    disabled={disabled || this.props.disabled}
                />
                <Dropdown
                    getValue={() => this.state.value}
                    saveValue={(value: string) => {
                        this.safeSetState({ value: value});
                        this.handleChange(value, this.props.getValue().notifications.jobFailedSMSEnabled);
                    }}
                    values={VALUES}
                    disabled={disabled || this.props.disabled}
                    // Wipe out the width being set internally in Dropdown
                    sx={{width: 'unset', marginLeft: '-6px'}}
                />
                
            </DIV>
            {(disabled && !this.props.disabled) && (
                <DIV sx={{display: 'inline-flex', width: 'calc(100% - 72px)',margin: '12px 36px'}}>
                    <DIV sx={{margin: 'auto 0px', fontStyle: 'italic'}}>
                        Notifications can be enabled in settings
                    </DIV>
                    <IconButton
                        size='large'
                        onClick={() => {
                            Global.followLink(Global.Target.SettingsPopup.PreferencesTab)
                            if (this.props.handleClose) this.props.handleClose();
                        }}
                        sx={{
                            display: 'inline-block',
                            width: '36px',
                            height: '36px',
                            padding: '3px',
                        }}
                    >
                        <OpenInNew sx={{height: '20px', width: '20px'}}/>
                    </IconButton>
                </DIV>
            )}
        </>;
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
