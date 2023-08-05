/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/


import * as React from 'react'
import { DIV, Global, LI, PermanentPopup, UL } from '../Global';

import {
    Button,
    DialogActions,
    DialogContent,
    DialogTitle,
    IconButton,
} from '@mui/material';

import { ShadowedDivider } from './ShadowedDivider'
import { Close, OpenInNew } from '@mui/icons-material';
import { CustomerState } from './CustomerState';

interface IProps {}

interface IState {}

export default class FreeTrialStartedPopup extends React.Component<IProps, IState> {
    // private _isMounted = false

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        
        return (
            <PermanentPopup
                open={Global.user.customerState == CustomerState.FREE_TRIAL && new Date(0).getTime() == Global.user.freeTrialStartedPopupDismissed.getTime()}
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
                                Your free trial has started ✅
                            </DIV>
                        </DIV>
                        <DIV sx={{flexGrow: 1}} />
                        <DIV>
                            <IconButton
                                size='large'
                                onClick={() => {
                                    Global.user.freeTrialStartedPopupDismissed = new Date()
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
                        Your two week free trial has started. Here are a few resources to help you make the most of it:
                        <UL sx={{lineHeight: '2'}}>
                            <LI>
                                Explore the knowledge base
                                <IconButton
                                    size='large'
                                    sx={{
                                        padding: 0.5,
                                        zIndex: 1,
                                    }}
                                    onClick={() => {
                                        window.open('https://optumi.notion.site/Optumi-Knowledge-Base-f51e2040569b46449601851c91caea29', '_blank')
                                    }}
                                >
                                    <OpenInNew sx={{height: '18px',width: '18px'}}/>
                                </IconButton>
                            </LI>
                            <LI>
                                Walk through an example notebook
                                <IconButton
                                    size='large'
                                    sx={{
                                        padding: 0.5,
                                    }}
                                    onClick={() => {
                                        window.open('https://optumi.notion.site/Launch-a-workload-with-an-example-notebook-0e473db440334c7d86b0dc398cb41761', '_blank')
                                    }}
                                >
                                    <OpenInNew sx={{height: '18px',width: '18px'}}/>
                                </IconButton>
                            </LI>
                            <LI>
                                Learn about the two ways to run notebooks
                                <IconButton
                                    size='large'
                                    sx={{
                                        padding: 0.5,
                                    }}
                                    onClick={() => {
                                        window.open('https://optumi.notion.site/Decide-when-to-launch-a-workload-as-a-session-vs-job-3266e474b89f4c9592b0d4f88fb28fec', '_blank')
                                    }}
                                >
                                    <OpenInNew sx={{height: '18px',width: '18px'}}/>
                                </IconButton>
                            </LI>
                        </UL>

                        For support you can always reach out to cs@optumi.com.
                    </DialogContent>
                    <DialogActions sx={{padding: '12px 6px 6px 6px'}}>
                        <Button
                            variant='contained'
                            color='primary'
                            onClick={() => {
                                Global.user.freeTrialStartedPopupDismissed = new Date()
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
