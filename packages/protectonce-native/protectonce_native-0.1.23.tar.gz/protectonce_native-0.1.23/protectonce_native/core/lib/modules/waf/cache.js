const LRU = require("lru-cache");

// class ResultCache {
//     constructor(metrics) {
//         // this._cache = {};
//         this._cache = new LRU({
//             max:    10000
//         });
//         this.metrics = metrics;
//         if (this.metrics) {
//             this.cache_hits_metric = this.metrics.getMetric("waf.cache.hits");
//             this.cache_misses_metric = this.metrics.getMetric("waf.cache.misses");
//             this.cache_lookups_metric = this.metrics.getMetric("waf.cache.lookups");
//         }
//     }
    
//     *getValueGen(key, getterGen) {
//         if (this.metrics) this.cache_lookups_metric.incrementValue()
//         if (this._cache.has(key)) {
//             if (this.metrics) this.cache_hits_metric.incrementValue()
//             // if (key.indexOf("ARGS-0")>-1 && key.indexOf("A")>-1) console.log("hit", key)
//             yield* this._cache.get(key);
//         } else {
//             // if (key.indexOf("ARGS-0")>-1 && key.indexOf("A")>-1) console.log("miss", key)
//             if (this.metrics) this.cache_misses_metric.incrementValue()
//             if (getterGen) {
//                 let values = Array.from(getterGen());
//                 this._cache.set(key, values);
//                 yield* values;
//             } 
//         }
//     }
    
//     // getterCB will call it cb parameter with each value if called, but the cache can skip it
//     // cache returns results to cb
//     getValueCB(key, cb, getterCB) {
//         if (this.metrics) this.cache_lookups_metric.incrementValue()
//         if (this._cache.has(key)) {
//             // console.log(key);
//             if (this.metrics) this.cache_hits_metric.incrementValue()
//             this._cache.get(key).forEach(cb);
//         } else {
//             if (this.metrics) this.cache_misses_metric.incrementValue()
//             if (getterCB) {
//                 let values = [];
//                 getterCB(value=>{ values.push(value); cb(value); })
//                 this._cache.set(key, values);
//             } 
//         }
//     }
    
//     getValueDirect(key, getter) {
//         if (this.metrics) this.cache_lookups_metric.incrementValue()
//         if (this._cache.has(key)) {
//             // console.log(key);
//             if (this.metrics) this.cache_hits_metric.incrementValue()
//             return this._cache.get(key);
//         } else {
//             if (this.metrics) this.cache_misses_metric.incrementValue()
//             if (getter) {
//                 let value = getter();
//                 this._cache.set(key, value);
//                 return value;
//             } 
//         }
//     }
    
//     setValue(key, value) {
//         return this._cache.set(key,  value);  
//     }
// }

// module.exports = ResultCache;

class FastVerdictCacheSet {
    constructor(options) {
        this.options = options || {};
        this.max = this.options.max || 10000;
        this.metrics = options.metrics;
        if (this.metrics) {
            this.cache_hits_metric = this.metrics.getMetric("waf.cache.hits");
            this.cache_misses_metric = this.metrics.getMetric("waf.cache.misses");
            this.cache_lookups_metric = this.metrics.getMetric("waf.cache.lookups");
        }
        
        this.once_recent = new Set();
        this.once_older = new Set();
        this.more_than_once = new Set();
    }
    
    get(key) {
        this.cache_lookups_metric.incrementValue();
        
        if (this._cache.has(key)) {
            this.cache_hits_metric.incrementValue();
            return true;
        }
        if (this.once_recent.has(key) || this.once_older.has(key)) {
            this.cache_hits_metric.incrementValue();
            this.more_than_once.add(key);
            this._checkSizes();
            return true;
        }
        this.cache_misses_metric.incrementValue();
        return false;
    }
    
    _checkSizes() {
        if (this.more_than_once.length >= this.max) {
            this.once_recent = this.once_older;
            this.once_older = this.more_than_once;
            this.more_than_once = new Set();
        } else {
            if (this.once_recent.length >= this.max) {
                this.once_older = this.once_recent;
                this.once_recent = new Set();
            }
        }
    }
    
    set(key, val) {
        if (val!=false) {
            this.once_recent.add(key);
            this._checkSizes();
        } else {
            this.delete(key);
        }
    }
    
    delete(key) {
        this.once_older.delete(key);
        this.once_recent.delete(key);
        this.more_than_once.delete(key);
    }
    
}

class FastVerdictCacheLRU {
    constructor(options) {
        this.options = options || {};
        this.max = this.options.max || 100000;
        this.metrics = options.metrics;
        this._cache = new LRU({
            max:    this.max
        });
        if (this.metrics) {
            this.cache_hits_metric = this.metrics.getMetric("waf.cache.hits");
            this.cache_misses_metric = this.metrics.getMetric("waf.cache.misses");
            this.cache_lookups_metric = this.metrics.getMetric("waf.cache.lookups");
        } else {
            throw new Error("Cache must have a metrics object")
        }
    }
    
    get(key) {
        this.cache_lookups_metric.incrementValue();
        
        if (this._cache.has(key)) {
            this.cache_hits_metric.incrementValue();
            // console.log(key)
            return true;
        }
        this.cache_misses_metric.incrementValue();
        return false;
    }
    
    set(key, val) {
        if (val!=false) {
            
            this._cache.set(key, true);
        } else {

        }
    }
}

module.exports = FastVerdictCacheLRU;

// const COUNT=     1000000;
// const UNIQUE=    100000;
// const CACHE_MAX= 10000;

// let lru = new LRU({
//     max:    CACHE_MAX
// });

// console.time("lru")
// for (let i=0; i<COUNT; i++ ) {
//     let key=`key_and_num_${Math.round(Math.random()*UNIQUE)}`;
//     lru.set(key, true);
// }

// let hits=0, misses=0;
// for (let i=0; i<COUNT; i++ ) {
//     let key=`key_and_num_${Math.round(Math.random()*UNIQUE)}`;
//     // console.log(key)
//     if (lru.get(key) == true) {
//         hits++
//     } else {
//         misses++
//     }
// }
// console.timeEnd("lru")
// console.log(`hits=${hits}. misses=${misses}`)

// let fvc = new FastVerdictCache({
//     max:    CACHE_MAX
// });

// console.time("fvc")
// for (let i=0; i<COUNT; i++ ) {
//     let key=`key_and_num_${Math.round(Math.random()*UNIQUE)}`;
//     fvc.set(key);
// }


// hits=0, misses=0;
// for (let i=0; i<COUNT; i++ ) {
//     let key=`key_and_num_${Math.round(Math.random()*UNIQUE)}`;
//     if (lru.get(key) == true) {
//         hits++
//     } else {
//         misses++
//     }
// }
// console.timeEnd("fvc")
// console.log(`hits=${hits}. misses=${misses}`)

