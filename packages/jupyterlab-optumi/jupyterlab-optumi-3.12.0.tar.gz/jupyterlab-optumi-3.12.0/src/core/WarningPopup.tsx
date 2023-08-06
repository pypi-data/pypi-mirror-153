/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { DIV, Global } from '../Global';

import {
    Button,
    Checkbox,
    CircularProgress,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    ListItemText,
    Theme,
} from '@mui/material';
import { withStyles } from '@mui/styles';

import { Header } from './Header'
import { ShadowedDivider } from './ShadowedDivider'

const StyledDialog = withStyles((theme: Theme) => ({
    root: {
        margin: '12px',
        padding: '0px',
    },
    paper: {
        backgroundColor: 'var(--jp-layout-color1)',
    },
}))(Dialog)

interface IProps {
    open: boolean,
    headerText?: string
    bodyText?: string
    bodyContent?: JSX.Element
    preventText?: string
    cancel?: {
        text: string
        onCancel?: (prevent: boolean) => void
        onCancelAsync?: (prevent: boolean) => Promise<any>
    }
    continue: {
        text: string
        onContinue?: (prevent: boolean) => void
        onContinueAsync?: (prevent: boolean) => Promise<any>
        color: 'primary' | 'secondary' | 'error' | 'success' | 'warning' | 'info'
    }
}

interface IState {
    prevent: boolean
    cancelWaiting: boolean
    continueWaiting: boolean
}

export default class WarningPopup extends React.Component<IProps, IState> {
    private _isMounted = false

    private ContinueButton: any;

    constructor(props: IProps) {
        super(props)
        this.state = {
            prevent: false,
            cancelWaiting: false,
            continueWaiting: false,
        }
        this.ContinueButton = withStyles((theme: Theme) => {
            const paletteColor = (() => {
                switch (this.props.continue.color) {
                    case 'primary': return theme.palette.primary
                    case 'secondary': return theme.palette.secondary
                    case 'success': return theme.palette.success
                    case 'error': return theme.palette.error
                    case 'warning': return theme.palette.warning
                    case 'info': return theme.palette.info
                }
            })()
            return ({
                root: {
                    color: paletteColor.contrastText,
                    backgroundColor: paletteColor.main,
                    '&:hover': {
                        backgroundColor: paletteColor.dark,
                        // Reset on touch devices, it doesn't add specificity
                        '@media (hover: none)': {
                            backgroundColor: paletteColor.main,
                        },
                    },
                },
            })
        })(Button);
    }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <StyledDialog
                open={this.props.open}
            >
                {this.props.headerText &&
                    <DialogTitle
                        sx={{
                            backgroundColor: 'var(--jp-layout-color2)',
                            height: '48px',
                            padding: '6px 30px',
                        }}>
                        <Header
                            title={this.props.headerText}
                            sx={{lineHeight: '24px'}}
                        />
                    </DialogTitle>
                }
                <ShadowedDivider />
                <DIV sx={{padding: '18px'}}>
                    {this.props.bodyText &&
                        <DialogContent sx={{padding: '6px 18px', whiteSpace: 'pre-wrap'}}>
                            {this.props.bodyText}
                        </DialogContent>
                    }
                    {this.props.bodyContent &&
                        <DialogContent sx={{padding: '6px 18px', whiteSpace: 'pre-wrap'}}>
                            {this.props.bodyContent}
                        </DialogContent>
                    }
                    <DialogActions sx={{padding: '12px 6px 6px 6px'}}>
                        {this.props.preventText &&
                            <>
                                <Checkbox
                                    checked={this.state.prevent}
                                    onClick={() => this.safeSetState({prevent: !this.state.prevent})}
                                />
                                <ListItemText
                                    disableTypography
                                    primary={this.props.preventText}
                                    sx={{marginLeft: '0px', fontSize: '14px'}}
                                />
                            </>
                        }
                        {this.props.cancel &&
                            <Button
                                variant='contained'
                                color='secondary'
                                sx={{opacity: this.state.continueWaiting ? '0' : '1', transition: 'all 225ms', pointerEvents: this.state.continueWaiting ? 'none' : 'auto'}}    // Hide this button if the other one is spinning
                                disabled={this.state.cancelWaiting}
                                onClick={async () => {
                                    setTimeout(() => this.safeSetState({prevent: false, cancelWaiting: true }), 250)
                                    if (this.props.cancel.onCancelAsync) {
                                        await this.props.cancel.onCancelAsync(this.state.prevent)
                                    } else {
                                        this.props.cancel.onCancel(this.state.prevent)
                                    }
                                    setTimeout(() => this.safeSetState({ cancelWaiting: false }), 250)
                                }}>
                                {this.state.cancelWaiting && (<CircularProgress size='1.75em'/>)}
                                <DIV sx={{paddingLeft: this.state.cancelWaiting ? '12px' : ''}}>
                                    {this.props.cancel.text}
                                </DIV>
                            </Button>
                        }
                        <this.ContinueButton
                            variant='contained'
                            sx={{marginLeft: '18px', opacity: this.state.cancelWaiting ? '0' : '1', transition: 'all 225ms', pointerEvents: this.state.continueWaiting ? 'none' : 'auto'}}    // Hide this button if the other one is spinning
                            disabled={this.state.continueWaiting}
                            onClick={async () => {
                                setTimeout(() => this.safeSetState({ continueWaiting: true }), 250)
                                if (this.props.continue.onContinueAsync) {
                                    await this.props.continue.onContinueAsync(this.state.prevent)
                                } else {
                                    this.props.continue.onContinue(this.state.prevent)
                                }
                                setTimeout(() => this.safeSetState({ continueWaiting: false }), 250)
                            }}
                        >
                            {this.state.continueWaiting && (<CircularProgress size='1.75em'/>)}
                            <DIV sx={{paddingLeft: this.state.continueWaiting ? '12px' : ''}}>
                                {this.props.continue.text}
                            </DIV>
                        </this.ContinueButton>
                    </DialogActions>
                </DIV>
           </StyledDialog>
        );
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
