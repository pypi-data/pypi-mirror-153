/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { DIV, Global, SPAN } from '../../../Global';

import { caretUpIcon, caretDownIcon } from '@jupyterlab/ui-components'

import DataConnectorDirListingContent from './DataConnectorDirListingContent'
import { DataConnectorMetadata } from './DataConnectorBrowser'

interface IProps {
    filter: string
    dataConnectors: DataConnectorMetadata[]
    onOpen: (dataConnector: DataConnectorMetadata) => void
    getSelected?: (getSelected: () => DataConnectorMetadata[]) => void
    handleDelete?: (dataConnectorMetadata: DataConnectorMetadata) => void
}

interface IState {
    selected: 'name' | 'dataService'
    sorted: 'forward' | 'backward'
}

export default class DataConnectorDirListing extends React.Component<IProps, IState> {
    private _isMounted = false

    constructor(props: IProps) {
        super(props)
        this.state = {
            selected: 'name',
            sorted: 'forward',
        }
    }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const sort = (a: DataConnectorMetadata, b: DataConnectorMetadata) => {
            const sortDirection = (a: any, b: any): number => a.localeCompare(b) * (this.state.sorted === 'forward' ? 1 : -1);
            if (this.state.selected === 'name') {
                if (a.name === b.name) return a.dataService.localeCompare(b.dataService);
                return sortDirection(a.name, b.name)
            } else if (this.state.selected === 'dataService') {
                if (a.dataService === b.dataService) return a.name.localeCompare(b.name);
                return sortDirection(a.dataService, b.dataService)
            }
        }
        return (
            <DIV className='jp-DirListing jp-FileBrowser-listing' sx={{overflow: 'hidden'}}>
                <DIV className='jp-DirListing-header'>
                    <DIV
                        className={'jp-DirListing-headerItem jp-id-data-service' + (this.state.selected === 'dataService' ? ' jp-mod-selected' : '')}
                        onClick={() => {
                            if (this.state.selected === 'dataService') {
                                this.safeSetState({sorted: this.state.sorted === 'forward' ? 'backward' : 'forward'})
                            } else {
                                this.safeSetState({selected: 'dataService', sorted: 'forward'})
                            }
                        }}
                        sx={{flex: '0 0 210px', textAlign: 'left', padding: '4px 12px 2px 17px'}}
                    >
                        <SPAN className='jp-DirListing-headerItemText'>
                            Data Service
                        </SPAN>
                        {this.state.selected === 'dataService' && (
                            <SPAN className='jp-DirListing-headerItemIcon' sx={{float: 'right'}}>
                                {this.state.sorted === 'forward' ? (
                                    <caretUpIcon.react container={<></> as unknown as HTMLElement} />
                                ) : (
                                    <caretDownIcon.react container={<></> as unknown as HTMLElement} />
                                )}
                            </SPAN>
                        )}
                    </DIV>
                    <DIV
                        className={'jp-DirListing-headerItem jp-id-name' + (this.state.selected === 'name' ? ' jp-mod-selected' : '')}
                        onClick={() => {
                            if (this.state.selected === 'name') {
                                this.safeSetState({sorted: this.state.sorted === 'forward' ? 'backward' : 'forward'})
                            } else {
                                this.safeSetState({selected: 'name', sorted: 'forward'})
                            }
                        }}
                        sx={{padding: '4px 12px 2px 17px'}}
                    >
                        <SPAN className='jp-DirListing-headerItemText'>
                            Name
                        </SPAN>
                        {this.state.selected === 'name' && (
                            <SPAN className='jp-DirListing-headerItemIcon' sx={{float: 'right'}}>
                                {this.state.sorted === 'forward' ? (
                                    <caretUpIcon.react container={<></> as unknown as HTMLElement} />
                                ) : (
                                    <caretDownIcon.react container={<></> as unknown as HTMLElement} />
                                )}
                            </SPAN>
                        )}
                    </DIV>
                </DIV>
                <DIV sx={{marginBottom: '6px'}} />
                <DataConnectorDirListingContent
                    filter={this.props.filter}
                    dataConnectors={this.props.dataConnectors}
                    handleDelete={this.props.handleDelete}
                    onOpen={this.props.onOpen}
                    sort={sort}
                    getSelected={this.props.getSelected}
                />
                <DIV sx={{marginBottom: '6px'}} />
            </DIV>
        )
    }

    public componentDidMount = () => {
        this._isMounted = true
    }

    public componentWillUnmount = () => {
        this._isMounted = false
    }

    private safeSetState = (map: any) => {
		if (this._isMounted) {
			let update = false
			try {
				for (const key of Object.keys(map)) {
					if (JSON.stringify(map[key]) !== JSON.stringify((this.state as any)[key])) {
						update = true
						break
					}
				}
			} catch (error) {
				update = true
			}
			if (update) {
				if (Global.shouldLogOnSafeSetState) console.log('SafeSetState (' + new Date().getSeconds() + ')');
				this.setState(map)
			} else {
				if (Global.shouldLogOnSafeSetState) console.log('SuppressedSetState (' + new Date().getSeconds() + ')');
			}
		}
	}
}