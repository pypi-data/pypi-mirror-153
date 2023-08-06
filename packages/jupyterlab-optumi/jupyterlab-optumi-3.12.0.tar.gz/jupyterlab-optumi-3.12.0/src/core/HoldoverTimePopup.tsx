/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/


import * as React from 'react'
import { DIV, Global, PermanentPopup } from '../Global';

import {
    Button,
    DialogActions,
    DialogContent,
    DialogTitle,
    IconButton,
} from '@mui/material';

import { ShadowedDivider } from './ShadowedDivider'
import { Close, OpenInNew } from '@mui/icons-material';
import { TextBox } from './TextBox';

interface IProps {}

interface IState {
    holdoverFocused: boolean
}

export default class HoldoverTimePopup extends React.Component<IProps, IState> {
    private _isMounted = false

    public constructor(props: IProps) {
        super(props)
        this.state = {
            holdoverFocused: false,
        }
    }

    private getUserHoldoverTimeValue(): number { return Math.round(Global.user.userHoldoverTime / 60) }
    private saveUserHoldoverTimeValue(userHoldoverTime: number) { Global.user.userHoldoverTime = userHoldoverTime * 60 }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        
        return (
            <PermanentPopup
                open={Global.user.appTracker.getDisplayNum() > 0 && new Date(0).getTime() == Global.user.holdoverTimePopupDismissed.getTime()}
            >
                <DialogTitle sx={{
                        display: 'inline-flex',
                        height: '60px',
                        padding: '6px',
                    }}>
                        <DIV sx={{
                            display: 'inline-flex',
                            minWidth: '150px',
                            fontSize: '16px',
                            fontWeight: 'bold',
                            paddingRight: '12px', // this is 6px counteracting the DialogTitle padding and 6px aligning the padding to the right of the tabs
                        }}>
                            <DIV sx={{margin: 'auto', paddingLeft: '12px'}}>
                                Heads up!
                            </DIV>
                        </DIV>
                        <DIV sx={{flexGrow: 1}} />
                        <DIV>
                            <IconButton
                                size='large'
                                onClick={() => {
                                    Global.user.holdoverTimePopupDismissed = new Date()
                                    this.forceUpdate()
                                }}
                                sx={{
                                    display: 'inline-block',
                                    width: '36px',
                                    height: '36px',
                                    padding: '3px',
                                    margin: '6px',
                                }}
                            >
                                <Close
                                    sx={{
                                        width: '30px',
                                        height: '30px',
                                        padding: '3px',
                                    }}
                                />
                            </IconButton>
                        </DIV>
					</DialogTitle>
                <ShadowedDivider />
                <DIV sx={{padding: '18px'}}>
                    <DialogContent sx={{padding: '6px 18px', whiteSpace: 'pre-wrap'}}>
                        You can configure how long machines are held onto after workloads finish. This can also be changed at any time in Settings
                                <IconButton
                                    size='large'
                                    sx={{
                                        padding: 0.5,
                                        zIndex: 1,
                                    }}
                                    onClick={() => {
                                        Global.followLink(Global.Target.SettingsPopup.LimitsTab)
                                    }}
                                >
                                    <OpenInNew sx={{height: '18px',width: '18px'}}/>
                                </IconButton>
                        <DIV sx={{display: 'inline-flex', width: '100%', justifyContent: 'center', marginTop: '24px'}}>
                            <TextBox<number>
                                sx={{width: '75px'}}
                                getValue={this.getUserHoldoverTimeValue}
                                saveValue={this.saveUserHoldoverTimeValue}
                                styledUnitValue={(value: number) => { return isNaN(value) ? "" : value.toFixed() }}
                                unstyleUnitValue={(value: string) => { return value.replace(/\d/g, '').length > 0 ? Number.NaN : Number.parseFloat(value); }}
                                onFocus={() => this.safeSetState({holdoverFocused: true})}
                                onBlur={() => this.safeSetState({holdoverFocused: false})}
                                minValue={0}
                                maxValue={+(Global.user.maxHoldoverTime / 60).toFixed()}
                            />
                            <DIV sx={{margin: 'auto 0px'}}>
                                minutes before releasing idle machines
                            </DIV>
                        </DIV>
                    </DialogContent>
                    <DialogActions sx={{padding: '12px 6px 6px 6px'}}>
                        <Button
                            variant='contained'
                            color='primary'
                            onClick={() => {
                                Global.user.holdoverTimePopupDismissed = new Date()
                            }}
                            sx={{marginLeft: '18x'}}
                        >
                           Got it
                        </Button>
                    </DialogActions>
                </DIV>
           </PermanentPopup>
        );
    }

    handleUserChange = () => this.forceUpdate();

    public componentDidMount = () => {
        this._isMounted = true
        Global.user.userInformationChanged.connect(this.handleUserChange);
        Global.onUserChange.connect(this.handleUserChange);
    }

    public componentWillUnmount = () => {
        Global.user.userInformationChanged.disconnect(this.handleUserChange);
        Global.onUserChange.disconnect(this.handleUserChange);
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
