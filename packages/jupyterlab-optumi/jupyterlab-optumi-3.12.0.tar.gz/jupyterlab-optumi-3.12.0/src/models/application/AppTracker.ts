/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { App } from './App';
import { Global } from '../../Global';

import { ServerConnection } from '@jupyterlab/services';

import { Status } from '../Module';

import { ISignal, Signal } from '@lumino/signaling';

export class AppTracker {
	private _polling = false;

	private _apps: App[] = [];
	private _appsChanged = new Signal<this, App[]>(this);

	constructor() {
		this._polling = true;
		this.receiveAppUpdates();
		this.receiveModuleUpdates();
	}

	get appsChanged(): ISignal<this, App[]> {
		return this._appsChanged;
	}

	get activeJobsOrSessions(): App[] {
		return this._apps.filter((app: App) => app.getAppStatus() != Status.COMPLETED);
	}

	get finishedJobsOrSessions(): App[] {
		return this._apps.filter((app: App) => app.getAppStatus() == Status.COMPLETED);
	}

	get activeSessions(): App[] {
		return this._apps.filter((app: App) => app.getAppStatus() != Status.COMPLETED && app.interactive);
	}

	get finishedSessions(): App[] {
		return this._apps.filter((app: App) => app.getAppStatus() == Status.COMPLETED && app.interactive);
	}

	get activeJobs(): App[] {
		return this._apps.filter((app: App) => app.getAppStatus() != Status.COMPLETED && !app.interactive);
	}

	get finishedJobs(): App[] {
		return this._apps.filter((app: App) => app.getAppStatus() == Status.COMPLETED && !app.interactive);
	}

	public addApp(app: App) {
		this._apps.unshift(app);
		if (Global.shouldLogOnEmit) console.log('SignalEmit (' + new Date().getSeconds() + ')');
		this._appsChanged.emit(this._apps);
		app.globalChangedTrigger = () => {
			if (Global.shouldLogOnEmit) console.log('SignalEmit (' + new Date().getSeconds() + ')');
			this._appsChanged.emit(this._apps)
		}
		app.changed.connect(app.globalChangedTrigger);
	}

	public removeApp(uuid: string) {
		var app: App = this._apps.filter((app: App) => app.uuid == uuid)[0];
		this._apps = this._apps.filter((app: App) => app.uuid != uuid);
		app.changed.disconnect(app.globalChangedTrigger);
		if (Global.shouldLogOnEmit) console.log('SignalEmit (' + new Date().getSeconds() + ')');
		this._appsChanged.emit(this._apps);
	}

	public getDisplayNum() {
		return this._apps.filter((app: App) => app.getAppStatus() != Status.COMPLETED).length;
	}

	public getNum() {
		return this._apps.length;
	}

	// If we are polling, send a new request 2 seconds after completing the previous request
	private  appPollDelay = 2000;
	private receiveAppUpdates() {
		if (!this._polling) return;
		const user = Global.user;
		// If there is an unsigned agreement, do not poll
        if (user == null || (user != null && user.unsignedAgreement)) {
			if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
			setTimeout(() => this.receiveAppUpdates(), this.appPollDelay);
            return;
        }

		try {
			const uuids: string[] = [];
			const lastInitializingLines: number[] = [];
			const lastPreparingLines: number[] = [];
			const lastRunningLines: number[] = [];
			for (var app of this.activeJobsOrSessions) {
				uuids.push(app.uuid);
				lastInitializingLines.push(app.initializing.length);
				lastPreparingLines.push(app.preparing.length);
				lastRunningLines.push(app.running.length);
			}
			// There is no need to make an empty request
			if (uuids.length > 0) {
				const settings = ServerConnection.makeSettings();
				const url = settings.baseUrl + "optumi/pull-workload-status-updates";
				const init: RequestInit = {
					method: 'POST',
					body: JSON.stringify({
						uuids: uuids,
						lastInitializingLines: lastInitializingLines,
						lastPreparingLines: lastPreparingLines,
						lastRunningLines: lastRunningLines,
					}),
				};
				ServerConnection.makeRequest(
					url,
					init, 
					settings
				).then((response: Response) => {
					if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
					setTimeout(() => this.receiveAppUpdates(), this.appPollDelay);
					Global.handleResponse(response);
					return response.json();
				}).then((body: any) => {
					var updated = false;
					for (var app of this._apps) {
						if (body[app.uuid]) {
							const appUpdated = app.handleUpdate(body[app.uuid]);
							updated = updated || appUpdated;
						}
					}
					if (updated) this._appsChanged.emit(this._apps);
				});
			} else {
				if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
				setTimeout(() => this.receiveAppUpdates(), this.appPollDelay);
			}
		} catch (err) {
			console.error(err);
			if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
			setTimeout(() => this.receiveAppUpdates(), this.modPollingDelay);
		}
	}
	// If we are polling, send a new request 1 seconds after completing the previous request
	private modPollingDelay = 2000;
	private async receiveModuleUpdates() {
		if (!this._polling) return;
		const user = Global.user;
        // If there is an unsigned agreement, do not poll
        if (user == null || (user != null && user.unsignedAgreement)) {
			if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
			setTimeout(() => this.receiveModuleUpdates(), this.modPollingDelay);
            return;
        }

		try {
			const workloadUUIDs: string[] = [];
			const moduleUUIDs: string[] = [];
			const lastUpdateLines: number[] = [];
			const lastOutputLines: number[] = [];
			const lastMonitorings: number[] = [];
			const lastPatches: number[] = [];

			for (var app of this.activeJobsOrSessions) {
				for (var module of app.modules) {
					if (module.modStatus != Status.COMPLETED) {
						workloadUUIDs.push(app.uuid);
						moduleUUIDs.push(module.uuid);
						lastUpdateLines.push(module.updates.length);
						lastOutputLines.push(module.output.length);
						lastMonitorings.push(module.monitoring.length);
						lastPatches.push(module.lastPatch);
					}
				}
			}
			const body: any = {
				workloadUUIDs: workloadUUIDs,
				moduleUUIDs: moduleUUIDs,
				lastUpdateLines: lastUpdateLines,
				lastOutputLines: lastOutputLines,
				lastPatches: lastPatches,
			}

			if (user.showMonitoringEnabled) body.lastMonitorings = lastMonitorings;

			// There is no need to make an empty request
			if (workloadUUIDs.length > 0) {
				const settings = ServerConnection.makeSettings();
				const url = settings.baseUrl + "optumi/pull-module-status-updates";
				const init: RequestInit = {
					method: 'POST',
					body: JSON.stringify(body),
				};
				ServerConnection.makeRequest(
					url,
					init, 
					settings
				).then((response: Response) => {
					if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
					setTimeout(() => this.receiveModuleUpdates(), this.modPollingDelay);
					Global.handleResponse(response);
					return response.json();
				}).then((body: any) => {
					var updated = false;
					for (var app of this._apps) {
						for (var module of app.modules) {
							if (body[module.uuid]) {
								const modUpdated = module.handleUpdate(body[module.uuid]);
								updated = updated || modUpdated;
							}
						}
					}
					if (updated) this._appsChanged.emit(this._apps);
				});
			} else {
				if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
				setTimeout(() => this.receiveModuleUpdates(), this.modPollingDelay);
			}
		} catch (err) {
			console.error(err);
			if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
			setTimeout(() => this.receiveModuleUpdates(), this.modPollingDelay);
		}
	}

	public stopPolling() {
		this._polling = false;
	}
}
