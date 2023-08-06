/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { Global, WhiteTextButton } from '../../Global';

import { ServerConnection } from '@jupyterlab/services';
import { NotebookModel } from '@jupyterlab/notebook';
import { ISignal, Signal } from '@lumino/signaling';

import { ProgressMessage } from '../ProgressMessage';
import { Module, Status } from '../Module';
import { AppTracker } from './AppTracker';
import { OptumiConfig } from '../OptumiConfig';
import { FileUploadConfig } from '../FileUploadConfig';
import { Machine, NoMachine } from '../machine/Machine';
import { Update } from '../Update';
import { Snackbar, SnackbarActionType } from '../Snackbar';
import FileServerUtils from '../../utils/FileServerUtils';
import { IdentityAppComponent } from './IdentityAppComponent';
import { AppComponent } from './AppComponent';
import { PopupAppComponent } from './PopupAppComponent';
import { FileMetadata } from '../../components/deploy/fileBrowser/FileBrowser';

import { applyPatch } from 'rfc6902';
import { SnackbarKey } from 'notistack';
import { SubscribeButton } from '../../core/SubscribeButton';

export enum Phase {
	Initializing = 'initializing',
	Preparing = 'preparing',
	Running = 'running',
}

export class App {
	private _changed = new Signal<this, App>(this);

	get changed(): ISignal<this, App> {
		return this._changed;
	}

	public globalChangedTrigger: () => void

	private _notebook: any;
	private _config: OptumiConfig;

	private applyPatch = (patch: any) => {
		applyPatch(this._notebook, patch);
	}

	private updateNotebook = (notebook: any) => {
		this._notebook = notebook;
	}

	private _path: string;
	private _uuid: string = "";
	private _modules: Module[] = [];

	private _initializing: ProgressMessage;
	private _preparing: ProgressMessage;
	private _running: ProgressMessage;

	private _files: FileMetadata[];

	private _timestamp: Date;
	private _runNum: number;

	constructor(path: string, notebook: any = {}, config: OptumiConfig = new OptumiConfig(), uuid: string = "",
		initializing: Update[] = [], preparing: Update[] = [], running: Update[] = [], files: FileMetadata[] = [], timestamp = new Date(), runNum: number = 0) {		

		this._notebook = notebook;
		this._config = config.copy();

		this._path = path;
		this._uuid = uuid;

		this._initializing = new ProgressMessage(Phase.Initializing, initializing);
		this._preparing = new ProgressMessage(Phase.Preparing, preparing);
		this._running = new ProgressMessage(Phase.Running, running);
		
		this._files = files;

		if (this._uuid != "") {
			this._initializing.appUUID = this._uuid;
			this._preparing.appUUID = this._uuid;
			this._running.appUUID = this._uuid;
		}

		this._timestamp = timestamp;
		this._runNum = runNum;

		// Handle errors where we were unable to load some of the updates
		if (this._running.started) {
			if (!this._preparing.completed) {
				this._preparing.addUpdate(new Update("Unable to retrieve preparing updates", ""), false);
				this._preparing.addUpdate(new Update("stop", ""), false);
			}
			if (!this._initializing.completed) {
				this._initializing.addUpdate(new Update("Unable to retrieve initializing updates", ""), false);
				this._initializing.addUpdate(new Update("stop", ""), false);
			}
		} else if (this._preparing.started) {
			if (!this._initializing.completed) {
				this._initializing.addUpdate(new Update("Unable to retrieve initializing updates", ""), false);
				this._initializing.addUpdate(new Update("stop", ""), false);
			}
		}
	}

