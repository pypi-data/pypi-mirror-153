/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global } from '../Global';

import { SxProps, Theme } from '@mui/system';
import { Slider, SliderThumb } from '@mui/material';
import { withStyles } from '@mui/styles';
import { Equalizer, FlashOn } from '@mui/icons-material';

interface IProps {
    getValue: () => number
    saveValue: (value: number) => void
    color: string
    sx?: SxProps<Theme>
}

interface IState {
    value: number,
}

let retrievingPreview: boolean = false;
let updatePreviewAgain: boolean = false;
let latestValue: number;

const icons = [
    <svg viewBox='0 0 24 24' style={{width: '1.5rem', height: '1.5rem', fill: 'var(--jp-layout-color2)'}}>
        <path d='M6.05 8.05c-2.73 2.73-2.73 7.15-.02 9.88 1.47-3.4 4.09-6.24 7.36-7.93-2.77 2.34-4.71 5.61-5.39 9.32 2.6 1.23 5.8.78 7.95-1.37C19.43 14.47 20 4 20 4S9.53 4.57 6.05 8.05z' />
    </svg>,
    <Equalizer sx={{fill: 'var(--jp-layout-color2)'}} />,
    <FlashOn sx={{fill: 'var(--jp-layout-color2)'}} />
]

export class IntentSlider extends React.Component<IProps, IState> {
    private _isMounted = false;

    private StyledSlider: any;

    public constructor(props: IProps) {
        super (props);
        this.StyledSlider = this.getStyledSlider();
        this.state = {
            value: this.props.getValue(),
        }
    }

    private getStyledSlider = () => {
        return withStyles({
            root: {
                height: '16px',
                width: 'calc(100% - 42px)',
                padding: '13px 0px',
                margin: '0px 21px'
            },
            thumb: { // hidden
                position: 'relative',
                transform: 'none',
                height: '42px',
                width: '42px', // So we show the label any time the slider is hovered
                margin: '-13px -21px',
                transition: 'none',
                backgroundColor: this.props.color,
                zIndex: 2,          // Draw the thumb over the custom marks we put in the bar
                // '&$focusVisible,&:hover': {
                //     boxShadow: 'none',
                // },
                '&$active': {
                    boxShadow: 'none',
                },
                '&::before': {
                    boxShadow: 'none',
                },
                '&:hover': {
                    boxShadow: 'none',
                },
            },
            thumbColorPrimary: {
                // '&$focusVisible,&:hover': {
                //     boxShadow: 'none',
                // },
                '&$active': {
                    boxShadow: 'none',
                },
            },
            active: {
                boxShadow: 'none',
            },
            track: { // left side
                height: '16px',
                color: this.props.color,
                opacity: 0,
                boxSizing: 'border-box',
                borderRadius: '8px',
            },
            rail: { // right side
                height: '16px',
                width: '100%',
                opacity: 0,
                boxSizing: 'border-box',
                borderRadius: '8px',
            },
            mark: {
                opacity: 0,
            },
            markActive: {
                opacity: 0,
            },
            markLabel: {
            },
            markLabelActive: {
            },
        }) (Slider);
    }

    private handleChange = async (event: Event, newValue: number | number[]) => {
		if (newValue instanceof Array) {
			// This is invalid
		} else {
            this.safeSetState({ value: newValue / 100 });
            this.slowDownSaveValue(newValue / 100);
        }
    }

    private handleChangeCommitted = async (event: React.ChangeEvent<{}>, newValue: number | number[]) => {
		if (newValue instanceof Array) {
			// This is invalid
		} else {
            this.safeSetState({ value: newValue / 100 });
            this.props.saveValue(newValue / 100);
        }
    }

    private delay = (ms: number) => { return new Promise(resolve => setTimeout(resolve, ms)) }
    private slowDownSaveValue = (newValue: number, bypassLimiter?: boolean) => {
        if (newValue != null) latestValue = newValue;
        if (bypassLimiter || !retrievingPreview) {
            retrievingPreview = true;
            this.delay(100).then(() => {
                this.props.saveValue(latestValue);
                if (updatePreviewAgain) {
                    updatePreviewAgain = false;
                    this.slowDownSaveValue(null, true);
                } else {
                    retrievingPreview = false;
                }
            }, () => {
                retrievingPreview = false;
            });
        } else {
            updatePreviewAgain = true;
        }
	}

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const icon = this.state.value < 0.33 ? 0 : this.state.value < 0.66 ? 1 : 2
        return (
            <DIV sx={this.props.sx}>
                <DIV sx={{position: 'relative', margin: '3px 6px'}}>
                    <this.StyledSlider
                        // sx={{position: 'relative'}}
                        onChange={this.handleChange}
                        onChangeCommitted={this.handleChangeCommitted}
                        min={0}
                        max={100}
                        value={this.state.value * 100}
                        components={{
                            Thumb: (props: any) => (
                                <SliderThumb sx={Object.assign({top: 'unset', left: this.state.value + '%'}, props.sx)} {...props}>
                                    {props.children}
                                    {icons[icon]}
                                </SliderThumb>
                            )
                        }}
                    />
                    <DIV sx={{
                            position: 'absolute', 
                            top: 'calc(50% - 8px)', 
                            left: '0px', 
                            width: '100%',
                            backgroundColor: 'var(--jp-layout-color2)',
                            height: '16px',
                            borderRadius: '8px',
                        }}
                    />
                    <DIV sx={{
                            position: 'absolute', 
                            zIndex: 1,
                            top: 'calc(50% - 8px)', 
                            left: '12px', 
                            color: 'var(--jp-ui-font-color1)',
                            fontSize: '11px',
                            opacity: this.state.value < 0.22 ? 0 : 1,
                            transition: 'opacity 250ms ease 0s',
                            fontStyle: 'italic',
                            height: '0px', overflow: 'visible', pointerEvents: 'none' // Pass click events to the slider behind
                        }}
                    >
                        {'cheaper'}
                    </DIV>
                    <DIV sx={{
                            position: 'absolute',
                            zIndex: 1,
                            top: 'calc(50% - 8px)', 
                            right: '12px', 
                            color: 'var(--jp-ui-font-color1)',
                            fontSize: '11px',
                            opacity: this.state.value > 0.82 ? 0 : 1,
                            transition: 'opacity 250ms ease 0s',
                            fontStyle: 'italic',
                            height: '0px', overflow: 'visible', pointerEvents: 'none' // Pass click events to the slider behind    
                        }}
                    >
                        {'faster'}
                    </DIV>
                </DIV>
            </DIV>
        )
    }

    private handleMetadataChange = () => this.safeSetState({ value: this.props.getValue(), weGotADot: '' })

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
