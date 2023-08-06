/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { Colors } from '../../../Colors';
import { Global, UL } from '../../../Global';

import { IntegrationMetadata, IntegrationType } from './IntegrationBrowser'
import IntegrationDirListingItem from './IntegrationDirListingItem'

interface IProps {
    filter: string
    integrations: IntegrationMetadata[]
    onOpen: (integration: IntegrationMetadata) => void
    sort: (a: IntegrationMetadata, b: IntegrationMetadata) => number
    getSelected?: (getSelected: () => IntegrationMetadata[]) => void
    handleDelete?: (integrationMetadata: IntegrationMetadata) => void
}

interface IState {
    selected: IntegrationMetadata[]
}

export default class IntegrationDirListingContent extends React.Component<IProps, IState> {
    private _isMounted = false

    firstClicked: IntegrationMetadata // Pressing enter operates on this file
    lastClicked: IntegrationMetadata

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
        const filter = (integration: IntegrationMetadata) => integration.name.replace(new RegExp('^' + this.props.filter.replace(/(.)/gi, '[^$1]*$1') + '.*$', 'i'), '').length === 0;
        const sortedIntegrations = this.props.integrations.filter(filter).sort(this.props.sort)
        return (
            <UL className='jp-DirListing-content' sx={{overflowY: 'auto'}}>
                {sortedIntegrations.length == 0 ? (
                    <>
                        <IntegrationDirListingItem
                            key={'empty'}
                            integrationMetadata={{
                                name: '--',
                                integrationType: IntegrationType.NONE,
                            } as IntegrationMetadata}
                            selected={false}
                            onClick={() => false}
                            onDoubleClick={() => false}
                        />
                    </>
                ) : (
                    <>
                        {sortedIntegrations.map(integration => (
                            <IntegrationDirListingItem
                                key={integration.path + integration.name}
                                integrationMetadata={integration}
                                selected={this.state.selected.includes(integration)}
                                handleButtonClick={this.props.handleDelete}
                                buttonText='Delete'
                                buttonColor={Colors.ERROR}
                                onClick={(event: React.MouseEvent<HTMLLIElement, MouseEvent>) => {
                                    if (this.props.getSelected === undefined) return; // If someone doesn't want what is selected, don't select.
                                    if (this.firstClicked === undefined) {
                                        if (event.shiftKey) {
                                            this.firstClicked = sortedIntegrations[0]
                                            this.lastClicked = sortedIntegrations[0]
                                        } else {
                                            this.firstClicked = integration
                                        }
                                    }
                                    if (event.ctrlKey) {
                                        const newSelected = [...this.state.selected]
                                        if (newSelected.includes(integration)) {
                                            newSelected.splice(newSelected.indexOf(integration), 1)
                                        } else {
                                            newSelected.push(integration)
                                        }
                                        this.safeSetState({selected: newSelected})
                                        this.lastClicked = integration
                                    } else if (event.shiftKey) {
                                        const newSelected = [...this.state.selected]
                                        let index = sortedIntegrations.indexOf(integration)
                                        const lastClickedIndex = sortedIntegrations.indexOf(this.lastClicked)
                                        const direction = index < lastClickedIndex ? 1 : -1
                                        while (!newSelected.includes(sortedIntegrations[index]) && index !== lastClickedIndex) {
                                            newSelected.push(sortedIntegrations[index])
                                            index += direction
                                        }
                                        if (index === lastClickedIndex && !newSelected.includes(this.lastClicked)) newSelected.push(this.lastClicked);
                                        this.safeSetState({selected: newSelected})
                                    } else {
                                        this.safeSetState({selected: [integration]})
                                        this.firstClicked = integration
                                        this.lastClicked = integration
                                    }
                                }}
                                onDoubleClick={(event: React.MouseEvent<HTMLLIElement, MouseEvent>) => {
                                    if (!event.ctrlKey && !event.shiftKey) this.props.onOpen(integration);
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