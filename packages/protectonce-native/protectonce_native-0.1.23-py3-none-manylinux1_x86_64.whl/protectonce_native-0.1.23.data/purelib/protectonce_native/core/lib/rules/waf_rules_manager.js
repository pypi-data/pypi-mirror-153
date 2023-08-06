const _ = require('lodash');
// const { Flows } = require('../modules/waf/ruleset');

// const RuleSet = require('../modules/waf/ruleset');
const WAF = require('../modules/waf');

class WAFRulesManager {
    constructor() {

    }

    updateWAFRuleSet(rulesDef) {
        WAF.updateRuleset(rulesDef);
    }


    isInitialised() {
        return true;
    }
}

module.exports = new WAFRulesManager();
