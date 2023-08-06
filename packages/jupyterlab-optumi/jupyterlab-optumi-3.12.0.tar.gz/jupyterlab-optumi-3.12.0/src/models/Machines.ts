/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { Machine, NoMachine } from './machine/Machine';

import { ISignal, Signal } from '@lumino/signaling';

export class Machines {
	public inventory: Machine[];

    private _machinesByName = new Map<string, Machine>()
    public getMachine(name: string): Machine {
        return this._machinesByName.get(name) || new NoMachine()
    }

    public cpuLabels: string[][]
    public cpuGrid: Machine[][][]
    public gpuLabels: string[][]
    public gpuGrid: Machine[][][]

    private _changed = new Signal<this, Machines>(this);

	get changed(): ISignal<this, Machines> {
		return this._changed;
	}

    public graphicsCardNums = new Map<string, number[]>();
    public graphicsCards: string[] = [];
    
    // compute values
    public computeCores: number[] = [];
    get computeCoresMin(): number { return this.computeCores[0]; }
    get computeCoresMax(): number  { return this.computeCores[this.computeCores.length-1]; }
    public computeScore: number[] = [];
    get computeScoreMin(): number { return this.computeScore[0]; }
    get computeScoreMax(): number  { return this.computeScore[this.computeScore.length-1]; }
    public computeFrequency: number[] = [];
    get computeFrequencyMin(): number { return this.computeFrequency[0]; }
    get computeFrequencyMax(): number  { return this.computeFrequency[this.computeFrequency.length-1]; }
    
    // Max graphics values
    public graphicsScore: number[] = [];
    get graphicsScoreMin(): number { return this.graphicsScore[0]; }
    get graphicsScoreMax(): number  { return this.graphicsScore[this.graphicsScore.length-1]; }
    public graphicsCores: number[] = [];
    get graphicsCoresMin(): number { return this.graphicsCores[0]; }
    get graphicsCoresMax(): number  { return this.graphicsCores[this.graphicsCores.length-1]; }
    public graphicsMemory: number[] = [];
    get graphicsMemoryMin(): number { return this.graphicsMemory[0]; }
    get graphicsMemoryMax(): number  { return this.graphicsMemory[this.graphicsMemory.length-1]; }
    public graphicsFrequency: number[] = [];
    get graphicsFrequencyMin(): number { return this.graphicsFrequency[0]; }
    get graphicsFrequencyMax(): number  { return this.graphicsFrequency[this.graphicsFrequency.length-1]; }
    public graphicsScoreByCard = new Map<string, number[]>();
    getGraphicsScoreByCardMin(value: string): number { return this.graphicsScoreByCard.get(value)[0]; }
    getGraphicsScoreByCardMax(value: string): number  { return this.graphicsScoreByCard.get(value)[this.graphicsScoreByCard.get(value).length-1]; }
    public graphicsCoresByCard = new Map<string, number[]>();
    getGraphicsCoresByCardMin(value: string): number { return this.graphicsCoresByCard.get(value)[0]; }
    getGraphicsCoresByCardMax(value: string): number  { return this.graphicsCoresByCard.get(value)[this.graphicsCoresByCard.get(value).length-1]; }
    public graphicsMemoryByCard = new Map<string, number[]>();
    getGraphicsMemoryByCardMin(value: string): number { return this.graphicsMemoryByCard.get(value)[0]; }
    getGraphicsMemoryByCardMax(value: string): number  { return this.graphicsMemoryByCard.get(value)[this.graphicsMemoryByCard.get(value).length-1]; }

    // Max memory values
    public memorySize: number[] = [];
    get memorySizeMin(): number { return this.memorySize[0]; }
    get memorySizeMax(): number  { return this.memorySize[this.memorySize.length-1]; }
    // Max storage values
    public storageSize: number[] = [];
    get storageSizeMin(): number { return this.storageSize[0]; }
    get storageSizeMax(): number  { return this.storageSize[this.storageSize.length-1]; }
    public storageIops: number[] = [];
    get storageIopsMin(): number { return this.storageIops[0]; }
    get storageIopsMax(): number  { return this.storageIops[this.storageIops.length-1]; }
    public storageThroughput: number[] = [];
    get storageThroughputMin(): number { return this.storageThroughput[0]; }
    get storageThroughputMax(): number  { return this.storageThroughput[this.storageThroughput.length-1]; }

    // The cheapest machine available, so we can adjust the resource cap slider
    public cheapestMachine: Machine = null;
    // The most expensive machine available, incase we want to adjust the max resource cap in the future
    public mostExpensiveMachine: Machine = null;

	constructor(machines: Machine[], cpuLabels: string[][], cpuGrid: Machine[][][], gpuLabels: string[][], gpuGrid: Machine[][][], maxCost: number) {
        this.inventory = [...machines];
        this.cpuLabels = [...cpuLabels];
        this.cpuGrid = [...cpuGrid];
        this.gpuLabels = [...gpuLabels];
        this.gpuGrid = [...gpuGrid];

        for (let row of cpuGrid) {
            var bucketSize = 0;
            for (let bucket of row) {
                if (bucket.length > bucketSize) bucketSize = bucket.length;
            }
            for (let bucket of row) {
                const thisBucketSize = bucket.length;
                for (let i = 0; i < bucketSize - thisBucketSize; i++) {
                    bucket.push(new NoMachine());
                }
            }
        }

        for (let row of gpuGrid) {
            var bucketSize = 0;
            for (let bucket of row) {
                if (bucket.length > bucketSize) bucketSize = bucket.length;
            }
            for (let bucket of row) {
                const thisBucketSize = bucket.length;
                for (let i = 0; i < bucketSize - thisBucketSize; i++) {
                    bucket.push(new NoMachine());
                }
            }
        }

        this.setAbsoluteMaxResources(maxCost);
        // Global.onUserChange.connect(() => this.setAbsoluteMaxResources());
    }

