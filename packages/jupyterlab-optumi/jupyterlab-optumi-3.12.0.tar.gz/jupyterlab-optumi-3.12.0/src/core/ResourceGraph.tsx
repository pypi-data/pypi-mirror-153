/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { Global } from '../Global';

import { Update } from '../models/Update';
import { App } from '../models/application/App';
import FormatUtils from '../utils/FormatUtils';

import Plotly, { Datum, PlotData } from 'plotly.js'
import Plot, { Figure } from 'react-plotly.js';
import { Colors } from '../Colors';

interface IProps {
    app: App
}

interface DataState {
    cell_starts: Date[]
    cell_ends: Date[]
    showCells: boolean
    xAxisAuto: boolean
    xAxisMin: Date
    xAxisMax: Date
}

interface PlotlyState {
    revision: number,
    data: Plotly.Data[]
    layout: Partial<Plotly.Layout>
    config: Partial<Plotly.Config>
}

interface IState extends DataState, PlotlyState {}

export class ResourceGraph extends React.Component<IProps, IState> {
    private _isMounted = false

    constructor(props: IProps) {
        super(props)
        this.state = {
            revision: 0,
            cell_starts: [],
            cell_ends: [],
            showCells: true,
            data: [],
            layout: {},
            config: {},
            xAxisAuto: true,
            xAxisMin: null,
            xAxisMax: null,
        }
    }

    public updateCellTimes = (state: Partial<IState>) => {
        if (!this.props.app.interactive) {
            state.cell_starts.splice(0, state.cell_starts.length);
            state.cell_ends.splice(0, state.cell_ends.length);
            for (let cell of this.props.app.notebook['cells']) {
                if (cell.cell_type === 'code') {
                    const metadata = cell['metadata'];
                    if (metadata) {
                        const papermill = metadata['papermill'];
                        if (papermill) {
                            if (papermill['start_time']) {
                                state.cell_starts.push(new Date(papermill['start_time'] + 'Z'));
                            }
                            if (papermill['end_time']) {
                                state.cell_ends.push(new Date(papermill['end_time'] + 'Z'));
                            }
                        }
                    }
                }
            }
        }
        this.updateLayout(state);
        this.updateCellTraces(state);
    }

    public updateResources = (state: Partial<IState>, update: Update, skipUpdateCellTimes?: boolean) => {
        const sampleString = update.line;
        if (sampleString.length === 0) return
        let sample = sampleString.split('|');
        const time = new Date(update.modifier);
        for (let i = 0; i < 21; i++) {
            ((state.data[i] as PlotData).x as Datum[]).push(time);
            ((state.data[i] as PlotData).y as Datum[]).push(+sample[20-i]);
        }
        if (state.xAxisAuto) {
            state.xAxisMin = ((state.data[0] as PlotData).x[0] as Date);
            state.xAxisMax = ((state.data[0] as PlotData).x[(state.data[0] as PlotData).x.length-1] as Date);
        }

        if (skipUpdateCellTimes !== true) this.updateCellTimes(state);
    }

    private updateCellTraces = (state: Partial<IState>) => {
        const x = []
        const y1 = []
        const y2 = []
        const text1 = []
        const text2 = []
        const xAxisMin = new Date(state.xAxisMin)
        const xAxisMax = new Date(state.xAxisMax)
        const totalDuration = xAxisMax.getTime() - xAxisMin.getTime();
        for (let i = 0; i < state.cell_starts.length; i++) {
            if (state.cell_ends.length > i) {
                var cell_start = new Date(state.cell_starts[i]);
                var cell_end = new Date(state.cell_ends[i]);
                const duration = cell_end.getTime() - cell_start.getTime();
                x.push(new Date(cell_start.getTime() + (duration / 2)));
                y1.push(95);
                y2.push(90);
                if (cell_start.getTime() < xAxisMax.getTime() && cell_end.getTime() > xAxisMin.getTime()) {
                    if (duration / totalDuration > 0.05) {
                        text1.push('Cell ' + (i + 1));
                        text2.push(FormatUtils.msToTime(duration));
                    } else {
                        text1.push('');
                        text2.push('');
                    }
                } else {
                    text1.push('');
                    text2.push('');
                }
            }
        };
        state.data.splice(-2, 2);
        state.data = state.data.concat([{ x: x, y: y1, text: text1, mode: 'text', textposition: 'middle center', name: 'CELLS', legendgroup: 'CELLS', hoverinfo: 'none' }, { x: x, y: y2, text: text2, mode: 'text', textposition: 'middle center', legendgroup: 'CELLS', showlegend: false, hoverinfo: 'none' }])
    }

