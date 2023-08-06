/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global } from '../Global';

import { SxProps, Theme } from '@mui/system';
import { Button, Dialog, DialogContent, DialogTitle, IconButton, Tab, Tabs } from '@mui/material';
import { withStyles } from '@mui/styles';
import { Close as CloseIcon, /*OpenInNew as OpenInNewIcon*/ } from '@mui/icons-material';

import { ServerConnection } from '@jupyterlab/services';

import { AccountIntegrationsSubMenu, AccountStorageSubMenu, AccountPreferencesSubMenu, AccountLimitsSubMenu, AccountBillingSubMenu } from './settings/SettingsMenu';
import { ShadowedDivider } from '../core';
import WarningPopup from '../core/WarningPopup';
import { Colors } from '../Colors';

const StyledDialog = withStyles({
    paper: {
        width: 'calc(min(80%, 600px + 150px + 2px))',
        // width: '100%',
        height: '80%',
        overflowY: 'visible',
        maxWidth: 'inherit',
    },
})(Dialog);

const enum Page {
    PREFERENCES = 0,
    LIMITS = 1,
    STORAGE = 2,
    INTEGRATIONS = 3,
    BILLING = 4,
}

interface IProps {
    sx?: SxProps<Theme>
    onOpen?: () => void
	onClose?: () => void
    balance: number
    machineCost: number
    serviceFeeCost: number
    storageCost: number
    egressCost: number
}

interface IState {
    open: boolean,
    selectedPanel: number,
    validPhoneNumber: boolean,
    showCloseWithInvalidNumberPopup: boolean,
}

// TODO:Beck The popup needs to be abstracted out, there is too much going on to reproduce it in more than one file
export class UserDialog extends React.Component<IProps, IState> {
    private _isMounted = false

    constructor(props: IProps) {
        super(props);
		this.state = {
            open: false,
            selectedPanel: Page.PREFERENCES,
            validPhoneNumber: true,
            showCloseWithInvalidNumberPopup: false,
		};
    }
    
    private handleClickOpen = () => {
        if (this.props.onOpen) this.props.onOpen()
		this.safeSetState({ open: true, selectedPanel: Page.PREFERENCES });
	}

