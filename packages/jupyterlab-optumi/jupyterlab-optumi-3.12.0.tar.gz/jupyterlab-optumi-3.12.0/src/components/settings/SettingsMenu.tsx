/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global } from '../../Global';

import { SxProps, Theme } from '@mui/system';
import { Button, Divider, IconButton, } from '@mui/material';
import { GetApp, Refresh } from '@mui/icons-material';

import { ServerConnection } from '@jupyterlab/services';

import { Header, Switch, TextBox } from '../../core';
import FormatUtils from '../../utils/FormatUtils';
import IntegrationBrowser, { DataConnectorMetadata, IntegrationMetadata, IntegrationType } from '../deploy/IntegrationBrowser/IntegrationBrowser';
import { AmazonS3ConnectorPopup } from '../deploy/AmazonS3ConnectorPopup';
import { GoogleCloudStorageConnectorPopup } from '../deploy/GoogleCloudStorageConnectorPopup';
import { GoogleDriveConnectorPopup } from '../deploy/GoogleDriveConnectorPopup';
import { KaggleConnectorPopup } from '../deploy/KaggleConnectorPopup';
import { WasabiConnectorPopup } from '../deploy/WasabiConnectorPopup';
// import { PhoneTextBox } from '../../core/PhoneTextBox';
import { AzureBlobStorageConnectorPopup } from '../deploy/AzureBlobStorageConnector';
import FileBrowser, { FileMetadata } from '../deploy/fileBrowser/FileBrowser';
import { SubscriptionActive } from './SubscriptionActive';

import { FreeTrial } from './FreeTrial';
import { PhoneTextBox } from '../../core/PhoneTextBox';
import { SubscriptionEnded } from './SubscriptionEnded';
import { CustomerState } from '../../core/CustomerState';
import { FreeTrialEnded } from './FreeTrialEnded';
import { EnvironmentVariablePopup } from '../../core/EnvironmentVariablePopup';

// Properties from parent
interface IAccountPreferencesSubMenuProps {
    phoneValidOnBlur?: (valid: boolean) => void
	sx?: SxProps<Theme>
}

const emUpSub = 'Upgrade subscription to unlock'

const LABEL_WIDTH = '80px'

interface IAccountPreferencesSubMenuState {
    switchKey: number
}

export class AccountPreferencesSubMenu extends React.Component<IAccountPreferencesSubMenuProps, IAccountPreferencesSubMenuState> {

