const _ = require('lodash');

const openRASP = require('./openRASP');
const ProtectOnceContext = require('../context');
const RegExpManager = require('../../utils/regex_manager');
const { ReportType } = require('../../reports/report');
const { SecurityActivity } = require('../../reports/security_activity');
const HeartbeatCache = require('../../reports/heartbeat_cache');
const RulesManager = require('../../rules/rules_manager');
const Constants = require('../../utils/constants');
const {
    RuntimeData,
    CommandData,
    XmlData,
    SsrfData,
    SsrfRedirectData
} = require('../../runtime/runtime_data');
const { SQLData } = require('../../runtime/runtime_data');
const { FileData } = require('../../runtime/runtime_data');
const Logger = require('../../utils/logger');
const nosql = require('./impl/nosql');

function createSecurityActivity(inputData, result, options) {
    let reportType = setBlockOrAlert(options.runtimeData, options.shouldBlock);
    const request = inputData.data || {};
    return {
        events: [
            {
                eventType: Constants.RASP_EVENT_TYPE,
                poSessionId: request.poSessionId,
                reportType,
                resultConfidence: result.confidence,
                resultName: result.name,
                resultMessage: result.message
            }
        ],
        shouldCollectStacktrace: true
    };
}
function setBlockOrAlert(runtimeData, shouldBlock) {
    let reportType = ReportType.REPORT_TYPE_ALERT;
    if (shouldBlock === true) {
        runtimeData.setBlock();
        reportType = ReportType.REPORT_TYPE_BLOCK;
    } else {
        runtimeData.setAlert();
    }
    return reportType;
}

function checkRegexp(data) {
    const runtimeData = new RuntimeData(data);
    const rule = RulesManager.getRule(runtimeData.context);

    if (!rule) {
        Logger.write(Logger.DEBUG && `RASP.checkRegexp: No rule found for id: ${runtimeData.context}`);
        return runtimeData;
    }

    const regExpressions = rule.regExps;
    let match = false;
    const args = runtimeData.args;
    for (let regExpId of regExpressions) {
        const regExp = RegExpManager.getRegExp(regExpId);

        // TODO: Use args from the rule instead of scanning all args
        for (let arg of args) {
            // FIXME: What about arguments which are other than string
            if (!_.isString(arg)) {
                continue;
            }

            if (arg.search(regExp) >= 0) {
                match = true;
                break;
            }
        }

        if (match === true) {
            break;
        }
    }

    if (match) {
        setBlockOrAlert(runtimeData, rule.shouldBlock);
        if (rule.shouldBlock === true) {
            runtimeData.message = 'ProtectOnce has blocked an attack';
        } else {
            runtimeData.message = 'ProtectOnce has detected an attack';
        }
        Logger.write(Logger.DEBUG && `RASP.checkRegexp: Attack found: ${runtimeData.message}`);
    }

    return runtimeData;
}

function detectSQLi(data) {
    try {
        const sqlData = new SQLData(data.data);

        const rule = RulesManager.getRule(data.context);
        if (!rule) {
            Logger.write(Logger.DEBUG && `RASP.detectSQLi: No rule found for id: ${data.context}`);
            return sqlData;
        }

        const context = ProtectOnceContext.get(sqlData.sessionId);
        const result = openRASP.detectSQLi(
            sqlData.query,
            sqlData.callStack,
            context
        );
        if (!result) {
            Logger.write(Logger.DEBUG && `RASP.detectSQLi: No attack found in query: ${sqlData.query}`);
            return sqlData;
        }

        Logger.write(Logger.DEBUG && `RASP.detectSQLi: Attack found in query: ${sqlData.query}`);

        return createSecurityActivity(data, result, {
            runtimeData: sqlData,
            shouldBlock: rule.shouldBlock
        });
    } catch (e) {
        Logger.write(Logger.DEBUG && `RASP.detectSQLi: failed with error: ${e}`);
        return {};
    }
}

function executeLFI(lfiType, data, fileData) {
    const rule = RulesManager.getRule(data.context);
    if (!rule) {
        Logger.write(Logger.DEBUG && `RASP.executeLFI: No rule found for type: ${lfiType}, id: ${data.context}`);
        return fileData;
    }

    const context = ProtectOnceContext.get(fileData.sessionId);
    const result = openRASP.detectLFI(
        lfiType,
        fileData.source,
        fileData.dest,
        fileData.path,
        fileData.realpath,
        fileData.filename,
        fileData.stack,
        fileData.url,
        context
    );
    if (!result) {
        Logger.write(Logger.DEBUG && `RASP.executeLFI: No attack found in data: ${JSON.stringify(fileData)}`);
        return fileData;
    }
    Logger.write(Logger.DEBUG && `RASP.executeLFI: Attack found in data: ${JSON.stringify(fileData)}`);

    return createSecurityActivity(data, result, {
        runtimeData: fileData,
        shouldBlock: rule.shouldBlock
    });
}

function getLfiType(mode) {
    if (mode.toLowerCase() === 'read') {
        return 'readFile'
    }
    if (mode.toLowerCase() === 'write') {
        return 'writeFile';
    }
    return;
}

