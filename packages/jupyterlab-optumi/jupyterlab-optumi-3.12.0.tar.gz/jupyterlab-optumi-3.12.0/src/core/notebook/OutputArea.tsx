/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { DIV, Global } from '../../Global';

import * as nbformat from '@jupyterlab/nbformat';

import { AnsiLink } from '../AnsiLink';

interface IProps {
    cell: any
    metadata: any
}

interface IState {}

export default class OutputArea extends React.Component<IProps, IState> {

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <DIV className='p-Widget lm-Widget jp-Cell-outputWrapper'>
                <DIV className='p-Widget lm-Widget jp-OutputArea jp-Cell-outputArea'>
                    <DIV className='p-Widget lm-Widget jp-OutputArea-child'>
                        <DIV className='p-Widget lm-Widget jp-OutputPrompt jp-OutputArea-prompt' />
                        {/* This extra div stops the out/err groups rendering as columns */}
                        <DIV sx={{display: 'block', width: '100%'}}>
                            {this.props.cell.outputs.map((output: any) => (
                                <DIV key={hashString(JSON.stringify(output))}>
                                    {(() => {
                                        var output_type = output.output_type as nbformat.OutputType;
                                        switch (output_type) {
                                            case "stream":
                                                return (
                                                    <DIV data-mime-type={output.name === 'stderr' ? 'application/vnd.jupyter.stderr' : 'application/vnd.jupyter.stdout'} className='p-Widget lm-Widget jp-RenderedText jp-OutputArea-output'>
                                                        <AnsiLink text={output.text} />
                                                    </DIV>
                                                )
                                            case "error":
                                                return (
                                                    <DIV data-mime-type={'application/vnd.jupyter.stderr'} className='p-Widget lm-Widget jp-RenderedText jp-OutputArea-output'>
                                                        {output.traceback.map((line: string) => (
                                                            <AnsiLink key={hashString(line)} text={line} />
                                                        ))}
                                                    </DIV>
                                                )
                                            case "execute_result":
                                                // Let this fall through to display data because
                                                // "Results of an execution are published as an execute_result. These are identical to display_data messages, with the addition of an execution_count key." - Jupyter messaging docs
                                            case "display_data":
                                                for (var firstPass = 0; firstPass < 2; firstPass++) {
                                                    for (var type in output.data) {
                                                        // We want to show the rich output, so only look at text/plain if that is the only data_type
                                                        if (firstPass == 0 && type == 'text/plain') continue;
                                                        return (
                                                            <DIV>
                                                                {type === 'text/html' ? (
                                                                    <DIV data-mime-type={type} className='p-Widget lm-Widget jp-RenderedHTMLCommon jp-RenderedHTML jp-OutputArea-output'>
                                                                        <DIV dangerouslySetInnerHTML={{ __html: output.data[type] }} />
                                                                    </DIV>
                                                                ) : type.startsWith('image/') ? (
                                                                    <DIV data-mime-type={type} className='p-Widget lm-Widget jp-RenderedImage jp-OutputArea-output'>
                                                                        <img src={"data:" + type + ";base64," + output.data[type]} className="jp-needs-light-background" />
                                                                    </DIV>
                                                                ) : type === 'text/plain' ? (
                                                                    <DIV data-mime-type={output.data[type]} className='p-Widget lm-Widget jp-RenderedText jp-OutputArea-output'>
                                                                        <pre>
                                                                            {output.data[type]}
                                                                        </pre>
                                                                    </DIV>
                                                                ) : (
                                                                    <></>
                                                                )}
                                                            </DIV>
                                                        )
                                                    }
                                                }
                                                // Note: this can fall through
                                            case "update_display_data":
                                                // I don't know what to do with this type, but i'm hoping we don't need to handle it
                                                return (<></>)
                                        }
                                    })()}
                                </DIV>
                            ))}
                        </DIV>
                    </DIV>
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

function hashString(toHash: string) {
	var hash = 0, i, chr;
	if (toHash.length === 0) return hash;
	for (i = 0; i < toHash.length; i++) {
		chr = toHash.charCodeAt(i);
		hash = ((hash << 5) - hash) + chr;
		hash |= 0; // Convert to 32bit integer
	}
	return hash;
};
