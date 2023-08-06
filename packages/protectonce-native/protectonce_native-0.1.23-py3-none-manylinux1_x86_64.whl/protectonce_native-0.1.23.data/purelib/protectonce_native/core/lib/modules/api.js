require('../utils/common_utils');
const _ = require('lodash');
const Constants = require('../utils/constants');
const qs = require('qs');
const { Route, Api, Inventory } = require('../reports/inventory');
const { SecurityActivity } = require('../reports/security_activity');
const HeartbeatCache = require('../reports/heartbeat_cache');
const Logger = require('../utils/logger');
const toJsonSchema = require('to-json-schema');


function storeRoute(inputData) {
    try {
        const routes = inputData.data;
        if (!_.isArray(routes)) {
            return;
        }

        let inventory = HeartbeatCache.getInventory();
        routes.forEach((route) => {
            route.paths.forEach((path) => {
                if (!_.isString(path) || !(_.isArray(route.methods) || _.isString(route.methods)) || !_.isString(route.host)) {
                    return;
                }
                const trimmedPath = path.replace(
                    Constants.PATH_TRIMMING_REGEX,
                    ''
                );

                const routeToBeAdded = new Route(
                    trimmedPath,
                    getMethodsForRoute(route.methods),
                    route.host
                );
                inventory = populateInventory(inventory, routeToBeAdded);
            });
        });

        HeartbeatCache.cacheInventory(inventory);
    } catch (error) {
        Logger.write(
            Logger.ERROR && `api.StoreRoute: Failed to store route: ${error}`
        );
    }
}

function getMethodsForRoute(routeMethods) {
    if (_.isString(routeMethods) && routeMethods === '*') {
        return supportedHttpMethods();
    }

    if (_.isArray(routeMethods)) {
        return routeMethods.filter((method) =>
            supportedHttpMethods().includes(method)
        );
    }

    return [];
}

function populateInventory(inventory, routeToBeAdded) {
    if (inventory && inventory.api && _.isArray(inventory.api.routes)) {
        addRouteToExistingInventory(inventory, routeToBeAdded);
        return inventory;
    }
    return new Inventory(new Api([routeToBeAdded]));
}

function addRouteToExistingInventory(inventory, routeToBeAdded) {
    const existingRoute = inventory.api.routes.find(
        (route) => route.path === routeToBeAdded.path
    );
    if (existingRoute) {
        existingRoute.addMethods(routeToBeAdded.methods);
        return;
    }
    inventory.api.addRoute(routeToBeAdded);
}

function parseHttpData(data) {
    try {
        const inputData = data.data;
        let securityActivity = HeartbeatCache.getReport(inputData.poSessionId);
        securityActivity = mapSecurityActivity(securityActivity, inputData);
        HeartbeatCache.cacheReport(securityActivity);
        return inputData;
    } catch (error) {
        Logger.write(
            Logger.ERROR &&
            `api.parseHttpData: Failed to parse http data: ${error}`
        );
        return {};
    }
}

function mapSecurityActivity(securityActivity, inputData) {
    if (!securityActivity) {
        securityActivity = new SecurityActivity();
        securityActivity.date = new Date();
        securityActivity.duration = 0;
        securityActivity.closed = false;
        securityActivity.requestId = inputData.poSessionId;
        if (inputData.poRequestId && inputData.poRequestId.includes(Constants.WORKLOAD_ID_SEPARATOR)) {
            securityActivity.poRequestId = inputData.poRequestId;
        }
    }
    securityActivity.url = inputData.url;
    securityActivity.requestVerb = inputData.method;
    securityActivity.requestPath = inputData.requestPath;
    securityActivity.user = inputData.user;
    securityActivity.protocol = inputData.protocol;
    if (_.isObject(inputData.queryParams)) {
        securityActivity.queryParams = toJsonSchema(inputData.queryParams);
    }

    securityActivity.host = inputData.host;
    if (_.isObject(inputData.pathParams)) {
        securityActivity.pathParams = toJsonSchema(inputData.pathParams);
    }
    securityActivity.ipAddresses = [inputData.sourceIP];
    securityActivity.requestHeaders = inputData.requestHeaders;
    securityActivity.responseHeaders = inputData.responseHeaders;
    const requestHeaders = inputData.requestHeaders
        ? inputData.requestHeaders
        : securityActivity.requestHeaders
            ? securityActivity.requestHeaders
            : {};

    const responseHeaders = inputData.responseHeaders
        ? inputData.responseHeaders
        : securityActivity.responseHeaders
            ? securityActivity.responseHeaders
            : {};

    securityActivity.requestBodySchema = getJsonSchema(
        inputData,
        inputData.requestBody,
        requestHeaders && _.getObjectKeysToLower(requestHeaders, 'content-type')
    );
    securityActivity.responseBodySchema = getJsonSchema(
        inputData,
        inputData.responseBody,
        responseHeaders && _.getObjectKeysToLower(responseHeaders, 'content-type')
    );

    securityActivity.statusCode = inputData.statusCode;

    return securityActivity;
}

function getJsonSchema(inputData, body, headerToCheck) {
    if (!_.isString(body) && !_.isObject(inputData.formData)) {
        return;
    }
    if (_.isString(body)) {
        const parsedBody = _.parseIfJson(body);
        if (_.isValidJsonRequest(headerToCheck) && parsedBody) {
            return toJsonSchema(parsedBody);
        }
    }
    if (_.isValidEncodedFormDataRequest(headerToCheck)) {
        if(_.isString(body)){
            const bodyObject = qs.parse(body.toString());
            return toJsonSchema(bodyObject);
        }
        return toJsonSchema(inputData.formData.fields);        
    }

    if (_.isObject(inputData.formData)) {
        if (_.isValidMultipartFormDataRequest(headerToCheck)) {
            let formData = {
                type: "object",
                properties: {}
            };
            if (_.isObject(inputData.formData.fields)) {
                formData = toJsonSchema(inputData.formData.fields);
            }
            if (_.isArray(inputData.formData.filesFieldNames) && inputData.formData.filesFieldNames.length) {
                inputData.formData.filesFieldNames.forEach((fileField) => {
                    formData.properties[fileField] = {
                        type: "file"
                    };
                });
            }
            return formData;
        }
    }

    return;
}

function supportedHttpMethods() {
    return [
        'GET',
        'PUT',
        'POST',
        'DELETE',
        'PATCH',
        'HEAD',
        'OPTIONS',
        'CONNECT',
        'TRACE'
    ];
}

function addPoRequestId(data) {
    try {
        if (!data) {
            return {};
        }
        const workLoadIdFromRequest = data.data.requestHeaders ?
            data.data.requestHeaders[Constants.OUTGOING_REQUEST_HEADER_POREQUESTID.toLowerCase()] : "";
        const workLoadId = process.env.PROTECTONCE_WORKLOAD_ID || _.getUuid();
        let mergedworkLoadId = workLoadId;
        if (workLoadIdFromRequest) {
            mergedworkLoadId = workLoadIdFromRequest + (workLoadId ? Constants.WORKLOAD_ID_SEPARATOR + workLoadId : "");
        }
        data.data.poRequestId = mergedworkLoadId;
        return data.data;
    } catch (error) {
        Logger.write(
            Logger.ERROR &&
            `api.addPoRequestId: Failed to add addPoRequestId: ${error}`
        );
    }
}

module.exports = {
    storeRoute,
    parseHttpData,
    addPoRequestId,
};
