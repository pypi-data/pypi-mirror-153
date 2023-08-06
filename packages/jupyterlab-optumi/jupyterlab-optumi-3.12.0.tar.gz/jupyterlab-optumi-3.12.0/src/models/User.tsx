/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

// import * as React from 'react'

import { Global, WhiteTextButton } from '../Global';

import { ServerConnection } from '@jupyterlab/services';
import { ISignal, Signal } from '@lumino/signaling';

import { App } from './application/App';
import { AppTracker } from './application/AppTracker';
import { Machines } from './Machines';
import { Machine } from './machine/Machine';
import { Page } from '../components/deploy/RequirementsBar';
import { FileTracker } from './FileTracker';
import { FileChecker } from './FileChecker';
import { EgressBucket } from './EgressBucket';
import { StorageBucket } from './StorageBucket';
import FormatUtils from '../utils/FormatUtils';
import { SnackbarKey } from 'notistack';
import React from 'react';
import { SubscribeButton } from '../core/SubscribeButton';
import { Snackbar } from './Snackbar';
import { CustomerState } from '../core/CustomerState';

export class User {
	
	// Helper function to avoid duplicate code when logging in
	public static handleLogin(responseData: any): User {
        var machines: Machine[] = []
        for (var i = 0; i < responseData.machines.length; i++) {
            machines.push(Machine.parse(responseData.machines[i]));
        }
		var gpuGrid: Machine[][][] = []
        for (var i = 0; i < responseData.gpuGrid.length; i++) {
			var row = []
			for (var j = 0; j < responseData.gpuGrid[i].length; j++) {
				var bucket = []
				for (var k = 0; k < responseData.gpuGrid[i][j].length; k++) {
					bucket.push(Machine.parse(responseData.gpuGrid[i][j][k]));
				}
				row.push(bucket)
			}
			gpuGrid.push(row)
        }
		var cpuGrid: Machine[][][] = []
        for (var i = 0; i < responseData.cpuGrid.length; i++) {
			var row = []
			for (var j = 0; j < responseData.cpuGrid[i].length; j++) {
				var bucket = []
				for (var k = 0; k < responseData.cpuGrid[i][j].length; k++) {
					bucket.push(Machine.parse(responseData.cpuGrid[i][j][k]));
				}
				row.push(bucket)
			}
			cpuGrid.push(row)
        }

		var egressBuckets = []
		for (var i = 0; i < responseData.egressBuckets.length; i++) {
			egressBuckets.push({ limit: responseData.egressBuckets[i].limit.val, cost: responseData.egressBuckets[i].cost } as EgressBucket)
		}

		var storageBuckets = []
		for (var i = 0; i < responseData.storageBuckets.length; i++) {
			storageBuckets.push({ limit: responseData.storageBuckets[i].limit.val, cost: responseData.storageBuckets[i].cost } as EgressBucket)
		}

        const newUser = new User(
            responseData.newAgreement,
            responseData.name,
            responseData.phoneNumber,
            +responseData.intent,
            +responseData.userBudget,
            +responseData.maxBudget,
            +responseData.budgetCap,
            +responseData.userRate,
            +responseData.maxRate,
            +responseData.rateCap,
            +responseData.userAggregateRate,
            +responseData.maxAggregateRate,
            +responseData.aggregateRateCap,
            +responseData.userHoldoverTime,
            +responseData.maxHoldoverTime,
            +responseData.holdoverTimeCap,
            +responseData.userRecommendations,
            +responseData.maxRecommendations,
            +responseData.recommendationsCap,
            +responseData.maxJobs,
            +responseData.jobsCap,
            +responseData.maxMachines,
            +responseData.machinesCap,
            +responseData.userExpertise,
			responseData.customerState as CustomerState,
			responseData.lastBillPaid,
			responseData.billingCycleAnchor ? new Date(responseData.billingCycleAnchor) : null,
			responseData.compressFilesEnabled,
			responseData.lastPage,
			responseData.stopJobPreventEnabled,
			responseData.deleteJobPreventEnabled,
			responseData.noRequirementsPreventEnabled,
			responseData.noFileUploadsPreventEnabled,
			responseData.startSessionPreventEnabled,
			responseData.notificationsEnabled,
			responseData.snapToInventoryEnabled,
			responseData.showMonitoringEnabled,
			responseData.showDownloadAllButtonEnabled,
			responseData.autoAddOnsEnabled,
			+responseData.egressTotal,
			+responseData.egressLimit,
			+responseData.egressMax,
			egressBuckets,
			storageBuckets, 
			+responseData.serviceFee,
			responseData.trialStart ? new Date(responseData.trialStart) : null,
			responseData.trialEnd ? new Date(responseData.trialEnd) : null,
			responseData.subscriptionStart ? new Date(responseData.subscriptionStart) : null,
			responseData.subscriptionEnd ? new Date(responseData.subscriptionEnd) : null,
			+responseData.credit,
			+responseData.runHistoryLength,
			new Date(responseData.freeTrialEgressLimitDismissed),
			new Date(responseData.freeTrialStorageLimitDismissed),
			new Date(responseData.freeTrialCreditLimitDismissed),
			new Date(responseData.freeTrialExpiredDismissed),
			new Date(responseData.starterEgressLimitDismissed),
			new Date(responseData.starterStorageLimitDismissed),
			new Date(responseData.starterPopupDismissed),
			new Date(responseData.freeTrialStartedPopupDismissed),
			new Date(responseData.holdoverTimePopupDismissed),
            new AppTracker(),
			new FileTracker(),
			new FileChecker(),
            new Machines(machines, responseData.cpuLabels, cpuGrid, responseData.gpuLabels, gpuGrid, responseData.maxRate)
        );
        if (!newUser.unsignedAgreement) newUser.synchronize(responseData);
        return newUser;
	}
	
