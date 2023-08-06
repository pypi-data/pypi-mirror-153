const BaseFilter = require("../base")
const Logger = require('../../../../utils/logger');

let poNative = null;
try {
  poNative = require('@protectonce/native');
} catch (e) {
  Logger.write(Logger.INFO && `failed to load @protectonce/native with error: ${e}`);
}

class DetectSQLIFilter extends BaseFilter {
  constructor(filterDef) {
    super(filterDef, "detectSQLI");
  }

  doCheckCB(data, originalData, findingCb, doneCb) {
    if (!poNative) {
      doneCb();
      return;
    }

    let match = poNative.detectSQLI(data);
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

module.exports = DetectSQLIFilter;
