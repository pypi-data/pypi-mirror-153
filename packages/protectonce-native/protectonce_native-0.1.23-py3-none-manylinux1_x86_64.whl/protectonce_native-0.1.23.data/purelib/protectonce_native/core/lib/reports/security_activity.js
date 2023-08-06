const _ = require('lodash');
const REPORT_TTL_MS = 30 * 1000;
const Constants = require('../utils/constants');
const HashStore = require('./hash_store');

class SecurityActivity {
    constructor(
        id,
        status,
        ipAddress,
        response,
        verb,
        path,
        user,
        protocol,
        host,
        pathParams,
        queryParams,
        requestHeaders,
        responseHeaders,
        requestBodySchema,
        responseBodySchema
    ) {
        this._events = [];
        this._requestId = id;
        this._statusCode = status;
        this._ipAddresses = [ipAddress];
        this._securityResponse = response;
        this._date = new Date();
        this._requestVerb = verb;
        this._requestPath = path;
        this._user = user ? user : '';
        this._protocol = protocol;
        this._duration = 0;
        this._closed = false;
        this._host = host;
        this._pathParams = pathParams;
        this._queryParams = queryParams;
        this._requestHeaders = requestHeaders;
        this._responseHeaders = responseHeaders;
        this._requestBodySchema = requestBodySchema;
        this._responseBodySchema = responseBodySchema;
        this._poRequestId = ''
    }

    addEvent(event) {
        if (_.isObject(event)) {
            this._events.push(event);
        }
    }

    set events(events) {
        if (_.isArray(events)) {
            this._events = events;
        }
    }

    set user(user) {
        if (_.isObject(user)) {
            this._user = user;
        }
    }

    set duration(duration) {
        this._duration = duration;
    }

    set host(host) {
        if (_.isString(host)) {
            this._host = host;
        }
    }

    set pathParams(pathParams) {
        if (_.isObject(pathParams)) {
            this._pathParams = pathParams;
        }
    }

    set securityResponse(securityResponse) {
        if (securityResponse) {
            this._securityResponse = securityResponse;
        }
    }

    set queryParams(queryParams) {
        if (_.isObject(queryParams)) {
            this._queryParams = queryParams;
        }
    }

    set requestId(id) {
        if (id) {
            this._requestId = id;
        }
    }

    set ipAddresses(ipAddresses) {
        if (_.isArray(ipAddresses) && ipAddresses[0]) {
            this._ipAddresses = ipAddresses;
        }
    }

    set date(date) {
        if (_.isDate(date)) {
            this._date = date;
        }
    }

    set requestVerb(requestVerb) {
        if (_.isString(requestVerb)) {
            this._requestVerb = requestVerb;
        }
    }

    set requestPath(requestPath) {
        if (_.isString(requestPath)) {
            this._requestPath = requestPath.replace(
                Constants.PATH_TRIMMING_REGEX,
                ''
            );
        }
    }

    set responseBodySchema(responseBodySchema) {
        if (_.isObject(responseBodySchema)) {
            this._responseBodySchema = responseBodySchema;
        }
    }

    set requestBodySchema(requestBodySchema) {
        if (_.isObject(requestBodySchema)) {
            this._requestBodySchema = requestBodySchema;
        }
    }

    set statusCode(statusCode) {
        if (statusCode) {
            this._statusCode = statusCode;
        }
    }

    set requestHeaders(requestHeaders) {
        if (_.isObject(requestHeaders)) {
            this._requestHeaders = filterSupportedHttpHeaders(requestHeaders);
        }
    }

    set responseHeaders(responseHeaders) {
        if (_.isObject(responseHeaders)) {
            this._responseHeaders = filterSupportedHttpHeaders(responseHeaders);
        }
    }
    set protocol(protocol) {
        if (_.isString(protocol)) {
            this._protocol = protocol;
        }
    }

    set closed(closed) {
        this._closed = closed;
    }

    set poRequestId(poRequestId) {
        this._poRequestId = poRequestId;
    }

    get requestId() {
        return this._requestId;
    }

    get user() {
        return this._user;
    }

    get duration() {
        return this._duration;
    }

    get host() {
        return this._host;
    }

    get pathParams() {
        return this._pathParams;
    }

    get securityResponse() {
        return this._securityResponse;
    }

    get queryParams() {
        return this._queryParams;
    }

    get ipAddresses() {
        return this._ipAddresses;
    }

    get date() {
        return this._date;
    }

    get requestVerb() {
        return this._requestVerb;
    }

    get requestPath() {
        return this._requestPath;
    }

    get responseBodySchema() {

        return this._responseBodySchema;
    }

    get requestBodySchema() {
        return this._requestBodySchema;
    }

    get statusCode() {
        return this._statusCode;
    }

    get requestHeaders() {
        return this._requestHeaders;
    }

    get responseHeaders() {
        return this._responseHeaders;
    }

    get protocol() {
        return this._protocol;
    }

    get closed() {
        return this._closed;
    }

    get events() {
        return this._events;
    }

    get poRequestId() {
        return this._poRequestId;
    }

    setClosed() {
        this.closed = true;
    }

    isClosed() {
        this._checkTTL();
        return this.closed;
    }

    _checkTTL() {
        const now = new Date();
        if (now - this._date >= REPORT_TTL_MS) {
            this.setClosed();
        }
    }

    getJson() {
        const securityActivity = {
            events: this.events,
            requestId: this.requestId,
            ipAddresses: this.ipAddresses,
            securityResponse: this.securityResponse,
            statusCode: this.statusCode,
            date: this.date,
            requestVerb: this.requestVerb,
            requestPath: this.requestPath,
            user: this.user,
            protocol: this.protocol,
            duration: this.duration,
            closed: this.closed,
            host: this.host,
            requestHeaders: this.requestHeaders,
            responseHeaders: this.responseHeaders,
            poRequestId: this._poRequestId
        };
        if(!HashStore.checkHash(this)) {
            securityActivity['pathParams'] = this.pathParams;
            securityActivity['queryParams'] = this.queryParams;
            securityActivity['requestBodySchema'] = this.requestBodySchema;
            securityActivity['responseBodySchema'] = this.responseBodySchema;
            securityActivity['hasApiData'] = true;
        }

        return securityActivity;
    }
}

function filterSupportedHttpHeaders(headers) {
    const SUPPORTED_HTTP_HEADERS = [
        'accept',
        'access-control-allow-origin',
        'content-length',
        'content-type',
        'from',
        'host',
        'origin',
        'referer',
        'server'
    ];
    const filteredHeaders = {};
    for (const [key, value] of Object.entries(headers)) {
        if (SUPPORTED_HTTP_HEADERS.includes(key.toLowerCase())) {
            filteredHeaders[key] = value;
        }
    }

    return filteredHeaders;
}

module.exports = {
    SecurityActivity
};
