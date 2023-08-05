/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global, StyledMenuItem, StyledSelect } from '../../../Global';

import { SxProps, Theme } from '@mui/system';
import { SelectChangeEvent } from '@mui/material';

import { GraphicsConfig } from '../../../models/GraphicsConfig';
import { OptumiMetadataTracker } from '../../../models/OptumiMetadataTracker';

interface IProps {
    sx?: SxProps<Theme>,
}

interface IState {
    selectedCard: string
}

export class GraphicsEquipment extends React.Component<IProps, IState> {
    private _isMounted = false

    constructor(props: IProps) {
        super(props);
        var card = this.getCardValue();
        card = Global.user.machines.graphicsCards.includes(card) ? card : 'U';
        this.state = {
            selectedCard: card,
        }
        this.saveCardValue(this.state.selectedCard);
    }
    
    private getCardValue(): string {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const graphics: GraphicsConfig = optumi.config.graphics;
        return graphics.boardType;
	}

	private async saveCardValue(value: string) {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const graphics: GraphicsConfig = optumi.config.graphics;
        graphics.boardType = value;
        tracker.setMetadata(optumi);
    }
    


    private handleCardChange = (event: SelectChangeEvent<unknown>, child: React.ReactNode) => {
        const value: string = event.target.value as string;
        this.safeSetState({ selectedCard: value });
        this.saveCardValue(value);
    }

    private getCardItems = (): JSX.Element[] => {
        var cardItems: JSX.Element[] = new Array();
        cardItems.push(<StyledMenuItem key={'U'} value={'U'}>Any</StyledMenuItem>)
        const availableCards = Global.user.machines.graphicsCards;
        for (var i = 0; i < availableCards.length; i++) {
            var value = availableCards[i]
            cardItems.push(<StyledMenuItem key={value} value={value}>{value}</StyledMenuItem>)
        }
        return cardItems;
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <DIV sx={{display: 'inline-flex', width: '100%', padding: '3px 0px'}}>
                {/* <DIV 
                    sx={{
                    minWidth: '68px',
                    lineHeight: '24px',
                    textAlign: 'center',
                    margin: '0px 6px',
                }}/> */}
                <DIV sx={{display: 'inline-flex', width: '100%', justifyContent: 'center'}}>
                    <DIV sx={{padding: '0px 6px 0px 6px'}}>
                        <StyledSelect
                            value={this.state.selectedCard}
                            variant='outlined'
                            onChange={this.handleCardChange}
                            SelectDisplayProps={{style: {padding: '3px 20px 3px 6px'}}}
                            MenuProps={{MenuListProps: {style: {paddingTop: '6px', paddingBottom: '6px'}}}}
                        >
                            {this.getCardItems()}
                        </StyledSelect>
                    </DIV>
                </DIV>               
                <DIV 
                    // title={this.props.tooltip || ''}
                    sx={{
                    minWidth: '68px',
                    lineHeight: '24px',
                    textAlign: 'center',
                    margin: '0px 6px',
                }}>
                    {'Cards'}
                </DIV>
            </DIV>
        )
    }

    private handleMetadataChange = () => { this.forceUpdate() }

    // Will be called automatically when the component is mounted
	public componentDidMount = () => {
        this._isMounted = true
		Global.metadata.getMetadataChanged().connect(this.handleMetadataChange);
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
		Global.metadata.getMetadataChanged().disconnect(this.handleMetadataChange);
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