	private _deploySubMenuChanged = new Signal<this, User>(this);

	get deploySubMenuChanged(): ISignal<this, User> {
		return this._deploySubMenuChanged;
	}

	private _selectedSettingsSubMenuChanged = new Signal<this, User>(this);

	get selectedSettingsSubMenuChanged(): ISignal<this, User> {
		return this._selectedSettingsSubMenuChanged;
	}

	private _userInformationChanged = new Signal<this, User>(this);

	get userInformationChanged(): ISignal<this, User> {
		return this._userInformationChanged;
	}

    private _unsignedAgreement: boolean;

	private _name: string;
	private _phoneNumber: string;
	private _intent: number;
	private _userBudget: number;
	private _maxBudget: number;
	private _budgetCap: number;
    private _userRate: number;
	private _maxRate: number;
    private _rateCap: number;
    private _userAggregateRate: number;
	private _maxAggregateRate: number;
    private _aggregateRateCap: number;
    private _userHoldoverTime: number;
	private _maxHoldoverTime: number;
    private _holdoverTimeCap: number;
    private _userRecommendations: number;
	private _maxRecommendations: number;
    private _recommendationsCap: number;
    private _maxJobs: number;
    private _jobsCap: number;
    private _maxMachines: number;
    private _machinesCap: number;
	private _userExpertise: number;
	private _customerState: CustomerState;
	private _lastBillPaid: boolean;
	private _billingCycleAnchor: Date;
	private _compressFilesEnabled: boolean;
	private _lastPage: number;
	private _stopJobPreventEnabled: boolean;
	private _deleteJobPreventEnabled: boolean;
	private _noRequirementsPreventEnabled: boolean;
	private _noFileUploadsPreventEnabled: boolean;
	private _startSessionPreventEnabled: boolean;
	private _notificationsEnabled: boolean;
	private _snapToInventoryEnabled: boolean;
	private _showMonitoringEnabled: boolean;
	private _showDownloadAllButtonEnabled: boolean;
	private _autoAddOnsEnabled: boolean;
	private _egressTotal: number;
	private _egressLimit: number;
	private _egressMax: number;
	private _egressBuckets: EgressBucket[];
	private _storageBuckets: StorageBucket[];
	private _serviceFee: number;
	private _trialStart: Date;
	private _trialEnd: Date;
	private _subscriptionStart: Date;
	private _subscriptionEnd: Date;
	private _credit: number;
	private _runHistoryLength: number;

	// Some markers to remember if a user has dismissed a warning snackbar
    private _freeTrialEgressLimitDismissed: Date = new Date(0)
    private _freeTrialStorageLimitDismissed: Date = new Date(0)
    private _freeTrialCreditLimitDismissed: Date = new Date(0)
    private _freeTrialExpiredDismissed: Date = new Date(0)
    
    private _starterEgressLimitDismissed: Date = new Date(0)
    private _starterStorageLimitDismissed: Date = new Date(0)
    private _starterPopupDismissed: Date = new Date(0)
    private _freeTrialStartedPopupDismissed: Date = new Date(0)
    private _holdoverTimePopupDismissed: Date = new Date(0)
	
	private _appTracker: AppTracker;
	private _fileTracker: FileTracker;
	private _fileChecker: FileChecker;
	private _machines: Machines;

	private _deploySubMenu: Page = Page.RESOURCES;

