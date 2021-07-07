const utils = require('./utils');
const moment = require('moment')

module.exports = async function (context) {
    try {
        context.log('Starting grouping function at', moment());
        await utils.read_data();

    } catch (err) {
        context.log('Error reading data', err);
    }
};

const main = async () => {
    try {
        console.log('Starting grouping function at', moment());
        await utils.read_data();

    } catch (err) {
        console.log('Error reading data', err);
    }
}
main()