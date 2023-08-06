/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

// Network: #10A0F9
// Disk: #00c650
// Swap: #575A4B
// RAM: #ba9fd1
// CPU: #f48f8d
// vRAM: #964A71
// GPU: #ffba7d

export class Colors {
    // All these colors need to be hex colors, since we sometimes add an alpha channel by appending 2 characters
    // TODO:JJ Change these places to use the alpha() MUI function

    public static refresh: () => any = null

    public static PRIMARY = '#10A0F9'
    public static SECONDARY = '#afaab0'
    public static ERROR = '#f48f8d'
    public static WARNING = '#ffba7d'
    public static SUCCESS = '#00c650'
    public static DISABLED = '#89858b'

    public static NETWORK = '#88AFFF'
    public static DISK = '#ADEBAD'
    public static SWAP = '#FEED85'
    public static RAM = '#BA9FCF'
    public static CPU = '#F48F8D'
    public static VRAM = '#B9C7E3'
    public static GPU = '#FFBA7D'

    public static CHIP_GREY = '#989898'

    // TODO:JJ look for hex colors using '#[0-9a-fA-F]{3,8}'
    // TODO:JJ look for rgb colors using 'rgb(' and 'rgba('

    // yellow: #FEED85
}