'use strict';

const { cbOnce, cbEach } = require("../common");

class StopProcessing {
        
}
    
class TargetProcessor {
    constructor(context, id) {
        this.byTarget = new WeakMap();
        this.stopOnFirstFinding = false;
        this.context = context || {};
        this.cache = this.context.cache;
        this.id = id;
        this.shouldCache = false;
        if (!this.cache) {
            this.shouldCache = false;
        }
    }
    
    buildTargetMap(listOfTPs) {
        for (let _tp of listOfTPs) {
            for (let targetName of _tp.getTargets()) {
                let targetList = this.byTarget[targetName] = this.byTarget[targetName] || []; 
                targetList.push(_tp);
            }
        }
    }
    
    getTargets() {
        return Object.keys(this.byTarget);
    }
    
    _cacheKey(targetName, value) {
        return `${this.id}.${targetName}.${value}`;
    }
    
    checkTargetCB(targetName, valueList, findingCb, doneCb) {
        if (!this.cache) {
            this.shouldCache = false;
        }
        if (this.shouldCache) {
            // remove any values known to be ok for this target
            valueList.values = valueList.values.filter(value=>!this.cache.get(this._cacheKey(targetName, value)));
            
            if (valueList.values.length == 0) {
                if (doneCb) doneCb();
                return // no findings
            } else {
                let goodValues = new Set(valueList.values);
                return this._checkTargetCB(targetName, valueList, 
                    (finding)=>{ 
                        findingCb(finding); 
                        goodValues.delete(finding.originalData); // we found something so we can't skip this next time
                    }, 
                    ()=>{ 
                        goodValues.forEach(value=>{
                            this.cache.set(this._cacheKey(targetName, value));
                        });
                        if (doneCb) doneCb();
                    }
                )
            }
            // return this.cache.getValueCB(this._cacheKey(targetName, valueList), cb, (_cb)=>this._checkTargetCB(targetName, valueList, _cb))
        } else {
            return this._checkTargetCB(targetName, valueList, findingCb, doneCb);
        }     
    }
    
    _checkTargetCB(targetName, valueList, cb, doneCb) {
        let that = this;
        let _tps = this.byTarget[targetName] || [];
        let waiting_count=0;
        if (_tps.length == 0) {
            return doneCb();
        }
        waiting_count = _tps.length;
        for (let tp of _tps) {
            tp.checkTargetCB(targetName, valueList, 
                (finding) => {
                    that.enrichFinding(finding);
                    cb(finding);
                    // if (this.stopOnFirstFinding) {
                    //     return false;
                    // }
                    },
                ()=> {
                    // console.log(`Called done for ${this.id}(${targetName})`)
                    if (--waiting_count == 0) {
                        if (doneCb) doneCb();
                    }
                }
            );
            if (tp.parentShouldStop()) {
                break
            }
        }   
    }
    
    // *checkTarget(targetName, valueList) {
    //     let that=this;
        
    //     let findingsGen = function*() {
    //         let _tps = that.byTarget[targetName] || [];
    //         for (let tp of _tps) {
    //             try {
    //                 for (let finding of tp.checkTarget(targetName, valueList)) {
    //                     that.enrichFinding(finding);
    //                     yield finding;
    //                     if (that.stopOnFirstFinding) {
    //                         return;
    //                     }
    //                 }
    //                 tp.findingsDone();
    //             } catch (err) {
    //                 if (err instanceof StopProcessing) {
    //                     break; 
    //                 } else {
    //                     throw err;
    //                 }
    //             }
    //         }
            
    //     }
    //     if (this.shouldCache) {
    //         yield *this.cache.getValue(this._cacheKey(targetName, valueList), findingsGen); 
    //     } else {
    //         yield *findingsGen();
    //     }
    // }
    
    enrichFinding(finding) {
        
    }
    
    findingsDone() {
        
    }
    
    parentShouldStop() {
        return false;
    }
}

TargetProcessor.StopProcessing = StopProcessing;

module.exports = TargetProcessor;