    constructor(props: IAccountPreferencesSubMenuProps) {
        super(props);
        this.state = {
            // We need to increment this when the user changes his number so the switch will be enabled/disabled properly
            switchKey: 0
        }
    }
    
    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <>
                <DIV sx={Object.assign({padding: '6px'}, this.props.sx)}>
                    {/* <ResourceTextBox<string>
                        getValue={this.getNameValue}
                        label='Name'
                        editPressRequired
                    /> */}
                    <PhoneTextBox
                        getValue={() => Global.user.phoneNumber ? Global.user.phoneNumber : ''}
                        saveValue={(phoneNumber: string) => {
                            if (phoneNumber == '') Global.user.notificationsEnabled = false;
                            Global.user.phoneNumber = phoneNumber;
                            // We need to update so the switch below will be updated properly
                            this.setState({ switchKey: this.state.switchKey+1 });
                        }}
                        validOnBlur={this.props.phoneValidOnBlur}
                        label='Phone'
                        labelWidth={LABEL_WIDTH}
                    />
                    <Switch
                        key={this.state.switchKey}
                        getValue={() => Global.user.notificationsEnabled }
                        saveValue={(notificationsEnabled: boolean) => { Global.user.notificationsEnabled = notificationsEnabled }}
                        label={'Enable SMS notifications to ' + Global.user.phoneNumber}
                        disabled={Global.user.phoneNumber == ''}
                        labelBefore
                        flip
                    />
                    <Switch
                        getValue={() => Global.user.compressFilesEnabled}
                        saveValue={(compressFilesEnabled: boolean) => { Global.user.compressFilesEnabled = compressFilesEnabled }}
                        label='Compress my files before uploading'
                        labelBefore
                        flip
                    />
                    <Switch
                        getValue={() => Global.user.snapToInventoryEnabled}
                        saveValue={(snapToInventoryEnabled: boolean) => { Global.user.snapToInventoryEnabled = snapToInventoryEnabled }}
                        label='Snap resource selection sliders to existing inventory'
                        labelBefore
                        flip
                    />
                    {Global.user.showDownloadAllButtonEnabled && (
                        <Button 
                            variant="outlined"
                            color="primary"
                            startIcon={<GetApp />}
                            sx={{width: '100%'}}
                            onClick={async () => {
                                const data = [];
                                for (let app of Global.user.appTracker.finishedJobsOrSessions) {
                                    const machine = app.machine;
                                    data.push(
                                        [
                                            this.stringToCSVCell(app.name),
                                            this.stringToCSVCell(app.annotationOrRunNum),
                                            app.timestamp,
                                            app.getTimeElapsed(),
                                            app.interactive ? 'N/A' : app.notebook.metadata.papermill.duration,
                                            app.getCost(),
                                            app.getAppMessage(),
                                            machine.name,
                                            machine.computeCores,
                                            FormatUtils.styleCapacityUnitValue()(machine.memorySize),
                                            FormatUtils.styleCapacityUnitValue()(machine.storageSize),
                                            machine.graphicsNumCards > 0 ? (machine.graphicsNumCards + ' ' + machine.graphicsCardType) : 'None',
                                            app.uuid,
                                        ]
                                    );
                                    
                                    var link = document.createElement("a");
                                    var blob = new Blob([JSON.stringify(app.machine)], {
                                        type: "text/plain;charset=utf-8"
                                    });
                                    link.setAttribute("href", window.URL.createObjectURL(blob));
                                    link.setAttribute("download", app.uuid + ".txt");
                                    document.body.appendChild(link); // Required for FF
                                    link.click();

                                    await new Promise(resolve => setTimeout(resolve, 100));

                                    // const ipynbContent = 'data:text/plain;charset=utf-8,'
                                    //     + JSON.stringify(app.notebook);
                                    var link = document.createElement("a");
                                    var blob = new Blob([JSON.stringify(app.notebook)], {
                                        type: "text/plain;charset=utf-8"
                                    });
                                    link.setAttribute("href", window.URL.createObjectURL(blob));
                                    link.setAttribute("download", app.uuid + ".ipynb");
                                    document.body.appendChild(link); // Required for FF
                                    link.click();

                                    await new Promise(resolve => setTimeout(resolve, 100));
                                }
            
                                const headers = [
                                    ["Name", "Annotation", "Start Time", "Duration (total)", "Duration (notebook)", "Cost", "Status", "Machine", "Cores", "RAM", "Disk", "GPUs", "UUID"]
                                ];
            
                                var link = document.createElement("a");
                                var blob = new Blob([headers.map(e => e.join(",")).join("\n") + '\n' + data.map(e => e.join(",")).join("\n") + '\n'], {
                                    type: "data:text/csv;charset=utf-8,"
                                });
                                link.setAttribute("href", window.URL.createObjectURL(blob));
                                link.setAttribute("download", "run_history.csv");
                                document.body.appendChild(link); // Required for FF
                                link.click();
                            }
                        }>
                            Download all runs
                        </Button>
                    )}
                </DIV>
            </>
        )
    }

    public stringToCSVCell(str: string): string {
        var s = "\"";
        for(let nextChar of str) {
            s += nextChar;
            if (nextChar == '"')
                s += "\"";
        }
        s += "\"";
        return s;
    }

    public shouldComponentUpdate = (nextProps: IAccountPreferencesSubMenuProps, nextState: IAccountPreferencesSubMenuState): boolean => {
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

// Properties from parent
interface IAccountLimitsSubMenuProps {
    // phoneValidOnBlur?: (valid: boolean) => void
	sx?: SxProps<Theme>
}

interface IAccountLimitsSubMenuState {
    holdoverFocused: boolean;
    budgetFocused: boolean;
    recsFocused: boolean;
}

export class AccountLimitsSubMenu extends React.Component<IAccountLimitsSubMenuProps, IAccountLimitsSubMenuState> {
    private _isMounted = false

    constructor(props: IAccountLimitsSubMenuProps) {
        super(props);
        this.state = {
            holdoverFocused: false,
            budgetFocused: false,
            recsFocused: false,
        }
    }
    private getUserBudgetValue(): number { return Global.user.userBudget }
    private saveUserBudgetValue(userBudget: number) { Global.user.userBudget = userBudget }

    private getMaxJobsValue(): number { return Global.user.maxJobs }
    private saveMaxJobsValue(value: number) { Global.user.maxJobs = value }

    private getMaxMachinesValue(): number { return Global.user.maxMachines }
    private saveMaxMachinesValue(value: number) { Global.user.maxMachines = value }

    private getUserHoldoverTimeValue(): number { return Math.round(Global.user.userHoldoverTime / 60) }
    private saveUserHoldoverTimeValue(userHoldoverTime: number) { Global.user.userHoldoverTime = userHoldoverTime * 60 }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return <>
            <DIV sx={Object.assign({padding: '6px'}, this.props.sx)}>
                {Global.user.userExpertise > 0 ? (<TextBox<number>
                    getValue={this.getUserBudgetValue}
                    saveValue={this.saveUserBudgetValue}
                    styledUnitValue={(value: number) => '$' + value.toFixed(2)}
                    unstyleUnitValue={(value: string) => { return value.replace('$', '').replace('.', '').replace(/\d/g, '').length > 0 ? Number.NaN : Number.parseFloat(value.replace('$', '')); }}
                    label='Budget'
                    labelWidth={LABEL_WIDTH}
                    onFocus={() => this.safeSetState({budgetFocused: true})}
                    onBlur={() => this.safeSetState({budgetFocused: false})}
                    helperText={this.state.budgetFocused ? `Must be between $1 and $${Global.user.maxBudget}` : 'Max monthly spend'}
                    minValue={1}
                    maxValue={Global.user.maxBudget}
                    // disabledMessage={Global.user.userExpertise < 2 ? emUpSub : ''}
                />) : (<></>)}
                <TextBox<number>
                    getValue={this.getMaxJobsValue}
                    saveValue={this.saveMaxJobsValue}
                    unstyleUnitValue={(value: string) => { return value.replace(/\d/g, '').length > 0 ? Number.NaN : Number.parseFloat(value); }}
                    label='Jobs/Sessions'
                    labelWidth={LABEL_WIDTH}
                    helperText={'Max combined number of concurrent jobs and sessions'}
                    disabledMessage={emUpSub}
                />
                <TextBox<number>
                    getValue={this.getMaxMachinesValue}
                    saveValue={this.saveMaxMachinesValue}
                    unstyleUnitValue={(value: string) => { return value.replace(/\d/g, '').length > 0 ? Number.NaN : Number.parseFloat(value); }}
                    label='Machines'
                    labelWidth={LABEL_WIDTH}
                    helperText='Max number of concurrent machines'
                    disabledMessage={emUpSub}
                />
                <TextBox<number>
                    getValue={this.getUserHoldoverTimeValue}
                    saveValue={this.saveUserHoldoverTimeValue}
                    styledUnitValue={(value: number) => { return isNaN(value) ? "" : value.toFixed() }}
                    unstyleUnitValue={(value: string) => { return value.replace(/\d/g, '').length > 0 ? Number.NaN : Number.parseFloat(value); }}
                    label='Auto-release'
                    labelWidth={LABEL_WIDTH}
                    onFocus={() => this.safeSetState({holdoverFocused: true})}
                    onBlur={() => this.safeSetState({holdoverFocused: false})}
                    helperText={this.state.holdoverFocused ? `Must be between 0 and ${Global.user.maxHoldoverTime / 60} minutes` : 'Time in minutes before releasing idle machines'}
                    minValue={0}
                    maxValue={+(Global.user.maxHoldoverTime / 60).toFixed()}
                />
                {/* <TextBoxDropdown
                    getValue={this.getUserHoldoverTimeValue}
                    saveValue={this.saveUserHoldoverTimeValue}
                    unitValues={[
                        // {unit: 'seconds', value: 1},
                        {unit: 'minutes', value: 60},
                        // {unit: 'hours', value: 3600},
                    ]}
                    label='Auto-release'
                    labelWidth={LABEL_WIDTH}
                    onFocus={() => this.safeSetState({holdoverFocused: true})}
                    onBlur={() => this.safeSetState({holdoverFocused: false})}
                    helperText={this.state.holdoverFocused ? `Must be between 0 and ${Global.user.maxHoldoverTime / 60} minutes` : 'Time in minutes before releasing idle machines'}
                    minValue={0}
                    maxValue={Global.user.maxHoldoverTime}
                /> */}
            </DIV>
        </>;
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

    public shouldComponentUpdate = (nextProps: IAccountLimitsSubMenuProps, nextState: IAccountLimitsSubMenuState): boolean => {
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

// Properties from parent
interface IAccountBillingSubMenuProps {
	sx?: SxProps<Theme>
    balance: number
    machineCost: number
    serviceFeeCost: number
    storageCost: number
    egressCost: number
}

interface IAccountBillingSubMenuState {
    balance: number
}

export class AccountBillingSubMenu extends React.Component<IAccountBillingSubMenuProps, IAccountBillingSubMenuState> {
    private _isMounted = false;
    private polling = false;
    private timeout: NodeJS.Timeout

    constructor(props: IAccountBillingSubMenuProps) {
        super(props);
        this.state = {
            balance: 0,
        }
    }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <>
                <DIV sx={Object.assign({padding: '6px'}, this.props.sx)}>
                    {Global.user.isSubscribed() ? (
                        <SubscriptionActive 
                            machineCost={this.props.machineCost}
                            serviceFeeCost={this.props.serviceFeeCost}
                            storageCost={this.props.storageCost}
                            egressCost={this.props.egressCost}
                        />
                    ) : Global.user.customerState == CustomerState.FREE_TRIAL ? (
                        <FreeTrial balance={this.props.balance}/>
                    ) : Global.user.customerState == CustomerState.FREE_TRIAL_ENDED ? (
                        <FreeTrialEnded balance={this.props.balance}/>
                    ) : (
                        <SubscriptionEnded balance={this.props.balance}/>
                    )}
                </DIV>
            </>
        )
    }

    private async receiveUpdate() {
		const settings = ServerConnection.makeSettings();
        const url = settings.baseUrl + "optumi/get-balance";
        const now = new Date();
        const epoch = new Date(0);
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				startTime: epoch.toISOString(),
				endTime: now.toISOString(),
			}),
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			if (this.polling) {
				// If we are polling, send a new request in 2 seconds
                if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
				this.timeout = setTimeout(() => this.receiveUpdate(), 2000);
			}
			Global.handleResponse(response);
			return response.json();
		}).then((body: any) => {
			if (body) {
                this.safeSetState({ balance: body.balance });
			}
        });
    }
    
    private handleUserChange = () => {
        this.forceUpdate();
    }

    // Will be called automatically when the component is mounted
	public componentDidMount = () => {
        this._isMounted = true;
        this.polling = true;
        this.receiveUpdate();
        Global.onUserChange.connect(this.handleUserChange);
        Global.user.userInformationChanged.connect(this.handleUserChange);
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
        Global.user.userInformationChanged.disconnect(this.handleUserChange);
        Global.onUserChange.disconnect(this.handleUserChange);
        this._isMounted = false;
        this.polling = false;
        if (this.timeout != null) clearTimeout(this.timeout)
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

    public shouldComponentUpdate = (nextProps: IAccountBillingSubMenuProps, nextState: IAccountBillingSubMenuState): boolean => {
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

// Properties from parent
interface IAccountIntegrationsSubMenuProps {
	sx?: SxProps<Theme>
}

interface IAccountIntegrationsSubMenuState {
    dataConnectors: DataConnectorMetadata[],
    browserKey: number,
}

export class AccountIntegrationsSubMenu extends React.Component<IAccountIntegrationsSubMenuProps, IAccountIntegrationsSubMenuState> {
    private _isMounted = false

    constructor(props: IAccountIntegrationsSubMenuProps) {
        super(props);
        this.state = {
            dataConnectors: [],
            browserKey: 0,
        }
    }

    // Use a key to force the data connector browser to refresh
    private forceNewBrowser = () => {
        this.safeSetState({ browserKey: this.state.browserKey + 1 })
    }

    public request = async () => {
        const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + 'optumi/get-integrations'
		return ServerConnection.makeRequest(url, {}, settings).then(response => {
			if (response.status !== 200) throw new ServerConnection.ResponseError(response);
			return response.json()
		})
    }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <>
                <DIV sx={Object.assign({}, this.props.sx)}>
                    <DIV sx={{display: 'inline-flex', margin: '6px'}}>
                        <Header title='Existing integrations' sx={{ lineHeight: '24px', margin: '6px 6px 6px 11px' }} />
                    </DIV>
                    <Divider />
                    <IntegrationBrowser
                        key={this.state.browserKey}
                        sx={{
                            maxHeight: 'calc(100% - 60px - 2px)',
                        }}
                        type={IntegrationType.ALL}
                        handleDelete={(dataConnectorMetadata: IntegrationMetadata) => {
                            const settings = ServerConnection.makeSettings();
                            const url = settings.baseUrl + "optumi/remove-integration";
                            const init: RequestInit = {
                                method: 'POST',
                                body: JSON.stringify({
                                    name: dataConnectorMetadata.name,
                                }),
                            };
                            ServerConnection.makeRequest(
                                url,
                                init, 
                                settings
                            ).then((response: Response) => {
                                Global.handleResponse(response);
                            }).then(() => {
                                var newDataConnectors = [...this.state.dataConnectors]
                                newDataConnectors = newDataConnectors.filter(dataConnector => dataConnector.name !== dataConnectorMetadata.name)
                                this.safeSetState({dataConnectors: newDataConnectors})
                                this.forceNewBrowser()
                            }).then(() => Global.dataConnectorChange.emit());                   
                        }}
                    />
                    <Divider sx={{marginTop: '33px'}}/>
                    <DIV sx={{display: 'inline-flex', margin: '6px'}}>
                        <Header title='New integrations' sx={{ lineHeight: '24px', margin: '6px 6px 6px 11px'  }} />
                    </DIV>
                    <Divider />
                    <DIV sx={{marginBottom: '6px'}} />
                    <AmazonS3ConnectorPopup onClose={this.forceNewBrowser} />
                    <AzureBlobStorageConnectorPopup onClose={this.forceNewBrowser} />
                    <GoogleCloudStorageConnectorPopup onClose={this.forceNewBrowser} />
                    <GoogleDriveConnectorPopup onClose={this.forceNewBrowser} />
                    <KaggleConnectorPopup onClose={this.forceNewBrowser} />
                    <WasabiConnectorPopup onClose={this.forceNewBrowser} />
                    <EnvironmentVariablePopup onClose={this.forceNewBrowser} />
                </DIV>
            </>
        )
    }

    public componentDidMount = () => {
        this._isMounted = true
        this.request().then(json => this.safeSetState({integrations: json.integrations}))
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

    public shouldComponentUpdate = (nextProps: IAccountIntegrationsSubMenuProps, nextState: IAccountIntegrationsSubMenuState): boolean => {
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

// Properties from parent
interface IAccountStorageSubMenuProps {
	sx?: SxProps<Theme>
}

interface IAccountStorageSubMenuState {}

export class AccountStorageSubMenu extends React.Component<IAccountStorageSubMenuProps, IAccountStorageSubMenuState> {
    
    constructor(props: IAccountStorageSubMenuProps) {
        super(props);
        this.state = {
            files: [],
            appsToFiles: new Map(),
            filesToApps: new Map(),
        }
    }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return <>
            <DIV sx={Object.assign({display: 'flex', flexDirection: 'column', overflowY: 'visible'}, this.props.sx)}>
                <DIV sx={{padding: '20px'}}>
                    <DIV sx={{lineHeight: '36px'}}>
                        Used storage: {FormatUtils.styleStorageOrEgress(Global.user.fileTracker.total, Global.user.fileTracker.limit)}
                        <IconButton
                            sx={{ width: '36px', height: '36px', padding: '3px' }}
                            size='large'
                            onClick={() => Global.user.fileTracker.receiveUpdate(false)}
                        >
                            <Refresh sx={{ width: '30px', height: '30px', padding: '3px' }} />
                        </IconButton>
                    </DIV>
                </DIV>
                <FileBrowser
                    sx={{maxHeight: 'calc(100% - 77px)', flexGrow: 1}}
                    request={(path: string) => Global.user.fileTracker.getContentsForFileBrowser(path)}
                    updateSignal={Global.user.fileTracker.getFilesChanged()}
                    onDownload={(file) => {
                        if (file.type == 'directory') {
                            const fixedPath = Global.convertJupyterPathToOptumiPath(file.path)
                            this.downloadFiles(Global.user.fileTracker.expandDirectory(fixedPath, false), fixedPath)
                        } else {
                            this.downloadFiles([file])
                        }
                    }}
                    onDelete={(file) => {
                        if (file.type == 'directory') {
                            const fixedPath = Global.convertJupyterPathToOptumiPath(file.path)
                            this.deleteFiles(Global.user.fileTracker.expandDirectory(fixedPath), fixedPath)
                        } else {
                            this.deleteFiles(file.content)
                        }
                    }}
                    />
            </DIV>
        </>;
    }

    private async deleteFiles(files: FileMetadata[], directory: string = "") {
        Global.user.fileTracker.deleteFiles(files, directory);
    }

    private async downloadFiles(files: FileMetadata[], directory: string = "") {
		Global.user.fileTracker.downloadFiles(files[0].path, files, false, directory);
    }

    private handleUserChange = () => {
        Global.user.fileTracker.getFilesChanged().connect(this.handleFilesChange);
    }

    private handleFilesChange = () => {
        this.forceUpdate();
    }

    // Will be called automatically when the component is mounted
	public componentDidMount = () => {
        if (Global.user != null) {
            this.handleUserChange();
        }
        Global.onUserChange.connect(this.handleUserChange);
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
        if (Global.user != null) Global.user.fileTracker.getFilesChanged().disconnect(this.handleFilesChange);
        Global.onUserChange.disconnect(this.handleUserChange);
    }

    public shouldComponentUpdate = (nextProps: IAccountStorageSubMenuProps, nextState: IAccountStorageSubMenuState): boolean => {
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
