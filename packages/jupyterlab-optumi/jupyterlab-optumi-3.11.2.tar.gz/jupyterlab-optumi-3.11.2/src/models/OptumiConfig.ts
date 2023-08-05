/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { Global } from "../Global";

import { ComputeConfig } from "./ComputeConfig";
import { GraphicsConfig } from "./GraphicsConfig";
import { MemoryConfig } from "./MemoryConfig";
import { NotificationConfig } from "./NotificationConfig";
import { PackageConfig } from "./PackageConfig";
import { StorageConfig } from "./StorageConfig";
import { UploadConfig } from "./UploadConfig";
import { User } from "./User";

export enum Expertise {
	BASIC = "basic",
    RATING = "rating",
    SIMPLIFIED = "simplified",
	COMPONENT = "component",
	EQUIPMENT = "equipment"
}

export class OptumiConfig {
	public intent: number;
	public compute: ComputeConfig;
	public graphics: GraphicsConfig;
    public memory: MemoryConfig;
    public storage: StorageConfig;
	public upload: UploadConfig;
	public machineAssortment: string[];
	public notifications: NotificationConfig;
	public package: PackageConfig;
	public interactive: boolean;
	public annotation: string;
	
	constructor(map: any = {}, version: string = Global.version, user: User = null) {
        this.intent = (map.intent != undefined ? map.intent : ((user) ? user.intent : 0.5));
		this.compute = new ComputeConfig(map.compute || {}, user);
		this.graphics = new GraphicsConfig(map.graphics || {}, user); 
        this.memory = new MemoryConfig(map.memory || {}, user);
        this.storage = new StorageConfig(map.storage || {});
		this.upload = new UploadConfig(map.upload || {});
		this.machineAssortment = map.machineAssortment || []
		this.notifications = new NotificationConfig(map.notifications || {});
		this.package = new PackageConfig(map.package || {});
		this.interactive = map.interactive == undefined ? false : map.interactive;
		this.annotation = map.annotation || "";
	}

	public copy(): OptumiConfig {
		return new OptumiConfig(JSON.parse(JSON.stringify(this)));
	}
}