function detectOpenFileLFI(data) {
    try {
        const fileData = new FileData(data.data);
        const lfiType = getLfiType(_.isString(fileData.mode) && fileData.mode);
        if (lfiType) {
            return executeLFI(lfiType, data, fileData);
        }
    } catch (e) {
        Logger.write(Logger.DEBUG && `RASP.detectOpenFileLFI: failed with error: ${e}`);
    }
    return {};
}

function detectUploadFileLFI(data) {
    try {
        const fileData = new FileData(data.data);
        return executeLFI('fileUpload', data, fileData);
    } catch (e) {
        Logger.write(Logger.DEBUG && `RASP.detectUploadFileLFI: failed with error: ${e}`);
        return {};
    }
}

function detectDeleteFileLFI(data) {
    try {
        const fileData = new FileData(data.data);
        return executeLFI('deleteFile', data, fileData);
    } catch (e) {
        Logger.write(Logger.DEBUG && `RASP.detectDeleteFileLFI: failed with error: ${e}`);
        return {};
    }
}

function detectRenameFileLFI(data) {
    try {
        const fileData = new FileData(data.data);
        return executeLFI('rename', data, fileData);
    } catch (e) {
        Logger.write(Logger.DEBUG && `RASP.detectRenameFileLFI: failed with error: ${e}`);
        return {};
    }
}

function detectListDirectoryLFI(data) {
    try {
        const fileData = new FileData(data.data);
        return executeLFI('directory', data, fileData);
    } catch (e) {
        Logger.write(Logger.DEBUG && `RASP.detectListDirectoryLFI: failed with error: ${e}`);
        return {};
    }
}

function detectIncludeLFI(data) {
    try {
        const fileData = new FileData(data.data);
        return executeLFI('include', data, fileData);
    } catch (e) {
        Logger.write(Logger.DEBUG && `RASP.detectIncludeLFI: failed with error: ${e}`);
        return {};
    }
}

function detectShellShock(data) {
    try {
        const commandData = new CommandData(data.data);

        const rule = RulesManager.getRule(data.context);
        if (!rule) {
            Logger.write(Logger.DEBUG && `RASP.detectShellShock: No rule found for id: ${data.context}`);
            return commandData;
        }

        const context = ProtectOnceContext.get(commandData.sessionId);
        const result = openRASP.detectShellShock(
            commandData.command,
            commandData.stack,
            context
        );
        if (!result) {
            Logger.write(Logger.DEBUG && `RASP.detectShellShock: No attack found for command: ${commandData.command}`);
            return commandData;
        }
        Logger.write(Logger.DEBUG && `RASP.detectShellShock: Attack found for command: ${commandData.command}`);

        return createSecurityActivity(data, result, {
            runtimeData: commandData,
            shouldBlock: rule.shouldBlock
        });
    } catch (e) {
        Logger.write(Logger.DEBUG && `RASP.detectShellShock: failed with error: ${e}`);
        return {};
    }
}

function preprocessDetectSsrf(data) {
    const paramUrl = new URL(decodeURIComponent(data.url));
    data.url = paramUrl.pathname;
    data.hostname = paramUrl.hostname;
    const ip = data.hostname.match(/\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/);
    if (ip === null) {
        data.ip = [];
    } else {
        data.ip = ip;
    }
    if (!data.hostname && ip === null) {
        data.url = paramUrl.toString();
    }
    return data;
}

function detectSsrf(data) {
    try {
        if (!data.data.hasOwnProperty('hostname') &&
            !data.data.hasOwnProperty('ip')) {
            data.data = preprocessDetectSsrf(data.data);
        }
        const ssrfData = new SsrfData(data.data);

        const rule = RulesManager.getRule(data.context);
        if (!rule) {
            Logger.write(Logger.DEBUG && `RASP.detectSsrf: No rule found for id: ${data.context}`);
            return ssrfData;
        }

        const context = ProtectOnceContext.get(ssrfData.sessionId);
        const result = openRASP.detectSsrf(
            ssrfData.url,
            ssrfData.hostname,
            ssrfData.ip,
            ssrfData.origin_ip,
            ssrfData.origin_hostname,
            context
        );
        if (!result) {
            Logger.write(Logger.DEBUG && `RASP.detectSsrf: No attack found for data: ${JSON.stringify(ssrfData)}`);
            return ssrfData;
        }

        Logger.write(Logger.DEBUG && `RASP.detectSsrf: Attack found for data: ${JSON.stringify(ssrfData)}`);

        return createSecurityActivity(data, result, {
            runtimeData: ssrfData,
            shouldBlock: rule.shouldBlock
        });
    } catch (e) {
        Logger.write(Logger.DEBUG && `RASP.detectSsrf: failed with error: ${e}`);
        return {};
    }
}

