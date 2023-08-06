const { SecurityActivity } = require('../../reports/security_activity');
const { Event } = require('../../reports/event');
const HeartbeatCache = require('../../reports/heartbeat_cache');
const Logger = require('../../utils/logger');
const userManager = require('./user_manager');
const ProtectOnceContext = require('../context');
const { ReportType } = require('../../reports/report');
const PlaybooksManager = require('../playbooks/playbooks_manager');
const Constants = require('../../utils/constants');
require('../../utils/common_utils');
const _ = require('lodash');
const { EventType } = require('../../utils/event_type');

/* This method creates securityActivity object for signUp data of user
* It adds signup event in Event object inside SecurityActivity object 
* It also returns action object with values (allow and block) based 
  on userName passed is in blocked user list
* @param  {Object} signUpData - signUp data received as input
*          @param {Object} data This holds actual signup data
*              @param {String} poSessionId
*              @param {String} userName
*/
function storeSignUpData(signUpData) {
    try {
        const poSessionId = signUpData.data.poSessionId;
        const userName = signUpData.data.userName;
        const userData = { "poSessionId": poSessionId, "userName": userName, "status": "success" };
        const result = PlaybooksManager.checkIfBlockedByUser(userName);
        const event = getEvent(userData, EventType.EVENT_TYPE_SIGNUP, result);
        Logger.write(Logger.DEBUG && `calling storeSignUpData with userName : ${userName}`);
        createSecurityActivity(poSessionId, createUser(userName), event);
        return {
            result
        };
    } catch (e) {
        Logger.write(Logger.DEBUG && `Failed calling storeSignUpData with error : ${e}`);
        return { "result": { "action": ReportType.REPORT_TYPE_NONE } };
    }
}

function createUser(userName) {
    return {
        "identifier": userName
    }
}

/* This method creates securityActivity object for login data of user
* It adds login event in Event object inside SecurityActivity object 
* It also returns action object with values (allow and block) based 
  on userName passed is in blocked user list
* @param  {Object} loginData - loginData received as input
*          @param {Object} data This holds actual login data
*              @param {String} poSessionId
*              @param {String} success
*              @param {String} userName
*/
function storeLoginData(loginData) {
    try {
        const poSessionId = loginData.data.poSessionId;
        const success = loginData.data.success;
        const userName = loginData.data.userName;
        const userData = { "poSessionId": poSessionId, "userName": userName, "status": success ? "success" : "failure" };

        const result = PlaybooksManager.checkIfBlockedByUser(userName);
        const event = getEvent(userData, EventType.EVENT_TYPE_LOGIN, result);
        Logger.write(Logger.DEBUG && `calling storeLoginData with status : ${success} ` && `userName : ${userName}`);
        createSecurityActivity(poSessionId, createUser(userName), event);
        return { result };
    } catch (e) {
        Logger.write(Logger.DEBUG && `Failed calling storeLoginData with error : ${e}`);
        return { "result": { "action": ReportType.REPORT_TYPE_NONE } };
    }
}

function getEvent(userData, eventType, result) {
    const status = result.action === ReportType.REPORT_TYPE_BLOCK ? 'failure' : userData.status;

    const event = new Event("", userData.poSessionId, result.action === ReportType.REPORT_TYPE_BLOCK, "", new Date(),
        new Date(), eventType, "", "", status, null, result.action, result.redirectUrl, "", populateEventAttributes(userData.poSessionId, result.action));
    return event;
}

function populateEventAttributes(sessionId, action) {
    const context = ProtectOnceContext.get(sessionId);
    const requestContentTypeHeader = getContentTypeHeader(context.requestHeaders);
    const responseContentTypeHeader = getContentTypeHeader(context.responseHeaders);
    const responseStatus = getResponseStatus(context, action);

    return {
        [Constants.BLOCKED_KEY]: action === ReportType.REPORT_TYPE_BLOCK,
        [Constants.APPLICATION_ENV_KEY]: PlaybooksManager.environment,
        [Constants.REQUEST_HEADERS_CONTENT_TYPE_KEY]: requestContentTypeHeader,
        [Constants.RESPONSE_HEADERS_CONTENT_TYPE_KEY]: responseContentTypeHeader,
        [Constants.RESPONSE_STATUS_KEY]: responseStatus
    };
}

function getContentTypeHeader(headers) {
    return headers && _.getObjectKeysToLower(headers, 'content-type');
}

function getResponseStatus(context, action) {
    if (context.statusCode) {
        return isSuccessStatusCode(context.statusCode) ? 'success' : 'failure';
    }
    if (action === ReportType.REPORT_TYPE_BLOCK) {
        return 'failure';
    }

    return 'success';
}

function isSuccessStatusCode(statusCode) {
    return statusCode >= 200 && statusCode <= 399;
}

function getAction(userName) {
    return userManager.isUserInBlockedList(userName) ? ReportType.REPORT_TYPE_BLOCK : ReportType.REPORT_TYPE_NONE;
}


function createSecurityActivity(poSessionId, user, event) {
    const context = ProtectOnceContext.get(poSessionId);
    let securityActivity = HeartbeatCache.getReport(poSessionId);
    if (!securityActivity) {
        securityActivity = new SecurityActivity(poSessionId, "status", context.sourceIP, "200", context.method, context.requestPath, user);
    } else {
        securityActivity.user = user;
    }
    if (event) {
        securityActivity.addEvent(event);
    }
    HeartbeatCache.cacheReport(securityActivity);
}

/*This method creates securityActivity object for user details 
* It adds user object inside securityActivity object with identifier as key and 
* userName as value
* It also returns action object with values (allow and block) based 
  on userName passed is in blocked user list
* @param  {Object} identifyData - identifyData received as input
*          @param {Object} data This holds actual user data
*              @param {String} poSessionId
*              @param {String} userName
*/
function identify(identifyData) {
    try {
        const poSessionId = identifyData.data.poSessionId;
        const userName = identifyData.data.userName;
        const userData = { "poSessionId": poSessionId, "userName": userName };
        const result = PlaybooksManager.checkIfBlockedByUser(userName);
        let event = undefined;
        if ([ReportType.REPORT_TYPE_BLOCK, ReportType.REPORT_TYPE_REDIRECT].includes(result.action)) {
            event = getEvent(userData, "auth", result);
        }
        createSecurityActivity(poSessionId, createUser(userName), event);
        return { result };
    } catch (e) {
        Logger.write(Logger.DEBUG && `Failed calling identify with error : ${e}`);
        return { "result": { "action": ReportType.REPORT_TYPE_NONE } };
    }
}

function checkIfBlocked(userData) {
    try {
        const poSessionId = userData.data.poSessionId;
        const userName = userData.data.userName;
        const result = { "action": getAction(userName) };
        let event = undefined;
        if (result.action === ReportType.REPORT_TYPE_BLOCK) {
            event = getEvent(userData.data, "userMonitoring", result);
        }
        createSecurityActivity(poSessionId, createUser(userName), event);
        return { result };
    }
    catch (e) {
        Logger.write(Logger.DEBUG && `Failed calling checkIfBlocked with error : ${e}`);
    }
    return { "result": { "action": ReportType.REPORT_TYPE_NONE } };
}

module.exports = {
    checkIfBlocked: checkIfBlocked,
    storeSignUpData: storeSignUpData,
    storeLoginData: storeLoginData,
    identify: identify
}

