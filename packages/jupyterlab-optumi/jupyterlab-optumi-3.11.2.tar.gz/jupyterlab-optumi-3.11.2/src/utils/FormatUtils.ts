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
    
    public static styleCapacityValue() {
        return (value: number): string => {
            if (value == -1) return 'unsp'
            if (value < Math.pow(1024, 3)) {
                return (value / Math.pow(1024, 2)).toFixed(3);
            } else if (value < Math.pow(1024, 4)) {
                return (value / Math.pow(1024, 3)).toFixed(3);
            } else if (value < Math.pow(1024, 5)) {
                return (value / Math.pow(1024, 4)).toFixed(3);
            } else {
                return (value / Math.pow(1024, 5)).toFixed(3);
            }
        };
    }

    public static styleShortCapacityUnit() {
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
    
    public static unstyleCapacityValue() {
        return (value: number, unit: string): number => {
            if (value == -1) return value
            if (isNaN(value)) return Number.NaN
            switch (unit.toLowerCase()) {
            case 'm':
            case 'mb':
                return value * Math.pow(1024, 2)
            case 'g':
            case 'gb':
                return value * Math.pow(1024, 3)
            case 't':
            case 'tb':
                return value * Math.pow(1024, 4)
            case 'p':
            case 'pb':
                return value * Math.pow(1024, 5)
            default:
                return value
            }
        }
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
    
    // export function possibleCapacityUnitValue() {
    //     return (unitValue: string): boolean => {
    //         return unitValue.includes(/^(\d{1,4}|\d{1,2}\.\d|\d\.\d{2}) ?[mgtpezy]ib$/i)
    //     }
    // }
    
    // export function unstyleCapacityUnitValue() {
    //     return (unitValue: string): number => {
    //         if (unitValue == 'unsp') return -1
    //         var value: number = Number.parseFloat(unitValue.replace(/[^0-9\.]+/, ''))
    //         if (isNaN(value)) return Number.NaN
    //         var unit: string = unitValue.replace(/[0-9\.]+/, '').trim()
    //         switch (unit.toLowerCase()) {
    //         case 'mb':
    //             return value * Math.pow(1024, 2)
    //         case 'gb':
    //             return value * Math.pow(1024, 3)
    //         case 'tb':
    //             return value * Math.pow(1024, 4)
    //         case 'pb':
    //             return value * Math.pow(1024, 5)
    //         default:
    //             return Number.NaN
    //         }
    //     }
    // }
    
    public static styleThroughputUnit() {
        return (value: number): string => {
            if (value == -1) return ''
            if (value < Math.pow(1000, 3)) {
                return 'MBps';
            } else if (value < Math.pow(1000, 4)) {
                return 'GBps';
            } else if (value < Math.pow(1000, 5)) {
                return 'TBps';
            } else {
                return 'PBps';
            }
        };
    }
    
    public static styleThroughputValue() {
        return (value: number): string => {
            if (value == -1) return 'unsp'
            if (value < Math.pow(1000, 3)) {
                return (value / Math.pow(1000, 2)).toFixed(3);
            } else if (value < Math.pow(1000, 4)) {
                return (value / Math.pow(1000, 3)).toFixed(3);
            } else if (value < Math.pow(1000, 5)) {
                return (value / Math.pow(1000, 4)).toFixed(3);
            } else {
                return (value / Math.pow(1000, 5)).toFixed(3);
            }
        };
    }
    
    public static unstyleThroughputValue() {
        return (value: number, unit: string): number => {
            if (value == -1) return value
            if (isNaN(value)) return Number.NaN
            switch (unit.toLowerCase()) {
            case 'm':
            case 'mbps':
                return value * Math.pow(1000, 2)
            case 'g':
            case 'gbps':
                return value * Math.pow(1000, 3)
            case 't':
            case 'tbps':
                return value * Math.pow(1000, 4)
            case 'p':
            case 'pbps':
                return value * Math.pow(1000, 5)
            default:
                return value
            }
        }
    }
    
    public static styleThroughputUnitValue() {
        return (value: number): string => {
            if (value == -1) return 'unsp'
            if (value < Math.pow(1000, 3)) {
                return FormatUtils.customPrecision(value / Math.pow(1000, 2)) + ' MBps';
            } else if (value < Math.pow(1000, 4)) {
                return FormatUtils.customPrecision(value / Math.pow(1000, 3)) + ' GBps';
            } else if (value < Math.pow(1000, 5)) {
                return FormatUtils.customPrecision(value / Math.pow(1000, 4)) + ' TBps';
            } else {
                return FormatUtils.customPrecision(value / Math.pow(1000, 5)) + ' PBps';
            }
        };
    }
    
    // export function unstyleThroughputUnitValue() {
    //     return (unitValue: string): number => {
    //         if (unitValue == 'unsp') return -1
    //         var value: number = Number.parseFloat(unitValue.replace(/[^0-9\.]+/, ''))
    //         if (isNaN(value)) return Number.NaN
    //         var unit: string = unitValue.replace(/[0-9\.]+/, '').trim()
    //         switch (unit.toLowerCase()) {
    //         case 'mbps':
    //             return value * Math.pow(1000, 2)
    //         case 'gbps':
    //             return value * Math.pow(1000, 3)
    //         case 'tbps':
    //             return value * Math.pow(1000, 4)
    //         case 'pbps':
    //             return value * Math.pow(1000, 5)
    //         default:
    //             return Number.NaN
    //         }
    //     }
    // }
    
    public static styleFrequencyUnit() {
        return (value: number): string => {
            if (value == -1) return ''
            if (value < Math.pow(1000, 3)) {
                return 'MHz';
            } else if (value < Math.pow(1000, 4)) {
                return 'GHz';
            } else if (value < Math.pow(1000, 5)) {
                return 'THz';
            } else {
                return 'PHz';
            }
        };
    }
    
    public static styleFrequencyValue() {
        return (value: number): string => {
            if (value == -1) return 'unsp'
            if (value < Math.pow(1000, 3)) {
                return (value / Math.pow(1000, 2)).toFixed(3);
            } else if (value < Math.pow(1000, 4)) {
                return (value / Math.pow(1000, 3)).toFixed(3);
            } else if (value < Math.pow(1000, 5)) {
                return (value / Math.pow(1000, 4)).toFixed(3);
            } else {
                return (value / Math.pow(1000, 5)).toFixed(3);
            }
        };
    }
    
    public static unstyleFrequencyValue() {
        return (value: number, unit: string): number => {
            if (value == -1) return value
            if (isNaN(value)) return Number.NaN
            switch (unit.toLowerCase()) {
            case 'm':
            case 'mhz':
                return value * Math.pow(1000, 2)
            case 'g':
            case 'ghz':
                return value * Math.pow(1000, 3)
            case 't':
            case 'thz':
                return value * Math.pow(1000, 4)
            case 'p':
            case 'phz':
                return value * Math.pow(1000, 5)
            default:
                return value
            }
        }
    }
    
    public static styleFrequencyUnitValue() {
        return (value: number): string => {
            if (value == -1) return 'unsp'
            if (value < Math.pow(1000, 3)) {
                return FormatUtils.customPrecision(value / Math.pow(1000, 2)) + ' MHz';
            } else if (value < Math.pow(1000, 4)) {
                return FormatUtils.customPrecision(value / Math.pow(1000, 3)) + ' GHz';
            } else if (value < Math.pow(1000, 5)) {
                return FormatUtils.customPrecision(value / Math.pow(1000, 4)) + ' THz';
            } else {
                return FormatUtils.customPrecision(value / Math.pow(1000, 5)) + ' PHz';
            }
        };
    }
    
    // export function unstyleFrequencyUnitValue() {
    //     return (unitValue: string): number => {
    //         if (unitValue == 'unsp') return -1
    //         var value: number = Number.parseFloat(unitValue.replace(/[^0-9\.]+/, ''))
    //         if (isNaN(value)) return Number.NaN
    //         var unit: string = unitValue.replace(/[0-9\.]+/, '').trim()
    //         switch (unit.toLowerCase()) {
    //         case 'mhz':
    //             return value * Math.pow(1000, 2)
    //         case 'ghz':
    //             return value * Math.pow(1000, 3)
    //         case 'thz':
    //             return value * Math.pow(1000, 4)
    //         case 'phz':
    //             return value * Math.pow(1000, 5)
    //         default:
    //             return Number.NaN
    //         }
    //     }
    // }
    
    public static styleDurationUnitValue() {
        return (value: number): string => {
            if (value == -1) return 'unsp'
            if (value < 60) {
                return FormatUtils.customPrecision(value, 2) + ' s';
            } else if (value / 60 < 60) {
                return FormatUtils.customPrecision(value / 60, 2) + ' min';
            } else if (value / 60 / 60 < 24) {
                return FormatUtils.customPrecision(value / 60 / 60, 2) + ' hr';
            } else {
                return FormatUtils.customPrecision(value / 60 / 60 / 24) + ' d';
            }
        };
    }
    
    // export function unstyleDurationUnitValue() {
    //     return (unitValue: string): number => {
    //         if (unitValue == 'unsp') return -1
    //         var value: number = Number.parseFloat(unitValue.replace(/[^0-9\.]+/, ''))
    //         if (isNaN(value)) return Number.NaN
    //         var unit: string = unitValue.replace(/[0-9\.]+/, '').trim()
    //         switch (unit.toLowerCase()) {
    //         case 's':
    //             return value
    //         case 'min':
    //         case 'm':
    //             return value * 60
    //         case 'hr':
    //         case 'h':
    //             return value * 60 * 60
    //         case 'd':
    //             return value * 60 * 60 * 24
    //         default:
    //             return Number.NaN
    //         }
    //     }
    // }
    
    public static styleRatingUnit() {
        return (value: number): string => {
            if (value == -1) return ''
            return '%';
        }
    }
    
    public static styleRatingValue() {
        return (value: number): string => {
            if (value == -1) return 'unsp'
            return (value * 100).toFixed(3);
        }
    }
    
    public static unstyleRatingValue() {
        return (value: number, unit: string): number => {
            if (value == -1) return value
            if (isNaN(value)) return Number.NaN
            return value / 100
        }
    }
    
    // export function styleRatingUnitValue() {
    //     return (value: number): string => {
    //         if (value == -1) return 'unsp'
    //         return FormatUtils.customPrecision(value, 2) + '%';
    //     }
    // }
    
    // export function unstyleRatingUnitValue() {
    //     return (unitValue: string): number => {
    //         if (unitValue == 'unsp') return -1
    //         var value: number = Number.parseFloat(unitValue.replace(/[^0-9\.]+/, ''))
    //         if (isNaN(value)) return Number.NaN
    //         if (unitValue.replace(/[0-9\.%]/g, '') != '') return Number.NaN
    //         return value;
    //     }
    // }
    
    public static styleRateUnit() {
        return (value: number): string => {
            return '$/hr';
        };
    }
    
    public static styleRateValue() {
        return (value: number): string => {
            return value.toString();
        };
    }
    
    public static styleRateUnitValue() {
        return (value: number): string => {
            return '$' + value.toFixed(2) + '/hr';
        };
    }
    
    // export function unstyleRateUnitValue() {
    //     return (unitValue: string): number => {
    //         var value: number = Number.parseFloat(unitValue.replace(/[^0-9\.]/g, ''))
    //         if (isNaN(value)) return Number.NaN
    //         var unit: string = unitValue.replace(/[0-9\.]+/, '').trim()
    //         switch (unit.toLowerCase()) {
    //         case '$/min':
    //             return value * 60;
    //         case '$/hr':
    //             return value * 1;
    //         case '$/day':
    //             return value / 24;
    //         default:
    //             return Number.NaN
    //         }
    //     }
    // }
    
    public static styleRate() {
        return (value: number): string => {
            if (isNaN(value)) {
                return 'no match';
            } else if (value >= 0.1) {
                return '$' + value.toFixed(2) + '/hr';
            } else {
                return (value * 100).toFixed(1) + '¢/hr';
            }
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