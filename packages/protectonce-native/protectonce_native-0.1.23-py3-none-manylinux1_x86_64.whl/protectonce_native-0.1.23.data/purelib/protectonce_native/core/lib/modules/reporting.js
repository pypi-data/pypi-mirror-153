const _ = require('lodash');

const Constants = require('../utils/constants');
const { ReportType } = require('../reports/report');
const { SecurityActivity } = require('../reports/security_activity');
const { Event } = require('../reports/event');
const HeartbeatCache = require('../reports/heartbeat_cache');
const Logger = require('../utils/logger');
const { syncRules } = require('./sync');

function createSecurityActivity(data) {
  let sessionId = null;
  try {
    if (_.isArray(data.data) && data.data[0] && data.data[0].poSessionId) {

      return mapEventsAndGetAction(data.data, data.data[0].poSessionId);
    }
  } catch (error) {
    Logger.write(
      Logger.ERROR && `Error occurred while storing stackTace : ${error}`
    );
  }
  return {
    action: ReportType.REPORT_TYPE_NONE,
    sessionId
  };
}

function storeStackTrace(data) {
  let sessionId = null;
  try {
    if (_.isArray(data.data) && data.data[0] && data.data[0].poSessionId) {
      sessionId = data.data[0].poSessionId;
      return mapEventsAndGetAction(data.data, sessionId);
    }
  } catch (error) {
    Logger.write(
      Logger.ERROR && `Error occurred while storing stackTace : ${error}`
    );
  }
  return {
    action: ReportType.REPORT_TYPE_NONE,
    sessionId
  };
}

function mapEvents(eventsToMap) {
  try {
    let blocked = false;
    const mappedEvents = eventsToMap.reduce((acc, event) => {
      if (
        _.isString(event.eventType) &&
        event.reportType &&
        event.poSessionId &&
        event.resultName
      ) {
        blocked = blocked || event.reportType === ReportType.REPORT_TYPE_BLOCK;

        acc.push(
          new Event(
            event.eventType,
            event.poSessionId,
            event.reportType === ReportType.REPORT_TYPE_BLOCK,
            event.resultConfidence,
            new Date(),
            new Date(),
            event.resultName,
            '',
            event.resultMessage,
            500,
            event.stackTrace,
            event.reportType,
            event.redirectUrl
          )
        );
      }
      return acc;
    }, []);
    const actionObject = getAction(blocked, mappedEvents);
    return {
      mappedEvents,
      action: actionObject.action,
      redirectUrl: actionObject.redirectUrl
    };
  } catch (e) {
    Logger.write(Logger.DEBUG && `Failed to mapEvents with error: ${e}`);
    return {};
  }
}

function getAction(blocked, events) {
  if (events.some((event) => event.category === Constants.PLAYBOOK_EVENT_TYPE)) {
    const playbookEvent = events.find((event) => event.category === 'playbook');
    return {
      action: playbookEvent.action,
      redirectUrl: playbookEvent.redirect_url
    };
  }

  events = events.filter(event => event.category !== Constants.PLAYBOOK_EVENT_TYPE);

  if (blocked) {
    if (events.find((event) => event.category === Constants.RASP_EVENT_TYPE)) {
      return {
        action: ReportType.REPORT_TYPE_BLOCK
      };
    }
    if (events.find((event) => event.category === Constants.WAF_EVENT_TYPE)) {
      return {
        action: ReportType.REPORT_TYPE_ABORT
      };
    }
  }

  return {
    action: ReportType.REPORT_TYPE_NONE
  };
}

function generateWafEvents(data) {
  let sessionId = null;
  try {
    const findings = data.data.findings;
    if (!_.isArray(findings)) {
      return {
        events: [],
        shouldCollectStacktrace: false
      };
    }
    sessionId = data.data.poSessionId;
    let events = [];
    for (let finding of findings) {
      events.push({
        eventType: finding.eventType ? finding.eventType : Constants.WAF_EVENT_TYPE,
        poSessionId: sessionId,
        reportType: finding.action,
        redirectUrl: finding.redirectUrl,
        resultName: finding.flowName
      });
    }

    return mapEventsAndGetAction(events, sessionId);
  } catch (e) {
    Logger.write(Logger.ERROR && `Failed to generateWafEvents with error: ${e}`);
  }
  return {
    action: ReportType.REPORT_TYPE_NONE,
    sessionId
  };
}

function mapEventsAndGetAction(events, sessionId) {
  try {
    const { mappedEvents, action, redirectUrl } = mapEvents(
      events
    );
    if (_.isArray(mappedEvents) && _.isString(action)) {
      const securityActivity = new SecurityActivity(sessionId);
      securityActivity.events.push(...mappedEvents);

      HeartbeatCache.cacheReportEvents(securityActivity);
      return {
        action,
        redirectUrl,
        sessionId
      };
    }
  } catch (error) {
    Logger.write(Logger.ERROR && `Failed to mapEventsAndGetAction with error: ${e}`);
  }
  return {
    action: ReportType.REPORT_TYPE_NONE,
    sessionId
  };
}

function forceSendHeatbeat(report) {
  try {
    if (_.isAWSLambdaEnv() && _.isObject(report) && _.isObject(report.data) && (report.data.action === 'block' || report.data.action === 'abort' || report.data.action === 'redirect')) {
      HeartbeatCache.setClosed(report.data.sessionId);
      syncRules(true);
      return report;
    }
  } catch (e) {
    Logger.write(Logger.ERROR && `Failed to forceSendHeatbeat with error: ${e}`);
  }
  return report;
}

module.exports = {
  createSecurityActivity,
  generateWafEvents,
  storeStackTrace,
  forceSendHeatbeat
};