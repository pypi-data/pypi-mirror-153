const RuntimeAction = {
    RUNTIME_ACTION_NONE: 'none',
    RUNTIME_ACTION_ALERT: 'alert',
    RUNTIME_ACTION_BLOCK: 'block',
    RUNTIME_ACTION_SKIP: 'skip'
};

class RuntimeData {
    constructor(runtimeData) {
        this.args = runtimeData.args || [];
        this.context = runtimeData.context || '';
        this.action = RuntimeAction.RUNTIME_ACTION_NONE;
        this.message = runtimeData.message || '';
        this.result = runtimeData.result || null;
        this.modifyArgs = runtimeData.modifyArgs || {};
        this.callStack = runtimeData.callStack || [];
    }

    setBlock() {
        this.action = RuntimeAction.RUNTIME_ACTION_BLOCK;
    }

    setAlert() {
        this.action = RuntimeAction.RUNTIME_ACTION_ALERT;
    }

    setSkip() {
        this.action = RuntimeAction.RUNTIME_ACTION_SKIP;
    }
}

class RASPData extends RuntimeData {
    constructor(raspData) {
        super(raspData);
        this.confidence = 0;
        this.sessionId = raspData.poSessionId || '';
    }
}

class WAFData extends RuntimeData {
    constructor(wafData) {
        super(wafData);
        this.name = wafData.name;
        this.internalName = wafData.internalName
        this.sessionId = wafData.poSessionId || '';
    }
}

class SQLData extends RASPData {
    constructor(sqlData) {
        super(sqlData);
        this.query = sqlData.query;
    }

    get params() {
        return {
            'query': this.query,
            'stack': this.callStack
        };
    }
}

class FileData extends RASPData {
    constructor(fileData) {
        super(fileData);
        this.path = fileData.path;
        this.realpath = fileData.realpath;
        this.filename = fileData.filename;
        this.source = fileData.source;
        this.dest = fileData.dest;
        this.stack = fileData.stack;
        this.url = fileData.url;
        this.mode = fileData.mode;
    }

    get params() {
        return {
            'path': this.path,
            'realpath': this.realpath,
            'stack': this.callStack
        };
    }
}

class CommandData extends RASPData {
    constructor(commandData) {
        super(commandData)
        this.command = commandData.command;
        this.stack = commandData.stack;
    }

    get params() {
        return {
            'command': this.command,
            'stack': this.stack,
            'callStack': this.callStack
        };
    }
}

class XmlData extends RASPData {
    constructor(xmlData) {
        super(xmlData)
        this.entity = xmlData.entity;
    }

    get params() {
        return {
            'entity': this.entity,
            'callStack': this.callStack
        };
    }
}

class SsrfData extends RASPData {
    constructor(ssrfData) {
        super(ssrfData)
        this.url = ssrfData.url;
        this.hostname = ssrfData.hostname;
        this.ip = ssrfData.ip;
        this.origin_ip = ssrfData.origin_ip;
        this.origin_hostname = ssrfData.origin_hostname;
    }

    get params() {
        return {
            'url': this.url,
            'hostname': this.hostname,
            'ip': this.ip,
            'origin_ip': this.origin_ip,
            'callStack': this.callStack
        };
    }
}


class SsrfRedirectData extends SsrfData {
    constructor(ssrfRedirectData) {
        super(ssrfRedirectData)
        this.url2 = ssrfRedirectData.url2;
        this.hostname2 = ssrfRedirectData.hostname2;
        this.ip2 = ssrfRedirectData.ip2;
        this.port2 = ssrfRedirectData.port2;
    }

    get params() {
        return {
            'hostname': this.hostname,
            'ip': this.ip,
            'url2': this.url2,
            'hostname2': this.hostname2,
            'ip2': this.ip2,
            'port2': this.port2,
            'callStack': this.callStack
        };
    }
}



module.exports = {
    RuntimeData: RuntimeData,
    SQLData: SQLData,
    FileData: FileData,
    CommandData: CommandData,
    SsrfData: SsrfData,
    XmlData: XmlData,
    SsrfRedirectData: SsrfRedirectData,
    WAFData: WAFData
};
