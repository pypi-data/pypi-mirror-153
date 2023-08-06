const CryptoJS = require("crypto-js");
const _ = require("lodash");
const Logger = require('../utils/logger');
const LRU = require('lru-cache');

class HashStore {
  constructor() {
    const options = {
      max: 1024
    };
    this.hashCache = new LRU(options);
  }

  checkHash(securityActivity) {
    try {
      if (!_.isObject(securityActivity) || !_.isString(securityActivity.requestPath) || !_.isString(securityActivity.requestVerb)) {
        return false;
      }
      const newHash = this._getHashForSecurityActivity(securityActivity);
      if (!newHash) {
        return false;
      }
      if (this.hashCache.has(newHash)) {
        return true;
      }
      this.hashCache.set(newHash, null);
    } catch (error) {
      Logger.write(
        Logger.ERROR && `checkHash: Failed to check hash: ${error}`
      );
    }
    return false;
  }

  _getHashForSecurityActivity(securityActivity) {
    try {
      const objectForHash = {
        requestPath: securityActivity.requestPath,
        requestVerb: securityActivity.requestVerb
      };

      this._addIfObject(objectForHash, 'pathParams', securityActivity.pathParams);
      this._addIfObject(objectForHash, 'queryParams', securityActivity.queryParams);
      this._addIfObject(objectForHash, 'requestBody', securityActivity.requestBodySchema);
      this._addIfObject(objectForHash, 'responseBody', securityActivity.responseBodySchema);

      return this._getHash(JSON.stringify(objectForHash));
    } catch (error) {
      Logger.write(
        Logger.ERROR && `_getHashForSecurityActivity: Failed to get hash for security activity: ${error}`
      );
    }
    return null;
  }

  _addIfObject(objectForHash, key, value) {
    if (_.isObject(value)) {
      objectForHash[key] = value;
    }
  }

  _getHash(stringForHash) {
    try {
      return CryptoJS.SHA256(stringForHash).toString();
    } catch (error) {
      Logger.write(
        Logger.ERROR && `_getHash: Failed to get hash: ${error}`
      );
    }
    return null;
  }
}

module.exports = new HashStore();