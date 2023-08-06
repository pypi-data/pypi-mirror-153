/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { IntegrationType } from "../components/deploy/IntegrationBrowser/IntegrationBrowser";
import { DataService } from "../components/deploy/IntegrationBrowser/IntegrationDirListingItemIcon";

export class IntegrationConfig {
    public name: string;
    public enabled: boolean;
    public integrationType: IntegrationType;

    constructor(map: any) {
        this.name = map.name;
        this.enabled = map.enabled == undefined ? true : map.enabled;
        this.integrationType = map.integrationType;
    }
}

export class DataConnectorConfig extends IntegrationConfig {
    public dataService: DataService;

    constructor(map: any) {
        super(Object.assign(map, { integrationType: IntegrationType.DATA_CONNECTOR }));
        this.dataService = map.dataService;
    }
}

export class EnvironmentVariableConfig extends IntegrationConfig {
    constructor(map: any) {
        super(Object.assign(map, { integrationType: IntegrationType.ENVIRONMENT_VARIABLE }));
    }
}