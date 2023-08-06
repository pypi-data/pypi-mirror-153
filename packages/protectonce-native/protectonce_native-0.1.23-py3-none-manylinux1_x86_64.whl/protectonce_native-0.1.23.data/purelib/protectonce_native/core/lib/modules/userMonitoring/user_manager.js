const _ = require('lodash');
class UserManager {
    constructor() {
        this.blockedUserList = [];
    }
    setBlockedUserList(blockedUserList) {
        if (_.isArray(blockedUserList)) {
            this.blockedUserList = blockedUserList.map(user => user.toLowerCase());
        }
    }
    isUserInBlockedList(userName) {
        return this.blockedUserList.includes(userName.toLowerCase());
    }
}

module.exports = new UserManager();