	// Static function for generating an app from controller synchronization structure
	public static reconstruct(appMap: any): App {
		// Reconstruct the app
        const initializing: Update[] = [];
        for (let i = 0; i < appMap.initializing.length; i++) {
            initializing.push(new Update(appMap.initializing[i], appMap.initializingmod[i]));
        }
        const preparing: Update[] = [];
        for (let i = 0; i < appMap.preparing.length; i++) {
            preparing.push(new Update(appMap.preparing[i], appMap.preparingmod[i]));
        }
        const running: Update[] = [];
        for (let i = 0; i < appMap.running.length; i++) {
            running.push(new Update(appMap.running[i], appMap.runningmod[i]));
        }

		const inputFiles: FileMetadata[] = [];
		if (appMap.files) {
			for (let i = 0; i < appMap.files.length; i++) {
				if (appMap.files[i] != '') {
					inputFiles.push({
						created: appMap.filescrt ? appMap.filescrt[i] : undefined, // Handle backwards compatibility from before we had creation time
						last_modified: appMap.filesmod ? appMap.filesmod[i] : undefined,
						name: (appMap.files[i] as string).split('/').pop(),
						path: appMap.files[i],
						size: +appMap.filessize[i],
						type: 'file',
						hash: appMap.hashes[i],
					} as FileMetadata);
				}
			}
		}

		var app: App = new App(appMap.name, JSON.parse(appMap.notebook), new OptumiConfig(JSON.parse(appMap.nbConfig)), appMap.uuid, initializing, preparing, running, inputFiles, new Date(appMap.timestamp), appMap.runNum);
		// Add modules
		for (let module of appMap.modules) {
            const output: Update[] = [];
			if (module.output) {
				for (let i = 0; i < module.output.length; i++) {
					output.push(new Update(module.output[i], module.outputmod[i]));
				}
			}
			const updates: Update[] = [];
			if (module.updates) {
				for (let i = 0; i < module.updates.length; i++) {
					updates.push(new Update(module.updates[i], module.updatesmod[i]));
				}
			}
            const outputFiles: FileMetadata[] = [];
			if (module.files) {
				for (let i = 0; i < module.files.length; i++) {
					if (module.files[i] != '') {
						outputFiles.push({
							created: module.filescrt ? module.filescrt[i] : undefined, // Handle backwards compatibility from before we had creation time
							last_modified: module.filesmod ? module.filesmod[i] : undefined,
							name: (module.files[i] as string).split('/').pop(),
							path: module.files[i],
							size: +module.filessize[i],
							type: 'file',
							hash: module.hashes[i],
						} as FileMetadata);
					}
				}
			}
			const monitoring: Update[] = [];
			if (module.monitoring) {
				for (let i = 0; i < module.monitoring.length; i++) {
					monitoring.push(new Update(module.monitoring[i], module.monitoringmod[i]));
				}
			}
			var lastPatch: number = 0;
			if (module.patches) {
				for (let i = 0; i < module.patches.length; i++) {
					const patch = module.patches[i];
					try {
						app.applyPatch(JSON.parse(patch));
						const n = module.patchesmod[i]
						if (!isNaN(parseFloat(n)) && isFinite(n)) lastPatch = +n;
					} catch (err) {
						if (patch != 'stop') console.warn('Unable to apply patch ' + patch);
					}
				}
			}
			if (module.notebook) {
				const notebook = module.notebook;
				try {
					app.updateNotebook(JSON.parse(notebook));
					const n = module.patchesmod[0]
					if (!isNaN(parseFloat(n)) && isFinite(n)) lastPatch = +n;
				} catch (err) {
					console.warn('Unable to update notebook ' + notebook);
				}
			}

			var mod: Module = new Module(module.uuid, module.machine ? Machine.parse(module.machine) : null, module.token, output, updates, outputFiles, monitoring, lastPatch);
			mod.applyPatch = app.applyPatch;
			app._modules.push(mod);
		}
		return app;
	}

