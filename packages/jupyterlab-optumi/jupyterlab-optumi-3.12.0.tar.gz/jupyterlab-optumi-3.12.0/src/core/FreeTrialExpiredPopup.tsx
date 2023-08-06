/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/


import * as React from 'react'
import { DIV, Global, LI, PermanentPopup, UL } from '../Global';

import {
    DialogActions,
    DialogContent,
    DialogTitle,
    IconButton,
} from '@mui/material';

import { ShadowedDivider } from './ShadowedDivider'
import { Close } from '@mui/icons-material';
import { SubscribeButton } from './SubscribeButton';
import { CustomerState } from './CustomerState';

interface IProps {}

interface IState {}

export default class FreeTrialExpiredPopup extends React.Component<IProps, IState> {
    // private _isMounted = false

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        
        const now = new Date();
        return (
            <PermanentPopup
                open={Global.user.customerState == CustomerState.FREE_TRIAL_ENDED && (now.getTime() - Global.user.freeTrialExpiredDismissed.getTime() > Global.dismissalTimeout)}
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
                                Your Optumi trial has ended
                            </DIV>
                        </DIV>
                        <DIV sx={{flexGrow: 1}} />
                        <DIV>
                            <IconButton
                                size='large'
                                onClick={() => {
                                    Global.user.freeTrialExpiredDismissed = new Date()
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
                        Your 2-week free trial has ended. Here are a few things to remember:
                        <UL>
                            <LI>Credit will expire</LI>
                            <LI>Data will be removed in 2 weeks (so there's time for you to retrieve it)</LI>
                            <LI>You will still be able to log in, view workload details and download files</LI>
                            <LI>You can Subscribe to retain data and launch more workloads</LI>
                        </UL>
                    </DialogContent>
                    <DialogActions sx={{padding: '12px 6px 6px 6px'}}>
                        <SubscribeButton />
                    </DialogActions>
                </DIV>
           </PermanentPopup>
        );
    }

    handleUserChange = () => this.forceUpdate();

    public componentDidMount = () => {
        // this._isMounted = true
        Global.user.userInformationChanged.connect(this.handleUserChange);
        Global.onUserChange.connect(this.handleUserChange);
    }

    public componentWillUnmount = () => {
        Global.user.userInformationChanged.disconnect(this.handleUserChange);
        Global.onUserChange.disconnect(this.handleUserChange);
        // this._isMounted = false
    }

    // private safeSetState = (map: any) => {
	// 	if (this._isMounted) {
	// 		let update = false
	// 		try {
	// 			for (const key of Object.keys(map)) {
	// 				if (JSON.stringify(map[key]) !== JSON.stringify((this.state as any)[key])) {
	// 					update = true
	// 					break
	// 				}
	// 			}
	// 		} catch (error) {
	// 			update = true
	// 		}
	// 		if (update) {
	// 			if (Global.shouldLogOnSafeSetState) console.log('SafeSetState (' + new Date().getSeconds() + ')');
	// 			this.setState(map)
	// 		} else {
	// 			if (Global.shouldLogOnSafeSetState) console.log('SuppressedSetState (' + new Date().getSeconds() + ')');
	// 		}
	// 	}
	// }
}
