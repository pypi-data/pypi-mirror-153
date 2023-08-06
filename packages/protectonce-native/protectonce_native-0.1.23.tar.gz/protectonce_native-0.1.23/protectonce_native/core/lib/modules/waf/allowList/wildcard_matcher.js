const BaseMatcher = require('./base_matcher');
const logger = require('../../../utils/logger');
const Constants = require('../../../utils/constants');

class WildcardMatcher extends BaseMatcher {
  constructor(item, type) {
    super();
    this._regEx = this._getRegEx(item, type);
  }

  _getRegEx(item, type) {
    switch (type) {
      case Constants.IP_FILTER_KEY:
        return new RegExp(
          `${item
            .replace(/\*/gm, '\\d{1,3}')
            .replace(/\./gm, '\\.')}`
        );
      case Constants.PATH_FILTER_KEY:
      case Constants.PARAMETER_FILTER_KEY:
      case Constants.USER_FILTER_KEY:
        return new RegExp(`${item.replace(/\*/gm, '[\\S]+')}`);
      default:
        logger.write(logger.ERROR && `Received invalid type : ${type}.`);
        return undefined;
    }
  }

  match(itemToMatch) {
    if (this._regEx) {
      return itemToMatch.match(this._regEx);
    }
    return false;
  }
}

module.exports = WildcardMatcher;