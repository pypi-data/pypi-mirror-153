/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { User } from "./User";

export class NotificationConfig {
    public jobStartedSMSEnabled: boolean;
    public jobCompletedSMSEnabled: boolean;
    public jobFailedSMSEnabled: boolean;
    public packageReadySMSEnabled: boolean;

    constructor(map: any = {}, user: User = null) {
        this.jobStartedSMSEnabled = map.jobStartedSMSEnabled || false;
        this.jobCompletedSMSEnabled = map.jobCompletedSMSEnabled || false;
        this.jobFailedSMSEnabled = map.jobFailedSMSEnabled || false;
        this.packageReadySMSEnabled = map.packageReadySMSEnabled || false;
    }
}