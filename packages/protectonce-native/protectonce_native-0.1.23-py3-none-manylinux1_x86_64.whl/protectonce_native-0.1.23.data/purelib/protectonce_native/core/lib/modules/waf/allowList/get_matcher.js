const WildcardMatcher = require('./wildcard_matcher');
const ContainsMatcher = require('./contains_matcher');
const EqualsMatcher = require('./equals_matcher');

function getMatcherByOperator(item, operator, type) {
  switch (operator) {
    case 'wildcard':
      return new WildcardMatcher(item, type);
    case 'contains':
      return new ContainsMatcher(item, type);
    case 'equals':
      return new EqualsMatcher(item, type);
    default:
      return new EqualsMatcher(item, type);
  }
}

module.exports = {getMatcherByOperator};