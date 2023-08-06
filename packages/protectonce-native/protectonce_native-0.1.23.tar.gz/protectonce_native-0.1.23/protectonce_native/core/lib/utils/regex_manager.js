class RegExpManager {
    constructor() {
        this._regExps = {};
    }

    getRegExp(expression) {
        if (!this._regExps[expression]) {
            this._regExps[expression] = new RegExp(expression);
        }

        return this._regExps[expression];
    }
}

module.exports = new RegExpManager();
