class ProtectOnceContext {

    constructor() {
        this._contextMap = {};
    }

    create(id, context) {
        this._contextMap[id] = context;
    }

    update(id, context) {
        if (!this._contextMap[id]) {
            this._contextMap[id] = context;
            return;
        }

        this._contextMap[id] = {
            ...this._contextMap[id],
            ...context
        };
    }

    release(id) {
        const context = this._contextMap[id];
        delete this._contextMap[id];
        return context;
    }

    get(id) {
        return this._contextMap[id];
    }
}

module.exports = new ProtectOnceContext();
