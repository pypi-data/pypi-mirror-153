/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { DIV, Global, SPAN, StyledMenuItem, StyledSelect } from '../../Global';

import { SelectChangeEvent } from '@mui/material';

import { OptumiMetadataTracker } from '../../models/OptumiMetadataTracker';
import { GraphicsConfig } from '../../models/GraphicsConfig';
import { ChipPopper } from '../ChipPopper';
import { ChipSlider } from '../ChipSlider';
import { Expertise } from '../../models/OptumiConfig';
import FormatUtils from '../../utils/FormatUtils';
import { Switch } from '../../core';
import { Colors } from '../../Colors';

interface IProps {}

interface IState {
    open: boolean
    selectedCard: string
}

export class GPUChipPopper extends React.Component<IProps, IState> {
    _isMounted = false;

    public constructor(props: IProps) {
        super(props)
        var card = this.getCardValue();
        // TODO:JJ Get this list of valid names/numbers from the available graphics cards
        card = Global.user.machines.graphicsCards.includes(card) ? card : 'U';
        this.state = {
            open: false,
            selectedCard: card,
        }
        this.saveCardValue(this.state.selectedCard);
    }

    private getMinMaxMemory = () => {
        const cardValue = this.getCardValue();
        const machines = Global.user.machines;
        if (cardValue == 'U') return [machines.graphicsMemoryMin, machines.graphicsMemoryMax];
        return [machines.getGraphicsMemoryByCardMin(cardValue), machines.getGraphicsMemoryByCardMax(cardValue)];
    }

    private getHeaderDescription = (): string => {
        const required = this.getRequiredValue();
        if (!required) return `Any`;

        const cardValue = this.getCardValue();
        var cardDesc = cardValue == 'U' ? '' : cardValue;

        const minMax = this.getMinMaxMemory();

        const min = minMax[0];
        const max = minMax[1];
        const styleUnit = FormatUtils.styleCapacityUnit();
        const styleValue = FormatUtils.styleShortCapacityValue();
        const value = [...this.getRAMValue()];
        var ramDesc = '';
        if (value[0] == -1) value[0] = min;
        if (value[1] == -1) value[1] = max;
        if (value[0] === min && value[1] === max) {
            // Do nothing
        } else if (value[0] !== min && value[1] !== max) {
            const maxUnit = styleUnit(value[1]);
            const minValue = styleValue(value[0], maxUnit)
            const maxValue = styleValue(value[1])
            if (minValue == maxValue) ramDesc = `${minValue} ${styleUnit(value[1])}`
            else ramDesc = `${minValue}-${maxValue} ${styleUnit(value[1])}`
        } else if (value[0] !== min) {
            ramDesc = `Min ${styleValue(value[0])} ${styleUnit(value[0])}`
        } else if (value[1] !== max) {
            ramDesc = `Max ${styleValue(value[1])} ${styleUnit(value[1])}`
        }
        if (!(cardDesc || ramDesc)) return 'Required';
        if (cardDesc && ramDesc) return cardDesc + ', ' + ramDesc;
        return cardDesc + ramDesc;
    }

    public getChipDescription = () => {
        var desc = this.getHeaderDescription()
        if (desc.includes(',')) return desc.replace(',', ':');
        return 'GPU: ' + desc;
    }

    private getRequiredValue(): boolean {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const graphics: GraphicsConfig = optumi.config.graphics;
        // TODO:JJ This is kind of hacky
        return graphics.cores[0] != -1;
	}

