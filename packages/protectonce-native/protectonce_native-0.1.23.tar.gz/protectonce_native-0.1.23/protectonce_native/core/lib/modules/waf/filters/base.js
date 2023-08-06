'use strict';

const { buildTransformerChainCB } = require("../transformations");
const TargetProcessor = require("../ruleset/base")
const { hashStr, cbOnce, cbEach } = require("../common");

class BaseFilter extends TargetProcessor {
    constructor(filterDef, type, context) {
        super(context, "filter_" + String(hashStr(JSON.stringify(filterDef)))); // use hash of the whole thing as context id so we cache based on that
        this.targets = filterDef.targets;
        this.transformer = buildTransformerChainCB(filterDef.transformations);
        this.minLength = filterDef.options.min_length || 0;
        this.includeTransient = !!filterDef.options.match_inter_transformers;
        this.type = type;
        this.shouldCache = false;
        if (!this.cache) this.shouldCache = false;
    }

    getTargets() {
        return this.targets;
    }

    checkTargetCB(targetName, valueList, findingCb, doneCb) {
        let waitingCount = 0;
        let doneCalled = false;

        valueList.getTransformedValuesCB(this.transformer, this.includeTransient,
            ([value, orig]) => {
                if (value && (!this.minLength || value.length >= this.minLength)) {
                    if (this.shouldCache) {
                        // yield* this.cache.getValue(`${this.id}.${targetName}.${value}`, ()=>this.doCheck(value, orig)) // TODO: try without targetName
                        let cacheKey = `${this.id}.${value}`;
                        if (this.cache.get(cacheKey)) { // cache says we already cleared this one
                            return
                        }
                        let foundFinding = false;
                        this.doCheckCB(value, orig,
                            cbOnce(findingCb, () => foundFinding = true),
                            () => {
                                if (!foundFinding) {
                                    this.cache.set(cacheKey);
                                }
                            });
                    } else {
                        this.doCheckCB(value, orig,
                            findingCb,
                            () => {
                            })
                    }
                }
            },
            () => {
                if (doneCb) doneCb();
            }
        )
        // if (waitingCount==0 && !doneCalled) {
        //     if (doneCb) doneCb(); // we never found any values, so just call done
        // }
    }

    // *checkTarget(targetName, valueList) {
    //     let that=this;
    //     for (let [value, orig] of valueList.getTransformedValues(this.transformer, this.includeTransient)) {
    //         if (!this.minLength || value.length >= this.minLength) {
    //             if (this.shouldCache) {
    //                 yield* this.cache.getValue(`${this.id}.${targetName}.${value}`, ()=>this.doCheck(value, orig)) // TODO: try without targetName
    //             } else {
    //                 yield *this.doCheck(value, orig)
    //             }
    //         }  
    //     }
    // }

    enrichFinding(finding) {
        finding.type = this.type;
    }

    doCheck(data, originalData) {
        throw new Error("Not Implemented");
    }

    doCheckCB(data, originalData, cb, doneCb) {
        throw new Error("Not Implemented");
    }

}

module.exports = BaseFilter;