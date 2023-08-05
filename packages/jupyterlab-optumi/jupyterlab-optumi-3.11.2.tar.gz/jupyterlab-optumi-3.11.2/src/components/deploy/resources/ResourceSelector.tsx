/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global } from '../../../Global';

import { SxProps, Theme } from '@mui/system';
import { IconButton } from '@mui/material';
import { ChevronLeft, ChevronRight } from '@mui/icons-material';

import { OptumiMetadataTracker } from '../../../models/OptumiMetadataTracker';
import { Expertise } from '../../../models/OptumiConfig';

interface IProps {
    getValue: (tracker: OptumiMetadataTracker) => Expertise
    saveValue: (tracker: OptumiMetadataTracker, value: Expertise) => void
    sx?: SxProps<Theme>
    title: string,
    children: JSX.Element[] | JSX.Element,
    childrenLabels: Expertise[]
}

interface IState {
    currentLevel: number
}

export class ResourceSelector extends React.Component<IProps, IState> {
    _isMounted = false;

    public constructor(props: IProps) {
        super (props);
        this.state = {
            currentLevel: this.props.childrenLabels.indexOf(this.props.getValue(Global.metadata)),
        };
    }

    // This had to be written because ResourcePanel complained that a single element
    // was not an array, so we had to accept both and handle internally
    private getChildren = (): JSX.Element[] => {
        var children: JSX.Element[] | JSX.Element = this.props.children;
        if (children instanceof Array) {
			// The filter below allows us to remove levels conditionally (if they aren't added they evaluate as false)
            return children.filter(child => React.isValidElement(child));
        } else {
            var singleton: JSX.Element[] = [];
            singleton.push(children);
            return singleton;
        }
    }

    private decreaseExpertise = (): void => {
        const newLevel = this.state.currentLevel - 1;
        if (this.state.currentLevel > 0) {
            this.safeSetState({ currentLevel: newLevel });
        }
        this.props.saveValue(Global.metadata, this.props.childrenLabels[newLevel] as Expertise);
    }

    private increaseExpertise = (): void => {
        const newLevel = this.state.currentLevel + 1;
        if (this.state.currentLevel < this.getChildren().length - 1) {
            this.safeSetState({ currentLevel: newLevel})
        }
        this.props.saveValue(Global.metadata, this.props.childrenLabels[newLevel]);
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        this.props.children;
        // The padding is not in the div because the padding affects the ability to click the chevrons
        // The position and left/right on the icons is so all chevrons are aligned vertically no matter the size of the text
        // The title is in an inline-block div because we want the chevrons around the title and they use position: absolute
        // The lineHeight in the title centers the text vertically (24px comes from the chevron height from the inspector)
        return (
            <DIV sx={this.props.sx}>
                <DIV sx={{textAlign: 'center', margin: '6px'}}>
                    <DIV sx={{position: 'relative', textAlign: 'center'}}>
                        <IconButton
                            size='large'
                            disabled={this.state.currentLevel <= 0 ? true : false}
                            color='primary'
                            onClick={() => this.decreaseExpertise()}
                            sx={{position: 'absolute', left: '25%', padding: '3px'}}
                        >
                            <ChevronLeft />
                        </IconButton>
                        <DIV sx={{display: 'inline-block', fontSize: '16px', fontWeight: 'bold', lineHeight: '18px', margin: '6px'}}>
                            {this.props.title}
                        </DIV>
                        <IconButton
                            size='large'
                            disabled={this.state.currentLevel >= this.getChildren().length - 1 ? true : false}
                            color='primary'
                            onClick={() => this.increaseExpertise()}
                            sx={{position: 'absolute', right: '25%', padding: '3px'}}
                        >
                            <ChevronRight />
                        </IconButton>
                    </DIV>
                    {this.getChildren()[this.state.currentLevel]}
                </DIV>
            </DIV>
        );
    }

    private handleMetadataChange = () => {
        this.safeSetState({ currentLevel: this.props.childrenLabels.indexOf(this.props.getValue(Global.metadata)) });
    }

    // Will be called automatically when the component is mounted
	public componentDidMount = () => {
		this._isMounted = true;
		Global.metadata.getMetadataChanged().connect(this.handleMetadataChange);
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
		Global.metadata.getMetadataChanged().disconnect(this.handleMetadataChange);
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
