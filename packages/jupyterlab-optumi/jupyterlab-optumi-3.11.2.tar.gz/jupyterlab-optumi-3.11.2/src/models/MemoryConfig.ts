/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { User } from "./User";
import { Expertise } from "./OptumiConfig";

export class MemoryConfig {
    public expertise: Expertise;
    // Beginner properties
    public required: boolean;
    // Intermediate properties
    public rating: number[];
    // Expert properties
    public size: number[];
    // Dev Ops properties
    // TODO:JJ

    constructor(map: any = {}, user: User = null) {
        this.expertise = map.expertise || Expertise.COMPONENT;
        this.required = map.required || false;
        this.rating = map.rating || [-1, -1, -1];
        this.size = map.size || [-1, -1, -1];
    }
}