function detectXxe(data) {
    try {
        const xmlData = new XmlData(data.data);

        const rule = RulesManager.getRule(data.context);
        if (!rule) {
            Logger.write(Logger.DEBUG && `RASP.detectXxe: No rule found for id: ${data.context}`);
            return xmlData;
        }

        const context = ProtectOnceContext.get(xmlData.sessionId);
        const result = openRASP.detectXxe(xmlData.entity, context);
        if (!result) {
            Logger.write(Logger.DEBUG && `RASP.detectXxe: No attack found for entity: ${xmlData.entity}`);
            return xmlData;
        }
        Logger.write(Logger.DEBUG && `RASP.detectXxe: Attack found for entity: ${xmlData.entity}`);

        return createSecurityActivity(data, result, {
            runtimeData: xmlData,
            shouldBlock: rule.shouldBlock
        });
    } catch (e) {
        Logger.write(Logger.DEBUG && `RASP.detectXxe: failed with error: ${e}`);
        return {};
    }
}

function detectSsrfRedirect(data) {
    try {
        const ssrfRedirectData = new SsrfRedirectData(data.data);

        const rule = RulesManager.getRule(data.context);
        if (!rule) {
            Logger.write(Logger.DEBUG && `RASP.detectSsrfRedirect: No rule found for id: ${data.context}`);
            return ssrfRedirectData;
        }

        const context = ProtectOnceContext.get(ssrfRedirectData.sessionId);
        const result = openRASP.detectSsrfRedirect(
            ssrfRedirectData.hostname,
            ssrfRedirectData.ip,
            ssrfRedirectData.url,
            ssrfRedirectData.url2,
            ssrfRedirectData.hostname2,
            ssrfRedirectData.ip2,
            ssrfRedirectData.port2,
            context
        );
        if (!result) {
            Logger.write(Logger.DEBUG && `RASP.detectSsrfRedirect: No attack found for data: ${JSON.stringify(ssrfRedirectData)}`);
            return ssrfRedirectData;
        }
        Logger.write(Logger.DEBUG && `RASP.detectSsrfRedirect: Attack found for data: ${JSON.stringify(ssrfRedirectData)}`);

        return createSecurityActivity(data, result, {
            runtimeData: ssrfRedirectData,
            shouldBlock: rule.shouldBlock
        });
    } catch (e) {
        Logger.write(Logger.DEBUG && `RASP.detectSsrfRedirect: failed with error: ${e}`);
        return {};
    }
}

function parseNoSQLi(data) {
    try {
        const rule = RulesManager.getRule(data.context);
        if (!rule) {
            Logger.write(Logger.DEBUG && `RASP.detectNoSQLi: No rule found for id: ${data.context}`);
            return {};
        }
        const context = ProtectOnceContext.get(data.data.poSessionId);
        const values = nosql.check(data.data.query, context);
        return { "tokens": values, "noSQLiData": data };
    } catch (e) {
        Logger.write(Logger.ERROR && `RASP.detectNoSQLi: failed with error: ${e}`);
        return {};
    }
}

function checkRegex(data) {
    try {
        const regularExpressions = data.config.regexp;
        const input = data.data.tokens;
        let result = [];

        input.forEach(element => {
            let isMatch = false;
            regularExpressions.some(regex => {
                const regExp = RegExpManager.getRegExp(regex);
                if (regExp.test(element)) {
                    isMatch = true;
                    return true;
                }
            });
            result.push(isMatch);
        });
        return { "regexTokenResult": result, "noSQLiData": data.data.noSQLiData };
    } catch (e) {
        Logger.write(Logger.ERROR && `RASP.checkRegex: failed with error: ${e}`);
        return {};
    }
}

function reportNoSQLiAttack(data) {

    try {
        const regexTokenResult = data.data.regexTokenResult;
        const noSqliData = data.data.noSQLiData;
        let result = false;

        if (regexTokenResult) {
            result = regexTokenResult.some((value) => value);
        }
        const rule = RulesManager.getRule(noSqliData.context);
        const noSqliDataObject = new SQLData(noSqliData.data);

        const resultObject = {
            name: "NoSQLi",
            message: "NoSQLi-Query structure altered by user input",
        }

        const inputData = {
            data: {
                poSessionId: noSqliDataObject.sessionId
            }
        }
        if (result) {
            return createSecurityActivity(inputData, resultObject, {
                runtimeData: noSqliDataObject,
                shouldBlock: rule.shouldBlock
            });
        } else {
            return data.data.noSQLiData;
        }
    } catch (e) {
        Logger.write(Logger.ERROR && `RASP.reportNoSQLiAttack: failed with error: ${e}`);
        return {};
    }
}

module.exports = {
    checkRegexp: checkRegexp,
    detectSQLi: detectSQLi,
    parseNoSQLi: parseNoSQLi,
    checkRegex: checkRegex,
    reportNoSQLiAttack: reportNoSQLiAttack,
    detectOpenFileLFI: detectOpenFileLFI,
    detectUploadFileLFI: detectUploadFileLFI,
    detectDeleteFileLFI: detectDeleteFileLFI,
    detectRenameFileLFI: detectRenameFileLFI,
    detectListDirectoryLFI: detectListDirectoryLFI,
    detectIncludeLFI: detectIncludeLFI,
    detectShellShock: detectShellShock,
    detectSsrf: detectSsrf,
    detectXxe: detectXxe,
    detectSsrfRedirect: detectSsrfRedirect
};
