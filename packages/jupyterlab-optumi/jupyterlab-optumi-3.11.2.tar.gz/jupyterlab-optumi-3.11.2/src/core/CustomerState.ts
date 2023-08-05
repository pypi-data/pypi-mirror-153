/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

// NOTE: This needs to be kept in sync with the enum in the controller
export enum CustomerState {
    INIT = "init",
	FREE_TRIAL = "free trial",
	FREE_TRIAL_ENDED = "free trial ended",
	STARTER = "starter",
	SUBSCRIPTION_CANCELED = "subscription canceled",
}