	private handleClose = () => {
        this.safeSetState({ open: false, validPhoneNumber: true });
        if (this.props.onClose) this.props.onClose();
	}

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        var defaultProfilePicture: string = Global.user.name.replace(/(?<=\B)\w+/g, '').replace(/[ ]/g, '').toUpperCase()
        return (
            <DIV sx={Object.assign({}, this.props.sx)} >
                <IconButton
                    size='large'
                    onClick={this.handleClickOpen}
                    sx={{
                        display: 'inline-block',
                        width: '36px',
                        height: '36px',
                        padding: '6px',
                    }}
                >
                    <DIV sx={{
                        width: '24px',
                        height: '24px',
                        // margin: '6px auto',
                        borderRadius: '12px',
                        backgroundColor: Colors.PRIMARY,
                        color: 'white',
                        fontSize: '14px',
                        fontWeight: 'bold',
                        lineHeight: '24px',
                        textAlign: 'center'
                    }}>
                        {defaultProfilePicture[defaultProfilePicture.length-1]}
                    </DIV>
                </IconButton>
                <StyledDialog
					open={this.state.open}
					onClose={() => {
                        if (!this.state.validPhoneNumber) {
                            this.safeSetState({ showCloseWithInvalidNumberPopup: true });
                        } else {
                            this.handleClose();
                        }
                    }}
                    scroll='paper'
				>
					<DialogTitle sx={{
                        display: 'inline-flex',
                        height: '60px',
                        padding: '6px',
                    }}>
                        <DIV sx={{
                            display: 'inline-flex',
                            minWidth: '150px',
                            fontSize: '16px',
                            fontWeight: 'bold',
                            paddingRight: '12px', // this is 6px counteracting the DialogTitle padding and 6px aligning the padding to the right of the tabs
                        }}>
                            <DIV sx={{margin: 'auto', paddingLeft: '12px'}}>
            					Settings
                            </DIV>
                        </DIV>
                        <DIV sx={{flexGrow: 1}} />
                        <DIV>
                            <Button 
                                onClick={() => window.open('https://login.optumi.com/enduser/settings?iframe=true&iframeControlHideAll=true', '_blank')}
                                disableElevation
                                sx={{ height: '36px', margin: '6px' }}
                                variant="outlined"
                                color="primary"
                                // endIcon={<OpenInNewIcon/>}
                            >
                                Edit profile
                            </Button>
                            <Button
                                disableElevation
                                sx={{ height: '36px', margin: '6px' }}
                                variant="outlined"
                                color="primary"
                                onClick={this.logout}
                            >
                                Logout
                            </Button>
                        </DIV>
                        <DIV>
                            <WarningPopup
                                open={this.state.showCloseWithInvalidNumberPopup}
                                headerText="Heads Up!"
                                bodyText={`The phone number you entered is invalid. If you continue we'll revert back to your previous number.`}
                                cancel={{
                                    text: `Edit number`,
                                    onCancel: (prevent: boolean) => {
                                        this.safeSetState({ showCloseWithInvalidNumberPopup: false })
                                    },
                                }}
                                continue={{
                                    text: `Continue`,
                                    onContinue: (prevent: boolean) => {
                                        this.safeSetState({ showCloseWithInvalidNumberPopup: false })
                                        this.handleClose()
                                    },
                                    color: `primary`,
                                }}
                            />
                            <IconButton
                                size='large'
                                onClick={() => {
                                    if (!this.state.validPhoneNumber) {
                                        this.safeSetState({ showCloseWithInvalidNumberPopup: true });
                                    } else {
                                        this.handleClose();
                                    }
                                }}
                                sx={{
                                    margin: '6px',
                                    display: 'inline-block',
                                    width: '36px',
                                    height: '36px',
                                    padding: '3px',
                                }}
                            >
                                <CloseIcon
                                    sx={{
                                        width: '30px',
                                        height: '30px',
                                        padding: '3px',
                                    }}
                                />
                            </IconButton>
                        </DIV>
					</DialogTitle>
                    <ShadowedDivider />
                    <DIV sx={{display: 'flex', height: 'calc(100% - 60px - 2px)'}}>
                        <DIV sx={{width: '150px'}}>
                            <DialogContent sx={{
                                overflowY: 'auto',
                                height: '100%',
                                padding: '0px',
                            }}>
                                <DIV sx={{
									display: 'flex',
									flexDirection: 'column',
									padding: '6px',
									height: '100%',
								}}>
                                    <Tabs
                                        value={this.state.selectedPanel}
                                        onChange={(event, newValue) => this.safeSetState({selectedPanel: newValue})}
                                        orientation='vertical'
                                        variant='fullWidth'
                                        indicatorColor='primary'
                                        textColor='primary'
                                        sx={{minHeight: '24px', flexGrow: 1}}
                                    >
                                        <Tab
                                            disableRipple
                                            label='Preferences'
                                            sx={{
                                                padding: '0px',
                                                minWidth: 'auto',
                                                minHeight: '36px',
                                            }}
                                            value={Page.PREFERENCES}
                                        />
                                        <Tab
                                            disableRipple
                                            label='Limits'
                                            sx={{
                                                padding: '0px',
                                                minWidth: 'auto',
                                                minHeight: '36px',
                                            }}
                                            value={Page.LIMITS}
                                        />
                                        <Tab
                                            disableRipple
                                            label='Integrations'
                                            sx={{
                                                padding: '0px',
                                                minWidth: 'auto',
                                                minHeight: '36px',
                                            }}
                                            value={Page.INTEGRATIONS}
                                        />
                                        <Tab
                                            disableRipple
                                            label='Storage'
                                            sx={{
                                                padding: '0px',
                                                minWidth: 'auto',
                                                minHeight: '36px',
                                            }}
                                            value={Page.STORAGE}
                                        />
                                        <Tab
                                            disableRipple
                                            label='Billing'
                                            sx={{
                                                padding: '0px',
                                                minWidth: 'auto',
                                                minHeight: '36px',
                                            }}
                                            value={Page.BILLING}
                                        />
                                    </Tabs>
                                    <DIV sx={{
										margin: '12px',
										color: 'var(--jp-ui-font-color3)',
										textAlign: 'center',
										fontSize: '10px',
									}}>
                                        Version {Global.version}
                                    </DIV>
                                </DIV>
                            </DialogContent>
                        </DIV>
                        <ShadowedDivider orientation='vertical' />
                        <DIV sx={{display: 'flex', flexFlow: 'column', overflow: 'hidden', width: 'calc(100% - 150px)', height: '100%'}}>
                            <DialogContent sx={{
                                flexGrow: 1, 
                                overflowY: 'auto',
                                width: '100%',
                                height: '100%',
                                padding: '0px',
                                marginBottom: '0px', // This is because MuiDialogContentText-root is erroneously setting the bottom to 12
                                // lineHeight: 'var(--jp-code-line-height)',
                                fontSize: 'var(--jp-ui-font-size1)',
                                fontFamily: 'var(--jp-ui-font-family)',
                            }}>
                                <DIV sx={{
                                    // Height needs to be 100% otherwise it will cause problems with the phone number country selection
                                    display: 'flex', flexFlow: 'column', overflow: 'hidden', height: '100%'
                                }}>
                                    {this.state.selectedPanel == Page.PREFERENCES ? (
                                        <>
                                            {/* <DIV sx={{display: 'flex', padding: '6px 6px 0px 6px', maxWidth: '450px'}}>
                                                <DIV sx={{width: '68px', margin: '0px 6px'}}>
                                                    <DIV sx={{
                                                        width: '48px',
                                                        height: '48px',
                                                        margin: '6px auto',
                                                        borderRadius: '24px',
                                                        backgroundColor: Colors.PRIMARY,
                                                        color: 'white',
                                                        fontSize: (28 - defaultProfilePicture.length * 4) + 'px',
                                                        fontWeight: 'bold',
                                                        lineHeight: '48px',
                                                        textAlign: 'center'
                                                    }}>
                                                        {defaultProfilePicture}
                                                    </DIV>
                                                </DIV>
                                                <DIV sx={{display: 'table', height: '48px', margin: '6px', flexGrow: 1}}>
                                                    <DIV sx={{display: 'table-cell', verticalAlign: 'middle'}}>
                                                        <SPAN sx={{fontSize: '16px', lineHeight: '1', fontWeight: 'normal'}}>
                                                            {Global.user.name}
                                                        </SPAN>
                                                        <br />
                                                    </DIV>
                                                </DIV>
                                            </DIV> */}
                                            <AccountPreferencesSubMenu
                                                sx={{flexGrow: 1, overflowY: 'auto', maxWidth: '450px'}}
                                                phoneValidOnBlur={(valid: boolean) => {
                                                    this.setState({ validPhoneNumber: valid });
                                                }}
                                            />
                                        </>
                                    ) : this.state.selectedPanel == Page.LIMITS ? (
                                        <AccountLimitsSubMenu sx={{flexGrow: 1, overflowY: 'auto', maxWidth: '450px'}} />
                                    ) : this.state.selectedPanel == Page.BILLING ? (
                                        <AccountBillingSubMenu
                                            sx={{flexGrow: 1, maxWidth: '450px'}}
                                            balance={this.props.balance}
                                            machineCost={this.props.machineCost}
                                            serviceFeeCost={this.props.serviceFeeCost}
                                            storageCost={this.props.storageCost}
                                            egressCost={this.props.egressCost}
                                        />
                                    ): this.state.selectedPanel == Page.INTEGRATIONS ? (
                                        <AccountIntegrationsSubMenu sx={{flexGrow: 1, overflowY: 'auto'}} />
                                    ) : this.state.selectedPanel == Page.STORAGE && (
                                        <AccountStorageSubMenu sx={{flexGrow: 1, overflowY: 'auto'}} />
                                    )}
                                </DIV>
                            </DialogContent>
                        </DIV>
                    </DIV>
				</StyledDialog>
            </DIV>
        );
    }

    // Log out of the REST interface
	private logout() {
        Global.user = null;
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/logout";
		const init = {
			method: 'GET',
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		);
	}

    public componentDidMount = () => {
        this._isMounted = true
        Global.setLink(Global.Target.SettingsPopup.PreferencesTab, async () => this.safeSetState({open: true, selectedPanel: Page.PREFERENCES}))
        Global.setLink(Global.Target.SettingsPopup.LimitsTab, async () => this.safeSetState({open: true, selectedPanel: Page.LIMITS}))
        Global.setLink(Global.Target.SettingsPopup.IntegrationsTab, async () => this.safeSetState({open: true, selectedPanel: Page.INTEGRATIONS}))
        Global.setLink(Global.Target.SettingsPopup.StorageTab, async () => this.safeSetState({open: true, selectedPanel: Page.STORAGE}))
        Global.setLink(Global.Target.SettingsPopup.BillingTab, async () => this.safeSetState({open: true, selectedPanel: Page.BILLING}))
    }

    public componentWillUnmount = () => {
        Global.deleteLinksUnder(Global.Target.SettingsPopup)
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
