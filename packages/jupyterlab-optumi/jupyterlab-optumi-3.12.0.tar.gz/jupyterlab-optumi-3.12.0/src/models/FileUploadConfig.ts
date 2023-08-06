/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

export class FileUploadConfig {
    public hash: string;
    public path: string;
    public size: number;
    public created: Date;
    public lastModified: Date;
    public type: 'file' | 'notebook' | 'directory';
    public mimetype: string;
    public enabled: boolean;

    constructor(map: any) {
        this.hash = map.hash;
        this.path = map.path;
        this.size = map.size;
        this.created = map.created;
        this.lastModified = map.lastModified;
        this.type = map.type || 'file';
        this.mimetype = map.mimetype || 'text/plain';
        this.enabled = map.enabled == undefined ? false : map.enabled
    }
}
