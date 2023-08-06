/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { DIV, Global } from '../../Global';

import InputArea from './InputArea'
import OutputArea from './OutputArea'

interface IProps {
    cell: any
    metadata: any
    renderInColor: boolean
}

interface IState {}

export default class CodeCell extends React.Component<IProps, IState> {

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <DIV className='p-Widget lm-Widget jp-Cell jp-CodeCell jp-Notebook-cell' onContextMenu={(e: any) => e.preventDefault()}>
                <InputArea cell={this.props.cell} metadata={this.props.metadata} renderInColor={this.props.renderInColor} />
                {this.props.cell.outputs && this.props.cell.outputs.length > 0 && (
                    <OutputArea cell={this.props.cell} metadata={this.props.metadata} />
                )}
            </DIV>
        )
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