	private async saveRequiredValue(value: boolean) {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const graphics: GraphicsConfig = optumi.config.graphics;
        graphics.expertise = Expertise.SIMPLIFIED;
        if (value) {
            // TODO:JJ This is kind of hacky
            graphics.cores = [1, -1, -1];
        } else {
            // TODO:JJ This is kind of hacky
            graphics.cores = [-1, -1, -1];
            graphics.boardType = 'U';
            graphics.memory = [-1, -1, -1];
        }
        tracker.setMetadata(optumi);
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
        if (graphics.boardType == value) return;
        graphics.expertise = Expertise.SIMPLIFIED;
        graphics.boardType = value;
        // const machines = Global.user.machines;
        // const min = machines.getGraphicsMemoryByCardMin(value);
        // const max = machines.getGraphicsMemoryByCardMax(value);
        // TODO:JJ Do this for more than just memory
        // if (graphics.memory[0] != -1 && graphics.memory[0] < min) graphics.memory[0] = -1;
        // if (graphics.memory[2] != -1 && graphics.memory[2] < min) graphics.memory[2] = -1;
        // if (graphics.memory[0] > max) graphics.memory[0] = -1;
        // if (graphics.memory[2] > max) graphics.memory[2] = -1;
        graphics.memory[0] = -1;
        graphics.memory[2] = -1;
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

    private getRAMValue(): number[] {
        const tracker: OptumiMetadataTracker = Global.metadata;
		const optumi = tracker.getMetadata();
        const size = optumi.config.graphics.memory;
		return [size[0], size[2]]
	}

	private saveRAMValue(value: number[]) {
        const tracker: OptumiMetadataTracker = Global.metadata;
		const optumi = tracker.getMetadata();
        optumi.config.graphics.expertise = Expertise.SIMPLIFIED;
        optumi.config.graphics.memory = [value[0], -1, value[1]];
        tracker.setMetadata(optumi);
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const required = this.getRequiredValue();
        const minMaxMemory = this.getMinMaxMemory();
		return (
            <ChipPopper
                sx={{width: 'calc(50% - 12px)', margin: '0px 6px 6px'}}
                title='GPU'
                color={Colors.GPU}
                clearValue={() => {
                    this.saveRequiredValue(false);
                }}
                getChipDescription={this.getChipDescription}
                getHeaderDescription={this.getHeaderDescription}
                popperContent={
                    <DIV sx={{
                        display: 'flex',
                        flexDirection: 'column',
                    }}>
                        <DIV sx={{display: 'inline-flex', width: '100%', marginTop: '12px'}}>
                            <SPAN sx={{margin: '6px 0px'}}>
                                Required
                            </SPAN>
                            <DIV sx={{flexGrow: 1}} />
                            <Switch
                                sx={{padding: '0px'}}
                                getValue={this.getRequiredValue}
                                saveValue={this.saveRequiredValue}
                                color={Colors.GPU}
                            />
                            <DIV sx={{flexGrow: 4}} />
                            <SPAN sx={{margin: '6px 0px'}}>
                                Type
                            </SPAN>
                            <DIV sx={{flexGrow: 1}} />
                            <StyledSelect
                                sx={{margin: 'auto 0px', height: '25px', padding: '3px 24px 3px 6px'}}
                                disabled={!required}
                                value={this.state.selectedCard}
                                onChange={this.handleCardChange}
                                SelectDisplayProps={{style: {width: '68px', paddingTop: 0.25, paddingRight: 2, paddingBottom: 0.25, paddingLeft: 0.5}}}
                                MenuProps={{MenuListProps: {style: {paddingTop: 0.5, paddingBottom: 0.5}}}}
                                displayEmpty
                                inputProps={{ 'aria-label': 'Without label' }}
                            >
                                {this.getCardItems()}
                            </StyledSelect>
                        </DIV>
                        {Global.user.snapToInventoryEnabled ? (
                            <ChipSlider
                                key={this.state.selectedCard + '-snap'}
                                disabled={!required}
                                getValue={this.getRAMValue}
                                saveValue={this.saveRAMValue}
                                label={'Memory'}
                                marks={(this.state.selectedCard == 'U' ? Global.user.machines.graphicsMemory : Global.user.machines.graphicsMemoryByCard.get(this.state.selectedCard)).map(x => { return { value: x } })}
                                step={null}
                                color={Colors.GPU}
                                styleUnit={FormatUtils.styleCapacityUnit()}
                                styleValue={FormatUtils.styleShortCapacityValue()}
                            />
                        ) : (
                            <ChipSlider
                                key={this.state.selectedCard + '-no-snap'}
                                disabled={!required}
                                getValue={this.getRAMValue}
                                saveValue={this.saveRAMValue}
                                label={'Memory'}
                                min={minMaxMemory[0]}
                                max={minMaxMemory[1]}
                                step={1024 * 1024 * 1024}
                                color={Colors.GPU}
                                styleUnit={FormatUtils.styleCapacityUnit()}
                                styleValue={FormatUtils.styleShortCapacityValue()}
                            />
                        )}
                    </DIV>
                }
            />
		);
	}

    private handleMetadataChange = () => {
        var card = this.getCardValue();
        // TODO:JJ Get this list of valid names/numbers from the available graphics cards
        card = Global.user.machines.graphicsCards.includes(card) ? card : 'U';
        this.safeSetState({
            selectedCard: card,
            required: this.getRequiredValue(),
        });
    };

    private handleUserChange = () => this.forceUpdate();

    public componentDidMount = () => {
		this._isMounted = true;
        Global.metadata.getMetadataChanged().connect(this.handleMetadataChange);
        Global.user.userInformationChanged.connect(this.handleUserChange);
        const tracker: OptumiMetadataTracker = Global.metadata;
        // Make sure the metadata is simplified, make sure it is valid with out new approach
        const optumi = tracker.getMetadata();
        optumi.config.graphics.expertise = Expertise.SIMPLIFIED;
        if (optumi.config.graphics.cores == [-1, -1, -1]) optumi.config.graphics.boardType = 'U'
        tracker.setMetadata(optumi);
	}

	public componentWillUnmount = () => {
        Global.metadata.getMetadataChanged().disconnect(this.handleMetadataChange);
        Global.user.userInformationChanged.disconnect(this.handleUserChange);
		this._isMounted = false;
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
