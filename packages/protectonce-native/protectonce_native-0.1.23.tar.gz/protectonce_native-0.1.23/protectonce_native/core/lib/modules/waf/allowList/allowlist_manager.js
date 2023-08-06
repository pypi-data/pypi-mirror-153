const _ = require('lodash');
const AllowlistOperations = require('./allowlist_operations');

class AllowlistManager {
    constructor(allowList) {
        this.allowIP = [];
        this.allowParameter = [];
        this.allowPaths = [];
        this._setAllowList(allowList);
        this.allowlistOperations = new AllowlistOperations(this.allowIP, this.allowPaths, this.allowParameter);
    }
    _setAllowList(allowList) {
        if (!_.isObject(allowList)) { return; }
        allowList = allowList.allowList || {};
        if (_.isArray(allowList.ipAddressWithDetails)) {
            this.allowIP = allowList.ipAddressWithDetails;
        }
        if (_.isArray(allowList.parameter)) {
            this.allowParameter = allowList.parameter;
        }
        if (_.isArray(allowList.path)) {
            this.allowPaths = allowList.path;
        }
    }

    shouldBypassRequest(request) {
        if (this._checkIpAllowList(request.sourceIP)) {
            return true;
        }
        return this._checkPathAllowList(request.path);
    }

    filterParameters(request) {
        return this.allowlistOperations.filterParameters(request);
    }

    _checkIpAllowList(sourceIP) {
        return this.allowlistOperations.checkIpAllowList(sourceIP);
    }

    _checkPathAllowList(path) {
        return this.allowlistOperations.checkPathAllowList(path);
    }
}
module.exports = AllowlistManager;