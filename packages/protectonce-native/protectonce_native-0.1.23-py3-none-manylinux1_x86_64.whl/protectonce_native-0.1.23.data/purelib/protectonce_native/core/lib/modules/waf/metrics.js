
class Metric {
    constructor(_initial) {
        this._value = _initial === undefined ? 0 : _initial;
    }
    
    setValue(value) {
        return (this._value = value);
    }
    
    getValue() {
        return this._value;
    }
    
    incrementValue(step) {
        if (step === undefined) step = 1;
        this._value += step;
        return this._value;
    }
}

class Metrics {
    constructor(options) {
        this._data = {};
        this.options = options || {};
    }
    
    setValue(key, value) {
        return this.getMetric(key).setValue(value);
    }
    
    getMetric(key, _default) {
        if (key in this._data) { 
            return this._data[key];
        } else {
            return this._data[key] = new Metric(_default);
        }
    }
    
    getValue(key, _default) {
        return this.getMetric(key, _default).valueOf();
    }
    
    incrementValue(key, step) {
        if (step === undefined) step = 1;
        return this.getMetric(key).incrementValue(step);
    }
    
    toJSON(obj) {
        let res = {};
        for (let [key, value] of Object.entries(this._data)) {
            let path = key.split('.');
            let target = res;
            while (path.length>1) {
                let pp = path.shift();
                target = target[pp] = target[pp] || {};
            }
            target[path.shift()] = value.getValue();
        }
        return res;
    }
}

module.exports = Metrics;