/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { Global } from "../Global";

import { v4 as uuid } from 'uuid';

export class OptumiMetadata {
    public nbKey: string;
    public nbKeyHistory: string[];
	public version: string;
	
	constructor(map: any = {}) {
        this.nbKey = map.nbKey || uuid();
        this.nbKeyHistory = map.nbKeyHistory || [];
		this.version = map.version || Global.version;
		if (this.version.includes("DEV")) this.version = "DEV";
	}
}
