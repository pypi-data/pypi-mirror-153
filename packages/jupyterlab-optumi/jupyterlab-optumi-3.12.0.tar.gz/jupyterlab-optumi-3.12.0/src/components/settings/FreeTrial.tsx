/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global, LI, UL } from '../../Global';

import FormatUtils from '../../utils/FormatUtils';
import { Header, Label } from '../../core';
import { InfoPopup } from '../../core/InfoPoppup';
import { PlansPopup } from '../../core/PlansPopup';
import { SubscribeButton } from '../../core/SubscribeButton';
import { Tag } from '../Tag';
import moment from 'moment';


// Properties from parent
interface IProps {
    balance: number
}

// Properties for this component
interface IState {
    portalWaiting: boolean,
    showStoragePopup: boolean
    plansOpen: boolean
}

export class FreeTrial extends React.Component<IProps, IState> {
    _isMounted = false;

    constructor(props: IProps) {
        super(props);
        this.state = {
            portalWaiting: false,
            showStoragePopup: false,
            plansOpen: false,
        }
    }

	// The contents of the component
	public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const expiration = new Date(Global.user.trialStart);
       	expiration.setDate(expiration.getDate() + 14); 

        var until : string;
        if (moment(new Date()).format('MM-DD') == moment(expiration).format('MM-DD')) {
            until = moment(expiration).format('hh:mm')
        } else {
            until = moment(expiration).format('MM/DD')
        }
		return (
            <>
                <DIV sx={{display: 'flex'}}>
                    <Header title='Current plan' />
                    <PlansPopup
                        open={this.state.plansOpen}
                        handleClose={() => this.safeSetState({ plansOpen: false })}
                        openButton={
                            <Tag label='View plans'
                                onClick={() => this.safeSetState({ plansOpen: true })}
                            />
                        }
                    />
                </DIV>
                <DIV sx={{display: 'flex', width: '100%'}}>
                    <Label label={'Free trial until ' + until}
                        getValue={() => FormatUtils.formatCredit(this.props.balance) + ' credit'}
                        align='left' valueAlign='right' lineHeight='20px'
                        info={
                            <InfoPopup title='Free Trial' sx={{marginY: 'auto', marginLeft: 0.5, marginRight: -0.5, marginBottom: '2px'}} popup={
                                <DIV sx={{padding: '12px'}}>
                                        A few things to remember about your free trial:
                                    <UL>
                                        <LI>No credit card required</LI>
                                        <LI>It is valid for 2 weeks</LI>
                                        <LI>You get a $5 promotional credit for machines to run notebooks</LI>
                                        <LI>At the end of the trial your promotional credit will expire and your data will be deleted (unless you subscribe!)</LI>
                                    </UL>
                                </DIV>
                            } />
                        }
                    />
                    {/* the ml and mr below are odd because the line has 12px margin on the right combined with the icon being 14px and the overflow getting cut off at 12px */}
                </DIV>
                <Label label='Storage'
                    getValue={() => 'Up to ' + FormatUtils.styleCapacityUnitValue()(Global.user.storageBuckets[0].limit)}
                    align='left' valueAlign='right' lineHeight='20px'
                    info={
                        <InfoPopup title='Storage' sx={{marginY: 'auto', marginLeft: 0.5, marginRight: -0.5, marginBottom: '2px'}} popup={
                            <DIV sx={{padding: '12px'}}>
                                Storage refers to data you store persistently in the Optumi platform, such as uploaded files used as input for notebooks. It does not include temporary disk space on machines provisioned to run your notebooks.
                            </DIV>
                        } />
                    }
                />
                <Label label='Egress'
                    getValue={() => 'Up to ' + FormatUtils.styleCapacityUnitValue()(Global.user.egressBuckets[0].limit)}
                    align='left' valueAlign='right' lineHeight='20px'
                    info={
                        <InfoPopup title='Egress' sx={{marginY: 'auto', marginLeft: 0.5, marginRight: -0.5, marginBottom: '2px'}} popup={
                            <DIV sx={{padding: '12px'}}>
                                Egress refers to data (files, images, logs) transferred out of the Optumi platform. Examples include:
                                <UL>
                                    <LI>Using your notebook to send files to Amazon RedShift or Google BigQuery</LI>
                                    <LI>Downloading a file from the Optumi platform to your laptop</LI>
                                </UL>
                            </DIV>
                        } />
                    }
                />
                <DIV sx={{display: 'flex', width: '100%', padding: 0.5}}>
                    <SubscribeButton sx={{width: '50%', marginX: 'auto'}}/>
                </DIV>
            </>
		);
    }
    
    // Will be called automatically when the component is mounted
	public componentDidMount = () => {
        this._isMounted = true;
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
        this._isMounted = false;
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
