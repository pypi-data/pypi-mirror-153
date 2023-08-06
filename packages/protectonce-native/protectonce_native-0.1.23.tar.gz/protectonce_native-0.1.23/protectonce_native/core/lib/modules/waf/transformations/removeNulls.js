const _ = require('lodash');

module.exports = function lowercaseBuilder() {
    const nullPattern=/\0/g;
    return function lowercase(data) {
        return _.isString(data) ? data.replace(nullPattern, '') : data;
    }
}
