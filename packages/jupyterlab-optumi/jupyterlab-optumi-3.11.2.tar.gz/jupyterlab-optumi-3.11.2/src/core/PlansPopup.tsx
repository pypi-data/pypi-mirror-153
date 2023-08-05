/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { DIV, Global } from '../Global';

import { Button, Dialog, DialogTitle, IconButton } from '@mui/material';
import { withStyles } from '@mui/styles';
import { Close } from '@mui/icons-material';

import { ShadowedDivider } from '.';
import { SxProps, Theme } from '@mui/system';
import { EgressBuckets } from '../components/EgressBuckets';
import { StorageBuckets } from '../components/StorageBuckets';
import { Colors } from '../Colors';
import { SubscribeButton } from './SubscribeButton';
import FormatUtils from '../utils/FormatUtils';

const StyledDialog = withStyles({
    paper: {
        width: 'calc(min(80%, 600px + 150px + 2px))',
        // width: '100%',
        // height: '80%',
        overflowY: 'visible',
        maxWidth: 'inherit',
    },
})(Dialog);

interface IProps {
    sx?: SxProps<Theme>
    buttons?: JSX.Element
    openButton: JSX.Element
    open: boolean
    handleClose: () => any
}

interface IState {}

export class PlansPopup extends React.Component<IProps, IState> {

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
		return <>
            {this.props.openButton}
            <StyledDialog
                open={this.props.open}
                onClose={this.props.handleClose}
                scroll='paper'
            >
                <DialogTitle
                    sx={{
                        display: 'inline-flex',
                        height: '60px',
                        padding: '6px',
                    }}>
                    <DIV sx={{
                        display: 'inline-flex',
                        minWidth: '225px',
                        fontSize: '16px',
                        fontWeight: 'bold',
                        paddingRight: '12px', // this is 6px counteracting the DialogTitle padding and 6px aligning the padding to the right of the tabs
                    }}>
                        <DIV sx={{margin: 'auto 6px', paddingLeft: '12px'}}>
                            Plans
                        </DIV>
                    </DIV>
                    <DIV sx={{flexGrow: 1}} />
                    <IconButton
                        size='large'
                        onClick={this.props.handleClose}
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
                </DialogTitle>
                <ShadowedDivider />
                <DIV sx={{
                    padding: '12px',
                    fontSize: 'var(--jp-ui-font-size1)',
                    overflow: 'auto',
                }}>
                    <DIV sx={{padding: '12px'}}>
                        <DIV sx={{width: 'fit-content', margin: '6px auto', fontSize: '24px', fontWeight: 'bold'}}>
                            Pricing
                        </DIV>
                        <DIV sx={{width: 'fit-content', margin: '6px auto'}}>
                            Our Starter tier charges ${Global.user.serviceFee.toFixed(2)}/hour when one or more machines (used for sessions and jobs) are running. Machines are charged separately and you only pay for what you use. We pass through machine costs as billed by our cloud providers, including any promotional pricing.
                        </DIV>
                        <DIV sx={{width: '100%', display: 'inline-flex', justifyContent: 'center'}}>
                            <DIV 
                                sx={{
                                    textAlign: 'center', 
                                    padding: '12px', 
                                    margin: '12px', 
                                    border: '1px solid ' + Colors.SECONDARY, 
                                    borderRadius: '6px',
                                    width: 'fit-content'
                                }}
                            >
                                <DIV sx={{width: 'fit-content', margin: '6px auto', fontSize: '24px', fontWeight: 'bold'}}>
                                    Starter
                                </DIV>
                                <DIV sx={{color: Colors.PRIMARY, fontSize: '20px', fontWeight: 'bold'}}>
                                    ${Global.user.serviceFee.toFixed(2)}/hour
                                </DIV>
                                <DIV>
                                    {Global.user.maxJobs + ' parallel jobs/sessions'}
                                </DIV>
                                <DIV>
                                    {'SMS notifications'}
                                </DIV>
                                {Global.user.isSubscribed() ? (
                                    <Button
                                        sx={{margin: '12px', width: '150px'}}
                                        variant='contained'
                                        color='primary'
                                        disabled
                                    >
                                        Subscribed
                                    </Button>
                                ) : (
                                    <SubscribeButton sx={{width: '150px', margin: '12px'}}/>
                                )}
                            </DIV>
                            <DIV 
                                sx={{
                                    textAlign: 'center', 
                                    padding: '12px', 
                                    margin: '12px', 
                                    border: '1px solid ' + Colors.SECONDARY, 
                                    borderRadius: '6px',
                                    width: 'fit-content',
                                    display: 'flex',
                                    flexDirection: 'column',
                                }}
                            >
                                <DIV sx={{width: 'fit-content', margin: '6px auto', fontSize: '24px', fontWeight: 'bold'}}>
                                    Pro
                                </DIV>
                                <DIV sx={{color: Colors.PRIMARY, fontSize: '20px', fontWeight: 'bold'}}>
                                    Coming soon
                                </DIV>
                                <DIV sx={{flexGrow: '1'}}/>
                                <Button
                                    sx={{margin: '12px', width: '150px'}}
                                    variant='contained'
                                    color='primary'
                                    onClick={() => window.open('https://02y48lsf4ft.typeform.com/to/EbE8axZj', '_blank')}
                                >
                                    Contact us
                                </Button>
                            </DIV>
                        </DIV>
                        {this.props.buttons && (
                            <DIV sx={{display: 'inline-flex', width: '100%', justifyContent: 'center'}}>
                                {this.props.buttons}
                            </DIV>
                        )}
                        <DIV sx={{width: 'fit-content', margin: '6px auto', fontSize: '24px', fontWeight: 'bold'}}>
                            Dynamic upgrades
                        </DIV>
                        <DIV sx={{width: 'fit-content', margin: '6px auto 18px auto'}}>
                            <DIV sx={{margin: '6px'}}>
                                If enabled, storage and egress tiers will be automatically upgraded as you consume more of each resource. For example, if in a given billing period you use {FormatUtils.styleCapacityUnitValue()((Global.user.storageBuckets[1].limit + Global.user.storageBuckets[2].limit) / 2)} of storage, you will be charged ${Global.user.storageBuckets[2].cost}.
                            </DIV>
                            <DIV sx={{margin: '6px'}}>
                                If disabled, you will not be able to consume more than the storage and egress limits included in your current tier.
                            </DIV>
                            <DIV sx={{margin: '6px'}}>
                                At the beginning of every billing cycle you will start off in the lowest possible tier based on your usage.
                            </DIV>
                        </DIV>
                        <StorageBuckets buckets={Global.user.storageBuckets}/>
                        <EgressBuckets buckets={Global.user.egressBuckets}/>
                        <DIV sx={{width: 'fit-content', margin: '18px auto 6px auto', fontSize: '10px'}}>
                            Unit prefixes (such as '2 GB') should be interpreted as binary units ('2 GiB') as further explained
                            <a href='https://en.wikipedia.org/wiki/Gigabyte' target='_blank' style={{marginLeft: '3px', color: 'var(--jp-ui-font-color0)', textDecoration: 'underline'}}>
							    here
						    </a>
                        </DIV>
                    </DIV>
                </DIV>
            </StyledDialog>
        </>;
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
