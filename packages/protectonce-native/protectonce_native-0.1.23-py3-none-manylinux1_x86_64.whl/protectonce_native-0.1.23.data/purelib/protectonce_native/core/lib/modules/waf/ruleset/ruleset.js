'use strict';

const Rule = require("./rule");
const Flow = require("./flow");
const FieldMapping = require("./fieldMapping");
const TargetProcessor = require("./base");
const ResultCache = require("../cache");
const Metrics = require("../metrics");

class RuleSet extends TargetProcessor {
    
    constructor(ruleSetDef, context) {
        context = context || {};
        ruleSetDef = ruleSetDef || {};
        if (!context.metrics) {
            context.metrics = new Metrics();
        }
        context.cache = new ResultCache({ metrics: context.metrics });
        super(context, ruleSetDef.id || "");
        this.shouldCache = true;
        
        this.rules = (ruleSetDef.rules||[]).reduce((rules, ruleDef)=>{ let rule = new Rule(ruleDef, context); rules[rule.id]=rule; return rules;}, {});
        this.flows = (ruleSetDef.flows||[]).filter(flow=>flow.status!=="disabled").map(flowDef => new Flow(flowDef, this.rules, context));
        this.fieldMappings = Object.entries(ruleSetDef.field_mapping||{}).reduce((maps, [requestType, mapDef])=>{ maps[requestType] = new FieldMapping(mapDef); return maps;}, {}); 
        this.buildTargetMap(this.flows);        
    }

    mapData(dataType, data, targetCb, doneCb) {
        let fieldMapping = this.fieldMappings[dataType];
        if (!fieldMapping) {
            throw new Error(`Unsupported request type ${dataType}`);
        }
        
        fieldMapping.mapData(data, targetCb, doneCb);
    }


}

module.exports = RuleSet;