    constructor(unsignedAgreement: boolean, name: string, phoneNumber: string, intent: number, 
        userBudget: number, maxBudget: number, budgetCap: number, 
        userRate: number, maxRate: number, rateCap: number, 
        userAggregateRate: number, maxAggregateRate: number, aggregateRateCap: number, 
        userHoldoverTime: number, maxHoldoverTime: number, holdoverTimeCap: number, 
        userRecommendations: number, maxRecommendations: number, recommendationsCap: number, 
        maxJobs: number, jobsCap: number, 
        maxMachines: number, machinesCap: number, 
		userExpertise: number, customerState: CustomerState, lastBillPaid: boolean, billingCycleAnchor: Date,
		compressFilesEnabled: boolean, lastPage: number, 
		stopJobPreventEnabled: boolean, deleteJobPreventEnabled: boolean, noRequirementsPreventEnabled: boolean, noFileUploadsPreventEnabled: boolean, 
		startSessionPreventEnabled: boolean, notificationsEnabled: boolean, snapToInventoryEnabled: boolean, showMonitoringEnabled: boolean, showDownloadAllButtonEnabled: boolean,
		autoAddOnsEnabled: boolean, egressTotal: number, egressLimit: number, egressMax: number,
		egressBuckets: EgressBucket[], storageBuckets: StorageBucket[], serviceFee: number, 
		trialStart: Date, trialEnd: Date, subscriptionStart: Date, subscriptionEnd: Date, 
		credit: number, runHistoryLength: number,
		freeTrialEgressLimitDismissed: Date, freeTrialStorageLimitDismissed: Date, freeTrialCreditLimitDismissed: Date, freeTrialExpiredDismissed: Date, 
		starterEgressLimitDismissed: Date, starterStorageLimitDismissed: Date, starterPopupDismissed: Date, freeTrialStartedPopupDismissed: Date, holdoverTimePopupDismissed: Date,
		appTracker: AppTracker, fileTracker: FileTracker, fileChecker: FileChecker, machines: Machines) {
        this._unsignedAgreement = unsignedAgreement === undefined ? true : unsignedAgreement;
        this._name = name;
        this._phoneNumber = phoneNumber;
		this._intent = intent;
        this._userBudget = userBudget;
        this._maxBudget = maxBudget;
        this._budgetCap = budgetCap;
        this._userRate = userRate;
        this._maxRate = maxRate;
        this._rateCap = rateCap;
        this._userAggregateRate = userAggregateRate;
        this._maxAggregateRate = maxAggregateRate;
        this._aggregateRateCap = aggregateRateCap;
        this._userHoldoverTime = userHoldoverTime;
        this._maxHoldoverTime = maxHoldoverTime;
        this._holdoverTimeCap = holdoverTimeCap;
        this._userRecommendations = userRecommendations;
        this._maxRecommendations = maxRecommendations;
        this._recommendationsCap = recommendationsCap;
        this._maxJobs = maxJobs;
        this._jobsCap = jobsCap;
        this._maxMachines = maxMachines;
        this._machinesCap = machinesCap;

		this._userExpertise = userExpertise;
		this._customerState = customerState;
		this._lastBillPaid = lastBillPaid;
		this._billingCycleAnchor = billingCycleAnchor;

		this._compressFilesEnabled = compressFilesEnabled;
		this._lastPage = lastPage;
		this._stopJobPreventEnabled = stopJobPreventEnabled;
		this._deleteJobPreventEnabled = deleteJobPreventEnabled;
		this._noRequirementsPreventEnabled = noRequirementsPreventEnabled;
		this._noFileUploadsPreventEnabled = noFileUploadsPreventEnabled;
		this._startSessionPreventEnabled = startSessionPreventEnabled;
		this._notificationsEnabled = notificationsEnabled;
		this._snapToInventoryEnabled = snapToInventoryEnabled;
		this._showMonitoringEnabled = showMonitoringEnabled;
		this._showDownloadAllButtonEnabled = showDownloadAllButtonEnabled;
		this._autoAddOnsEnabled = autoAddOnsEnabled;
		this._egressTotal = egressTotal;
		this._egressLimit = egressLimit;
		this._egressMax = egressMax;
		this._egressBuckets = egressBuckets;
		this._storageBuckets = storageBuckets;
		this._serviceFee = serviceFee;
		this._trialStart = trialStart;
		this._trialEnd = trialEnd;
		this._subscriptionStart = subscriptionStart;
		this._subscriptionEnd = subscriptionEnd;
		this._credit = credit;
		this._runHistoryLength = runHistoryLength;

		this._freeTrialEgressLimitDismissed = freeTrialEgressLimitDismissed;
		this._freeTrialStorageLimitDismissed = freeTrialStorageLimitDismissed;
		this._freeTrialCreditLimitDismissed = freeTrialCreditLimitDismissed;
		this._freeTrialExpiredDismissed = freeTrialExpiredDismissed;
		
		this._starterEgressLimitDismissed = starterEgressLimitDismissed;
		this._starterStorageLimitDismissed = starterStorageLimitDismissed;
		this._starterPopupDismissed = starterPopupDismissed;
		this._freeTrialStartedPopupDismissed = freeTrialStartedPopupDismissed;
		this._holdoverTimePopupDismissed = holdoverTimePopupDismissed;

		this._appTracker = appTracker;
		this._fileTracker = fileTracker;
		this._fileChecker = fileChecker;
        this._machines = machines;

		setTimeout(() => this.getUserInformation(), 10000);

		this.generateSnackbars();
    }
    
    get unsignedAgreement(): boolean {
		return this._unsignedAgreement;
    }
    
    set unsignedAgreement(unsignedAgreement: boolean) {
		if (unsignedAgreement === this._unsignedAgreement) {
			return;
		}
		this._unsignedAgreement = unsignedAgreement;
		this._userInformationChanged.emit(this);
	}

	get name(): string {
		return this._name;
	}

	set name(name: string) {
		if (name === this._name) {
			return;
		}
		this._name = name;
		this._userInformationChanged.emit(this);
	}

	get phoneNumber(): string {
		return this._phoneNumber;
	}

	set phoneNumber(phoneNumber: string) {
		if (phoneNumber === this._phoneNumber) {
			return;
		}
		this._phoneNumber = phoneNumber;
		this.setUserInformation("phoneNumber", phoneNumber);
	}

	// TODO:JJ When you delete this you should also delete RequirementsBar.tsx
	get deploySubMenu(): Page {
		return this._deploySubMenu;
	}

	set deploySubMenu(deploySubMenu: Page) {
		if (deploySubMenu === this._deploySubMenu) {
			return;
		}
		this._deploySubMenu = deploySubMenu;
		if (Global.shouldLogOnEmit) console.log('SignalEmit (' + new Date().getSeconds() + ')');
		this._deploySubMenuChanged.emit(this);
	}

