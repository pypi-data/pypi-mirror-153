const WAF = require("./waf");
const ProtectOnceContext = require('../context');

module.exports = new WAF({}, { poContext: ProtectOnceContext });
