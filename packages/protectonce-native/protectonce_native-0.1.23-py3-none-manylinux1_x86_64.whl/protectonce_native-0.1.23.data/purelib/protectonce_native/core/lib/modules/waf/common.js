"use strict";
const Logger = require('../../utils/logger');

module.exports.cbOnce = function (cb, doOnce) {
    let done = false;
    return function () {
        if (!done) {
            done = true;
            doOnce();
        }
        if (cb) return cb.apply(this, arguments);
    }
}

module.exports.cbEach = function (cb, doEach) {
    return function () {
        doEach();
        if (cb) return cb.apply(this, arguments);
    }
}

module.exports.hashStr = hashStr5;
module.exports.combineHash = combineHash;

let murmurhash = null;
try {
    if (typeof TextEncoder === 'undefined') {
        // This is a workaround for murmurhash to work on node 10
        global.TextEncoder = require("util").TextEncoder;
    }
    murmurhash = require("murmurhash").v3;
} catch (e) {
    Logger.write(Logger.INFO && `failed to load murmurhash-native with error: ${e}`);
    murmurhash = () => { return ''; }
}

class StrHash {
    constructor(strOrBuffer) {
        if (!strOrBuffer) strOrBuffer = "";
        this._hash = murmurhash(strOrBuffer, "buffer");
    }

    valueOf() {
        return this._hash;
    }

    combine(otherHash) {
        for (let i = 0, len = this._hash.length; i < len; i++) {
            this._hash.writeUInt8(this._hash.readUInt8(i) ^ otherHash._hash.readUInt8(i), i);
        }
    }
}
module.exports.StrHash = StrHash;

function hashStr5(s) {
    return murmurhash(s);
}

function combineHash(h1, h2) {

}

function hashStr1(...strs) {
    let hash = 5381;
    for (let s of strs) {
        let i = s.length;
        while (i) {
            hash = (hash * 33) ^ s.charCodeAt(--i);
        }
    }

    /* JavaScript does bitwise operations (like XOR, above) on 32-bit signed
    * integers. Since we want the results to be always positive, convert the
    * signed int to an unsigned by doing an unsigned bitshift. */
    return hash >>> 0;
}

const HASH_SIZE = 64; //bits
const _HASH_MOD = 2n ** BigInt(HASH_SIZE);
function hashStr2(...strs) {
    let hash = BigInt(5381);
    for (let s of strs) {
        let i = s.length;
        while (i) {
            hash = (hash * 33n) ^ BigInt(s.charCodeAt(--i));
        }
    }

    /* JavaScript does bitwise operations (like XOR, above) on 32-bit signed
    * integers. Since we want the results to be always positive, convert the
    * signed int to an unsigned by doing an unsigned bitshift. */
    // return hash >>> 0;
    return (hash % _HASH_MOD).toString();
}

function hashStr3(...strs) {
    return strs.join(":")
}

function hashStr4(...strs) {
    let hash = 5381;
    for (let s of strs) {
        let i = s.length;
        while (i) {
            hash = (hash * 33) + s.charCodeAt(--i);
        }
    }

    /* JavaScript does bitwise operations (like XOR, above) on 32-bit signed
    * integers. Since we want the results to be always positive, convert the
    * signed int to an unsigned by doing an unsigned bitshift. */
    return hash;
}
