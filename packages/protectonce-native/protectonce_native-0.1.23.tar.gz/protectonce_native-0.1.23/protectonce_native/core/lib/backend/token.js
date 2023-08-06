const BackendConfig = require('./config');

class APIToken {
    constructor() {
        this._accessToken = null;
        this._refreshToken = null;
    }

    update(auth) {
        this._accessToken = auth.accessToken;
        this._refreshToken = auth.refreshToken;
    }

    get authHeader() {
        if (this._accessToken == null) {
            return this._getBasicAuthHeader();
        }

        return this._getBearerToken();
    }

    get refreshToken() {
        return this._refreshToken;
    }

    _getBasicAuthHeader() {
        return `Basic ${Buffer.from(`${BackendConfig.clientId}:${BackendConfig.token}`).toString('base64')}`
    }

    _getBearerToken() {
        return `Bearer ${this._accessToken}`;
    }
}

module.exports = new APIToken();
