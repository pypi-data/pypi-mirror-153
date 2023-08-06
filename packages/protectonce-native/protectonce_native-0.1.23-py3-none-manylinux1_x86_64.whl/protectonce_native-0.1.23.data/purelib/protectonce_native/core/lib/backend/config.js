const url = require('url');
const path = require('path');

const Constants = require('../utils/constants');
const Logger = require('../utils/logger');

class BackendConfig {
    constructor() {
        this._clientId = null;
        this._token = null;
        this._endpoint = null;
        this._port = null;
        this._protocol = null;
        this._setConfig();
        this._removeProtocol();
    }

    reload() {
        this._setConfig();
    }

    get clientId() {
        return this._clientId;
    }

    get token() {
        return this._token;
    }

    get endpoint() {
        return this._endpoint;
    }

    get port() {
        return this._port;
    }

    get protocol() {
        return this._protocol;
    }

    _setConfig() {
        try {
            const configFile = this._getConfigFilePath();
            const config = require(configFile);

            this._parseToken(config);
        } catch (e) {
            Logger.write(Logger.INFO && `Failed to read config file. Falling back to environment variables: ${e}`);
            this._clientId = process.env[Constants.BACKEND_REST_API_CLIENT_ID_ENV] || '';
            this._token = process.env[Constants.BACKEND_REST_API_TOKEN_ENV] || '';
            this._endpoint = process.env[Constants.BACKEND_REST_API_URL_ENV] || '';
            this._port = process.env[Constants.BACKEND_REST_API_PORT_ENV] || null;
        }
    }

    _parseToken(tokenJSON) {
        const token = tokenJSON[Constants.PROTECT_ONCE_CONFIG_TOKEN_BASE_KEY] || {};
        // FIXME: This is required to parse twice because of the structure of encoded base64 token string on UI
        const config = JSON.parse(JSON.parse(Buffer.from(token, 'base64').toString()));
        this._clientId = config[Constants.PROTECT_ONCE_CONFIG_CLIENT_ID_KEY];
        this._token = config[Constants.PROTECT_ONCE_CONFIG_TOKEN_KEY];
        this._endpoint = config[Constants.PROTECT_ONCE_CONFIG_ENDPOINT_KEY];
        this._port = config[Constants.PROTECT_ONCE_CONFIG_ENDPOINT_PORT_KEY] || null;
    }

    _getConfigFilePath() {
        if (process.env[Constants.PROTECT_ONCE_CONFIG_FILE_ENV]) {
            return process.env[Constants.PROTECT_ONCE_CONFIG_FILE_ENV];
        }

        return path.join(process.cwd(), 'protectOnce.json');
    }

    _removeProtocol() {
        let parsedUrl = url.parse(this._endpoint, false);
        if (parsedUrl.host) {
            this._endpoint = url.parse(this._endpoint, false).host;
        }
        this._protocol = parsedUrl.protocol;
    }
}

module.exports = new BackendConfig();
