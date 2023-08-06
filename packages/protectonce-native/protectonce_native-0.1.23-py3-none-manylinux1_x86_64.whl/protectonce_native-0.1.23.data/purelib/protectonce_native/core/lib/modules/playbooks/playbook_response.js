const _ = require('lodash');
const { ReportType } = require('../../reports/report');
class PlaybookResponse {
  constructor() {
    this._operator = 'equals';
  }

  set action(action) {
    if (_.isString(action) && [ReportType.REPORT_TYPE_REDIRECT, ReportType.REPORT_TYPE_BLOCK, ReportType.REPORT_TYPE_NO_RESPONSE].includes(action.toLowerCase())) {
      this._action = action;
    }
  }

  get action() {
    return this._action;
  }

  set redirectUrl(redirectUrl) {
    if (_.isString(redirectUrl)) {
      this._redirectUrl = redirectUrl;
    }
  }

  get redirectUrl() {
    return this._redirectUrl;
  }

  set operator(operator) {
    if (_.isString(operator)) {
      this._operator = operator;
    }
  }

  get operator() {
    return this._operator;
  }

  set by(by) {
    if (_.isString(by)) {
      this._by = by;
    }
  }

  get by() {
    return this._by;
  }

  set ip(ip) {
    if (_.isString(ip)) {
      this._ip = ip;
    }
  }

  get ip() {
    return this._ip;
  }

  set user(user) {
    if (_.isString(user)) {
      this._user = user;
    }
  }

  get user() {
    return this._user;
  }
}

module.exports = PlaybookResponse;