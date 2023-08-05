/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { OptumiConfig } from "./OptumiConfig"

export enum PackageState {
	ACCEPTED = "accepted",
    SHIPPED = "shipped",
    OPENED = "opened",
    CANCELED = "canceled",
}

export class Package {
    public path: string
    public timestamp: Date
    public nbKey: string
    public label: string
    public packageState: string
    public originalNotebook: any
    public originalConfig: OptumiConfig
    public optimizedNotebook: any
    public optimizedConfig: OptumiConfig
    public auto: boolean

    constructor(path: string, timestamp: Date, nbKey: string, label: string, packageState: PackageState, originalNotebook: any, originalConfig: OptumiConfig, optimizedNotebook: any, optimizedConfig: OptumiConfig, auto: boolean) {
        this.path = path
        this.timestamp = timestamp;
        this.nbKey = nbKey;
        this.label = label;
        this.packageState = packageState;
        this.originalNotebook = originalNotebook;
        this.originalConfig = originalConfig;
        this.optimizedNotebook = optimizedNotebook;
        this.optimizedConfig = optimizedConfig;
        this.auto = auto;
    }

    public update(pack: Package) {
        this.path = pack.path;
        this.timestamp = pack.timestamp;
        this.nbKey = pack.nbKey;
        this.label = pack.label;
        this.packageState = pack.packageState;
        this.originalNotebook = pack.originalNotebook;
        this.originalConfig = pack.originalConfig;
        this.optimizedNotebook = pack.optimizedNotebook;
        this.optimizedConfig = pack.optimizedConfig;
        this.auto = pack.auto;
    }

    static fromMap(map: any = {}): Package {
        return new Package(map.path, new Date(map.timestamp), map.nbKey, map.label, map.packageState as PackageState, 
            map.originalNotebook ? JSON.parse(map.originalNotebook) : null, 
            map.originalConfig ? new OptumiConfig(JSON.parse(map.originalConfig)) : null, 
            map.optimizedNotebook ? JSON.parse(map.optimizedNotebook) : null, 
            map.optimizedConfig ? new OptumiConfig(JSON.parse(map.optimizedConfig)) : null,
            map.auto == undefined ? false : map.auto);
    }
}