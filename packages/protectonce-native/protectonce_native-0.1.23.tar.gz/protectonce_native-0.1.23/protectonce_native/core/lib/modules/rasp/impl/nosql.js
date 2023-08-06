const _ = require('lodash');
const Logger = require('../../../utils/logger');
const headerInjection = ["user-agent", "referer", "x-forwarded-for"]
const nosqlHelper = require("./nosqlHelper");

function getObject(key, value) {
  const obj = {
    [key]: value
  }
  return JSON.stringify(obj, function (k, v) { return v === undefined ? "undefined" : v });
}

function getTokens(object, tokens) {

  if (_.isEmpty(object)) {
    return tokens;
  }

  for (let [key, value] of Object.entries(object)) {
    if (_.isString(value)) {
      const parsed = _.parseIfJson(value);
      if (parsed) {
        value = parsed;
      }
    }
    if (_.isArray(value)) {
      for (let elem of value) {
        if (_.isObject(elem)) {
          tokens.push(getTokens(elem, tokens));
        }
      }
      tokens.push(getObject(key, value));
    }
    else if (_.isObject(value)) {
      getTokens(value, tokens);
    } else {
      tokens.push(getObject(key, value));
    };
  }
}

function getMatchingTokens(queryObj, requestObj) {
  let result = [];
  for (const queryObjectEntry of queryObj) {
    const found = requestObj.find((requestObjectEntry) => requestObjectEntry === queryObjectEntry);
    if (found) {
      result.push(found);
    }
  }
  return result;
}


function parseBody(query, json) {
  try {
    const queryObj = JSON.parse(query);
    let queryObjectTokens = [];
    getTokens(queryObj, queryObjectTokens);
    let requestObjectTokens = [];
    getTokens(json, requestObjectTokens);
    return getMatchingTokens(queryObjectTokens, requestObjectTokens);
  } catch (e) {
    Logger.write(Logger.DEBUG && `NoSqli:parseBody: failed with error: ${e}`);
  }
  return [];
}

function parseQueryParametersAndHeaders(query, context) {
  let result = [];
  try {
    let parameters = context.parameter || {};
    let queryParamsResult = parseQueryParameters(parameters, query);
    if (_.isArray(queryParamsResult) && queryParamsResult.length > 0) {
      result = result.concat(queryParamsResult);
    }
    let requestHeaderResult = parseRequestHeaders(context.header, query);
    if (_.isArray(requestHeaderResult) && requestHeaderResult.length > 0) {
      result = result.concat(requestHeaderResult);
    }
  } catch (e) {
    Logger.write(Logger.DEBUG && `NoSqli:parseQueryParametersAndHeaders: failed with error: ${e}`);
  }
  return result;
}

function check(query, context) {
  context = nosqlHelper.toContext(context);
  let parsedValues = [];
  try {
    if (!_.isEmpty(context.json)) {
      let parsedBodyResult = parseBody(query, context.json);
      if (_.isArray(parsedBodyResult) && parsedBodyResult.length > 0) {
        parsedValues = parsedValues.concat(parsedBodyResult);
      }
    }
    let parsedQueryParamsResult = parseQueryParametersAndHeaders(query, context);
    if (_.isArray(parsedQueryParamsResult) && parsedQueryParamsResult.length > 0) {
      parsedValues = parsedValues.concat(parsedQueryParamsResult);
    }
  } catch (e) {
    Logger.write(Logger.DEBUG && `NoSqli:check: failed with error: ${e}`);
  }
  return parsedValues;
}

function parseRequestHeaders(headers, query) {

  let result = [];
  Object.keys(headers).forEach(function (name) {
    if (name.toLowerCase() == "cookie") {
      var cookies = getCookies(headers.cookie)
      for (name in cookies) {
        result = result.concat(isQueryContainsInput([cookies[name]], query));
      }
    }
    else if (headerInjection.indexOf(name.toLowerCase()) != -1) {
      result = result.concat(isQueryContainsInput([headers[name]], query));
    }
  })
  return result;
}

function getCookies(cookieStr) {
  let cookieItems = cookieStr.split(';')
  let result = {}
  for (let i = 0; i < cookieItems.length; i++) {
    let item = cookieItems[i].trim()
    if (item.length == 0) {
      continue
    }
    let keyLen = item.indexOf("=")
    if (keyLen <= 0) {
      continue
    }
    let key = unescape(item.substr(0, keyLen))
    let value = unescape(item.substr(keyLen + 1))
    result[key] = value

  }
  return result
}

function parseQueryParameters(parameters, query) {
  let results = [];
  Object.keys(parameters).forEach(function (name) {
    var valueList = []
    Object.values(parameters[name]).forEach(function (value) {
      if (typeof value == 'string') {
        valueList.push(value)
      } else {
        valueList = valueList.concat(Object.values(value))
      }
    })
    results = results.concat(isQueryContainsInput(valueList, query));
  })
  return results;
}

function isQueryContainsInput(values, query) {
  let result = [];
  values.forEach(function (value) {
    if (query.includes(value)) {
      result.push(value);
    }
  });
  return result;
}


module.exports = {
  check: check
}