    //  It is useful for us to know what the cost of the cheapest machine is
    public getCheapestMachineCost(): number {
        if (this.cheapestMachine != null) {
            return this.cheapestMachine.rate;
        }
        return 0;
    }

    public getMostExpensiveMachineCost(): number {
        if (this.mostExpensiveMachine != null) {
            return this.mostExpensiveMachine.rate
        }
        return 0;
    }

    public setAbsoluteMaxResources(maxCost: number) {
        for (let machine of this.inventory) {
            this._machinesByName.set(machine.name, machine)

            if (machine.rate > maxCost) continue;

            if (machine.graphicsNumCards > 0) {
                if (machine.graphicsCardType == 'Unspecified') continue;
                // Try to get card from list we have info about
                var cardNums = this.graphicsCardNums.get(machine.graphicsCardType);
                if (cardNums) {
                    // If we already have info about the card, add the new info about the card to the old info
                    this.graphicsCardNums.set(machine.graphicsCardType, cardNums.concat([machine.graphicsNumCards]));
                } else {
                    // If this is a new card, add it to the list along with its info
                    this.graphicsCards.push(machine.graphicsCardType);
                    this.graphicsCardNums.set(machine.graphicsCardType, [machine.graphicsNumCards]);
                }

                var graphicsScore: number = machine.graphicsScore;
                if (!this.graphicsScore.includes(graphicsScore)) this.graphicsScore.push(graphicsScore);
                if (!this.graphicsScoreByCard.has(machine.graphicsCardType)) {
                    this.graphicsScoreByCard.set(machine.graphicsCardType, [graphicsScore]);
                } else if (!this.graphicsScoreByCard.get(machine.graphicsCardType).includes(graphicsScore)) {
                    this.graphicsScoreByCard.get(machine.graphicsCardType).push(graphicsScore);
                }
                
                var graphicsCores: number = machine.graphicsCores;
                if (!this.graphicsCores.includes(graphicsCores)) this.graphicsCores.push(graphicsCores);
                if (!this.graphicsCoresByCard.has(machine.graphicsCardType)) {
                    this.graphicsCoresByCard.set(machine.graphicsCardType, [graphicsCores]);
                } else if (!this.graphicsCoresByCard.get(machine.graphicsCardType).includes(graphicsCores)) {
                    this.graphicsCoresByCard.get(machine.graphicsCardType).push(graphicsCores);
                }

                var graphicsMemory: number = machine.graphicsMemory;
                if (!this.graphicsMemory.includes(graphicsMemory)) this.graphicsMemory.push(graphicsMemory);
                if (!this.graphicsMemoryByCard.has(machine.graphicsCardType)) {
                    this.graphicsMemoryByCard.set(machine.graphicsCardType, [graphicsMemory]);
                } else if (!this.graphicsMemoryByCard.get(machine.graphicsCardType).includes(graphicsMemory)) {
                    this.graphicsMemoryByCard.get(machine.graphicsCardType).push(graphicsMemory);
                }

                var graphicsFrequency: number = machine.graphicsFrequency;
                if (!this.graphicsFrequency.includes(graphicsFrequency)) this.graphicsFrequency.push(graphicsFrequency);
            }
        
            var computeCores: number = machine.computeCores[1];
            if (!this.computeCores.includes(computeCores)) this.computeCores.push(computeCores);

            var computeScore: number = machine.computeScore[1];
            if (!this.computeScore.includes(computeScore)) this.computeScore.push(computeScore);

            var computeFrequency: number = machine.computeFrequency;
            if (!this.computeFrequency.includes(computeFrequency)) this.computeFrequency.push(computeFrequency);
            
            var memorySize: number = machine.memorySize;
            if (!this.memorySize.includes(memorySize)) this.memorySize.push(memorySize);

            var storageSize: number = machine.storageSize;
            if (!this.storageSize.includes(storageSize)) this.storageSize.push(storageSize);

            var storageIops: number = machine.storageIops;
            if (!this.storageIops.includes(storageIops)) this.storageIops.push(storageIops);

            var storageThroughput: number = machine.storageThroughput;
            if (!this.storageThroughput.includes(storageThroughput)) this.storageThroughput.push(storageThroughput);

            var rate = machine.rate;
            if (this.mostExpensiveMachine == null || rate > this.mostExpensiveMachine.rate) this.mostExpensiveMachine = machine;
            if (this.cheapestMachine == null || rate < this.cheapestMachine.rate) this.cheapestMachine = machine;
        }

        this.graphicsCardNums.forEach(x => x.sort((a, b) => a - b));
        this.graphicsCards.sort();
        
        // compute values
        this.computeCores.sort((a, b) => a - b);
        this.computeScore.sort((a, b) => a - b);
        this.computeFrequency.sort((a, b) => a - b);
        
        // Max graphics values
        this.graphicsScore.sort((a, b) => a - b);
        this.graphicsCores.sort((a, b) => a - b);
        this.graphicsMemory.sort((a, b) => a - b);
        this.graphicsFrequency.sort((a, b) => a - b);
        this.graphicsScoreByCard.forEach(x => x.sort((a, b) => a - b));
        this.graphicsCoresByCard.forEach(x => x.sort((a, b) => a - b));
        this.graphicsMemoryByCard.forEach(x => x.sort((a, b) => a - b));
    
        // Max memory values
        this.memorySize.sort((a, b) => a - b);
        // Max storage values
        this.storageSize.sort((a, b) => a - b);
        this.storageIops.sort((a, b) => a - b);
        this.storageThroughput.sort((a, b) => a - b);
    }
}
