const _ = require('lodash');
const { buildFilter } = require("../filters");
const TargetProcessor = require("./base");

class Rule extends TargetProcessor {
    
    constructor(ruleDef, context) {
        super(context, ruleDef.rule_id);
        this.filters = ruleDef.filters.map(filterDef=>buildFilter(filterDef, context)).filter(f=>f); //remove nulls
        this.buildTargetMap(this.filters);
        this.shouldCache = false;
    }
    
    enrichFinding(finding) {
        finding.ruleId = this.id;
    }
}

module.exports = Rule;