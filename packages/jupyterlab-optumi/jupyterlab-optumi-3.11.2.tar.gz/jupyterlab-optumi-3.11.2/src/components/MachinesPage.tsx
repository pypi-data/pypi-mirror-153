/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global } from '../Global';

import { SxProps, Theme } from '@mui/system';

import { Machine } from '../models/machine/Machine';
import { Divider } from '@mui/material';
import { Header, Label } from '../core';
import FormatUtils from '../utils/FormatUtils';
import { WarningRounded } from '@mui/icons-material';
import { Tag } from './Tag';
import { CustomerState } from '../core/CustomerState';

interface IProps {
    sx?: SxProps<Theme>
    rate: number
    balance: number
    machines: Machine[],
    machineCost: number
    serviceFeeCost: number
    storageCost: number
    egressCost: number
}

interface IState {}

export class MachinesPage extends React.Component<IProps, IState> {

	// The contents of the component
	public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        var sorted = [...this.props.machines].sort((m1,m2) => {
			if (m1.time > m2.time) {
				return -1;
			}
			if (m1.time < m2.time) {
				return 1;
			}
			return 0;
		});

        var machines: JSX.Element[] = new Array();
        for (var i = 0; i < sorted.length; i++) {
            var machine: Machine = sorted[i]
            if (Global.user.userExpertise >= 2 || machine.getStateMessage() != 'Releasing') {
                machines.push(
                    <DIV key={machine.uuid} sx={{display: 'inline-flex', width: '100%', padding: '6px 0px'}}>
                        {machine.getComponent()}
                    </DIV>
                );
            }
        }
		return (
			<DIV sx={Object.assign({display: 'flex', flexFlow: 'column', overflow: 'hidden'}, this.props.sx)}>
                <DIV sx={{margin: '6px'}}>
                    <DIV sx={{display: 'flex'}}>
                        <Header title={'Machines'} />
                    </DIV>
                    <Label label='Current rate'
                        getValue={() => `$${this.props.rate.toFixed(2)}/hr`}
                        lineHeight='18px' align='left' valueAlign='right'
                    />
                    {/* {Global.user.isSubscribed() && (
                        <DIV sx={{opacity: 0.5, textAlign: 'center'}}>
                            Billing cycle resets on the {ordinal_suffix_of(Global.user.billingCycleAnchor.getDate())} of the month
                        </DIV>
                    )} */}
                    {Global.user.isSubscribed() && !Global.user.lastBillPaid && (
                        <>
                            <Divider variant='middle' />
                            <DIV sx={{margin: '12px', justifyContent: 'center', height: '21px', display: 'inline-flex', width: 'calc(100% - 24px)'}}>
                                <DIV sx={{marginLeft: '-26px'}}>
                                    <WarningRounded sx={{color: 'error.main', lineHeight: '20px', width: '20px', height: '20px', marginRight: '6px'}} />
                                </DIV>
                                <DIV sx={{lineHeight: '21px'}}>
                                    Last payment failed, please update
                                </DIV>
                            </DIV>
                        </>
                    )}
                </DIV>
                <DIV sx={{flexGrow: 1, overflowY: 'auto', padding: '6px'}}>
                    {machines.length > 0 && (
                        machines
                    )}
                </DIV>
                <DIV sx={{margin: '12px 0px'}}>
                    <DIV sx={{display: 'flex'}}>
                        <Header title='Usage' />
                        <Tag label='View billing' onClick={() => Global.followLink(Global.Target.SettingsPopup.BillingTab)}/>
                    </DIV>
                    <Label label='Storage'
                        getValue={() => FormatUtils.styleStorageOrEgress(Global.user.fileTracker.total, Global.user.fileTracker.limit)}
                        lineHeight='18px' align='left' valueAlign='right'
                    />
                    <Label label='Egress'
                        getValue={() => FormatUtils.styleStorageOrEgress(Global.user.egressTotal, Global.user.egressLimit)}
                        lineHeight='18px' align='left' valueAlign='right'
                    />
                    {Global.user.isSubscribed() ? (
                        <Label label='Total cost'
                            getValue={() => {
                                if (this.props.machineCost == null || this.props.egressCost == null || this.props.storageCost == null || this.props.serviceFeeCost == null) return '--'
                                var sum = +FormatUtils.floorAndToFixed(this.props.machineCost, 2) + +FormatUtils.floorAndToFixed(this.props.egressCost, 2) + +FormatUtils.floorAndToFixed(this.props.storageCost, 2) + +FormatUtils.floorAndToFixed(this.props.serviceFeeCost, 2);
                                if (sum == 0 && (this.props.machineCost > 0 || this.props.egressCost > 0 || this.props.storageCost > 0 || this.props.serviceFeeCost > 0)) return '< $0.01'
                                return `${FormatUtils.formatCost(sum)}`;
                            }}
                            lineHeight='18px' align='left' valueAlign='right'
                        />
                        
                    ) : Global.user.customerState == CustomerState.FREE_TRIAL && (
                        <Label label='Credits'
                            getValue={() => `${FormatUtils.formatCredit(this.props.balance)}`}
                            lineHeight='18px' align='left' valueAlign='right'
                        />
                    )}
                </DIV>
            </DIV>
		);
    }

     // Will be called automatically when the component is mounted
	public componentDidMount = () => {
        if (Global.user != null) {
            Global.user.fileTracker.getFilesChanged().connect(() => this.forceUpdate());
            Global.user.userInformationChanged.connect(() => this.forceUpdate())
        }
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
        if (Global.user != null) {
            Global.user.fileTracker.getFilesChanged().disconnect(() => this.forceUpdate());
            Global.user.userInformationChanged.disconnect(() => this.forceUpdate())
        }
    }
}
