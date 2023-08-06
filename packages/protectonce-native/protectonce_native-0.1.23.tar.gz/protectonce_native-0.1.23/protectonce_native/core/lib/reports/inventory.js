class Inventory {
  constructor(api) {
    this.api = api;
  }
}

class Api {
  constructor(routes) {
    this.routes = routes;
  }

  addRoute(route) {
    if (!(this.routes && this.routes.length)) {
      this.routes = [route];
    }
    this.routes.push(route);
  }
}

class Route {
  constructor(path, methods, host) {
    this.path = path;
    this.methods = methods;
    this.host = host;
  }

  addMethods(methods) {
    this.methods = Array.from(new Set([...this.methods, ...methods]));
  }
}

module.exports = {
  Route,
  Api,
  Inventory
};
