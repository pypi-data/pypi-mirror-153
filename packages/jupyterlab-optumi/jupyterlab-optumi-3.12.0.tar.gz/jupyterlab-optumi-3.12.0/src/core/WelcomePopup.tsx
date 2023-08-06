/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { ServerConnection } from '@jupyterlab/services';


import * as React from 'react'
import { DIV, Global, LI, PermanentPopup, UL } from '../Global';

import {
    Button,
    CircularProgress,
    DialogContent,
    DialogTitle,
    Divider,
} from '@mui/material';

import { ShadowedDivider } from './ShadowedDivider'
import { User } from '../models/User';
import { SubscribeButton } from './SubscribeButton';
import { Header } from './Header';
import { CustomerState } from './CustomerState';

interface IProps {}

interface IState {
    plansOpen: boolean
    freeTrialWaiting: boolean
}

export default class WelcomePopup extends React.Component<IProps, IState> {
    private _isMounted = false

    public constructor(props: IProps) {
        super (props);
        this.state = {
            plansOpen: false,
            freeTrialWaiting: false
        }
    }

    // Log out of the REST interface (Copied from SettingsPage aside from setState call)
    private logout = () => {
        const settings = ServerConnection.makeSettings();
        const url = settings.baseUrl + "optumi/logout";
        const init = {
            method: 'GET',
        };
        ServerConnection.makeRequest(
            url,
            init, 
            settings
        ).then((response: Response) => {
            Global.user = null;
        });
    }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <PermanentPopup
                open={Global.user.customerState == CustomerState.INIT}
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
                                Welcome 👋
                            </DIV>
                        </DIV>
                        <DIV sx={{flexGrow: 1}} />
                        <DIV>
                            <Button
                                disableElevation
                                sx={{ height: '36px', margin: '6px' }}
                                variant="outlined"
                                color="primary"
                                onClick={() => {
                                    const user: User = Global.user;
                                    if (user.appTracker.activeSessions.length != 0) {
                                        this.safeSetState({ showLogoutWithSessionPopup: true });
                                    } else {
                                        this.logout()
                                    }
                                }}
                            >
                                Logout
                            </Button>
                        </DIV>
					</DialogTitle>
                <ShadowedDivider />
                <DIV sx={{padding: '18px'}}>
                    <DialogContent sx={{padding: '6px 18px', whiteSpace: 'pre-wrap'}}>
                        <DIV sx={{display: 'inline-flex', width: '100%'}}>
                            <DIV sx={{width: '50%', margin: '12px 24px 12px 12px', display: 'inline', position: 'relative'}}>
                                <Header title='Free trial' sx={{fontSize: '18px'}} />
                                <UL sx={{lineHeight: '2'}}>
                                    <LI>No credit card required</LI>
                                    <LI>$5 of credit for running notebooks</LI>
                                    <LI>Valid for 2 weeks</LI>
                                    <LI>Credit and data will be deleted after 2 weeks (unless you subscribe!)</LI>
                                </UL>
                                
                                <DIV sx={{width: '100%', textAlign: 'center', position: 'absolute', bottom: '0'}}>
                                    <Button
                                        variant='outlined'
                                        color='primary'
                                        onClick={() => {
                                            Global.user.trialStart = new Date()
                                            // Global.user.customerState = CustomerState.FREE_TRIAL
                                            this.safeSetState({freeTrialWaiting: true})
                                        }}
                                        sx={{marginLeft: '18x', width: '100%'}}
                                    >
                                        {this.state.freeTrialWaiting ? (<CircularProgress size='1.75em'/>) : 'Start free trial'}
                                    </Button>
                                </DIV>
                            </DIV>
                            <Divider orientation='vertical' variant='middle' flexItem />
                            <DIV sx={{width: '50%', margin: '12px 12px 12px 24px', display: 'inline'}}>
                                <Header title='Starter' sx={{fontSize: '18px'}} />
                                <UL sx={{lineHeight: '2'}}>
                                    <LI>$0.10/hour when one or more machines are running</LI>
                                    <LI>Machine costs are passed through from our cloud providers</LI>
                                    <LI>10 GB of free storage</LI>
                                    <LI>5 GB of free egress</LI>
                                </UL>
                                <DIV sx={{width: '100%', textAlign: 'center'}}>
                                    <SubscribeButton sx={{width: '100%'}} />
                                </DIV>
                            </DIV>
                        </DIV>
                    </DialogContent>
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