    private updateLayout = (state: Partial<IState>) => {
        const shapes = state.showCells ?
        state.cell_ends.map((x, i) =>
            ({
                type: 'rect',
                x0: state.cell_starts[i],
                y0: 0,
                x1: x,
                y1: 100,
                line: {
                    color: 'rgba(0, 0, 0, 0.5)',
                    width: 1,
                },
            } as Partial<Plotly.Shape>)
        ) : [];
        state.layout = {
            shapes: shapes,
            xaxis: {
                title: 'Time',
                range: [state.xAxisMin, state.xAxisMax]
            },
            yaxis: {
                title: 'Resource Utilization (%)',
                range: [0, 100],
                fixedrange: true,
            },
            legend: {
                traceorder: 'reversed',
            },
        }
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <Plot
                divId={this.props.app.uuid + '-graph'}
                style={{width: '100%', height: '100%'}}
                key={this.props.app.uuid + '-graph'}
                data={this.state.data}
                layout={this.state.layout}
                config={this.state.config}
                onInitialized={(figure: Readonly<Figure>, graphDiv: Readonly<HTMLElement>) => this.setState({data: figure.data, layout: figure.layout})}
                onUpdate={(figure: Readonly<Figure>, graphDiv: Readonly<HTMLElement>) => this.setState({data: figure.data, layout: figure.layout})}
                onRestyle={(event: Readonly<Plotly.PlotRestyleEvent>) => {
                    for (let i = 0; i < event[1].length; i++) {
                        if (event[1][i] == 21) {
                            const newState: Partial<IState> = this.cloneState(this.state);
                            newState.showCells = event[0].visible[i] === true;
                            this.updateLayout(newState);
                            newState.revision++;
                            this.safeSetState(newState);
                            break;
                        }
                    }
                }}
                onRelayout={(event: Readonly<Plotly.PlotRelayoutEvent>) => {
                    if (event['xaxis.autorange']) {
                        const newState: Partial<IState> = this.cloneState(this.state);
                        newState.xAxisAuto = true;
                        newState.xAxisMin = ((newState.data[0] as PlotData).x[0] as Date);
                        newState.xAxisMax = ((newState.data[0] as PlotData).x[(newState.data[0] as PlotData).x.length-1] as Date);
                        this.updateLayout(newState);
                        this.updateCellTraces(newState);
                        newState.revision++;
                        this.safeSetState(newState);                        
                    } else if (event['xaxis.range[0]'] || event['xaxis.range[1]']) {
                        const newState: Partial<IState> = this.cloneState(this.state);
                        newState.xAxisAuto = false;
                        newState.xAxisMin = new Date(event['xaxis.range[0]']);
                        newState.xAxisMax = new Date(event['xaxis.range[1]']);
                        this.updateLayout(newState);
                        this.updateCellTraces(newState);
                        newState.revision++;
                        this.safeSetState(newState); 
                    }
                }}
            />
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

    private safeSetState = (map: any) => {
        if (this._isMounted) {
            if (Global.shouldLogOnSafeSetState) console.log('SafeSetState (' + new Date().getSeconds() + ')');
            this.setState(map)
        }
    }

    private handleResourceChange = (update: Update) => {
        const newState: Partial<IState> = this.cloneState(this.state);
        this.updateResources(newState, update);
        newState.revision++;
        this.safeSetState(newState);
    }

    // We need this to clone the state including dates
    private cloneState = (state: IState): IState => {
        const newState = JSON.parse(JSON.stringify(state));
        for (let data of newState.data) {
            data.x = data.x.map((x: string) => new Date(x));
        }
        newState.cell_starts = newState.cell_starts.map((x: string) => new Date(x));
        newState.cell_ends = newState.cell_ends.map((x: string) => new Date(x));
        newState.xAxisMin = new Date(newState.xAxisMin);
        newState.xAxisMax = new Date(newState.xAxisMax);
        return newState;
    }

    public componentDidMount = () => {
        this._isMounted = true
        let newState: Partial<IState> = {
            data: [
                { x: [], y: [], mode: 'lines', type: 'scatter', line: { shape: 'spline', width: 0 }, name: 'NET max', hoverinfo: 'none', legendgroup: 'NET', showlegend: false },
                { x: [], y: [], mode: 'lines', type: 'scatter', line: { shape: 'spline', color: Colors.NETWORK }, fill: 'tonexty', fillcolor: Colors.NETWORK + '60', name: 'NET', legendgroup: 'NET' },
                { x: [], y: [], mode: 'lines', type: 'scatter', line: { shape: 'spline', width: 0 }, fill: 'tonexty', fillcolor: Colors.NETWORK + '60', name: 'NET min', hoverinfo: 'none', legendgroup: 'NET', showlegend: false },

                { x: [], y: [], mode: 'lines', type: 'scatter', line: { shape: 'spline', width: 0 }, name: 'DISK max', hoverinfo: 'none', legendgroup: 'DISK', showlegend: false },
                { x: [], y: [], mode: 'lines', type: 'scatter', line: { shape: 'spline', color: Colors.DISK }, fill: 'tonexty', fillcolor: Colors.DISK + '60', name: 'DISK', legendgroup: 'DISK' },
                { x: [], y: [], mode: 'lines', type: 'scatter', line: { shape: 'spline', width: 0 }, fill: 'tonexty', fillcolor: Colors.DISK + '60', name: 'DISK min', hoverinfo: 'none', legendgroup: 'DISK', showlegend: false },
                
                { x: [], y: [], mode: 'lines', type: 'scatter', line: { shape: 'spline', width: 0 }, name: 'SWAP max', hoverinfo: 'none', legendgroup: 'SWAP', showlegend: false },
                { x: [], y: [], mode: 'lines', type: 'scatter', line: { shape: 'spline', color: Colors.SWAP }, fill: 'tonexty', fillcolor: Colors.SWAP + '60', name: 'SWAP', legendgroup: 'SWAP' },
                { x: [], y: [], mode: 'lines', type: 'scatter', line: { shape: 'spline', width: 0 }, fill: 'tonexty', fillcolor: Colors.SWAP + '60', name: 'SWAP min', hoverinfo: 'none', legendgroup: 'SWAP', showlegend: false },

                { x: [], y: [], mode: 'lines', type: 'scatter', line: { shape: 'spline', width: 0 }, name: 'RAM max', hoverinfo: 'none', legendgroup: 'RAM', showlegend: false },
                { x: [], y: [], mode: 'lines', type: 'scatter', line: { shape: 'spline', color: Colors.RAM }, fill: 'tonexty', fillcolor: Colors.RAM + '60', name: 'RAM', legendgroup: 'RAM' },
                { x: [], y: [], mode: 'lines', type: 'scatter', line: { shape: 'spline', width: 0 }, fill: 'tonexty', fillcolor: Colors.RAM + '60', name: 'RAM min', hoverinfo: 'none', legendgroup: 'RAM', showlegend: false },
                
                { x: [], y: [], mode: 'lines', type: 'scatter', line: { shape: 'spline', width: 0 }, name: 'CPU max', hoverinfo: 'none', legendgroup: 'CPU', showlegend: false },
                { x: [], y: [], mode: 'lines', type: 'scatter', line: { shape: 'spline', color: Colors.CPU }, fill: 'tonexty', fillcolor: Colors.CPU + '60', name: 'CPU', legendgroup: 'CPU' },
                { x: [], y: [], mode: 'lines', type: 'scatter', line: { shape: 'spline', width: 0 }, fill: 'tonexty', fillcolor: Colors.CPU + '60', name: 'CPU min', hoverinfo: 'none', legendgroup: 'CPU', showlegend: false },
                
                { x: [], y: [], mode: 'lines', type: 'scatter', line: { shape: 'spline', width: 0 }, name: 'VRAM max', hoverinfo: 'none', legendgroup: 'VRAM', showlegend: false },
                { x: [], y: [], mode: 'lines', type: 'scatter', line: { shape: 'spline', color: Colors.VRAM }, fill: 'tonexty', fillcolor: Colors.VRAM + '60', name: 'VRAM', legendgroup: 'VRAM' },
                { x: [], y: [], mode: 'lines', type: 'scatter', line: { shape: 'spline', width: 0 }, fill: 'tonexty', fillcolor: Colors.VRAM + '60', name: 'VRAM min', hoverinfo: 'none', legendgroup: 'VRAM', showlegend: false },
                

                { x: [], y: [], mode: 'lines', type: 'scatter', line: { shape: 'spline', width: 0 }, name: 'GPU max', hoverinfo: 'none', legendgroup: 'GPU', showlegend: false },
                { x: [], y: [], mode: 'lines', type: 'scatter', line: { shape: 'spline', color: Colors.GPU }, fill: 'tonexty', fillcolor: Colors.GPU + '60', name: 'GPU', legendgroup: 'GPU' },
                { x: [], y: [], mode: 'lines', type: 'scatter', line: { shape: 'spline', width: 0 }, fill: 'tonexty', fillcolor: Colors.GPU + '60', name: 'GPU min', hoverinfo: 'none', legendgroup: 'GPU', showlegend: false },
                
                { /* This empty entry is needed */ },
                { /* This empty entry is needed */ },
            ],
            layout: {},
            config: {
                toImageButtonOptions: {
                    filename: this.props.app.uuid,
                    format: 'png',
                    height: 1000,
                    width: 3000,
                },
                responsive: true,
                displaylogo: false,
                modeBarButtonsToRemove: [
                    'lasso2d',
                    'select2d',
                    'resetScale2d',
                    'toggleSpikelines',
                    'hoverClosestCartesian',
                    'hoverCompareCartesian',
                ]
            },
            cell_starts: [],
            cell_ends: [],
            showCells: true,
            xAxisAuto: true,
        }

        // const numSamples = this.props.app.modules[0].monitoring.length;
        // const jump = Math.ceil(numSamples / 500);
        // for (let i = 0; i < (numSamples-jump); i+=jump) {
        //     const sample = this.props.app.modules[0].monitoring[i]
        //     this.updateResources(newState, sample, true)
        // }

        for (let sample of this.props.app.modules[0].monitoring) {
            this.updateResources(newState, sample, true)
        }
        this.updateCellTimes(newState);
        newState.xAxisMin = ((newState.data[0] as PlotData).x[0] as Date);
        newState.xAxisMax = ((newState.data[0] as PlotData).x[(newState.data[0] as PlotData).x.length-1] as Date);
        
        this.safeSetState(newState);
        this.props.app.modules[0].addUpdateCallback(this.handleResourceChange)
    }

    public componentWillUnmount = () => {
        this.props.app.modules[0].removeUpdateCallback(this.handleResourceChange)
        this._isMounted = false
    }
}
