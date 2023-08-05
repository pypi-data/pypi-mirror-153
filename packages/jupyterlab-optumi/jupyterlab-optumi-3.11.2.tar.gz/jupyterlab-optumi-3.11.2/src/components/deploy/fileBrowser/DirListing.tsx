/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { DIV, Global, SPAN } from '../../../Global';

import { caretUpIcon, caretDownIcon } from '@jupyterlab/ui-components'

import DirListingContent from './DirListingContent'
import { FileMetadata } from './FileBrowser'

interface IProps {
    filter: string
    files: FileMetadata[]
    getSelected?: (getSelected: () => FileMetadata[]) => void
    onOpen: (file: FileMetadata) => void
    onDownload?: (file: FileMetadata) => void
    onDelete?: (file: FileMetadata) => void
}

interface IState {
    selected: 'name' | 'modified'
    sorted: 'forward' | 'backward'
}

export default class DirListing extends React.Component<IProps, IState> {
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
        const sort = (a: FileMetadata, b: FileMetadata) => {
            if (a.type !== b.type && (a.type === 'directory' || b.type === 'directory')) return a.type.localeCompare(b.type);
            const sortDirection = (a: any, b: any): number => a.localeCompare(b) * (this.state.sorted === 'forward' ? 1 : -1);

            if (this.state.selected === 'name') {
                return sortDirection(a.name, b.name)
            } else if (this.state.selected === 'modified') {
                return sortDirection(b.last_modified, a.last_modified)
            }
        }
        return (
            <DIV className='jp-DirListing jp-FileBrowser-listing' sx={{overflow: 'hidden'}}>
                <DIV className='jp-DirListing-header'>
                    <DIV
                        className={'jp-DirListing-headerItem jp-id-name' + (this.state.selected === 'name' ? ' jp-mod-selected' : '')}
                        onClick={() => {
                            if (this.state.selected === 'name') {
                                this.safeSetState({sorted: this.state.sorted === 'forward' ? 'backward' : 'forward'})
                            } else {
                                this.safeSetState({selected: 'name', sorted: 'forward'})
                            }
                        }}
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
                    <DIV
                        className={'jp-DirListing-headerItem jp-id-modified' + (this.state.selected === 'modified' ? ' jp-mod-selected' : '')}
                        onClick={() => {
                            if (this.state.selected === 'modified') {
                                this.safeSetState({sorted: this.state.sorted === 'forward' ? 'backward' : 'forward'})
                            } else {
                                this.safeSetState({selected: 'modified', sorted: 'forward'})
                            }
                        }}
                        style={{flex: '0 0 150px'}}
                    >
                        <SPAN className='jp-DirListing-headerItemText'>
                            Last Modified
                        </SPAN>
                        {this.state.selected === 'modified' && (
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
                <DirListingContent
                    filter={this.props.filter}
                    files={this.props.files}
                    onOpen={this.props.onOpen}
                    sort={sort}
                    getSelected={this.props.getSelected}
                    onDownload={this.props.onDownload}
                    onDelete={this.props.onDelete}
                />
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
