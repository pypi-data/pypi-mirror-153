const https = require('https');
const Constants = require('../utils/constants');
const BackendConfig = require('./config');
const Token = require('./token');
const Logger = require('../utils/logger');
const _ = require('lodash');

class RestAPI {
    constructor(path, data) {
        this._path = path;
        try {
            this._data = JSON.stringify(data);
        } catch (e) {
            this._data = '';
        }
    }

    get url() {
        return BackendConfig.endpoint;
    }

    get port() {
        return BackendConfig.port;
    }

    get protocol() {
        return BackendConfig.protocol;
    }

    get postOptions() {
        const postOpts = {
            hostname: this.url,
            path: this._path,
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': this._data.length,
                'Authorization': Token.authHeader
            }
        };

        if (this.port) {
            postOpts['port'] = this.port;
        }

        if (Token.refreshToken) {
            postOpts.headers[Constants.BACKEND_REST_API_REFRESH_TOKEN_HEADER] = Token.refreshToken
        }

        return postOpts;
    }

    post() {
        return new Promise((resolve, reject) => {
            Logger.write(Logger.DEBUG && `REST API: Sending request to: ${this.url}`);
            const that = this;
            const req = https.request(this.postOptions, res => {
                Logger.write(Logger.DEBUG && `REST API: url: ${that.url} returned status: ${res.statusCode}`);
                if (res.statusCode === Constants.APP_DELETE_STATUS_CODE) {
                    resolve({ 'data': '{}', 'statusCode': res.statusCode });
                    return;
                }

                let data = '';
                res.on('data', d => {
                    data += d.toString();
                })

                res.on('end', () => {
                    const responseObj = JSON.parse(data);
                    const authDetails = responseObj['authDetails'];
                    if (authDetails) {
                        Token.update(authDetails);
                    }
                    resolve({ 'data': JSON.stringify(responseObj), 'statusCode': res.statusCode });
                });
            })

            req.on('error', error => {
                // Error should be printed by caller to avoid duplicate prints
                reject(error);
            })

            req.write(this._data)
            req.end()
        });
    }

    getProtocol() {
        return (this.protocol ? this.protocol + '//' : 'https://');
    }

    getPort() {
        return (this.port ? ':' + this.port : '');
    }

    buildRequestUrl() {
        const requestUrl = this.getProtocol() + this.url + this.getPort() + this._path;
        return requestUrl;
    }

    getRequestHeaders() {
        const headers = {
            'Content-Type': 'application/json',
            'Content-Length': this._data.length,
            'Authorization': Token.authHeader
        }
        if (Token.refreshToken) {
            headers[Constants.BACKEND_REST_API_REFRESH_TOKEN_HEADER] = Token.refreshToken
        }
        return headers;
    }

    postSync() {
        const syncRequest = require('sync-request');
        Logger.write(Logger.DEBUG && `REST API postSync: Sending request to: ${this.url}`);
        if (!this.url) {
            return { 'data': '{}', 'statusCode': 200 };
        }
        const requestUrl = this.buildRequestUrl();
        Logger.write(Logger.DEBUG && `REST API postSync: RequestUrl: ${requestUrl}`);
        let response = syncRequest('POST', requestUrl, {
            headers: this.getRequestHeaders(),
            json: JSON.parse(this._data),
            timeout: 10000
        });
        if (_.isObject(response) && response.statusCode !== 200) {
            return { 'data': '{}', 'statusCode': response.statusCode };
        }
        const responseObj = JSON.parse(response.getBody());
        const authDetails = responseObj['authDetails'];
        if (authDetails) {
            Token.update(authDetails);
        }
        const rulesData = { 'data': JSON.stringify(responseObj), 'statusCode': response.statusCode };
        return rulesData;
    }

}

module.exports = RestAPI;
