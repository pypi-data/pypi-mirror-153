/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global, SPAN } from '../../Global';

import { Update } from '../../models/Update';
import NotebookUtils from '../../utils/NotebookUtils';

import { AnsiLink } from '../../core/AnsiLink';

interface IProps {
    source: Update[];
    autoScroll: boolean;
}

// Properties for this component
interface IState {}

export class ScrollableDiv extends React.Component<IProps, IState> {
    private readonly element: React.RefObject<HTMLInputElement>;
    
    public constructor(props: IProps) {
        super(props);
		this.element = React.createRef();
    }

    private getFormattedContents = (): JSX.Element => {
        var source: Update[] = this.props.source;
		if (source.length == 0) {
			return (<SPAN sx={{display: 'inline-block', color: 'var(--jp-ui-font-color1)'}}>No output to display</SPAN>);
		} else {
            const lines: string[] = [];
            for (let outputLine of source) {
                lines.push(outputLine.line);
            }
            var ansiText = NotebookUtils.fixOverwrittenChars(lines);
            return (
                <AnsiLink sx={{display: 'inline-block', color: 'var(--jp-ui-font-color1)'}} key={lines[0]} text={ansiText} />
            );
        }
        return (<></>);
		// return content;
	}

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');

        return (
            <DIV sx={{padding: '20px', overflow: 'auto', whiteSpace: 'pre'}} innerRef={this.element}>
                {this.getFormattedContents()}
            </DIV>
        );
    }

    public getSnapshotBeforeUpdate = (prevProps: IProps, prevState: IState): Object => {
        if (this.props.autoScroll && this.element.current != null) {
            return {
                "scrollTop": this.element.current.scrollTop,
                "scrollHeight": this.element.current.scrollHeight,
                "clientHeight": this.element.current.clientHeight
            }
        }
        return null;
	}

	public componentDidUpdate = (prevProps: IProps, prevState: IState, snapshot: any): void => {
        if (this.props.autoScroll && snapshot != null) {
            // if (this.element.current != null) {
                var element = this.element.current;
                if (snapshot.scrollTop >= snapshot.scrollHeight - snapshot.clientHeight) {
                    element.scrollTo({
                        top: element.scrollHeight - element.clientHeight,
                        behavior: 'smooth'
                    });
                }
            // }
        }
	}

    // Will be called automatically when the component is mounted
	public componentDidMount = (): void => {
        if (this.props.autoScroll) {
            var element = this.element.current;
            element.scrollTo({
                top: element.scrollHeight - element.clientHeight,
                behavior: 'auto'
            });
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
