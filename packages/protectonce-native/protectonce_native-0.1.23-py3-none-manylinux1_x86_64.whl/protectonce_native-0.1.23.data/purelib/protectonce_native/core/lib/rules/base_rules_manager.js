const RulesManager = require('./rules_manager');
const WAFRulesManager = require('./waf_rules_manager');

class BaseRulesManager {
    constructor() {
        this._rulesmanager = RulesManager;
        this._wafrulesmanager = WAFRulesManager;
        this._hash = '';
    }

    get rulesManager() {
        return this._rulesmanager;
    }

    get wafRulesManager() {
        return this._wafrulesmanager;
    }

    get rulesHash() {
        return this._hash;
    }

    initialiseRulesManager(rules) {
        this.RulesManager.handleIncomingRules(rules.rasp);
        this.WAFRulesManager.initialiseWAFRuleSet(rules.waf);
        this._hash = rules.hash;
    }
}

module.exports = new BaseRulesManager();