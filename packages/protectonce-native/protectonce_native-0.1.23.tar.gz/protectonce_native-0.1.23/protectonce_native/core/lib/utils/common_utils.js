const _ = require('lodash');
const uuid = require('uuid');

function toBoolean(value) {
  if (!value) {
    return false;
  }
  if (typeof value == 'number' || typeof value == 'boolean') {
    return !!value;
  }
  return _.replace(_.trim(value.toLowerCase()), /[""'']/ig, '') === 'true' ? true : false;
}

function parseIfJson(str) {
  try {
    return JSON.parse(str);
  } catch (e) {
    return false;
  }
}

function isAWSLambdaEnv() {
  return process.env.AWS_EXECUTION_ENV && process.env.AWS_EXECUTION_ENV.startsWith('AWS_Lambda_');
}

function isValidJsonRequest(headerToCheck) {
  return _.isString(headerToCheck) && headerToCheck.toLowerCase().includes('json');
}

function isValidEncodedFormDataRequest(headerToCheck) {
  return _.isString(headerToCheck) && headerToCheck.toLowerCase().includes('application/x-www-form-urlencoded');
}

function isValidMultipartFormDataRequest(headerToCheck) {
  return _.isString(headerToCheck) && headerToCheck.toLowerCase().includes('multipart/form-data');
}

function isPromise(promise) {
  return !!promise && typeof promise.then === 'function'
}

function getObjectKeysToLower(object, keyToGet) {
  return object && object[Object.keys(object).find(key => key.toLowerCase() === keyToGet.toLowerCase())];
}

function getUuid() {
  return uuid.v4();
}

_.mixin({
  'toBoolean': toBoolean,
  'isPromise': isPromise,
  'parseIfJson': parseIfJson,
  'isValidJsonRequest': isValidJsonRequest,
  'isValidEncodedFormDataRequest': isValidEncodedFormDataRequest,
  'isValidMultipartFormDataRequest': isValidMultipartFormDataRequest,
  'getObjectKeysToLower': getObjectKeysToLower,
  'getUuid': getUuid,
  'isAWSLambdaEnv': isAWSLambdaEnv
});
