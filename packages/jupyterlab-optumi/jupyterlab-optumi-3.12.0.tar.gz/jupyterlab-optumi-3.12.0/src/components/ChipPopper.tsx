/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { DIV, Global, SPAN } from '../Global';

import { alpha, SxProps, Theme } from '@mui/system';
import { Chip, darken, IconButton, lighten } from '@mui/material';
import { withStyles } from '@mui/styles';
import { Close, KeyboardArrowDown, KeyboardArrowUp } from '@mui/icons-material';

import { Popper } from '../core/Popper';

interface IProps {
    sx: SxProps<Theme>
    title: string
    color: string
    clearValue: () => any
    getChipDescription?: () => string
    getHeaderDescription: () => string
    popperContent: JSX.Element
}

interface IState {
    open: boolean
}

export class ChipPopper extends React.Component<IProps, IState> {
    _isMounted = false;
    close: () => void = () => {}
    stopPropagation: () => void = () => {}

    private StyledChip: any

    public constructor(props: IProps) {
        super(props)
        this.state = {
            open: false,
        }
        this.StyledChip = withStyles(theme => ({
            root: {
                height: '20px',
                fontSize: '12px',
                // borderWidth: '2px',
                // borderStyle: 'solid',
                transition: 'all 300ms cubic-bezier(0.4, 0, 0.2, 1) 0ms',
                transitionProperty: 'background-color',
                '&:active': {
                    boxShadow: 'none',
                }
            },
            icon: {
                position: 'absolute',
                right: theme.spacing(0.75),
            },
            label: {
                position: 'absolute',
                left: theme.spacing(0.5),
                padding: theme.spacing(0),
            },
            clickable: {
                '&:hover': {
                    filter: 'brightness(0.95)',
                    transition: 'filter 250ms cubic-bezier(0.4, 0, 0.2, 1) 0ms'
                },
            },
        }))(Chip)
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const description = this.props.getHeaderDescription();
        const modified: boolean = description != 'Any';
        const jpLayoutColor2 = getComputedStyle(document.documentElement).getPropertyValue('--jp-layout-color2').trim()
		return (
            <Popper
                color={this.props.color}
                onOpen={() => this.safeSetState({open: true})}
                onClose={() => this.safeSetState({open: false})}
                close={(close: () => void) => this.close = close}
                stopPropagation={(stopPropagation: () => void) => this.stopPropagation = stopPropagation}
                button={
                    <this.StyledChip
                        key={this.props.title + 'chip'}
                        sx={Object.assign({
                            color: Global.themeManager == undefined || Global.themeManager.isLight(Global.themeManager.theme) ? darken(modified ? this.props.color : jpLayoutColor2, 0.35) : lighten(modified ? this.props.color : jpLayoutColor2, 0.35),
                            backgroundColor: modified ? alpha(this.props.color, 0.25) : 'var(--jp-layout-color2)' + ' !important'
                        }, this.props.sx)}
                        label={this.props.getChipDescription ? this.props.getChipDescription() : this.props.title + ': ' + this.props.getHeaderDescription()}
                        icon={(
                            modified ? (
                                <IconButton
                                    size='large'
                                    sx={{
                                        padding: 0.25,
                                        marginTop: -0.25,
                                        marginRight: -0.75,
                                        marginBottom: -0.25,
                                        marginLeft: -0.25,
                                        zIndex: 1,
                                    }}
                                    onClick={() => {
                                        this.props.clearValue()
                                        this.stopPropagation()
                                    }}
                                >
                                    <Close sx={{height: '14px',width: '14px', color: Global.themeManager == undefined || Global.themeManager.isLight(Global.themeManager.theme) ? darken(modified ? this.props.color : jpLayoutColor2, 0.35) : lighten(modified ? this.props.color : jpLayoutColor2, 0.35)}}/>
                                </IconButton>
                            ) : this.state.open ? (
                                <KeyboardArrowUp sx={{height: '14px',width: '14px'}}/>
                            ) : (
                                <KeyboardArrowDown sx={{height: '14px',width: '14px'}}/>
                            )
                        )}
                    />
                }
                popup={
                    <DIV sx={{
                        display: 'flex',
                        flexDirection: 'column',
                        margin: 1,
                        fontSize: '15px',
                        lineHeight: '15px',
                    }}>
                        <DIV sx={{display: 'flex'}}>
                            <SPAN sx={{fontWeight: 'bold'}}>
                                {this.props.title}:
                            </SPAN>
                            <SPAN sx={{whiteSpace: 'pre'}}>
                                {` ${description}`}
                            </SPAN>
                            <DIV sx={{width: '100%'}} />
                            <IconButton
                                size='large'
                                sx={{padding: 0.5, margin: -0.5}}
                                onClick={this.close}
                            >
                                <Close sx={{width: '15px', height: '15px'}}/>
                            </IconButton>
                        </DIV>
                        <DIV sx={{fontSize: '14px'}}>
                            {this.props.popperContent}
                        </DIV>
                    </DIV>
                }
            />
        );
	}

    private handleThemeChange = () => this.forceUpdate()
    private handleMetadataChange = () => this.forceUpdate()

    public componentDidMount = () => {
		this._isMounted = true;
        Global.themeManager.themeChanged.connect(this.handleThemeChange);
        Global.metadata.getMetadataChanged().connect(this.handleMetadataChange);
	}

	public componentWillUnmount = () => {
        Global.themeManager.themeChanged.disconnect(this.handleThemeChange);
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