	public handleUpdate(body: any): boolean {
		let updated = false
		if (body.initializing != null) {
			if (body.initializing.length > 0) updated = true;
			for (let i = 0; i < body.initializing.length; i++) {
				this._initializing.addUpdate(new Update(body.initializing[i], body.initializingmod[i]), false);
			}
		}
		if (body.preparing != null) {
			if (body.preparing.length > 0) updated = true;
			for (let i = 0; i < body.preparing.length; i++) {
				this._preparing.addUpdate(new Update(body.preparing[i], body.preparingmod[i]), false);
				// Special case a warning when we fail to get a machine and start trying a new one
				if ((body.preparing[i] as string).startsWith('Machine unavailable, trying another')) {
					if (Global.shouldLogOnEmit) console.log('SignalEmit (' + new Date().getSeconds() + ')');
					Global.snackbarEnqueue.emit(new Snackbar(
						this.name + " (" +  this.annotationOrRunNum + "): " + body.preparing[i],
						{ variant: 'warning', }
					));
				}
			}
		}
		if (body.running != null) {
			if (body.running.length > 0) updated = true;
			for (let i = 0; i < body.running.length; i++) {
				if (body.running[i] == 'Completed') {
					if (Global.shouldLogOnEmit) console.log('SignalEmit (' + new Date().getSeconds() + ')');
					Global.snackbarEnqueue.emit(new Snackbar(
						this.name + " (" + this.annotationOrRunNum + "): " + body.running[i],
						{ variant: 'success', }
					));
				} else if (body.running[i] == 'Failed') {
					if (Global.shouldLogOnEmit) console.log('SignalEmit (' + new Date().getSeconds() + ')');
					Global.snackbarEnqueue.emit(new Snackbar(
						this.name + " (" + this.annotationOrRunNum + "): " + body.running[i],
						{ variant: 'error', }
					));
				}
				const update = new Update(body.running[i], body.runningmod[i]);
				if (update.modifier.startsWith('{')) {
					try {
						const jsonPayload = JSON.parse(update.modifier);
						if (jsonPayload.snackbar) {
							const actions = jsonPayload.actions as SnackbarActionType[];
							const action = (key: SnackbarKey) => (
								<>
									{actions.includes(SnackbarActionType.SUBSCRIBE) && !Global.user.isSubscribed() &&
										<SubscribeButton
											variant='whiteText'
											color='secondary'
										/>
									}
									{actions.includes(SnackbarActionType.ENABLE_AUTO_ADD_ONS) && Global.user.isSubscribed() &&
										<WhiteTextButton
											onClick={() => {
												Global.followLink(Global.Target.SettingsPopup.BillingTab)
											}}
										>
											View upgrade settings
										</WhiteTextButton>
									}
									{actions.includes(SnackbarActionType.DISMISS) &&
										<WhiteTextButton
											onClick={() => {
												Global.snackbarClose.emit(key)
											}}
										>
											Dismiss
										</WhiteTextButton>
									}
								</>
							);
							Global.snackbarEnqueue.emit(new Snackbar(
								jsonPayload.snackbar,
								{ variant: jsonPayload.level, persist: !actions.includes(SnackbarActionType.AUTO_REMOVE), action }
							));
						}
					} catch (err) {
						console.error(err);
					}
				}
				this._running.addUpdate(update, false);
			}
		}
		return updated;
	}

	get notebook(): any {
		const copy = JSON.parse(JSON.stringify(this._notebook));
		// JupyterLab combines lines with \n, but we need to combine them with ''
		for (var cell of copy.cells) {
			if (cell.outputs) {
				for (var output of cell.outputs) {
					if (output.text) {
						if (Array.isArray(output.text)) {
							output.text = (output.text as string[]).join('');
						} else {
							output.text = output.text.toString()
						}
					}
				}
			}
		}
		// Let JupyterLab handle the formatting
		const model = new NotebookModel()
		model.fromJSON(copy);
		model.initialize()
		const formatted = model.toJSON()
		return formatted
	}

	get config(): OptumiConfig {
		return this._config;
	}

