const config = require('./config');
const utils = require('./utils');

module.exports = async function (context, myTimer) {
    try {
        context.log('Starting script');

        for (let source of config.sources) {
            await utils[`run_${source.type}`](source);
        }

        context.log('Finishing script');
    } catch (err) {
        context.log(err);
    }
}