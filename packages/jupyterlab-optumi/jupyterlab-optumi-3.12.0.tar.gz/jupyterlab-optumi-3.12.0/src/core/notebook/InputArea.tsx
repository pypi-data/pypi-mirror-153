/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { DIV, Global } from '../../Global';

import Editor from './Editor'
import Markdown from './Markdown'

interface IProps {
    cell: any
    metadata: any
    renderInColor: boolean
}

interface IState {}

export default class InputArea extends React.Component<IProps, IState> {

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        var exec_count = ' ';
        var scrollID = '';
        // If the notebook is running, add a star toa ll cells
        if (this.props.metadata.papermill && this.props.metadata.papermill.start_time && !this.props.metadata.papermill.end_time) exec_count = '*';
        // If the cell is finished, show the execution count
        if (this.props.cell.execution_count != null) exec_count = this.props.cell.execution_count;
        // Papermill puts an execution_count in a cell even if it is still running, so patch that here, also set the scroll id
        if (this.props.cell.metadata.papermill && this.props.cell.metadata.papermill.start_time && !this.props.cell.metadata.papermill.end_time) {
            exec_count = '*';
            scrollID = 'scrollHere'
        }
        return (
            <DIV id={scrollID} className='p-Widget lm-Widget jp-Cell-inputWrapper'>
                <DIV className='p-Widget lm-Widget jp-InputArea jp-Cell-inputArea'>
                    <DIV className='p-Widget lm-Widget jp-InputPrompt jp-InputArea-prompt'>
                    {this.props.cell.cell_type === 'code' ? (
                        <>
                            {this.props.cell.execution_count !== undefined && `[${exec_count}]:`}
                        </>
                    ) : this.props.cell.cell_type === 'markdown' ? (
                        <></>
                    ) : (
                        <></>
                    )}
                    </DIV>
                    {this.props.cell.cell_type === 'code' ? (
                        <Editor cell={this.props.cell} metadata={this.props.metadata} renderInColor={this.props.renderInColor} />
                    ) : this.props.cell.cell_type === 'markdown' ? (
                        <Markdown cell={this.props.cell} metadata={this.props.metadata} />
                    ) : (
                        <></>
                    )}
                </DIV>
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