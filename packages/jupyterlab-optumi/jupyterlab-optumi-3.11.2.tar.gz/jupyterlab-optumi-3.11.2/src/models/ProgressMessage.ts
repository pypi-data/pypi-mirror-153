/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { Global } from '../Global';

import { ServerConnection } from '@jupyterlab/services';

import { Phase } from './application/App';
import { Update } from './Update';
import FormatUtils from '../utils/FormatUtils';
import NotebookUtils from '../utils/NotebookUtils';

export class ProgressMessage {
	private _appUUID = "";
	private _phase: Phase;
	private _updates: Update[];

	constructor(phase: Phase, updates: Update[] = []) {
		this._phase = phase;
		this._updates = updates;
	}

	set appUUID(appUUID: string) {
		this._appUUID = appUUID;
	}

	public get phase(): Phase {
		return this._phase
	}

	public get message(): string {
		for (let i = this._updates.length -1; i >= 0; i--) {
			const update = this._updates[i];
			if (update.line != 'error' && update.line != 'stop' && update.line != '' && !update.modifier.startsWith('{')) {
				return update.line;
			} 
		}
		return "";
    }

    public get messages(): [string, string, boolean][] {
        var message: string = "";
		var lastNonDetail = "";
        for (let update of this._updates) {
			if (update.line != 'error' && update.line != 'stop' && update.line != '') {
				if (!update.modifier.startsWith('{')) {
					// Suppress duplicate update messages
					if (update.line != lastNonDetail) {
						lastNonDetail = update.line
					}
				}
				message += update.line
				if (!message.endsWith('\n')) message += '\n'
			}
        }
		var messages = NotebookUtils.fixOverwrittenChars(message).split('\n')
		var ret: [string, string, boolean][] = []
		TOP:
		for (let m of messages) {
			for (let update of this._updates) {
				if (update.line == m && !update.modifier.startsWith('{')) {
					ret.push([m, undefined, false])
					continue TOP
				} else  if (update.line.replace(/[^a-z0-9]/gi, '').startsWith(m.replace(/[^a-z0-9]/gi, '')) && update.modifier.startsWith('{')) {
					const jsonPayload = JSON.parse(update.modifier);
					ret.push([m, jsonPayload.level, true])
					continue TOP
				}
			}
			ret.push([m, undefined, true])
		}
		return ret
    }

	// There are cases where we do not want to send an update to the controller
	public addUpdate(update: Update, send: boolean = true) {
		if (this._updates.length == 0 || this._updates[this._updates.length-1].line != update.line) {
			// We do not want to record the same update twice
			this._updates.push(update);
			if (send) this.pushStatusUpdate(update);
		}
	}

	public get length(): number {
		return this._updates.length;
	}

	public get started(): boolean {
		return this._updates.length > 0;
	}

    public get elapsed(): string {
        try {
            var start: number = null;
            var end = new Date().getTime();
			for (let update of this._updates) {
				// If the update does not have a valid date, ignore it
				try {
					var date = Date.parse(update.modifier)
					if (!isNaN(date)) {
						if (start == null) start = date
						if (this.completed) end = date;
					}
				} catch (err) {}
			}
			if (start == null) return undefined
			const diff = end - start;
			// Pave over the case where the system clock is wildly off
			if (diff < 0) return FormatUtils.msToTime(0);
            return FormatUtils.msToTime(diff);
        } catch (err) {
            return undefined
        }
	}

	public get endTime(): Date {
		var end = new Date().getTime();
		if (this.completed) {
			for (let update of this._updates) {
				// If the update does not have a valid date, ignore it
				try {
					var date = Date.parse(update.modifier)
					if (!isNaN(date)) {
						end = date;
					}
				} catch (err) {}
			}
			return new Date(end);
		}
		return undefined;
	}

	public get completed(): boolean {
        for (let update of this._updates) {
            if (update.line == "stop") return true;
        }
        return false;
	}

	public get error(): boolean {
		for (let update of this._updates) {
            if (update.line == "error") return true;
			if (update.line != 'error' && update.line != 'stop' && update.line != '') {
				if (update.modifier.startsWith('{')) {
					const jsonPayload = JSON.parse(update.modifier);
					if (jsonPayload.level == 'error') return true;
				}
			}
        }
        return false;
	}

	public get warning(): boolean {
		for (let update of this._updates) {
			if (update.line != 'error' && update.line != 'stop' && update.line != '') {
				if (update.modifier.startsWith('{')) {
					const jsonPayload = JSON.parse(update.modifier);
					if (jsonPayload.level == 'warning') return true;
				}
			}
        }
		return false
	}

	public get warningMessages(): string[] {
		const warnings: string[] = []
		for (let update of this._updates) {
			if (update.line != 'error' && update.line != 'stop' && update.line != '') {
				if (update.modifier.startsWith('{')) {
					const jsonPayload = JSON.parse(update.modifier);
					if (jsonPayload.level == 'warning') warnings.push(jsonPayload.tooltip);
				}
			}
        }
		return warnings
	}

	private sending = false;
	private sendQueue : Update[] = [];

	private pushStatusUpdate(update: Update) {
		if (this._appUUID == "") {
			console.log("Status update not pushed because app UUID is empty");
			return;
		}
		// If we are already sending a message, queue this new message
		if (this.sending) {
			this.sendQueue.push(update);
		} else {
			this.sending = true;
			this.sendMessage(update);
		}
	}

	private sendNextMessage = () => {
		const nextUpdate = this.sendQueue.shift();
		if (nextUpdate) {
			this.sendMessage(nextUpdate);
		} else {
			this.sending = false;
		}
	}

	private sendMessage(update: Update) {
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/push-workload-initializing-update";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				uuid: this._appUUID,
				update: update.line,
			}),
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			// Send the next message (in order to try to be robust, we will send the next message even if we encountered an error sending the previous one)
			this.sendNextMessage();
			Global.handleResponse(response);
		}, () => {
			// If we encounter an error, we will want to send the next message...
			this.sendNextMessage();
		});
	}
}
