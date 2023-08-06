/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../../Global';
import FormatUtils from '../../utils/FormatUtils';

import { IdentityMachineComponent } from './IdentityMachineComponent';
import { MachineComponent } from './MachineComponent';
import { MachinePreviewComponent } from './MachinePreviewComponent';

export class Machine {
    computeCores: number[] = [0, 0, 0]
    computeFrequency: number = 0
    computeRating: number = 0
    computeScore: number[] = [0, 0, 0]
    graphicsCardType: string = 'None'
    graphicsCores: number = 0
    graphicsFrequency: number = 0
    graphicsMemory: number = 0
    graphicsNumCards: number = 0
    graphicsRating: number = 0
    graphicsScore: number = 0
    memoryRating: number = 0
    memorySize: number = 0
    storageRating: number = 0
    storageSize: number = 0
    storageIops: number = 0
    storageThroughput: number = 0
    uuid: string
    name: string
    dnsName: string
    rate: number
    promo: boolean
    state: string
    time: Date
    app: string

    public getDetails(): string {
        const machines = Global.user.machines
        return this.graphicsNumCards > 0 ? 
            'GPU: ' + this.graphicsNumCards + ' ' + this.graphicsCardType + '\n' +
            'vRAM: ' + FormatUtils.styleCapacityUnitValue()(this.graphicsMemory) + '\n' +
            'CPU: ' + (this.computeCores[1] == this.computeCores[2] ? Math.round(this.computeCores[1] * 100) / 100 : Math.round(this.computeCores[1] * 100) / 100 + '-' + Math.round(this.computeCores[2] * 100) / 100) + ' cores\n' +
            'RAM: ' + FormatUtils.styleCapacityUnitValue()(this.memorySize) + '\n' +
            'Disk: ' + FormatUtils.styleCapacityUnitValue()(this.storageSize) + '\n' +
            'GPU Rating: ' + ((this.graphicsScore / machines.graphicsScoreMax) * 100).toFixed() + '%\n' +
            'CPU Rating: ' + (this.computeScore[1] == this.computeScore[2] ? (this.computeScore[1] / machines.computeScoreMax * 100).toFixed() : (this.computeScore[1] / machines.computeScoreMax * 100).toFixed() + '-' + (this.computeScore[2] / machines.computeScoreMax * 100).toFixed()) + '%'
        :  
            'CPU: ' + (this.computeCores[1] == this.computeCores[2] ? Math.round(this.computeCores[1] * 100) / 100 : Math.round(this.computeCores[1] * 100) / 100 + '-' + Math.round(this.computeCores[2] * 100) / 100) + ' cores\n' +
            'RAM: ' + FormatUtils.styleCapacityUnitValue()(this.memorySize) + '\n' +
            'Disk: ' + FormatUtils.styleCapacityUnitValue()(this.storageSize) + '\n' +
            'CPU Rating: ' + (this.computeScore[1] == this.computeScore[2] ? (this.computeScore[1] / machines.computeScoreMax * 100).toFixed() : (this.computeScore[1] / machines.computeScoreMax * 100).toFixed() + '-' + (this.computeScore[2] / machines.computeScoreMax * 100).toFixed()) + '%'
    }

    public getComponent(): React.CElement<any, MachineComponent> {
        return React.createElement(MachineComponent, {key: this.uuid, machine: this});
    }

    public getPreviewComponent(): React.CElement<any, MachinePreviewComponent> {
        return React.createElement(MachinePreviewComponent, {key: this.uuid, machine: this});
    }

    public getIdentityComponent(): React.CElement<any, IdentityMachineComponent> {
        return React.createElement(IdentityMachineComponent, {key: this.uuid, machine: this});
    }

    public getStateMessage(): string {
        switch (this.state) {
            case 'requisition requested':
            case 'requisition in progress':
                return 'Acquiring'
            case 'requisition completed':
                return 'Configuring'
            case 'setup completed':
                return this.app ? 'Busy' : 'Idle'
            case 'teardown requested':
            case 'sequestration requested':
            case 'sequestration in progress':
            case 'sequestration completed':
                return 'Releasing'
            case 'unused':
            default:
                return ''
        }
    }

    public isVisible(): boolean {
        switch (this.state) {
            case 'requisition requested':
            case 'requisition in progress':
            case 'requisition completed':
            case 'setup completed':
                return true
            case 'teardown requested':
            case 'sequestration requested':
            case 'sequestration in progress':
            case 'sequestration completed':
            case 'unused':
            default:
                return false
        }
    }

    public static parse = (map: any): Machine => {
        // If this has a timestamp, we need to convert it to a prototype manually
        if (map.time) map.time = new Date(map.time)
        return Object.setPrototypeOf(map, Machine.prototype)
    }
}

export class NoMachine extends Machine {
    // Use this class to indicate there is no machine that matches
}