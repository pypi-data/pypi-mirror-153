const _ = require('lodash');

module.exports = function lowercaseBuilder() {
    return function lowercase(data) {
        return _.isString(data) ? data.toLowerCase() : data;
    }
}
