/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { User } from "./User";

export enum Platform {
    LAPTOP = "laptop",
    COLAB = "colab",
    KAGGLE = "kaggle",
}

export enum KaggleAccelerator {
    GPU = "GPU Accelerator",
    TPU = "TPU Accelerator",
    NONE = "No accelerator"
}

export class PackageConfig {
    public notebookRuns: true | false | null;
    public runHours: number;
    public runMinutes: number;
    public runPlatform: string | null;
    public kaggleAccelerator: KaggleAccelerator | null;

    constructor(map: any = {}, user: User = null) {
        this.notebookRuns = map.notebookRuns === undefined ? null : map.notebookRuns
        this.runHours = map.runHours || 0
        this.runMinutes = map.runMinutes || 0
        this.runPlatform = map.runPlatform || null
        this.kaggleAccelerator = map.kaggleAccelerator || null
    }
}