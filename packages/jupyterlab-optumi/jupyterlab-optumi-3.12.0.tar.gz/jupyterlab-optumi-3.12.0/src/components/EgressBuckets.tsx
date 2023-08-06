/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Colors } from '../Colors';
import { Header } from '../core';
import { DIV, Global } from '../Global';
import { EgressBucket } from '../models/EgressBucket';
import FormatUtils from '../utils/FormatUtils';

interface IProps {
    buckets: EgressBucket[]
}

interface IState {}

export class EgressBuckets extends React.Component<IProps, IState> {

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <DIV sx={{width: '100%', justifyContent: 'center'}}>
                <Header sx={{width: 'fit-content', margin: '6px auto'}} title="Egress" />
                    <DIV sx={{display: 'inline-flex', width: '100%', justifyContent: 'center'}}>
                    {this.props.buckets.map((bucket, index) => (
                        <DIV 
                            sx={{
                                width: '115px',
                                textAlign: 'center', 
                                padding: '12px', 
                                margin: index == 0 ? '6px 0px 6px 6px' : (index == this.props.buckets.length-1 ? '6px 6px 6px 0px' : '6px 0px'),
                                border: '1px solid ' + Colors.SECONDARY, 
                                borderRadius: index == 0 ? '6px 0px 0px 6px' : (index == this.props.buckets.length-1 ? '0px 6px 6px 0px' : '0px'),
                            }}
                        >
                            <DIV sx={{color: Colors.PRIMARY, fontSize: '20px', fontWeight: 'bold'}}>
                                {bucket.cost == 0 ? 'Free' : '$' + bucket.cost}
                            </DIV>
                            <DIV>
                                {'Up to ' + FormatUtils.styleCapacityUnitValue()(bucket.limit)}
                            </DIV>
                        </DIV>
                    ))}
                </DIV>
            </DIV>
        )
    }

    // public shouldComponentUpdate = (nextProps: IProps, nextState: IState): boolean => {
    //     try {
    //         if (JSON.stringify(this.props) != JSON.stringify(nextProps)) return true;
    //         if (JSON.stringify(this.state) != JSON.stringify(nextState)) return true;
    //         if (Global.shouldLogOnRender) console.log('SuppressedRender (' + new Date().getSeconds() + ')');
    //         return false;
    //     } catch (error) {
    //         return true;
    //     }
    // }
}
