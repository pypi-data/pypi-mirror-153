require('../utils/common_utils');
const _ = require('lodash');

class Method {
    constructor(method) {
        this.method = method['method'] || '';
        this.args = this._parseArgs(method['args']);
        this.kwargs = this._parseArgs(method['kwargs']);
    }

    _parseArgs(args) {
        if (typeof args === 'undefined') {
            return ['*'];
        }

        return args;
    }
}

class Event {
    constructor(event) {
        this.on = event['on'] || '';
        this.lazy = event['lazy'] || false;
    }
}

class Handler {
    constructor(handler) {
        this.type = handler['type'] || '';
        this.method = handler['method'] || '';
        this.config = handler['config'] || {};
    }
}

class Handlers {
    constructor(handlers) {
        this.before = [];
        this.after = [];
        this._parseHandlers(handlers)
    }

    _parseHandlers(handlers) {
        if (Array.isArray(handlers)) {
            // FIXME: This is a stopgap solution till the backend structure is fixed
            this.before = this._createHandlers(handlers);
            return;
        }

        const before = handlers['before'] || [];
        this.before = this._createHandlers(before);

        const after = handlers['after'] || [];
        this.after = this._createHandlers(after);
    }

    _createHandlers(handlers) {
        let _handlers = [];
        handlers.forEach(handler => {
            _handlers.push(new Handler(handler));
        });
        return _handlers;
    }
}

class Context {
    constructor(context) {
        this.attackType = context['attack_type'] || '';
        this.regex = context['regex'] || [];
    }
}

class Config {
    constructor(context) {
        this.enabled = _.toBoolean(context['enabled']);
        this.block = _.toBoolean(context['block']);
    }
}

class Intercept {
    constructor(intercept) {
        this.module = intercept['module'] || '';
        this.class = intercept['class'] || '';
        this.method = intercept['method'] || '';

        const methods = intercept['methods'] || [];
        this.methods = [];
        methods.forEach(method => {
            this.methods.push(new Method(method));
        });

        const events = intercept['events'] || [];
        this.events = [];
        events.forEach(event => {
            this.events.push(new Event(event));
        });

        const handlers = intercept['handlers'] || {};
        this.handlers = new Handlers(handlers);

        this.context = new Context(intercept['context'] || {});
        this.config = new Config(intercept['config'] || {});
    }
}

class Rule {
    constructor(rule) {
        this.id = rule['id'] || '';
        this.type = rule['type'] || '';
        this.intercept = new Intercept(rule['intercept'] || {});
    }

    get runtimeRule() {
        return {
            'type': this.type,
            'intercept': {
                'module': this.intercept.module,
                'class': this.intercept.class,
                'method': this.intercept.method,
                'methods': this.intercept.methods,
                'events': this.intercept.events,
                'handlers': this.intercept.handlers,
                'context': this.id
            }
        }
    }

    get regExps() {
        return this.intercept.context.regex;
    }

    get isEnabled() {
        return this.intercept.config.enabled;
    }

    get shouldBlock() {
        return this.intercept.config.block;
    }
}

module.exports = Rule;
