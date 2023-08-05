/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

export class WasabiRegion {
    public region: string
    public description: string

    constructor(region: string, description: string) {
        this.region = region;
        this.description = description;
    }
}

export class WasabiRegions {
    private static regions = {
        US_EAST_1: new WasabiRegion("us-east-1", "US East (N. Virginia)"),
        US_EAST_2: new WasabiRegion("us-east-2", "US East (N. Virginia)"),
        US_CENTRAL_1: new WasabiRegion("us-central-1", "US Central (Texas)"),
        US_WEST_1: new WasabiRegion("us-west-1", "US West (Oregon)"),
        EU_CENTRAL_1: new WasabiRegion("eu-central-1", "EU (Amsterdam)"),
        AP_NORTHEAST_1: new WasabiRegion("ap-northeast-1", "AP (Tokyo)"),
    }

    static get US_EAST_1() { return WasabiRegions.regions.US_EAST_1 }
    static get US_EAST_2() { return WasabiRegions.regions.US_EAST_2 }
    static get US_CENTRAL_1() { return WasabiRegions.regions.US_CENTRAL_1 }
    static get US_WEST_1() { return WasabiRegions.regions.US_WEST_1 }
    static get EU_CENTRAL_1() { return WasabiRegions.regions.EU_CENTRAL_1 }
    static get AP_NORTHEAST_1() { return WasabiRegions.regions.AP_NORTHEAST_1 }

    static get values() { return [

        WasabiRegions.US_EAST_1,
        WasabiRegions.US_EAST_2,
        WasabiRegions.US_CENTRAL_1,
        WasabiRegions.US_WEST_1,
        WasabiRegions.EU_CENTRAL_1,
        WasabiRegions.AP_NORTHEAST_1,
    ] }
}
