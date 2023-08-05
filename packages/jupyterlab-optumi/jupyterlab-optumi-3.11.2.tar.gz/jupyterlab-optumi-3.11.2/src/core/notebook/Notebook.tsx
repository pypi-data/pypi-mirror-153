/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { DIV, Global } from '../../Global'

import CodeCell from './CodeCell'
import MarkdownCell from './MarkdownCell'

interface IProps {
    notebook: {cells: any[], metadata: any}
}

interface IState {}

export default class Notebook extends React.Component<IProps, IState> {
    private oldOpen: (event: MouseEvent) => boolean

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const notebook = this.props.notebook
        // const words = notebook.cells.map(cell => (cell.source as string).split(/\b/).length).reduce((a, b) => a + b, 0)
        const words = notebook.cells.map(cell => cell.source.length).reduce((a, b) => a + b, 0) / 5
        const renderInColor = words < 2500
        let i = 0;
        return (
            <DIV className='p-Widget lm-Widget jp-Notebook jp-NotebookPanel-notebook jp-mod-scrollPastEnd jp-mod-commandMode'>
                {notebook.cells.map(cell => 
                    cell.cell_type === 'code' ? (
                        <CodeCell key={i++} cell={cell} metadata={notebook.metadata} renderInColor={renderInColor} />
                    ) : cell.cell_type === 'markdown' ? (
                        <MarkdownCell key={i++} cell={cell} metadata={notebook.metadata} renderInColor={renderInColor} />
                    ) : (
                        <></>
                    )
                )}
            </DIV>
        )
    }

    private papermillErrorCell: HTMLElement = null
    public componentDidMount = () => {
        // Remove the papermill error cell from any elements if they exist
        this.papermillErrorCell = document.getElementById('papermill-error-cell');
        if (this.papermillErrorCell) {
            this.papermillErrorCell.id = ''
            // Avoid removing the id from the notebook in the popup
            if (!document.getElementById('papermill-error-cell')) {
                this.papermillErrorCell.id = 'papermill-error-cell';
                this.papermillErrorCell = null;
            }
        }
        // Scroll to the current executing cell if there is one running
        location.href = "#";
        location.href = "#scrollHere";
        // Override the JupyterLab context menu open (disable it)
        this.oldOpen = Global.lab.contextMenu.open;
        Global.lab.contextMenu.open = () => false;
    }

    // Add context menu items back
    public componentWillUnmount = () => {
        // Restore the old JupyterLab context menu open
        Global.lab.contextMenu.open = this.oldOpen;
        // Restore the old error cell
        if (this.papermillErrorCell) {
            this.papermillErrorCell.id = 'papermill-error-cell';
            this.papermillErrorCell = null;
        }
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
