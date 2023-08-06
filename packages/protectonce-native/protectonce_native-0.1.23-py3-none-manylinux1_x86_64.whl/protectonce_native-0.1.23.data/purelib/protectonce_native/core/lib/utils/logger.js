const _ = require('lodash');

const LogLevel = {
    'PO_LOG_LEVEL_QUIET': 0,
    'PO_LOG_LEVEL_ERROR': 1,
    'PO_LOG_LEVEL_INFO': 2,
    'PO_LOG_LEVEL_VERBOSE': 3
}

class Logger {
    constructor() {
        let logLevel = process.env.PROTECTONCE_LOG_LEVEL || 'error';
        this._setLogLevel(logLevel);
    }

    write(message) {
        if (!this._tag) {
            return;
        }

        console.log(`[${this._tag}] ${message}`);
        this._tag = null;
    }

    get ERROR() {
        return this._shouldPrint(LogLevel.PO_LOG_LEVEL_ERROR, 'PO_CORE_ERROR');
    }

    get INFO() {
        return this._shouldPrint(LogLevel.PO_LOG_LEVEL_INFO, 'PO_CORE_INFO');
    }

    get DEBUG() {
        return this._shouldPrint(LogLevel.PO_LOG_LEVEL_VERBOSE, 'PO_CORE_DEBUG');
    }

    _shouldPrint(logLevel, tag) {
        if (this._logLevel < logLevel) {
            this._tag = null;
            return false;
        }

        this._tag = tag;
        return true;
    }

    _setLogLevel(logLevel) {
        this._logLevel = LogLevel.PO_LOG_LEVEL_ERROR;
        if (!_.isString(logLevel)) {
            return;
        }

        const lowerLogLevel = logLevel.toLowerCase();
        if (lowerLogLevel === 'quiet') {
            this._logLevel = LogLevel.PO_LOG_LEVEL_QUIET;
            return;
        }

        if (lowerLogLevel === 'error') {
            this._logLevel = LogLevel.PO_LOG_LEVEL_ERROR;
            return;
        }

        if (lowerLogLevel === 'info') {
            this._logLevel = LogLevel.PO_LOG_LEVEL_INFO;
            return;
        }

        if (lowerLogLevel === 'verbose') {
            this._logLevel = LogLevel.PO_LOG_LEVEL_VERBOSE;
            return;
        }
    }
}

module.exports = new Logger();
