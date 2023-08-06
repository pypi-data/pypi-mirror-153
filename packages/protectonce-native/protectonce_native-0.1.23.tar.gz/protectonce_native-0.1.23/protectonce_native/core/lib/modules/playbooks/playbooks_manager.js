const _ = require('lodash');
const Logger = require('../../utils/logger');
const PlaybookResponse = require('./playbook_response');
const Constants = require('../../utils/constants');
const { ReportType } = require('../../reports/report');
const { getMatcherByOperator } = require('../waf/allowList/get_matcher');
class PlaybooksManager {
  constructor() {
    this.playbookResponseList = [];
    this._environment = null;
  }

  set environment(environment) {
    this._environment = environment;
  }

  get environment() {
    return this._environment;
  }

  setPlaybookResponseList(playbookResponseList) {
    if (_.isArray(playbookResponseList)) {
      this.playbookResponseList = playbookResponseList.map(mapPlaybookResponse);
    }
  }

  checkIfBlockedByIp(sourceIP) {
    let result = {
      action: ReportType.REPORT_TYPE_NO_RESPONSE
    };
    try {
      if (this.playbookResponseList.length) {
        this.playbookResponseList.forEach((playbookResponse) => {
          if ([Constants.IP_FILTER_KEY, Constants.USER_IP_FILTER_KEY].includes(playbookResponse.by.toUpperCase()) && this._checkIfIpBlockedByPlaybook(sourceIP, playbookResponse)) {
            if ((playbookResponse.action === ReportType.REPORT_TYPE_BLOCK && result.action !== ReportType.REPORT_TYPE_BLOCK) || (playbookResponse.action === ReportType.REPORT_TYPE_REDIRECT && ![ReportType.REPORT_TYPE_BLOCK, ReportType.REPORT_TYPE_REDIRECT].includes(result.action))) {
              result = {
                action: playbookResponse.action,
                redirectUrl: playbookResponse.redirectUrl
              };
            }
          }
        });
      }
    } catch (error) {
      Logger.write(
        Logger.DEBUG && `playbooks manager: Failed to check if blocked by ip : ${e}`
      );
    }
    return result;
  }

  checkIfBlockedByUser(username) {
    let result = {
      action: ReportType.REPORT_TYPE_NO_RESPONSE
    };
    try {
      if (this.playbookResponseList.length) {
        for (const playbookResponse of this.playbookResponseList) {
          if ([Constants.USER_FILTER_KEY, Constants.USER_IP_FILTER_KEY].includes(playbookResponse.by.toUpperCase()) && this._checkIfUserBlockedByPlaybook(username, playbookResponse)) {
            if ((playbookResponse.action === ReportType.REPORT_TYPE_BLOCK && result.action !== ReportType.REPORT_TYPE_BLOCK) || (playbookResponse.action === ReportType.REPORT_TYPE_REDIRECT && ![ReportType.REPORT_TYPE_BLOCK, ReportType.REPORT_TYPE_REDIRECT].includes(result.action))) {
              result = {
                action: playbookResponse.action,
                redirectUrl: playbookResponse.redirectUrl
              };
            }
          }
        }
      }
    } catch (error) {
      Logger.write(
        Logger.DEBUG && `playbooks manager: Failed to check if blocked by ip : ${e}`
      );
    }
    return result;
  }

  _checkIfIpBlockedByPlaybook(sourceIP, playbookResponse) {
    const matcher = getMatcherByOperator(playbookResponse.ip, playbookResponse.operator, Constants.IP_FILTER_KEY);
    return matcher.match(sourceIP);
  }

  _checkIfUserBlockedByPlaybook(username, playbookResponse) {
    const matcher = getMatcherByOperator(playbookResponse.user, playbookResponse.operator, Constants.USER_FILTER_KEY);
    return matcher.match(username);
  }
}

function mapPlaybookResponse(response) {
  const playbookResponse = new PlaybookResponse();
  playbookResponse.action = response.type;
  playbookResponse.redirectUrl = response['redirect_uri'];
  playbookResponse.operator = response.operator;
  playbookResponse.by = response.by;
  playbookResponse.ip = response.ip;
  playbookResponse.user = response.userId;
  return playbookResponse;
}

module.exports = new PlaybooksManager();