	get intent(): number {
		return this._intent;
	}

	set intent(intent: number) {
		if (intent === this._intent) {
			return;
		}
		this._intent = intent;
		this.setUserInformation("intent", intent);
	}

	get userBudget(): number {
		return this._userBudget;
	}

	set userBudget(userBudget: number) {
		if (userBudget === this._userBudget) {
			return;
		}
		this._userBudget = userBudget;
		this.setUserInformation("userBudget", userBudget);
    }
    
    get maxBudget(): number {
		return this._maxBudget;
	}

	set maxBudget(maxBudget: number) {
		if (maxBudget === this._maxBudget) {
			return;
		}
		this._maxBudget = maxBudget;
		this.setUserInformation("maxBudget", maxBudget);
    }
    
    get budgetCap(): number {
		return this._budgetCap;
	}
    
    get userRate(): number {
		return this._userRate;
	}

	set userRate(userRate: number) {
		if (userRate === this._userRate) {
			return;
		}
		this._userRate = userRate;
		this.setUserInformation("userRate", userRate);
    }
    
    get maxRate(): number {
		return this._maxRate;
	}

	set maxRate(maxRate: number) {
		if (maxRate === this._maxRate) {
			return;
		}
		this._maxRate = maxRate;
		this.setUserInformation("maxRate", maxRate);
    }
    
    get rateCap(): number {
		return this._rateCap;
	}
    
    get userAggregateRate(): number {
		return this._userAggregateRate;
	}

	set userAggregateRate(userAggregateRate: number) {
		if (userAggregateRate === this._userAggregateRate) {
			return;
		}
		this._userAggregateRate = userAggregateRate;
		this.setUserInformation("userAggregateRate", userAggregateRate);
    }
    
    get maxAggregateRate(): number {
		return this._maxAggregateRate;
	}

	set maxAggregateRate(maxAggregateRate: number) {
		if (maxAggregateRate === this._maxAggregateRate) {
			return;
		}
		this._maxAggregateRate = maxAggregateRate;
		this.setUserInformation("maxAggregateRate", maxAggregateRate);
    }
    
    get aggregateRateCap(): number {
		return this._aggregateRateCap;
    }
    
    get userHoldoverTime(): number {
		return this._userHoldoverTime;
	}

	set userHoldoverTime(userHoldoverTime: number) {
		if (userHoldoverTime === this._userHoldoverTime) {
			return;
		}
		this._userHoldoverTime = userHoldoverTime;
		this.setUserInformation("userHoldoverTime", userHoldoverTime);
    }
    
    get maxHoldoverTime(): number {
		return this._maxHoldoverTime;
	}

	set maxHoldoverTime(maxHoldoverTime: number) {
		if (maxHoldoverTime === this._maxHoldoverTime) {
			return;
		}
		this._maxHoldoverTime = maxHoldoverTime;
		this.setUserInformation("maxHoldoverTime", maxHoldoverTime);
    }
    
    get holdoverTimeCap(): number {
		return this._holdoverTimeCap;
	}
    get userRecommendations(): number {
		return this._userRecommendations;
	}

	set userRecommendations(userRecommendations: number) {
		if (userRecommendations === this._userRecommendations) {
			return;
		}
		this._userRecommendations = userRecommendations;
		this.setUserInformation("userRecommendations", userRecommendations);
    }
    
    get maxRecommendations(): number {
		return this._maxRecommendations;
	}

	set maxRecommendations(maxRecommendations: number) {
		if (maxRecommendations === this._maxRecommendations) {
			return;
		}
		this._maxRecommendations = maxRecommendations;
		this.setUserInformation("maxRecommendations", maxRecommendations);
    }
    
    get recommendationsCap(): number {
		return this._recommendationsCap;
	}
    get maxJobs(): number {
		return this._maxJobs;
	}

	set maxJobs(maxJobs: number) {
		if (maxJobs === this._maxJobs) {
			return;
		}
		this._maxJobs = maxJobs;
		this.setUserInformation("maxJobs", maxJobs);
    }

    get jobsCap(): number {
		return this._jobsCap;
	}

    get maxMachines(): number {
		return this._maxMachines;
	}

	set maxMachines(maxMachines: number) {
		if (maxMachines === this._maxMachines) {
			return;
		}
		this._maxMachines = maxMachines;
		this.setUserInformation("maxMachines", maxMachines);
    }
    
    get machinesCap(): number {
		return this._machinesCap;
	}

	get userExpertise(): number {
		return this._userExpertise;
	}

	get customerState(): CustomerState {
		return this._customerState;
	}

	// NOTE: This function simply allows us to update the state of a user before we get confirmation from the controller, so it is an extension change only
	set customerState(customerState: CustomerState) {
		if (customerState === this._customerState) {
			return;
		}
		this._customerState = customerState;
		this._userInformationChanged.emit(this);
	}

	public isSubscribed() {
		switch (this._customerState) {
			case CustomerState.STARTER:
				return true;
			case CustomerState.FREE_TRIAL:
			case CustomerState.FREE_TRIAL_ENDED:
			case CustomerState.INIT:
			case CustomerState.SUBSCRIPTION_CANCELED:
		}
		return false;
	}

	get lastBillPaid(): boolean {
		return this._lastBillPaid;
	}

	get billingCycleAnchor(): Date {
		return this._billingCycleAnchor;
	}

