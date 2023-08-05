/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { SubHeader } from '../../core';
import { DIV, Global } from '../../Global';

import { Machine } from './Machine';

interface IProps {
    machine: Machine
}

interface IState {}

export class MachineCapability extends React.Component<IProps, IState> {
    _isMounted = false;

    constructor(props: IProps) {
        super(props);
        this.state = {};
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const machine = this.props.machine;
        return (
            <>
                <SubHeader title='Machine used'/>
                <DIV sx={{margin: '6px'}}>
                    {machine.getIdentityComponent()}
                </DIV>
                <SubHeader title='Full machine details'/>
                <DIV sx={{whiteSpace: 'pre', margin: '6px'}}>
                    {machine.getDetails()}
                </DIV>
            </>
       );
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


    public componentDidMount = () => {
        this._isMounted = true
    }

	public componentWillUnmount = () => {
        this._isMounted = false
    }
}
