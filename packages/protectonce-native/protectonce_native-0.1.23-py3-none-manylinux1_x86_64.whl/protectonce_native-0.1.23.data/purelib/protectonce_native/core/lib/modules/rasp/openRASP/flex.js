'use strict';

const Logger = require('../../../utils/logger');

let poNative = null;
try {
    poNative = require('@protectonce/native');
} catch (e) {
    Logger.write(Logger.INFO && `failed to load @protectonce/native with error: ${e}`);
}

global.tokenize = function (query, type) {
    if (!poNative) {
        return [];
    }

    const result = []
    const arr = poNative.flex_tokenize(query, type) || []
    for (let i = 0; i < arr.length; i += 2) {
        const start = arr[i]
        const stop = arr[i + 1]
        const text = query.substring(start, stop)
        result.push({ start, stop, text })
    }
    return result
}