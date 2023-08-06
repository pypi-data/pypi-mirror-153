/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { OptionsObject } from "notistack";
import { Colors } from "../Colors";

/// NOTE: Look here for possible props: https://iamhosseindhv.com/notistack/api#enqueuesnackbar-options

export const providerOptions = {
    success: { backgroundColor: Colors.SUCCESS + ' !important' },
    error: { backgroundColor: Colors.ERROR + ' !important' },
    warning: { backgroundColor: Colors.WARNING + ' !important' },
    info: { backgroundColor: Colors.PRIMARY + ' !important' },
}

export enum SnackbarActionType {
    DISMISS = "dismiss",
	SUBSCRIBE = "subscribe",
	ENABLE_AUTO_ADD_ONS = "enable auto add ons",
	AUTO_REMOVE = "auto remove",
}

export class Snackbar {
    message: string;
    options: OptionsObject;

    private standardOptions: OptionsObject = {
        anchorOrigin: {
            vertical: 'bottom',
            horizontal: 'right',
        },
    }

    constructor(message: string, options: OptionsObject) {
        this.message = message;
        this.options = Object.assign({ key: message, preventDuplicate: true }, options, this.standardOptions);
    }
}
