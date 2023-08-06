const interface = require('./interface');
const _ = require('lodash');
const Logger = require('../utils/logger');

class MethodInvoker {
    constructor(mod, method, inData) {
        this._method = null;
        this._context = null;
        this._parseMethod(mod, method);

        this._inData = this._parseInData(inData);
    }

    invoke() {
        if (!this._method) {
            Logger.write(Logger.DEBUG && `MethodInvoker: Failed to invoke empty method`);
            return Promise.resolve();
        }

        return new Promise((resolve, reject) => {
            try {
                Logger.write(Logger.DEBUG && `MethodInvoker: Invoking method with data: ${JSON.stringify(this._inData)}`);
                const result = this._method.call(this._context, this._inData);
                if (_.isPromise(result)) {
                    result.then((response) => {
                        Logger.write(Logger.DEBUG && `MethodInvoker: Promise returning ${JSON.stringify(result)}`);
                        resolve(this._toResponse(response));
                    });
                    return;
                }

                Logger.write(Logger.DEBUG && `MethodInvoker: Returning ${JSON.stringify(result)}`);
                resolve(this._toResponse(result));
            } catch (e) {
                reject(e);
            }
        });
    }

    _toResponse(result) {
        const response = JSON.stringify(result || {});
        return { data: Buffer.from(response, 'utf-8'), type: 10, size: response.length };
    }

    _parseMethod(mod, method) {
        const parts = method.split('.');
        if (parts.length === 1) {
            this._setMethod(mod, method);
            return;
        }

        const methodName = parts.pop();
        let currentModule = mod;
        for (let part of parts) {
            currentModule = currentModule[part];
            if (!currentModule) {
                return;
            }
        }

        this._setMethod(currentModule, methodName);
    }

    _setMethod(mod, method) {
        if (this._isValidMethod(mod, method)) {
            this._context = mod;
            this._method = mod[method];
        }
    }

    _isValidMethod(mod, method) {
        return method in mod && typeof mod[method] === 'function';
    }

    _parseInData(inData) {
        if (!inData) {
            return null;
        }

        return JSON.parse(inData.data.toString());
    }
}

global.protectOnceInvokeInterface = function (method, inData, outData) {
    const rI = new MethodInvoker(interface, method, inData, outData);
    return rI.invoke();
}
