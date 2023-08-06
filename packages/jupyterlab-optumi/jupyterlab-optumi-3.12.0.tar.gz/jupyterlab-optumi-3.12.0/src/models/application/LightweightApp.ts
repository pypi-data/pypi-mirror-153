/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { Global } from '../../Global';

import { OptumiConfig } from "../OptumiConfig";
import { AppLaunchComponent } from './AppLaunchComponent';
import { IdentityAppComponent } from './IdentityAppComponent';
import { TrackedOptumiMetadata } from '../OptumiMetadataTracker';
import { OptumiMetadata } from '../OptumiMetadata';
import { Machine } from '../machine/Machine';

export class LightweightApp {
    uuid: string
    path: string
    _config: OptumiConfig

    constructor(uuid: string, path: string, config: OptumiConfig) {
        this.uuid = uuid;
        this.path = path
        this._config = config
    }

    get name(): string {
		return this.path.split('/').pop().replace('.ipynb', '');
	}

    get config(): OptumiConfig {
		return this._config;
	}

	set config(config: OptumiConfig) {
		this._config = config.copy();

		// Update the metadata tracker
		Global.metadata.setMetadata(new TrackedOptumiMetadata(this.path, new OptumiMetadata({ nbKey: this.uuid }), config.copy()));
	}

    get runNum(): number {
        return 0;
    }

    public getLaunchComponent(machine: Machine, balance: number): React.CElement<any, AppLaunchComponent> {
        return React.createElement(AppLaunchComponent, {key: this.path, lightweightApp: this, machine: machine, balance: balance});
    }

    public getIdentityComponent(): React.CElement<any, IdentityAppComponent> {
        return React.createElement(IdentityAppComponent, {key: this.path, app: this});
    }
}