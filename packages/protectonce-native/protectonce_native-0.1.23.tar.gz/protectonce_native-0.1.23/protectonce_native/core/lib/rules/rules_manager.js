const _ = require('lodash');

const Rule = require('./rule');
const Constants = require('../utils/constants');
const Logger = require('../utils/logger');
const WAFRulesManager = require('./waf_rules_manager');
const UserManager = require('../modules/userMonitoring/user_manager');
const PlaybooksManager = require('../modules/playbooks/playbooks_manager');
class RulesManager {
    constructor() {
        this._rules = {};
        this._hash = '';
        this._appDeleted = false;
    }

    get rules() {
        return Object.values(this._rules);
    }

    get hash() {
        return this._hash;
    }

    get shouldMonitor() {
        return this._agentMonitoring === 'enabled';
    }

    getRule(id) {
        if (!this.shouldMonitor || this.isAppDeleted()) {
            return null;
        }

        const rule = this._rules[id];
        if (rule && rule.isEnabled) {
            Logger.write(Logger.DEBUG && `RulesManager: Returning rule for id: ${id}, rule: ${JSON.stringify(rule)}`);
            return rule;
        }

        Logger.write(Logger.DEBUG && `RulesManager: Rule: ${JSON.stringify(rule)} for id: ${id} is disabled`);
        return null;
    }

    get runtimeRules() {
        // TODO: Optimise the runtime rules
        const runtimeRules = [];
        this.rules.forEach(rule => {
            runtimeRules.push(rule.runtimeRule);
        });
        Logger.write(Logger.DEBUG && `RulesManager: Returning runtime rules: ${JSON.stringify(runtimeRules)}`);
        return runtimeRules;
    }

    set rules(rules) {
        if (!_.isArray(rules) || rules.length === 0) {
            // Do not update rules if no rules are returned from backend
            return;
        }

        // TODO: Need to have optimized rules storage once backend starts sending rules diff
        this._rules = {};
        for (let rule of rules) {
            const ruleObj = new Rule(rule);
            this._rules[rule.id] = ruleObj;
        }
    }

    handleIncomingRules(rulesData) {
        Logger.write(Logger.DEBUG && `RulesManager: Rules received from BE: ${JSON.stringify(rulesData)}`);
        if (_.isObject(rulesData) && rulesData['statusCode'] === Constants.APP_DELETE_STATUS_CODE) {
            this._appDeleted = true;
            return;
        }
        const rulesJson = JSON.parse(rulesData.data);
        const environment = rulesJson.environment;
        const agentRule = rulesJson.agentRule || rulesJson.rulesSet;
        UserManager.setBlockedUserList(rulesJson.blockedUsers);
        PlaybooksManager.setPlaybookResponseList(rulesJson.actionList);
        PlaybooksManager.environment = environment;
        if (typeof agentRule === 'undefined' || !_.isObject(agentRule)) {
            return;
        }
        this._hash = agentRule.hash || '';

        if (_.isObject(agentRule.rasp) && agentRule.rasp.hooks) {
            this.rules = agentRule.rasp.hooks;
        } else {
            this.rules = [];
        }
        WAFRulesManager.updateWAFRuleSet(agentRule.waf);
        this._agentMonitoring = agentRule.agentMonitoring || 'enabled';

    }

    isAppDeleted() {
        return this._appDeleted;
    }
}

module.exports = new RulesManager();
