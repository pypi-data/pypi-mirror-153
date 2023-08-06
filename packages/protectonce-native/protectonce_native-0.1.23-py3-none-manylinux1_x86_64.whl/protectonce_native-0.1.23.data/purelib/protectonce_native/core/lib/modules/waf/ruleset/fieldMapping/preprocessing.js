const processors = require("./processors");

class Preprocessor {
    constructor (preprocessorDef) {
        this.type = preprocessorDef.type;
        this.processors = preprocessorDef.map(processors.getProcessor);
    }
    
    preprocess(data) {
        let val = data;
        for (let processor of this.processors) {
            if (!val || val.length==0) {
                break; // nothing found, so skip the rest of the chain
            }
            val = processor.process(val);
        }
        return val;
    }
}

class FieldPreprocessor extends Preprocessor {
    constructor (preprocessorDef) {
        super(preprocessorDef.processors);
        this.source = preprocessorDef.source;
        this.name = preprocessorDef.name;
    }
    
    preprocess(data) {
        data[this.name] = super.preprocess(data);
    }
}

module.exports = {
    Preprocessor,
    getPreprocessor(preprocessorDef) {
        switch(preprocessorDef.type) {
            case "field":
                return new FieldPreprocessor(preprocessorDef);
            default:
                throw new Error(`Unsupported preprocessor type received: ${preprocessorDef.type}`);
        }
    }
}