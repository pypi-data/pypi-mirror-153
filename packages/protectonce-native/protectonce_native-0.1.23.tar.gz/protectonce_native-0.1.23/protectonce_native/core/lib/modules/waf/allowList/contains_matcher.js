const BaseMatcher = require('./base_matcher');
const logger = require('../../../utils/logger');
const Constants = require('../../../utils/constants');

class ContainsMatcher extends BaseMatcher {
  constructor(item, type) {
    super();
    this._stringToMatchWith = this._getAttributeValueByType(item, type);
  }

  _getAttributeValueByType(item, type) {
    switch (type) {
      case Constants.IP_FILTER_KEY:
      case Constants.PATH_FILTER_KEY:
      case Constants.PARAMETER_FILTER_KEY:
      case Constants.USER_FILTER_KEY:
      case USER_IP_FILTER_KEY:
        return item;
      default:
        logger.write(logger.ERROR && `Received invalid type : ${type}.`);
        return undefined;
    }
  }

  match(stringToMatch) {
    if (this._stringToMatchWith) {
      return stringToMatch.includes(this._stringToMatchWith);
    }
    return false;
  }
}

module.exports = ContainsMatcher;