const BaseMatcher = require('./base_matcher');
const logger = require('../../../utils/logger');
const Constants = require('../../../utils/constants');

class EqualsMatcher extends BaseMatcher {
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
      case Constants.USER_IP_FILTER_KEY:
        return item;
      default:
        logger.write(logger.ERROR && `Received invalid type : ${type}.`);
        return undefined;
    }
  }

  match(stringToMatch) {
    if (this._stringToMatchWith) {
      return stringToMatch === this._stringToMatchWith;
    }
    return false;
  }
}

module.exports = EqualsMatcher;