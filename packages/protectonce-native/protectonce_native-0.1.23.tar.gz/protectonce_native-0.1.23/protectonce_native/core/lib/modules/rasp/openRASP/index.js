require('../../../utils/common_utils');
const _ = require('lodash');
const qs = require('qs');

require('./init')();

const Severity = {
    OPEN_RASP_SEVERITY_MINOR: 'minor',
    OPEN_RASP_SEVERITY_MAJOR: 'major',
    OPEN_RASP_SEVERITY_CRITICAL: 'critical'
};

function _toRASPParameters(context) {
    if (!context || (!context['queryParams'] && !context['pathParams'])) {
        return;
    }

    const parameters = { ...context['pathParams'], ...context['queryParams'] };

    Object.keys(parameters).forEach((key) => {
        if (_.isString(parameters[key])) {
            // open rasp expects each parameter to be an array of strings
            parameters[key] = [parameters[key]];
        }
    });
    return parameters;
}

function _toRASPJson(context) {
    if (!context) {
        return {};
    }

    const contentTypeHeader = context && context['requestHeaders'] && _.getObjectKeysToLower(context['requestHeaders'], 'content-type');
    if (_.isValidJsonRequest(contentTypeHeader)) {
        if (!_.isString(context['requestBody'])) {
            return {};
        }

        const parsedBody = _.parseIfJson(context['requestBody']);;

        if (!parsedBody) {
            return {};
        }

        return parsedBody;
    }

    if (_.isValidEncodedFormDataRequest(contentTypeHeader)) {
        if (!_.isString(context['requestBody'])) {
            return {};
        }

        return qs.parse(context['requestBody']);
    }

    if (_.isValidMultipartFormDataRequest(contentTypeHeader)) {
        if (!_.isObject(context['formData']) || !_.isObject(context['formData']['fields'])) {
            return {};
        }
        return context['formData']['fields'];
    }

    if (_.isString(context['requestBody'])) {
        return {
            body: context['requestBody']
        };
    }

    return {};
}

function _headerKeysToLower(context) {
    if (!context || !context['requestHeaders']) {
        return {};
    }

    const headers = {};
    Object.keys(context['requestHeaders']).forEach((key) => {
        headers[key.toLowerCase()] = context['requestHeaders'][key];
    });

    return headers;
}

function _toOpenRASPContext(context) {
    // TODO: Add json data as well
    const server = {
        os: process.platform
    };
    return {
        header: _headerKeysToLower(context),
        parameter: _toRASPParameters(context),
        server: server,
        appBasePath: (context && context['appBasePath']) || '',
        get_all_parameter:
            (context && context['get_all_parameter']) || undefined,
        url: (context && context['url']) || '',
        json: _toRASPJson(context)
    };
}

// FIXME: Need to move this to backend. Agent should report confidence instead
function _getSeverity(result) {
    const confidence = result['confidence'] || 0;
    if (confidence <= 60) {
        return Severity.OPEN_RASP_SEVERITY_MINOR;
    }

    if (confidence <= 90) {
        return Severity.OPEN_RASP_SEVERITY_MAJOR;
    }

    return Severity.OPEN_RASP_SEVERITY_CRITICAL;
}


function _check(type, params, context, callStack) {
    const raspParams = params;
    raspParams['stack'] = callStack || [];
    const results = RASP.check(type, raspParams, _toOpenRASPContext(context));

    if (!_.isArray(results) || results.length === 0) {
        return null;
    }

    return {
        name: results[0].algorithm || '',
        message: results[0].message || '',
        severity: _getSeverity(results[0]),
        confidence: results[0] && results[0]['confidence']
    };
}

/* expects context of the form:
 *  {
 *      "headers": {<key value pair of headers>},
 *      "queryParams": {<key value pair of query parameters>},
 *  }
 */
function detectSQLi(query, callStack, context) {
    if (!query) {
        return null;
    }

    return _check('sql', { query: query }, context, callStack);
}


function detectLFI(
    type,
    source,
    dest,
    path,
    realpath,
    filename,
    callStack,
    url,
    context
) {
    return _check(
        type,
        {
            path: path || '',
            realpath: realpath || '',
            filename: filename || '',
            source: source || '',
            dest: dest || '',
            url: url || ''
        },
        context,
        callStack
    );
}

function detectShellShock(command, callStack, context) {
    if (!command) {
        return null;
    }

    return _check('command', { command: command }, context, callStack);
}

function detectSsrf(url, hostname, ip, origin_ip, origin_hostname, context) {
    return _check(
        'ssrf',
        {
            url: url || '',
            hostname: hostname || '',
            ip: ip || '',
            origin_ip: origin_ip || '',
            origin_hostname: origin_hostname || ''
        },
        context
    );
}

function detectXxe(entity, context) {
    if (!entity) {
        return null;
    }

    return _check('xxe', { entity: entity }, context);
}

function detectSsrfRedirect(
    hostname,
    ip,
    url,
    url2,
    hostname2,
    ip2,
    port2,
    context
) {
    return _check(
        'ssrfRedirect',
        {
            hostname: hostname || '',
            ip: ip || '',
            url: url || '',
            url2: url2 || '',
            hostname2: hostname2 || '',
            ip2: ip2 || '',
            port2: port2 || ''
        },
        context
    );
}

module.exports = {
    detectSQLi: detectSQLi,
    detectLFI: detectLFI,
    detectShellShock: detectShellShock,
    detectSsrf: detectSsrf,
    detectXxe: detectXxe,
    detectSsrfRedirect: detectSsrfRedirect
};
