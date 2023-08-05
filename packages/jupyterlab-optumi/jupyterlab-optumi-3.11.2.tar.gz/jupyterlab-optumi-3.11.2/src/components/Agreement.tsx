/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { DIV, Global } from '../Global';

import { Button, Checkbox, Divider } from '@mui/material';

import { ServerConnection } from '@jupyterlab/services';

interface IProps {
    callback: () => void;
}

interface IState {
    agreed: boolean,
}

export class Agreement extends React.Component<IProps, IState> {
    _isMounted = false

    constructor(props: IProps) {
        super(props)
        this.state = {
            agreed: false,
        }
    }

    // Log out of the REST interface (Copied from SettingsPage aside from setState call)
	private logout = () => {
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/logout";
		const init = {
			method: 'GET',
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
            Global.user = null;
            this.safeSetState({open: false})
		});
	}

    private acceptAgreement = () => {
        const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/sign-agreement";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				timeOfSigning: new Date().toISOString(),
			}),
		};
		return ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response);
			return response.text();
		}).then((body: string) => {
            Global.user.unsignedAgreement = false;
            this.props.callback();
		});
    }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <>
                <DIV className='jp-optumi-logo'/>
                <DIV sx={{
                    display: 'flex',
                    flexFlow: 'column',
                    overflow: 'hidden',
                    height: '100%',
                }}>
                    <DIV
                        sx={{
                            padding: '0px',
                            flexGrow: 1,
                            // overflowY: 'auto',
                            overflowY: 'hidden',
                            whiteSpace: 'pre-wrap',
                            backgroundColor: 'white'
                        }}
                    >
                        <embed type="text/html" src={Global.agreementURL} style={{pointerEvents: 'none'}} height='100%' width='100%' />
                    </DIV>
                    <Divider variant='middle' />
                    <DIV sx={{padding: '6px', display: 'flex', justifyContent: 'center'}}>
                        <Checkbox
                            checked={this.state.agreed}
                            color='primary'
                            onClick={() => this.safeSetState({ agreed: !this.state.agreed})}
                            sx={{
                                padding: '6px',
                                margin: '0px',
                                flexGrow: 1,
                            }}
                        />
                        <DIV 
                            sx={{
                                padding: '6px',
                                margin: 'auto',
                                flexGrow: 1,
                                fontWeight: 'bold',
                                lineHeight: '12px'
                            }}
                        >
                            I have read and I agree to the Optumi Terms and Conditions of Service
                        </DIV>
                    </DIV>
                    <DIV sx={{padding: '6px', display: 'flex', justifyContent: 'center'}}>
                        <Button
                            onClick={this.logout}
                            color='secondary'
                            sx={{
                                padding: '9px',
                                fontWeight: 'bold',
                                fontSize: '14px',
                                lineHeight: '14px',
                                margin: '0px',
                                flexGrow: 1,
                            }}
                        >
                            Logout
                        </Button>
                        <Button
                            onClick={this.acceptAgreement}
                            color='primary'
                            variant='contained'
                            disabled={!this.state.agreed}
                            sx={{
                                padding: '9px',
                                fontWeight: 'bold',
                                fontSize: '14px',
                                lineHeight: '14px',
                                margin: '0px',
                                flexGrow: 1,
                            }}
                        >
                            I accept
                        </Button>
                    </DIV>
                </DIV>
            </>
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
