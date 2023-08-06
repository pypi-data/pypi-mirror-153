const {getMatcherByOperator} = require('./get_matcher');
const Constants = require('../../../utils/constants');

class AllowlistOperations {
  constructor(allowIPs, allowPaths, allowParameters) {
    this._ipMatchers = allowIPs.map((allowItem) => getMatcherByOperator(allowItem.ipAddress, allowItem.operator, Constants.IP_FILTER_KEY));
    this._pathMatchers = allowPaths.map((allowItem) => getMatcherByOperator(allowItem.path, allowItem.operator, Constants.PATH_FILTER_KEY));
    this._parameterMatchers = allowParameters.map((allowItem) => getMatcherByOperator(allowItem.parameter, allowItem.operator, Constants.PARAMETER_FILTER_KEY));
  }
  
  checkIpAllowList(itemToCompare) {
    for (const matcher of this._ipMatchers) {
      if (itemToCompare && matcher.match(itemToCompare)) {
        return true;
      }
    }
    return false;
  }

  checkPathAllowList(itemToCompare) {
    for (const matcher of this._pathMatchers) {
      if (itemToCompare && matcher.match(itemToCompare)) {
        return true;
      }
    }
    return false;
  }

  _checkParameterAllowList(itemToCompare) {
    for (const matcher of this._parameterMatchers) {
      if (itemToCompare && matcher.match(itemToCompare)) {
        return true;
      }
    }
    return false;
  }

  filterParameters(request) {
    for (const key of Object.keys(request.queryParams)) {
      const isParamToBeFiltered = this._checkParameterAllowList(key);
      if (isParamToBeFiltered) {
        request.queryParams.pathParams[0] =
          request.queryParams.pathParams[0].replace(
            `${key}=${request.queryParams[key]}`,
            ''
          );
        delete request.queryParams[key];
      }
    }
    return request.queryParams;
  }
}

module.exports = AllowlistOperations;
