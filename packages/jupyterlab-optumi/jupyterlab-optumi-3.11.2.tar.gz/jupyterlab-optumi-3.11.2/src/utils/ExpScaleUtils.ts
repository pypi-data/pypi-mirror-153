/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

export default class ExpScaleUtils {
    private min: number;
    private max: number;
    private step: number;
    private exponent: number;
    // Save this internally so we don't create the map unnecessarily
    private marks: any[];
    
    constructor(min: number, max: number, step: number, exponent: number, ignoreLabel?: boolean) {
        this.min = min;
        this.max = max;
        this.step = step;
        this.exponent = exponent;
        this.marks = this.generateMarks(ignoreLabel);
    }

    public getMarks(): any[] {
        return this.marks;
    }

    // Externally we will represent with the same number of decimals as in 'step'
    private scale = (x: number) => this.round(x ** this.exponent, this.countDecimals(this.step));
    public getScale(): (x: number) => number {
        return this.scale;
    }

    // Internally we will represent with 5 decimal places. This can be increased if necessary	
    private unscale = (x: number) => this.round(x ** (1/this.exponent), 5);
    public getUnscale(): (x: number) => number {
        return this.unscale;
    }

    private countDecimals(value: number): number {
        if(Math.floor(value) === value) return 0;
        return value.toString().split(".")[1].length || 0; 
    }
    
    private isWhole(value: number): boolean {
        const ret: boolean = value % 1 == 0
        return ret;
    }
    
    private round(value: number, precision: number): number {
        var multiplier = Math.pow(10, precision || 0);
        return Math.round(value * multiplier) / multiplier;
    }
    
    private generateMarks(ignoreLabel?: boolean): any {
        const marks: any[] = [];
        const roundDigits: number = this.countDecimals(this.step);
        var i: number = this.min;
        while (i <= this.max) {
            if (this.isWhole(i) && !ignoreLabel) {
                marks.push(
                    {
                        value: this.round(i ** (1/this.exponent), 5),
                        label: "$" + i.toFixed(0),
                    }
                );
            } else {
                marks.push(
                    {
                        value: this.round(i ** (1/this.exponent), 5),
                    }
                );
            }
            i += this.step;
            i = this.round(i, roundDigits);
        }
        return marks;
    }
}
