/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

export class Update {
    public line: string;
    public modifier: string;

    constructor(line: string, modifier: string) {
        this.line = line;
        this.modifier = modifier;
    }
}