	get compressFilesEnabled(): boolean {
		return this._compressFilesEnabled;
	}

	set compressFilesEnabled(compressFilesEnabled: boolean) {
		if (compressFilesEnabled === this._compressFilesEnabled) {
			return;
		}
		this._compressFilesEnabled = compressFilesEnabled;
		this.setUserInformation("compressFilesEnabled", compressFilesEnabled);
	}
	
	get lastPage(): number {
		return this._lastPage;
	}

	set lastPage(lastPage: number) {
		if (lastPage === this.lastPage) {
			return;
		}
		this._lastPage = lastPage;
		this.setUserInformation("lastPage", lastPage);
	}
	
	get stopJobPreventEnabled(): boolean {
		return this._stopJobPreventEnabled;
	}

	set stopJobPreventEnabled(stopJobPreventEnabled: boolean) {
		if (stopJobPreventEnabled === this._stopJobPreventEnabled) {
			return;
		}
		this._stopJobPreventEnabled = stopJobPreventEnabled;
		this.setUserInformation("stopJobPreventEnabled", stopJobPreventEnabled);
	}

	get deleteJobPreventEnabled(): boolean {
		return this._deleteJobPreventEnabled;
	}

	set deleteJobPreventEnabled(deleteJobPreventEnabled: boolean) {
		if (deleteJobPreventEnabled === this._deleteJobPreventEnabled) {
			return;
		}
		this._deleteJobPreventEnabled = deleteJobPreventEnabled;
		this.setUserInformation("deleteJobPreventEnabled", deleteJobPreventEnabled);
	}

	get noRequirementsPreventEnabled(): boolean {
		return this._noRequirementsPreventEnabled;
	}

	set noRequirementsPreventEnabled(noRequirementsPreventEnabled: boolean) {
		if (noRequirementsPreventEnabled === this._noRequirementsPreventEnabled) {
			return;
		}
		this._noRequirementsPreventEnabled = noRequirementsPreventEnabled;
		this.setUserInformation("noRequirementsPreventEnabled", noRequirementsPreventEnabled);
	}

	get noFileUploadsPreventEnabled(): boolean {
		return this._noFileUploadsPreventEnabled;
	}

	set noFileUploadsPreventEnabled(noFileUploadsPreventEnabled: boolean) {
		if (noFileUploadsPreventEnabled === this._noFileUploadsPreventEnabled) {
			return;
		}
		this._noFileUploadsPreventEnabled = noFileUploadsPreventEnabled;
		this.setUserInformation("noFileUploadsPreventEnabled", noFileUploadsPreventEnabled);
	}
	
	get startSessionPreventEnabled(): boolean {
		return this._startSessionPreventEnabled;
	}

	set startSessionPreventEnabled(startSessionPreventEnabled: boolean) {
		if (startSessionPreventEnabled === this._startSessionPreventEnabled) {
			return;
		}
		this._startSessionPreventEnabled = startSessionPreventEnabled;
		this.setUserInformation("startSessionPreventEnabled", startSessionPreventEnabled);
	}

	get notificationsEnabled(): boolean {
		return this._notificationsEnabled;
	}

	set notificationsEnabled(notificationsEnabled: boolean) {
		if (notificationsEnabled === this._notificationsEnabled) {
			return;
		}
		this._notificationsEnabled = notificationsEnabled;
		this.setUserInformation("notificationsEnabled", notificationsEnabled);
	}

	get snapToInventoryEnabled(): boolean {
		return this._snapToInventoryEnabled;
	}

	set snapToInventoryEnabled(snapToInventoryEnabled: boolean) {
		if (snapToInventoryEnabled === this._snapToInventoryEnabled) {
			return;
		}
		this._snapToInventoryEnabled = snapToInventoryEnabled;
		this.setUserInformation("snapToInventoryEnabled", snapToInventoryEnabled);
	}

	get showMonitoringEnabled(): boolean {
		return this._showMonitoringEnabled;
	}

	get autoAddOnsEnabled(): boolean {
		return this._autoAddOnsEnabled;
	}

	set autoAddOnsEnabled(autoAddOnsEnabled: boolean) {
		if (autoAddOnsEnabled === this._autoAddOnsEnabled) {
			return;
		}
		this._autoAddOnsEnabled = autoAddOnsEnabled;
		this.setUserInformation("autoAddOnsEnabled", autoAddOnsEnabled);
	}

	get showDownloadAllButtonEnabled(): boolean {
		return this._showDownloadAllButtonEnabled;
	}

	get egressTotal(): number {
		return this._egressTotal;
	}

	get egressLimit(): number {
		return this._egressLimit;
	}

	get egressMax(): number {
		return this._egressMax;
	}

	get egressBuckets(): EgressBucket[] {
		return this._egressBuckets;
	}

	get storageBuckets(): StorageBucket[] {
		return this._storageBuckets;
	}

	get serviceFee(): number {
		return this._serviceFee;
	}

	get trialStart(): Date {
		return this._trialStart;
	}

	set trialStart(trialStart: Date) {
		if (trialStart === this._trialStart) {
			return;
		}
		this._trialStart = trialStart;
		// We don't actually allow the user to pick the trial start date, so pass null here
		this.setUserInformation("trialStart", null);
	}

	get trialEnd(): Date {
		return this._trialEnd;
	}

	get subscriptionStart(): Date {
		return this._subscriptionStart;
	}

