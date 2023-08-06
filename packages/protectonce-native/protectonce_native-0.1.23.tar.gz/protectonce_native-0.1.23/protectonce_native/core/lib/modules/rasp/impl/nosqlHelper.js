
const _ = require('lodash');
const Logger = require('../../../utils/logger');
const qs = require('qs');

function _toParameters(context) {
  if (!context || (!context['queryParams'] && !context['pathParams'])) {
    return {};
  }

  const parameters = { ...context['pathParams'], ...context['queryParams'] };

  Object.keys(parameters).forEach((key) => {
    if (_.isString(parameters[key])) {
      // open rasp expects each parameter to be an array of strings
      parameters[key] = [parameters[key]];
    }
  });
  return parameters;
}

function _toJson(context) {
  if (!context) {
    return {};
  }

  const contentTypeHeader = context && context['requestHeaders'] && _.getObjectKeysToLower(context['requestHeaders'], 'content-type');
  if (_.isValidJsonRequest(contentTypeHeader)) {
    if (!_.isString(context['requestBody'])) {
      return {};
    }

    const parsedBody = _.parseIfJson(context['requestBody']);;

    if (!parsedBody) {
      return {};
    }

    return parsedBody;
  }

  if (_.isValidEncodedFormDataRequest(contentTypeHeader)) {
    if (!_.isString(context['requestBody'])) {
      return {};
    }

    return qs.parse(context['requestBody']);
  }

  if (_.isValidMultipartFormDataRequest(contentTypeHeader)) {
    if (!_.isObject(context['formData']) || !_.isObject(context['formData']['fields'])) {
      return {};
    }
    return context['formData']['fields'];
  }

  if (_.isString(context['requestBody'])) {
    return {
      body: context['requestBody']
    };
  }

  return {};
}

function _headerKeysToLower(context) {
  if (!context || !context['requestHeaders']) {
    return {};
  }

  const headers = {};
  Object.keys(context['requestHeaders']).forEach((key) => {
    headers[key.toLowerCase()] = context['requestHeaders'][key];
  });

  return headers;
}

function toContext(context) {
  try {
    const server = {
      os: process.platform
    };
    return {
      header: _headerKeysToLower(context),
      parameter: _toParameters(context),
      url: (context && context['url']) || '',
      json: _toJson(context)
    };
  } catch (e) {
    Logger.write(Logger.ERROR && `toContext: error : ${e}`);
  }
  return {};
}


module.exports = {
  toContext: toContext
}