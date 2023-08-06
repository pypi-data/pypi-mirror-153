const pm = require('picomatch');
const _ = require('lodash');
const preprocessing = require("./preprocessing");

class FieldMapping {

    constructor(fieldMappingDef) {
        this.preprocessors = (fieldMappingDef.preprocessing || []).map(preprocessing.getPreprocessor);
        this.entries = {};
        for (let [id, fieldDef] of Object.entries(fieldMappingDef.targets || {})) {
            let newMapping = new FieldMappingEntry(id, fieldDef);
            let source = newMapping.source;
            // map field mapping entries from the source->mapping so we can easily find the mappings given the fields
            this.entries[source] = this.entries[source] || [];
            this.entries[source].push(newMapping);
        }
    }

    mapData(data, targetCb, doneCb) {
        for (let preprocessor of this.preprocessors) {
            preprocessor.preprocess(data);
        }
        for (let [key, value] of Object.entries(data)) {
            for (let fieldMapping of this.entries[key] || []) {
                fieldMapping.mapField(key, value, data, (target, valueList) => {
                    targetCb(target, valueList);
                })
            }
        }
        doneCb();
    }
}

class FieldMappingEntry {
    constructor(id, fieldDef) {
        this.id = id;
        this.source = fieldDef.source;
        this.processKeys = fieldDef.process_keys;
        this.processValues = fieldDef.process_values;
        if (!fieldDef.key_filter) {
            this.keyFilter = () => true;
        }
        else {
            let filters = _.castArray(fieldDef.key_filter).map(f => pm(f));
            this.keyFilter = (k) => {
                for (let f of filters) {
                    if (f(k)) {
                        return true;
                    }
                }
                return false;
            }
        }
        if (fieldDef.processors) {
            let processor = new preprocessing.Preprocessor(fieldDef.processors);
            this.process = (data) => processor.preprocess(data);
        } else {
            this.process = (data) => data;
        }
    }

    mapField(key, value, srcData, cb) {
        let valueList = [];

        if (!value) {
            return;
        }

        if (typeof value === 'string') {
            valueList.push(this.process(value));
        }
        else if (typeof value === 'number') {
            valueList.push(this.process(value));
        }
        else if (Array.isArray(value)) {
            for (let v of value) {
                valueList.push(this.process(v));
            }
        }
        else { // assume it's an object
            for (let [k, v] of Object.entries(value)) {
                if (this.keyFilter(k)) {
                    if (this.processKeys) {
                        valueList.push(this.process(k));
                    }
                    if (this.processValues) {
                        if (_.isArray(v)) {
                            v.forEach(element => {
                                valueList.push(this.process(element));
                            });
                        }
                        else {
                            valueList.push(this.process(v));
                        }
                    }
                }
            }
        }
        cb(this.id, valueList);
    }
}


module.exports = FieldMapping;
