const _ = require('lodash');
const TargetProcessor = require("./base");
const { ReportType } = require("../../../reports/report");

class Step extends TargetProcessor {
    constructor(flowId, stepDef, rules, context) {
        super(context, `${flowId}.${stepDef.id}`);
        this.rules = stepDef.rule_ids.map(rule_id=>rules[rule_id]);
        this.buildTargetMap(this.rules);
        [this.action, this.continue] = this._decodeOnMatch(stepDef.on_match);
        // this.stopOnFirstFinding = !this.continue;
        this.shouldCache = false;
    }
    
    _decodeOnMatch(on_match) {
        return {
            exit_block: [ReportType.REPORT_TYPE_BLOCK, false],
            exit_monitor: [ReportType.REPORT_TYPE_REPORT, false]
        }[on_match];
    }
    
    findingsDone() {
        if (!this.continue) {
            throw new TargetProcessor.StopProcessing(); // don't process the rest of the steps in this flow
        }
    }
    
    enrichFinding(finding) {
        finding.stepId = this.id;
        finding.action = this.action;
    }
}

class Flow extends TargetProcessor {
    constructor(flowDef, rules, context) {
        super(context, flowDef.name);
        this.steps = flowDef.steps.map(stepDef=>new Step(this.id, stepDef, rules, context));
        this.buildTargetMap(this.steps)
        this.shouldCache = false;
    }
    
    enrichFinding(finding) {
        finding.flowName = this.id;
    }
}

module.exports = Flow;
