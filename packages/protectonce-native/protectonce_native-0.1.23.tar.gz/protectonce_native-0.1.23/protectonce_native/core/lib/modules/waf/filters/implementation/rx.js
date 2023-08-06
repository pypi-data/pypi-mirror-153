const BaseFilter = require("../base")
const Logger = require('../../../../utils/logger');
class RxFilter extends BaseFilter {
    constructor(filterDef, context) {
        super(filterDef, "rx", context);
        let options = this._decodeOptions(filterDef.options);
        this.regex = new RegExp(filterDef.value, options);
        this.pattern = filterDef.value;
    }

    _decodeOptions(optionsDef) {
        let optionString = ""
        if (!optionsDef.case_sensitive) {
            optionString += "i"
        }
        return optionString;
    }

    doCheckCB(data, originalData, findingCb, doneCb) {
        // return
        let match = data.match(this.regex);
        if (match) {
            findingCb({
                data,
                originalData,
                pattern: this.pattern
            });
        }
        doneCb();
    }
};

module.exports = RxFilter;