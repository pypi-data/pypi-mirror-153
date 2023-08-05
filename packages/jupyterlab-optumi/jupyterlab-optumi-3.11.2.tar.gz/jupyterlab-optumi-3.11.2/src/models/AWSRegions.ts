/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

export class AWSRegion {
    public region: string
    public description: string

    constructor(region: string, description: string) {
        this.region = region;
        this.description = description;
    }
}

export class AWSRegions {
    private static regions = {
        GovCloud: new AWSRegion("us-gov-west-1", "AWS GovCloud (US)"),
        US_GOV_EAST_1: new AWSRegion("us-gov-east-1", "AWS GovCloud (US-East)"),
        US_EAST_1: new AWSRegion("us-east-1", "US East (N. Virginia)"),
        US_EAST_2: new AWSRegion("us-east-2", "US East (Ohio)"),
        US_WEST_1: new AWSRegion("us-west-1", "US West (N. California)"),
        US_WEST_2: new AWSRegion("us-west-2", "US West (Oregon)"),
        EU_WEST_1: new AWSRegion("eu-west-1", "EU (Ireland)"),
        EU_WEST_2: new AWSRegion("eu-west-2", "EU (London)"),
        EU_WEST_3: new AWSRegion("eu-west-3", "EU (Paris)"),
        EU_CENTRAL_1: new AWSRegion("eu-central-1", "EU (Frankfurt)"),
        EU_NORTH_1: new AWSRegion("eu-north-1", "EU (Stockholm)"),
        EU_SOUTH_1: new AWSRegion("eu-south-1", "EU (Milan)"),
        AP_EAST_1: new AWSRegion("ap-east-1", "Asia Pacific (Hong Kong)"),
        AP_SOUTH_1: new AWSRegion("ap-south-1", "Asia Pacific (Mumbai)"),
        AP_SOUTHEAST_1: new AWSRegion("ap-southeast-1", "Asia Pacific (Singapore)"),
        AP_SOUTHEAST_2: new AWSRegion("ap-southeast-2", "Asia Pacific (Sydney)"),
        AP_NORTHEAST_1: new AWSRegion("ap-northeast-1", "Asia Pacific (Tokyo)"),
        AP_NORTHEAST_2: new AWSRegion("ap-northeast-2", "Asia Pacific (Seoul)"),
        AP_NORTHEAST_3: new AWSRegion("ap-northeast-3", "Asia Pacific (Osaka)"),
        SA_EAST_1: new AWSRegion("sa-east-1", "South America (Sao Paulo)"),
        CN_NORTH_1: new AWSRegion("cn-north-1", "China (Beijing)"),
        CN_NORTHWEST_1: new AWSRegion("cn-northwest-1", "China (Ningxia)"),
        CA_CENTRAL_1: new AWSRegion("ca-central-1", "Canada (Central)"),
        ME_SOUTH_1: new AWSRegion("me-south-1", "Middle East (Bahrain)"),
        AF_SOUTH_1: new AWSRegion("af-south-1", "Africa (Cape Town)"),
        US_ISO_EAST_1: new AWSRegion("us-iso-east-1", "US ISO East"),
        US_ISOB_EAST_1: new AWSRegion("us-isob-east-1", "US ISOB East (Ohio)"),
        US_ISO_WEST_1: new AWSRegion("us-iso-west-1", "US ISO West"),
    }

    static get GovCloud() { return AWSRegions.regions.GovCloud }
    static get US_GOV_EAST_1() { return AWSRegions.regions.US_GOV_EAST_1 }
    static get US_EAST_1() { return AWSRegions.regions.US_EAST_1 }
    static get US_EAST_2() { return AWSRegions.regions.US_EAST_2 }
    static get US_WEST_1() { return AWSRegions.regions.US_WEST_1 }
    static get US_WEST_2() { return AWSRegions.regions.US_WEST_2 }
    static get EU_WEST_1() { return AWSRegions.regions.EU_WEST_1 }
    static get EU_WEST_2() { return AWSRegions.regions.EU_WEST_2 }
    static get EU_WEST_3() { return AWSRegions.regions.EU_WEST_3 }
    static get EU_CENTRAL_1() { return AWSRegions.regions.EU_CENTRAL_1 }
    static get EU_NORTH_1() { return AWSRegions.regions.EU_NORTH_1 }
    static get EU_SOUTH_1() { return AWSRegions.regions.EU_SOUTH_1 }
    static get AP_EAST_1() { return AWSRegions.regions.AP_EAST_1 }
    static get AP_SOUTH_1() { return AWSRegions.regions.AP_SOUTH_1 }
    static get AP_SOUTHEAST_1() { return AWSRegions.regions.AP_SOUTHEAST_1 }
    static get AP_SOUTHEAST_2() { return AWSRegions.regions.AP_SOUTHEAST_2 }
    static get AP_NORTHEAST_1() { return AWSRegions.regions.AP_NORTHEAST_1 }
    static get AP_NORTHEAST_2() { return AWSRegions.regions.AP_NORTHEAST_2 }
    static get AP_NORTHEAST_3() { return AWSRegions.regions.AP_NORTHEAST_3 }

    static get SA_EAST_1() { return AWSRegions.regions.SA_EAST_1 }
    static get CN_NORTH_1() { return AWSRegions.regions.CN_NORTH_1 }
    static get CN_NORTHWEST_1() { return AWSRegions.regions.CN_NORTHWEST_1 }
    static get CA_CENTRAL_1() { return AWSRegions.regions.CA_CENTRAL_1 }
    static get ME_SOUTH_1() { return AWSRegions.regions.ME_SOUTH_1 }
    static get AF_SOUTH_1() { return AWSRegions.regions.AF_SOUTH_1 }
    static get US_ISO_EAST_1() { return AWSRegions.regions.US_ISO_EAST_1 }
    static get US_ISOB_EAST_1() { return AWSRegions.regions.US_ISOB_EAST_1 }
    static get US_ISO_WEST_1() { return AWSRegions.regions.US_ISO_WEST_1 }

    static get values() { return [
        AWSRegions.GovCloud,
        AWSRegions.US_GOV_EAST_1,
        AWSRegions.US_EAST_1,
        AWSRegions.US_EAST_2,
        AWSRegions.US_WEST_1,
        AWSRegions.US_WEST_2,
        AWSRegions.EU_WEST_1,
        AWSRegions.EU_WEST_2,
        AWSRegions.EU_WEST_3,
        AWSRegions.EU_CENTRAL_1,
        AWSRegions.EU_NORTH_1,
        AWSRegions.EU_SOUTH_1,
        AWSRegions.AP_EAST_1,
        AWSRegions.AP_SOUTH_1,
        AWSRegions.AP_SOUTHEAST_1,
        AWSRegions.AP_SOUTHEAST_2,
        AWSRegions.AP_NORTHEAST_1,
        AWSRegions.AP_NORTHEAST_2,
        AWSRegions.AP_NORTHEAST_3,
        AWSRegions.SA_EAST_1,
        AWSRegions.CN_NORTH_1,
        AWSRegions.CN_NORTHWEST_1,
        AWSRegions.CA_CENTRAL_1,
        AWSRegions.ME_SOUTH_1,
        AWSRegions.AF_SOUTH_1,
        AWSRegions.US_ISOB_EAST_1,
        AWSRegions.US_ISO_WEST_1
    ] }
}
