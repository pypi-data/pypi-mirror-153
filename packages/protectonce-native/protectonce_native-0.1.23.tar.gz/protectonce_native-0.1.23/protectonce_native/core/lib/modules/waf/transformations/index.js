// A transformation module must export a single function that returns an instance of a transformer function
// thus allowing it to allocate anything internal each time if it wants.
// A transformer should expect a single of value
// e.g.
// module.exports = function lowercaseBuilder() {
//     return function lowercase(data) {
//         return data.toLowerCase;
//     }
// }
const _ = require('lodash');

let transformerCache = {};

const _report=(list, cb, doneCb)=>{ list.forEach(cb); if (doneCb) doneCb(); }

function buildTransformerChainCB(transformersDef, prefix) {
    const transformerId = transformersDef.join("+");
    const cachedTransformer = transformerCache[transformerId];
    if (cachedTransformer) {
        return cachedTransformer;
    }
    
    let [first, ...rest] = transformersDef;
    let addOuterWrapper = (!prefix); //this is first call, so we need to add x=>[x,x] translater
    let transformer;
    if (first) {
        prefix = `${prefix || '>'}:${first}`;
        
        const nested = (rest.length>0) ? buildTransformerChainCB(rest, prefix) : _report;
        const firstTransformer = require(`./${first}`)(); // TODO: require these outside the function
        transformer = function(list, cb, doneCb, cache, reportTransients) {
            if (reportTransients) {
                _report(list, cb);
            }
            let transformedList = cache[prefix];
            if (transformedList == null) {
                transformedList=list.map(([s, orig])=>[firstTransformer(s),orig]);
            }
            return nested(transformedList, cb, doneCb, cache, reportTransients);
        }
    } else {
        transformer = _report;
    }
    if (addOuterWrapper) {
        let _transformer = transformer;
        transformer = function(list, cb, doneCb, cache, reportTransients) {
            list = list.map(x=>[x,x]);
            return _transformer(list, cb, doneCb, cache, reportTransients)
        }
    }
    
    transformer.id = transformerId;
    return transformer;
}

// function buildTransformerChain(transformersDef) {
//     try {
//         transformersDef = transformersDef || [];
//         let transformerId = transformersDef.join(":");
//         if (transformerCache[transformerId]) {
//             return transformerCache[transformerId];
//         }
//         let transformer;
//         if (transformersDef.length == 0) {
//             transformer = function* _transformer(sourceGen) { yield* sourceGen.map(x=>[x,x]) };
//         } else {
//             // let transformers = transformersDef.map(transformerName=>require(`./${transformerName}`)());
//             transformer = function *_transformer(sourceGen, cache, report_transients) {
//                 let list = sourceGen.map(x=>[x,x]);
//                 let transformPath = "src";
//                 for (let transformerName of transformersDef) {
//                     transformPath = `${transformPath}:${transformerName}`;
//                     if (cache[transformPath]) {
//                         if (report_transients) {
//                             for (let e_orig of list) {
//                                 yield e_orig;
//                             }
//                         }
//                         list = cache[transformPath];
//                     } else {
//                         const transformer = require(`./${transformerName}`)(); // TODO: require these outside the function
//                         let newList = [];
//                         for (let [e, orig] of list) {
//                             newList.push([transformer(e), orig]);
//                             if (report_transients) {
//                                 yield [e, orig];
//                             }
//                         }
//                         cache[transformPath] = newList;
//                         list = newList;

//                     }
//                 }
                
//                 for (let e_orig of list) {
//                     yield e_orig;
//                 }
//             }
//         }   
//         transformer.transformId = transformerId;
//         transformerCache[transformerId] = transformer;
        
//         return transformer
//     } catch (err) {
//         console.log(`Error building transformer chain: ${err}`)
//     }
// }

module.exports = {
    buildTransformerChainCB
}