	set config(config: OptumiConfig) {
		// Make sure we don't have a reference to configuration that will be changed
		this._config = config.copy();

		// Tell the controller about the change
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/push-workload-config";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				workload: this._uuid,
				nbConfig: JSON.stringify(config),
			}),
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response)
		});
	}

	get path(): string {
		return this._path;
	}

	get name(): string {
		return this._path.split('/').pop().replace('.ipynb', '');
	}

	get annotationOrRunNum(): string {
		return this.config.annotation == '' ? 'Run #' + this.runNum : this.config.annotation;
	}

	get uuid(): string {
		return this._uuid;
	}

	get modules(): Module[] {
		return this._modules;
	}

	get initializing(): ProgressMessage {
		return this._initializing;
	}

	get preparing(): ProgressMessage {
		return this._preparing;
	}

	get running(): ProgressMessage {
		return this._running;
	}

	get files(): FileMetadata[] {
		return this._files;
	}

	get timestamp(): Date {
		return this._timestamp;
	}

	get runNum(): number {
		return this._runNum;
	}

	get warning(): boolean {
		return this._running.warning;
	}

	get error(): boolean {
		for (let mod of this.modules) {
			if (mod.error) return true;
		}
		return this._initializing.error || this._preparing.error || this._running.error;
	}

	get interactive(): boolean {
		return this._config.interactive;
	}

	get sessionToken(): string {
        for (let mod of this.modules) {
			if (mod.sessionToken) return mod.sessionToken;
        }
        return undefined;
	}

    get machine(): Machine {
        for (let mod of this.modules) {
			if (mod.machine) return mod.machine;
        }
        return undefined;
	}

    public getComponent(): React.CElement<any, AppComponent> {
        return React.createElement(AppComponent, {key: this.uuid, app: this});
    }

    public getPopupComponent(onOpen: () => void, onClose: () => void): React.CElement<any, PopupAppComponent> {
        return React.createElement(PopupAppComponent, {key: this.uuid, app: this, onOpen: onOpen, onClose: onClose});
    }

    public getIdentityComponent(): React.CElement<any, IdentityAppComponent> {
        return React.createElement(IdentityAppComponent, {key: this.path, app: this});
    }
	
	public async previewNotebook(printRecommendations: boolean): Promise<Machine[]> {
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/preview-notebook";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				nbConfig: JSON.stringify(this._config),
				includeExisting: true,
			}),
		};
		return ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response);
			return response.json();
		}).then((body: any) => {
			if (printRecommendations) {
				console.log("////");
				console.log("///  Start Recommendations: ");
				console.log("//");

				for (let machine of body.machines) {
					console.log(Machine.parse(machine));
				}

				console.log("//");
				console.log("///  End Recommendations: ");
				console.log("////");
			}
            if (body.machines.length == 0) return [new NoMachine()]; // we have no recommendations
            const machines: Machine[] = [];
            for (let machine of body.machines) {
                machines.push(Machine.parse(machine));
            }
			return machines;
		});
	}

	// We only want to add this app to the app tracker if the initialization succeeds
	public async setupNotebook(appTracker: AppTracker) {
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/setup-notebook";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				name: this._path,
				timestamp: this._timestamp.toISOString(),
				notebook: {
					path: this._path,
					content: JSON.stringify(this._notebook),
				},
				nbConfig: JSON.stringify(this._config),
			}),
		};
		return ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response);
			return response.json();
		}).then((body: any) => {
			if (Global.shouldLogOnEmit) console.log('SignalEmit (' + new Date().getSeconds() + ')');
			Global.jobLaunched.emit();
			this._uuid = body.uuid;
			this._runNum = body.runNum;
			this._initializing.appUUID = this._uuid;
			this._preparing.appUUID = this._uuid;
			this._running.appUUID = this._uuid;
			this._initializing.addUpdate(new Update("Initializing", ""));
			appTracker.addApp(this);
			if (Global.shouldLogOnEmit) console.log('SignalEmit (' + new Date().getSeconds() + ')');
			this._changed.emit(this);
			this.launchNotebook();
		});
	}

	private previousLaunchStatus: any;
	private pollingDelay = 500;
	private getLaunchStatus() {
        // If there is an unsigned agreement, do not poll
        if (Global.user != null && Global.user.unsignedAgreement) {
            if (!this.error) {
				if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
				setTimeout(() => this.getLaunchStatus(), this.pollingDelay);
			}
            return;
        }
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/get-launch-status";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				uuid: this._uuid,
			}),
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response);
			if (response.status == 204) {
				if (!this.error) {
					if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
					setTimeout(() => this.getLaunchStatus(), this.pollingDelay);
				}
				return;
			}
			return response.json();
		}).then((body: any) => {
			if (body) {
				if (body.status == "Finished") {
					for (let i = 0; i < body.modules.length; i++) {
						const mod = new Module(body.modules[i]);
						mod.applyPatch = this.applyPatch
						mod.updateNotebook = this.updateNotebook
						this._modules.push(mod);
					}
					if (body.files) {
						for (let i = 0; i < body.files.length; i++) {
							if (body.files[i] != '') {
								this._files.push({
									created: body.filescrt[i],
									last_modified: body.filesmod[i],
									name: (body.files[i] as string).split('/').pop(),
									path: body.files[i],
									size: +body.filessize[i],
									type: 'file',
									hash: body.hashes[i],
								} as FileMetadata);
							}
						}
					}
				} else if (body.status == "Failed") {
					if (!this._initializing.completed) {
						this._initializing.addUpdate(new Update(body.message || 'Initialization failed', ""));
						this._initializing.addUpdate(new Update("error", ""));
						this._initializing.addUpdate(new Update("stop", ""));
					}
					if (body.snackbar) {
						if (Global.shouldLogOnEmit) console.log('SignalEmit (' + new Date().getSeconds() + ')');
						Global.snackbarEnqueue.emit(new Snackbar(
                            this.name + " (" + this.annotationOrRunNum + "): " + body.snackbar,
                            { variant: 'error', }
                        ));
					}
				} else {
					if (!this.error) {
						if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
						setTimeout(() => this.getLaunchStatus(), this.pollingDelay);
					}
                }
				if (JSON.stringify(body) !== JSON.stringify(this.previousLaunchStatus)) {
					if (Global.shouldLogOnEmit) console.log('SignalEmit (' + new Date().getSeconds() + ')');
					this._changed.emit(this);
					this.previousLaunchStatus = body
				}
            }
		}, (error: ServerConnection.ResponseError) => {
			if (!this.error) {
				if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
				setTimeout(() => this.getLaunchStatus(), this.pollingDelay);
			}
		});
	}

	// Convert and send a python notebook to the REST interface for deployment
	private async launchNotebook() {
		const uploadFiles: FileUploadConfig[] = this._config.upload.files;
		const requirements: string = this._config.upload.requirements;

		var data: any = {};

		if (requirements != null) {
			data.requirementsFile =  requirements;
		}

		data.paths = [];
		for (var uploadEntry of uploadFiles) {
			if (uploadEntry.enabled) {
				if (uploadEntry.type == 'directory') {
					for (var file of (await FileServerUtils.getRecursiveTree(Global.convertOptumiPathToJupyterPath(uploadEntry.path)))) {
						data.paths.push(Global.convertJupyterPathToOptumiPath(file.path));
					}
				} else {
					data.paths.push(uploadEntry.path);
				}
			}
		}

		data.uuid = this._uuid;
		data.notebook = {
			path: this._path,
			content: JSON.stringify(this._notebook),
		}
		data.timestamp = this._timestamp.toISOString();

		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/launch-notebook";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify(data),
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response);
			// TODO:JJ Take a look at this
			this._initializing.addUpdate(new Update("stop", ""));
			return response.json();
		}, (error: ServerConnection.ResponseError) => {
			// TODO:JJ Take a look at this
			this._initializing.addUpdate(new Update('Sorry, we had trouble running your workload. Please try again.', ""));
			this._initializing.addUpdate(new Update('error', ""));
			this._initializing.addUpdate(new Update('stop', ""));
		});
		this.getLaunchStatus();
	}

	getAppStatus(): Status {
		if (this.initializing.error && !this.preparing.started) return Status.COMPLETED;
		if (this.preparing.error && !this.running.started) return Status.COMPLETED;
		for (var mod of this._modules) {
			if (mod.modStatus == Status.RUNNING) return Status.RUNNING;
		}
		if (this.running.completed) return Status.COMPLETED;
		if (this.preparing.completed) return Status.RUNNING;
		return Status.INITIALIZING;
	}

	getAppMessage(): string {
		var message = "";
		if (this._initializing.message != "") message = this._initializing.message;
		if (this._preparing.message != "") message = this._preparing.message;
		if (this._running.message != "") message = this.adjustMessage(this._running.message);
		if (this.error) message = 'Failed'
		return message;
    }

	getDetailedAppMessage(): string {
		var message = "";
		if (this._initializing.message != "") message = this._initializing.message;
		if (this._preparing.message != "") message = this._preparing.message;
		if (this._running.message != "") message = this.adjustMessage(this._running.message);
		return message;
    }

	getAppWarningMessage(): string {
		return this._running.warningMessages.join('\n');
    }
    
	adjustMessage(message: string): string {
		// We will say a session is starting until we can connect to it
		if (this.interactive && message == 'Running' && !(this.modules.length > 0 && this.modules[0].sessionReady)) return 'Connecting';
		// We call a running app 'Connected'
		if (this.interactive && message == 'Running') return 'Connected';
		// We call a terminated or completed app 'closed',
		if (this.interactive && message == 'Terminating') return 'Closing';
		if (this.interactive && message == 'Terminated') return 'Closed';
		if (this.interactive && message == 'Completed') return 'Closed';
		return message;
	}

    getTimeElapsed(): string {
        if (!this._initializing.completed) return undefined;
		if (!this._preparing.completed) return undefined;
        return this._running.elapsed;
	}
	
	getEndTime(): Date {
		if (!this._initializing.completed) return undefined;
		if (!this._preparing.completed) return undefined;
        return this._running.endTime;
	}


    getCost(): string {
		if (this.getTimeElapsed() == undefined) return undefined;
		if (this.machine == undefined) return undefined;
		var rate = this.machine.rate;
		const split = this.getTimeElapsed().split(':');
		if (split.length == 3) {
			const hours = +split[0]
			const minutes = +split[1];
			const seconds = +split[2];
			const cost = ((hours * rate) + (minutes * rate / 60) + (seconds * rate / 3600));
        	return (cost.toFixed(2) == '0.00' ? '< $0.01' : '~ $' + cost.toFixed(2));
		} else {
			const minutes = +split[0];
			const seconds = +split[1];
			const cost = ((minutes * rate / 60) + (seconds * rate / 3600));
			return (cost.toFixed(2) == '0.00' ? '< $0.01' : '~ $' + cost.toFixed(2));
		}
    }

	getShowLoading(): boolean {
		if (this._running.started) return false;
		if (this._preparing.started) return this._preparing.message == 'Waiting for cloud provider';
		if (this._initializing.started) return false;
		return false;
	}

	// private formatTime = (): string => {
	// 	var app: App = this
	// 	var yesterday: Date = new Date()
	// 	yesterday.setDate(yesterday.getDate() - 1)
	// 	if (app.timestamp == undefined) return undefined;
	// 	var startTime = app.timestamp < yesterday ? app.timestamp.toLocaleDateString() : app.timestamp.toLocaleTimeString();
	// 	if (app.getEndTime() == undefined) return startTime;
	// 	var endTime = app.getEndTime() < yesterday ? app.getEndTime().toLocaleDateString() : app.getEndTime().toLocaleTimeString();
	// 	return startTime == endTime ? startTime : startTime + " - " + endTime;
	// };
}
