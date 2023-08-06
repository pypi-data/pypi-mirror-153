const cookie = require("cookie");
const url = require("url");
const path = require("path");

const {JSONPath} = require('jsonpath-plus');

class Processor {
    constructor(processerDef) {
        this.type = processerDef.type;
    }
    
    process(data) {
        throw new Error("Not implemented");
    }
}

class JSONPathProcessor extends Processor {
    constructor(processerDef) {
        super(processerDef);
        this.path = processerDef.path;
    }
    
    process(data) {
        let res = JSONPath(this.path, data);
        switch (res.length) {
            case 0:
                return null;
            case 1:
                return res[0];
            default:
                return res;
        } 
    }
}

class CookieParserProcessor extends Processor {
    
    constructor(processerDef) {
        super(processerDef);
    }
    
    process(data) {
        if (typeof data !== "string") {
            throw new Error(`CookieParserProcessor expected a string but received a ${typeof data}`);
        }
        return cookie.parse(data)
    }
}

class ParseUrlProcessor extends Processor {
    constructor(processerDef) {
        super(processerDef);
    }
    
    process(data) {
        if (typeof data !== "string") {
            throw new Error(`ParseUrlProcessor expected a string but received a ${typeof data}`);
        }
        let u = url.parse(data);
        u.basename = path.basename(u.pathname);
        return u;
    }
}

class LowerCaseProcessor extends Processor {
    constructor(processerDef) {
        super(processerDef);
    }
    
    process(data) {
        if (typeof data !== "string") {
            throw new Error(`ParseUrlProcessor expected a string but received a ${typeof data}`);
        }
        return data.toLowerCase();
    }
}

class UrlDecodeProcessor extends Processor {
    constructor(processerDef) {
        super(processerDef);
    }
    
    process(data) {
        if (typeof data !== "string") {
            throw new Error(`UrlDecodeProcessor expected a string but received a ${typeof data}`);
        }
        return decodeURIComponent(data);
    }
}

module.exports = {
    getProcessor(processerDef) {
        switch (processerDef.type) {
            case "cookieParser":
                return new CookieParserProcessor(processerDef);
            case "jsonPath":
                return new JSONPathProcessor(processerDef);
            case "parseUrl":
                return new ParseUrlProcessor(processerDef);
            case "lowerCase":
                return new LowerCaseProcessor(processerDef);
            case "urlDecode":
                return new UrlDecodeProcessor(processerDef);
            default:
                throw new Error(`Unsupporting Processor type: ${processerDef.type}`);
        }
    }
}