const _ = require('lodash');
const { hashStr, StrHash} = require("./common");

// const resultsCache = require("./cache");

class ValueList {
    constructor() {
        this.values = [];
        this.cache = {};
    }
    
    add(value) {
        this.values.push(value);
    }

    
    getTransformedValuesCB(transformerChain, includeTransient, cb, doneCb) {
        return transformerChain(this.values, cb, doneCb, this.cache, includeTransient);
    }
}

class DataFrame {
    constructor(ruleset) {
        this.dataMap = {};
        this.ruleset = ruleset;
    }
    
    addAndCheckCB(targetName, cb, doneCb, ...values) {
        // if (values.length==1 && _.isArray(values[0])) {
        //     values = values[0];
        // }
        let valueList = this.dataMap[targetName] = (this.dataMap[targetName] || new ValueList());
        values.forEach(v=>valueList.add(v));

        if (this.ruleset) {
            this.ruleset.checkTargetCB(targetName, valueList, cb, doneCb); 
        } else {
            doneCb();
        }
    }
    
    addAndCheckPromise(targetName, ...values) {
        return new Promise((res, rej)=> {
            let findings = [];
            this.addAndCheckCB(targetName, (finding)=>findings.push(finding), ()=>res(findings), ...values);
        })
    }
}

module.exports = DataFrame;