/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { DataConnectorUploadConfig } from "./DataConnectorUploadConfig";
import { FileUploadConfig as FileUploadConfig } from "./FileUploadConfig";

export class UploadConfig {
    public files: FileUploadConfig[] = [];
    public dataConnectors: DataConnectorUploadConfig[] = [];
    public requirements: string = "";

    constructor(map: any = {}) {
        // Handle backwards compatible 'fileVars'
        if (map.fileVars) {
            for (let file of map.fileVars) {
                this.files.push(new FileUploadConfig(file));
            }
        }

        if (map.files) {
            for (let file of map.files) {
                this.files.push(new FileUploadConfig(file));
            }
        }
        if (map.dataConnectors) {
            for (let dataConnector of map.dataConnectors) {
                this.dataConnectors.push(new DataConnectorUploadConfig(dataConnector));
            }
        }
        this.requirements = map.requirements || "";
    }
}