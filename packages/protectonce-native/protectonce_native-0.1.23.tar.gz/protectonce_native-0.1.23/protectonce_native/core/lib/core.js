const RuntimeInterface = require('./runtime/interface');
require('./runtime/invoker');

module.exports = {
    // This interface is only for nodejs runtime.
    // All other runtime should invoke core using agent-interface
    // which directly calls directly protectOnceInvokeInterface from runtime/invoke.js
    RuntimeInterface: RuntimeInterface
};