	get subscriptionEnd(): Date {
		return this._subscriptionEnd;
	}

	get credit(): number {
		return this._credit;
	}

	get runHistoryLength(): number {
		return this._runHistoryLength;
	}

	get freeTrialEgressLimitDismissed(): Date {
		return this._freeTrialEgressLimitDismissed;
	}

	set freeTrialEgressLimitDismissed(freeTrialEgressLimitDismissed: Date) {
		if (freeTrialEgressLimitDismissed === this._freeTrialEgressLimitDismissed) {
			return;
		}
		this._freeTrialEgressLimitDismissed = freeTrialEgressLimitDismissed;
		// We don't actually allow the user to pick the trial start date, so pass null here
		this.setUserInformation("freeTrialEgressLimitDismissed", null);
	}

	get freeTrialStorageLimitDismissed(): Date {
		return this._freeTrialStorageLimitDismissed;
	}

	set freeTrialStorageLimitDismissed(freeTrialStorageLimitDismissed: Date) {
		if (freeTrialStorageLimitDismissed === this._freeTrialStorageLimitDismissed) {
			return;
		}
		this._freeTrialStorageLimitDismissed = freeTrialStorageLimitDismissed;
		// We don't actually allow the user to pick the trial start date, so pass null here
		this.setUserInformation("freeTrialStorageLimitDismissed", null);
	}

	get freeTrialCreditLimitDismissed(): Date {
		return this._freeTrialCreditLimitDismissed;
	}

	set freeTrialCreditLimitDismissed(freeTrialCreditLimitDismissed: Date) {
		if (freeTrialCreditLimitDismissed === this._freeTrialCreditLimitDismissed) {
			return;
		}
		this._freeTrialCreditLimitDismissed = freeTrialCreditLimitDismissed;
		// We don't actually allow the user to pick the trial start date, so pass null here
		this.setUserInformation("freeTrialCreditLimitDismissed", null);
	}

    get freeTrialExpiredDismissed(): Date {
		return this._freeTrialExpiredDismissed;
	}

	set freeTrialExpiredDismissed(freeTrialExpiredDismissed: Date) {
		if (freeTrialExpiredDismissed === this._freeTrialExpiredDismissed) {
			return;
		}
		this._freeTrialExpiredDismissed = freeTrialExpiredDismissed;
		// We don't actually allow the user to pick the trial start date, so pass null here
		this.setUserInformation("freeTrialExpiredDismissed", null);
	}

	get starterEgressLimitDismissed(): Date {
		return this._starterEgressLimitDismissed;
	}

	set starterEgressLimitDismissed(starterEgressLimitDismissed: Date) {
		if (starterEgressLimitDismissed === this._starterEgressLimitDismissed) {
			return;
		}
		this._starterEgressLimitDismissed = starterEgressLimitDismissed;
		// We don't actually allow the user to pick the trial start date, so pass null here
		this.setUserInformation("starterEgressLimitDismissed", null);
	}

	get starterStorageLimitDismissed(): Date {
		return this._starterStorageLimitDismissed;
	}

	set starterStorageLimitDismissed(starterStorageLimitDismissed: Date) {
		if (starterStorageLimitDismissed === this._starterStorageLimitDismissed) {
			return;
		}
		this._starterStorageLimitDismissed = starterStorageLimitDismissed;
		// We don't actually allow the user to pick the trial start date, so pass null here
		this.setUserInformation("starterStorageLimitDismissed", null);
	}

	get starterPopupDismissed(): Date {
		return this._starterPopupDismissed;
	}

	set starterPopupDismissed(starterPopupDismissed: Date) {
		if (starterPopupDismissed === this._starterPopupDismissed) {
			return;
		}
		this._starterPopupDismissed = starterPopupDismissed;
		// We don't actually allow the user to pick the trial start date, so pass null here
		this.setUserInformation("starterPopupDismissed", null);
	}

	get freeTrialStartedPopupDismissed(): Date {
		return this._freeTrialStartedPopupDismissed;
	}

	set freeTrialStartedPopupDismissed(freeTrialStartedPopupDismissed: Date) {
		if (freeTrialStartedPopupDismissed === this._freeTrialStartedPopupDismissed) {
			return;
		}
		this._freeTrialStartedPopupDismissed = freeTrialStartedPopupDismissed;
		// We don't actually allow the user to pick the trial start date, so pass null here
		this.setUserInformation("freeTrialStartedPopupDismissed", null);
	}

	get holdoverTimePopupDismissed(): Date {
		return this._holdoverTimePopupDismissed;
	}

	set holdoverTimePopupDismissed(holdoverTimePopupDismissed: Date) {
		if (holdoverTimePopupDismissed === this._holdoverTimePopupDismissed) {
			return;
		}
		this._holdoverTimePopupDismissed = holdoverTimePopupDismissed;
		// We don't actually allow the user to pick the trial start date, so pass null here
		this.setUserInformation("holdoverTimePopupDismissed", null);
	}

	get fileTracker(): FileTracker {
		return this._fileTracker;
	}

	get appTracker(): AppTracker {
		return this._appTracker;
	}

	get fileChecker(): FileChecker {
		return this._fileChecker;
	}

	set machines(machines: Machines) {
		if (machines === this._machines) {
			return;
		}
		this._machines = machines;
	}

