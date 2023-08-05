/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { Colors } from '../../../Colors';
import { Global, UL } from '../../../Global';

import { DataConnectorMetadata } from './DataConnectorBrowser'
import DataConnectorDirListingItem from './DataConnectorDirListingItem'
import { DataService } from './DataConnectorDirListingItemIcon'

interface IProps {
    filter: string
    dataConnectors: DataConnectorMetadata[]
    onOpen: (dataConnector: DataConnectorMetadata) => void
    sort: (a: DataConnectorMetadata, b: DataConnectorMetadata) => number
    getSelected?: (getSelected: () => DataConnectorMetadata[]) => void
    handleDelete?: (dataConnectorMetadata: DataConnectorMetadata) => void
}

interface IState {
    selected: DataConnectorMetadata[]
}

export default class DataConnectorDirListingContent extends React.Component<IProps, IState> {
    private _isMounted = false

    firstClicked: DataConnectorMetadata // Pressing enter operates on this file
    lastClicked: DataConnectorMetadata

    constructor(props: IProps) {
        super(props)
        if (this.props.getSelected) this.props.getSelected(() => this.state.selected);
        this.state = {
            selected: []
        }
    }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        // The code in the RegExp converts 'tom' into '^[^t]*t[^o]*o[^m]*m.*$' which matches strings where those characters appear in that order while only checking each character once during the match for efficiency
        const filter = (dataConnector: DataConnectorMetadata) => dataConnector.name.replace(new RegExp('^' + this.props.filter.replace(/(.)/gi, '[^$1]*$1') + '.*$', 'i'), '').length === 0;
        const sortedDataConnectors = this.props.dataConnectors.filter(filter).sort(this.props.sort)
        return (
            <UL className='jp-DirListing-content' sx={{overflowY: 'auto'}}>
                {sortedDataConnectors.length == 0 ? (
                    <>
                        <DataConnectorDirListingItem
                            key={'empty'}
                            dataConnectorMetadata={{
                                name: '--',
                                dataService: DataService.EMPTY,
                            } as DataConnectorMetadata}
                            selected={false}
                            onClick={() => false}
                            onDoubleClick={() => false}
                        />
                    </>
                ) : (
                    <>
                        {sortedDataConnectors.map(dataConnector => (
                            <DataConnectorDirListingItem
                                key={dataConnector.path + dataConnector.name}
                                dataConnectorMetadata={dataConnector}
                                selected={this.state.selected.includes(dataConnector)}
                                handleButtonClick={this.props.handleDelete}
                                buttonText='Delete'
                                buttonColor={Colors.ERROR}
                                onClick={(event: React.MouseEvent<HTMLLIElement, MouseEvent>) => {
                                    if (this.props.getSelected === undefined) return; // If someone doesn't want what is selected, don't select.
                                    if (this.firstClicked === undefined) {
                                        if (event.shiftKey) {
                                            this.firstClicked = sortedDataConnectors[0]
                                            this.lastClicked = sortedDataConnectors[0]
                                        } else {
                                            this.firstClicked = dataConnector
                                        }
                                    }
                                    if (event.ctrlKey) {
                                        const newSelected = [...this.state.selected]
                                        if (newSelected.includes(dataConnector)) {
                                            newSelected.splice(newSelected.indexOf(dataConnector), 1)
                                        } else {
                                            newSelected.push(dataConnector)
                                        }
                                        this.safeSetState({selected: newSelected})
                                        this.lastClicked = dataConnector
                                    } else if (event.shiftKey) {
                                        const newSelected = [...this.state.selected]
                                        let index = sortedDataConnectors.indexOf(dataConnector)
                                        const lastClickedIndex = sortedDataConnectors.indexOf(this.lastClicked)
                                        const direction = index < lastClickedIndex ? 1 : -1
                                        while (!newSelected.includes(sortedDataConnectors[index]) && index !== lastClickedIndex) {
                                            newSelected.push(sortedDataConnectors[index])
                                            index += direction
                                        }
                                        if (index === lastClickedIndex && !newSelected.includes(this.lastClicked)) newSelected.push(this.lastClicked);
                                        this.safeSetState({selected: newSelected})
                                    } else {
                                        this.safeSetState({selected: [dataConnector]})
                                        this.firstClicked = dataConnector
                                        this.lastClicked = dataConnector
                                    }
                                }}
                                onDoubleClick={(event: React.MouseEvent<HTMLLIElement, MouseEvent>) => {
                                    if (!event.ctrlKey && !event.shiftKey) this.props.onOpen(dataConnector);
                                }}
                            />
                        ))}
                    </>
                )}
            </UL>
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