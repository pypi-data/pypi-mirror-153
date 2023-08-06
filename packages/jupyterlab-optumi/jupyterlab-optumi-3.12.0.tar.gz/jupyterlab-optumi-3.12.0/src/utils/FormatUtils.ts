/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

export default class FormatUtils {
    public static floorAndToFixed = (val: number, n = 0): string => {
        if (val == null) return null
        if (val == undefined) return undefined
        const scale = Math.pow(10, n);
        // To avoid errors with numbers with a lot of decimal points, round to n + 1 decimal places before flooring
        return (Math.floor(+val.toFixed(n + 1) * scale) / scale).toFixed(n);
    }
    
    public static styleStorageOrEgress = (total: number, limit: number): string => {
        var ret = FormatUtils.styleShortCapacityValue()(total, FormatUtils.styleCapacityUnit()(limit));
        if (ret == '0' && total > 0) ret = '< 0.01'
        return ret + ' of ' + FormatUtils.styleCapacityUnitValue()(limit)
    }
    
    public static formatCost = (cost: number): string => {
        if (cost > 0 && cost < 0.01) return '< $0.01'
        var ret = '$' + FormatUtils.floorAndToFixed(cost, 2)
        if (ret == '$0.00') return '--'
        return ret
    }

    public static formatCredit = (balance: number) => {
        if (balance > 0) return '$0.00'
        return FormatUtils.formatCost(-balance)
    }
    
    public static msToTime(s: number, includeMilliseconds: boolean = false) {
        var ms = s % 1000;
        s = (s - ms) / 1000;
        var secs = s % 60;
        s = (s - secs) / 60;
        var mins = s % 60;
        var hrs = (s - mins) / 60;
    
        return (hrs == 0 ? '' : (hrs < 10 ? '0' + hrs : hrs) + ':') + (mins < 10 ? '0' + mins : mins) + ':' + (secs < 10 ? '0' + secs : secs) + (includeMilliseconds ? '.' + ms : '');
    }

    public static styleCapacityUnit() {
        return (value: number): string => {
            if (value == -1) return ''
            if (value < Math.pow(1024, 3)) {
                return 'MB';
            } else if (value < Math.pow(1024, 4)) {
                return 'GB';
            } else if (value < Math.pow(1024, 5)) {
                return 'TB';
            } else {
                return 'PB';
            }
        };
    }
    
    public static styleShortCapacityValue() {
        return (value: number, unit: string = ''): string => {
            var ret;
            if (value == -1) return 'unsp'
            if (unit) {
                // We don't care about the size, use a specified unit
                if (unit == 'MB') {
                    ret = (value / Math.pow(1024, 2));
                } else if (unit == 'GB') {
                    ret = (value / Math.pow(1024, 3));
                } else if (unit == 'TB') {
                    ret = (value / Math.pow(1024, 4));
                } else {
                    ret = (value / Math.pow(1024, 5));
                }
            } else {
                // Get the unit that makes the most sense based on the number
                if (value < Math.pow(1024, 3)) {
                    ret = (value / Math.pow(1024, 2));
                } else if (value < Math.pow(1024, 4)) {
                    ret = (value / Math.pow(1024, 3));
                } else if (value < Math.pow(1024, 5)) {
                    ret = (value / Math.pow(1024, 4));
                } else {
                    ret = (value / Math.pow(1024, 5));
                }
            }
            if (ret.toFixed(0).length == 1) {
                if (ret.toFixed(2).endsWith('0')) {
                    if (ret.toFixed(1).endsWith('0')) {
                        return ret.toFixed(0);
                    }
                    return ret.toFixed(1);
                }
                return ret.toFixed(2);
            } else if (ret.toFixed(0).length == 2) {
                if (ret.toFixed(1).endsWith('0')) {
                    return ret.toFixed(0);
                }
                return ret.toFixed(1);
            }
            return ret.toFixed(0);
        };
    }
    
    public static styleCapacityUnitValue() {
        return (value: number): string => {
            if (value == -1) return 'unsp'
            if (value < 1024) {
                return value + ' bytes';
            } else if (value < Math.pow(1024, 2)) {
                return FormatUtils.customPrecision(value / Math.pow(1024, 1)) + ' KB';
            } else if (value < Math.pow(1024, 3)) {
                return FormatUtils.customPrecision(value / Math.pow(1024, 2)) + ' MB';
            } else if (value < Math.pow(1024, 4)) {
                return FormatUtils.customPrecision(value / Math.pow(1024, 3)) + ' GB';
            } else if (value < Math.pow(1024, 5)) {
                return FormatUtils.customPrecision(value / Math.pow(1024, 4)) + ' TB';
            } else {
                return FormatUtils.customPrecision(value / Math.pow(1024, 5)) + ' PB';
            }
        };
    }
    
    public static styleRateUnitValue() {
        return (value: number): string => {
            return '$' + value.toFixed(2) + '/hr';
        };
    }
    
    private static customPrecision(value: number, maxPrecision = 3): string {
        var places: number = Math.floor(value).toString().length;
        if (places <= maxPrecision) {
            var ret = value.toPrecision(maxPrecision);
            // Shorten the text if it ends in 0 or .
            while (ret.includes('.') && ret.endsWith('0')) ret = ret.substr(0, ret.length-1);
            if (ret.endsWith('.')) ret = ret.substr(0, ret.length-1);
            return ret;
        } else {
            return value.toString();
        }
    }
}