	get machines(): Machines {
		return this._machines;
	}
		
	public synchronize(responseData: any) {
		// Add apps from user information if they don't already exist
		if (responseData.jobs) {
			NEW_APPS:
			for (let newApp of responseData.jobs) {
				// Ignore this app if we already have an object for it
				for (let app of this.appTracker.finishedSessions) {
					if (app.uuid == newApp.uuid) continue NEW_APPS;
				}
				for (let app of this.appTracker.finishedJobs) {
					if (app.uuid == newApp.uuid) continue NEW_APPS;
				}
				for (let app of this.appTracker.activeSessions) {
					if (app.uuid == newApp.uuid) continue NEW_APPS;
				}
				for (let app of this.appTracker.activeJobs) {
					if (app.uuid == newApp.uuid) continue NEW_APPS;
				}
				this.appTracker.addApp(App.reconstruct(newApp));
			}
		}
	}

	private getUserInformation() {
		if (Global.user == null) return

		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/get-user-information";
		const init = {
			method: 'POST',
			body: JSON.stringify({
				includeAll: false,
			})
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response);
			return response.json();
		}).then((body: any) => {
			if (body) {
				if (body.name) this._name = body.name
				if (body.phoneNumber) this._phoneNumber = body.phoneNumber
				if (body.intent) this._intent = +body.intent
				if (body.userBudget) this._userBudget = +body.userBudget
				if (body.maxBudget) this._maxBudget = +body.maxBudget
				if (body.budgetCap) this._budgetCap = +body.budgetCap
				if (body.userRate) this._userRate = +body.userRate
				if (body.maxRate) this._maxRate = +body.maxRate
				if (body.rateCap) this._rateCap = +body.rateCap
				if (body.userAggregateRate) this._userAggregateRate = +body.userAggregateRate
				if (body.maxAggregateRate) this._maxAggregateRate = +body.maxAggregateRate
				if (body.aggregateRateCap) this._aggregateRateCap = +body.aggregateRateCap
				if (body.userHoldoverTime) this._userHoldoverTime = +body.userHoldoverTime
				if (body.maxHoldoverTime) this._maxHoldoverTime = +body.maxHoldoverTime
				if (body.holdoverTimeCap) this._holdoverTimeCap = +body.holdoverTimeCap
				if (body.userRecommendations) this._userRecommendations = +body.userRecommendations
				if (body.maxRecommendations) this._maxRecommendations = +body.maxRecommendations
				if (body.recommendationsCap) this._recommendationsCap = +body.recommendationsCap
				if (body.maxJobs) this._maxJobs = +body.maxJobs
				if (body.jobsCap) this._jobsCap = +body.jobsCap
				if (body.maxMachines) this._maxMachines = +body.maxMachines
				if (body.machinesCap) this._machinesCap = +body.machinesCap
				if (body.userExpertise) this._userExpertise = +body.userExpertise
				if (body.customerState) this._customerState = body.customerState as CustomerState
				if (body.lastBillPaid != undefined) this._lastBillPaid = body.lastBillPaid
				if (body.billingCycleAnchor) this._billingCycleAnchor = new Date(body.billingCycleAnchor)
				if (body.compressFilesEnabled != undefined) this._compressFilesEnabled = body.compressFilesEnabled
				if (body.lastPage) this._lastPage = body.lastPage
				if (body.stopJobPreventEnabled != undefined) this._stopJobPreventEnabled = body.stopJobPreventEnabled
				if (body.deleteJobPreventEnabled != undefined) this._deleteJobPreventEnabled = body.deleteJobPreventEnabled
				if (body.noRequirementsPreventEnabled != undefined) this._noRequirementsPreventEnabled = body.noRequirementsPreventEnabled
				if (body.noFileUploadsPreventEnabled != undefined) this._noFileUploadsPreventEnabled = body.noFileUploadsPreventEnabled
				if (body.startSessionPreventEnabled != undefined) this._startSessionPreventEnabled = body.startSessionPreventEnabled
				if (body.notificationsEnabled != undefined) this._notificationsEnabled = body.notificationsEnabled
				if (body.snapToInventoryEnabled != undefined) this._snapToInventoryEnabled = body.snapToInventoryEnabled
				if (body.showMonitoringEnabled != undefined) this._showMonitoringEnabled = body.showMonitoringEnabled
				if (body.showDownloadAllButtonEnabled != undefined) this._showDownloadAllButtonEnabled = body.showDownloadAllButtonEnabled
				if (body.autoAddOnsEnabled != undefined) this._autoAddOnsEnabled = body.autoAddOnsEnabled
				if (body.egressTotal) this._egressTotal = +body.egressTotal
				if (body.egressLimit) {
					if (this._egressLimit != 0 && +body.egressLimit > this._egressLimit) {
						const action = (key: SnackbarKey) => (
                            <>
                                <WhiteTextButton
                                    onClick={() => {
                                        Global.followLink(Global.Target.SettingsPopup.BillingTab)
                                    }}
                                >
                                    View upgrade settings
                                </WhiteTextButton>
                                <WhiteTextButton
                                    onClick={() => {
                                        Global.snackbarClose.emit(key) 
                                    }}
                                >
                                    Dismiss
                                </WhiteTextButton>
                            </>
                        );
                        Global.snackbarEnqueue.emit(new Snackbar(
                            'Your egress has been upgraded to ' + FormatUtils.styleCapacityUnitValue()(+body.egressLimit),
                            { variant: 'success', persist: true, action }
                        ));
                    }
					this._egressLimit = +body.egressLimit
				}
				if (body.egressMax) this._egressMax = +body.egressMax
				if (body.egressBuckets) {
					var egressBuckets = []
					for (var i = 0; i < body.egressBuckets.length; i++) {
						egressBuckets.push({ limit: body.egressBuckets[i].limit.val, cost: body.egressBuckets[i].cost } as EgressBucket)
					}
					this._egressBuckets = egressBuckets
				}
				if (body.storageBuckets) {
					var storageBuckets = []
					for (var i = 0; i < body.storageBuckets.length; i++) {
						storageBuckets.push({ limit: body.storageBuckets[i].limit.val, cost: body.storageBuckets[i].cost } as EgressBucket)
					}
					this._storageBuckets = storageBuckets
				}
				if (body.egressMax) this._egressMax = +body.egressMax
				if (body.serviceFee) this._serviceFee = +body.serviceFee
				if (body.trialStart) this._trialStart = new Date(body.trialStart)
				if (body.trialEnd) this._trialEnd = new Date(body.trialEnd)
				if (body.subscriptionStart) this._subscriptionStart = new Date(body.subscriptionStart)
				if (body.subscriptionEnd) this._subscriptionEnd = new Date(body.subscriptionEnd)
				if (body.credit) this._credit = +body.credit
				if (body.runHistoryLength) this._runHistoryLength = +body.runHistoryLength

				if (body.freeTrialEgressLimitDismissed) this._freeTrialEgressLimitDismissed = new Date(body.freeTrialEgressLimitDismissed);
				if (body.freeTrialStorageLimitDismissed) this._freeTrialStorageLimitDismissed = new Date(body.freeTrialStorageLimitDismissed);
				if (body.freeTrialCreditLimitDismissed) this._freeTrialCreditLimitDismissed = new Date(body.freeTrialCreditLimitDismissed);
				if (body.freeTrialExpiredDismissed) this._freeTrialExpiredDismissed = new Date(body.freeTrialExpiredDismissed);
				
				if (body.starterEgressLimitDismissed) this._starterEgressLimitDismissed = new Date(body.starterEgressLimitDismissed);
				if (body.starterStorageLimitDismissed) this._starterStorageLimitDismissed = new Date(body.starterStorageLimitDismissed);
				if (body.starterPopupDismissed) this._starterPopupDismissed = new Date(body.starterPopupDismissed);
				if (body.freeTrialStartedPopupDismissed) this._freeTrialStartedPopupDismissed = new Date(body.freeTrialStartedPopupDismissed);
				if (body.holdoverTimePopupDismissed) this._holdoverTimePopupDismissed = new Date(body.holdoverTimePopupDismissed);

				this._userInformationChanged.emit(this);
				this.generateSnackbars();
			}
			setTimeout(() => this.getUserInformation(), 10000);
		}, (err) => {
			// Make sure we still poll even if we encounter an error
			console.error(err)
			setTimeout(() => this.getUserInformation(), 10000);
		});
	}

	private generateSnackbars() {
		const now = new Date()
		if (!this.isSubscribed()) {
			// freeTrialEgressLimit
			if ((now.getTime() - this.freeTrialEgressLimitDismissed.getTime() > Global.dismissalTimeout) && this.egressTotal >= this.egressLimit) {
				const action = (key: SnackbarKey) => (
					<>
						<SubscribeButton
							variant='whiteText'
							color='secondary'
							onClick={() => {
								this.freeTrialEgressLimitDismissed = new Date();
							}}
						/>
						<WhiteTextButton
							onClick={() => {
								this.freeTrialEgressLimitDismissed = new Date();
								Global.snackbarClose.emit(key) 
							}}
						>
							Dismiss
						</WhiteTextButton>
					</>
				);
				Global.snackbarEnqueue.emit(new Snackbar(
					'You have reached the ' + FormatUtils.styleCapacityUnitValue()(this._egressLimit) + ' egress limit',
					{ variant: 'error', persist: true, action }
				));
			}
		} else {
			// starterEgressLimit
			if ((now.getTime() - this.starterEgressLimitDismissed.getTime() > Global.dismissalTimeout) && !this.autoAddOnsEnabled && this.egressTotal >= this.egressLimit) {
				const action = (key: SnackbarKey) => (
					<>
						<WhiteTextButton
							onClick={() => {
								Global.followLink(Global.Target.SettingsPopup.BillingTab)
							}}
						>
							View upgrade settings
						</WhiteTextButton>
						<WhiteTextButton
							onClick={() => {
								this.starterEgressLimitDismissed = new Date();
								Global.snackbarClose.emit(key) 
							}}
						>
							Dismiss
						</WhiteTextButton>
					</>
				);
				Global.snackbarEnqueue.emit(new Snackbar(
					'You have reached the ' + FormatUtils.styleCapacityUnitValue()(this._egressLimit) + ' egress limit',
					{ variant: 'error', persist: true, action, }
				));
			}
		}
	}

	private setUserInformation(param: string, value: any) {
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/set-user-information";
		const init = {
			method: 'POST',
			body: JSON.stringify({
				'param': param,
				'value': value,
			})
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response);
		});
		this._userInformationChanged.emit(this);
	}
}
