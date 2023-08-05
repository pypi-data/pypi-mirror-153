/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global, SkinnyButton, WhiteTextButton } from '../Global';

import { ServerConnection } from '@jupyterlab/services';

import { SxProps, Theme } from '@mui/system';
import { Button, CircularProgress } from '@mui/material';
import { loadStripe, Stripe, StripeError } from '@stripe/stripe-js';

interface IProps {
    sx?: SxProps<Theme>
    variant?: "text" | "contained" | "outlined" | 'whiteOutlined' | 'whiteText' | 'skinny'
    color?: "inherit" | "primary" | "secondary" | "success" | "error" | "info" | "warning"
    text?: string
    disableElevation?: boolean
    onClick?: () => any
}

interface IState {
    checkoutWaiting: boolean
}

const stripePromise = loadStripe(Global.stripe_key);

export class SubscribeButton extends React.Component<IProps, IState> {
    private _isMounted = false

    public constructor(props: IProps) {
        super (props);
        this.state = {
            checkoutWaiting: false
        }
    }

    private handleCheckoutClick = async () => {
        if (this.props.onClick) this.props.onClick();
        
        // Get Stripe.js instance    
        // Call your backend to create the Checkout Session
        
        this.safeSetState({ checkoutWaiting: true });

        const stripe: Stripe = await stripePromise;
        
        const settings = ServerConnection.makeSettings();
        const url = settings.baseUrl + "optumi/create-checkout";
        const init: RequestInit = {
            method: 'POST',
            body: JSON.stringify({
                items: [],
                redirect: settings.baseUrl,
            }),
        };
        ServerConnection.makeRequest(
            url,
            init,
            settings
        ).then((response: Response) => {
            Global.handleResponse(response);
            return response.json();
        }).then((body: any) => {
            // When the customer clicks on the button, redirect them to Checkout.
            return stripe.redirectToCheckout({
                sessionId: body.id,
            });
        }).then((result: {error: StripeError}) => {
            this.safeSetState({ checkoutWaiting: false });
            if (result.error) {
                // If `redirectToCheckout` fails due to a browser or network
                // error, display the localized error message to your customer
                // using `result.error.message`.
            }
        });
    };

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        if (this.props.variant == 'whiteOutlined') {
            return (
                <Button 
                    disabled={this.state.checkoutWaiting} 
                    variant='outlined'
                    sx={Object.assign(this.props.sx || {}, {color: 'white', borderColor: 'white'})}
                    onClick={this.handleCheckoutClick}
                    disableElevation={this.props.disableElevation || false}
                >
                    {this.state.checkoutWaiting ? (<CircularProgress size='1.75em'/>) : (this.props.text || 'Subscribe')}
                </Button>
            )
        } else if (this.props.variant == 'whiteText') {
            return (
                <WhiteTextButton 
                    disabled={this.state.checkoutWaiting} 
                    sx={this.props.sx}
                    onClick={this.handleCheckoutClick}
                    disableElevation={this.props.disableElevation || false}
                >
                    {this.state.checkoutWaiting ? (<CircularProgress size='1.75em' sx={{color: 'white'}} />) : (this.props.text || 'Subscribe')}
                </WhiteTextButton>
            )
        } else if (this.props.variant == 'skinny') {
            return (
                <SkinnyButton 
                    disabled={this.state.checkoutWaiting}
                    color={"primary"} 
                    variant={"contained"}
                    sx={this.props.sx}
                    onClick={this.handleCheckoutClick}
                    disableElevation={this.props.disableElevation || false}
                >
                    {this.state.checkoutWaiting ? (<CircularProgress size='14px'  thickness={8}/>) : (this.props.text || 'Subscribe')}
                </SkinnyButton>
            )
        } else {
            return (
                <Button 
                    disabled={this.state.checkoutWaiting} 
                    color={this.props.color || "primary"} 
                    variant={this.props.variant || "contained"}
                    sx={this.props.sx}
                    onClick={this.handleCheckoutClick}
                    disableElevation={this.props.disableElevation || false}
                >
                    {this.state.checkoutWaiting ? (<CircularProgress size='1.75em'/>) : (this.props.text || 'Subscribe')}
                </Button>
            )
        }
    }

    // Will be called automatically when the component is mounted
	public componentDidMount = () => {
        this._isMounted = true
	}

	// Will be called automatically when the component is unmounted
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
