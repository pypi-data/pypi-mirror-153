/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { Update } from './Update';
import { Machine } from './machine/Machine';
import { FileMetadata } from '../components/deploy/fileBrowser/FileBrowser';

export enum Status {
	INITIALIZING,
	RUNNING,
	COMPLETED,
}

export class Module {
	get sessionReady(): boolean {
		return this._sessionToken != null;
	}

	private _lastPatch: number;
	public applyPatch: (patch: any) => void;
	public updateNotebook: (notebook: any) => void;

	private readonly _uuid: string;

	private _sessionToken: string;

    private _machine: Machine;
    
    private _output: Update[];
    private _files: FileMetadata[];
    private _updates: Update[];
    private _monitoring: Update[];
	private _updateCallback: ((update: any) => void)[] = [];

	constructor(uuid: string, machine: Machine = null, sessionToken: string = null, output: Update[] = [], updates: Update[] = [], files: FileMetadata[] = [], monitoring: Update[] = [], lastPatch: number = 0) {
		this._uuid = uuid;

		this._sessionToken = sessionToken;

        this._machine = machine;

		this._output = output;

		this._updates = updates;
		this._files = files;
		this._monitoring = monitoring;

		this._lastPatch = lastPatch;
	}

	get uuid(): string {
		return this._uuid;
	}

	////
	/// We are not using the module stdin yet
	//

	get lastPatch(): number {
		return this._lastPatch;
	}

	get sessionToken(): string {
        return this._sessionToken;
	}

    get machine(): Machine {
        return this._machine;
    }

	get updates(): Update[] {
        return this._updates;
    }

    get output(): Update[] {
        return this._output;
    }

	get files(): FileMetadata[] {
		return this._files;
	}

	get monitoring(): Update[] {
        return this._monitoring;
    }

	get modStatus(): Status {
		for (var update of this._updates) {
			if (update.modifier == "stop") return Status.COMPLETED;
		}
		return Status.RUNNING;
	}

	get error(): boolean {
		for (var update of this._updates) {
			if (update.line == "error") return true;
		}
		return false;
    }

	public addUpdateCallback(callback: (update: any) => void) {
		this._updateCallback.push(callback)
	}

	public removeUpdateCallback(callback: (update: any) => void) {
		this._updateCallback = this._updateCallback.filter(obj => obj !== callback)
	}

	public handleUpdate(body: any): boolean {
		let updated = false
		if (body.output != null) {
			if (body.output.length > 0) updated = true;
			for (let i = 0; i < body.output.length; i++) {
				this._output.push(new Update(body.output[i], body.outputmod[i]));
			}
		}
		if (body.notebook!= null) {
			const notebook = body.notebook;
			try {
				this.updateNotebook(JSON.parse(notebook));
				const n = body.patchesmod[0]
				if (!isNaN(parseFloat(n)) && isFinite(n)) this._lastPatch = +n;
			} catch (err) {
				console.warn('Unable to update notebook ' + notebook);
			}
		}
		if (body.patches != null) {
			// Apply any patch(es)
			for (var i = 0; i < body.patches.length; i++) {
				const patch = body.patches[i];
				try {
					this.applyPatch(JSON.parse(patch));
					const n = body.patchesmod[i]
					if (!isNaN(parseFloat(n)) && isFinite(n)) this._lastPatch = +n;
				} catch (err) {
					if (patch != 'stop') console.warn('Unable to apply patch ' + patch);
				}
			}
		}
		// new OutputFile(body.files[i], , body.filessize[i]))
		if (body.files != null) {
			this._files = [];
			for (let i = 0; i < body.files.length; i++) {
				if (body.files[i] != '') {
					updated = true
					this._files.push({
						created: body.filescrt[i],
						last_modified: body.filesmod[i],
						name: (body.files[i] as string).split('/').pop(),
						path: body.files[i],
						size: +body.filessize[i],
						type: 'file',
						hash: body.hashes[i]
					} as FileMetadata);
				}
			}
		}
		if (this._sessionToken == null && body.token != null) {
			updated = true
			this._sessionToken = body.token;
			window.open('https://' + this.machine.dnsName + ':54321?token=' + this._sessionToken, '_blank');
		}
		if (body.updates != null) {
			if (body.updates.length > 0) updated = true;
			for (let i = 0; i < body.updates.length; i++) {
				this._updates.push(new Update(body.updates[i], body.updatesmod[i]));
			}
		}
		if (body.machine != null) {
			updated = true;
			this._machine = Machine.parse(body.machine);
		}
		if (body.monitoring != null) {
			if (body.monitoring.length > 0) updated = true;
			for (let i = 0; i < body.monitoring.length; i++) {
				const update = new Update(body.monitoring[i], body.monitoringmod[i]);
				this._monitoring.push(update);
				for (let callback of this._updateCallback) {
					callback(update)
				}
			}
		}
		return updated;
	}
}
