const fs = require('fs');
const moment = require('moment');
const csvWriter = require('csv-write-stream');
const config = require('./config');
const { BlobServiceClient } = require('@azure/storage-blob');

const run_date = async (source) => {
    const init = moment(source.from);
    const finish = moment(source.to);

    for (let date = init; date.diff(finish, 'days') <= 0; date.add(1, 'days')) {

        try {
            console.log('Starting scrapper', source.label);
            const scrapper = require(`./scrappers/${source.scrapper}.js`);

            const news = await scrapper.run(source, date);
            console.log('Finishing scrapper', source.label, 'data', news.length);

            upload_data(news);

        } catch (err) {
            console.log(`Error getting ${source.label} in ${date}`);
        }

    }
}

const run_number = async (source) => {
    for (let page = 1; page <= source.max; page++) {

        try {
            console.log('Starting scrapper', source.label);
            const scrapper = require(`./scrappers/${source.scrapper}.js`);

            const news = await scrapper.run(source, page);
            console.log('Finishing scrapper', source.label, 'data', news.length);

            upload_data(news);

        } catch (err) {
            console.log(`Error getting ${source.label} in page ${page}`);
        }

    }
}

const write_csv = (data) => {
    console.log('Storing data');
    const writer = (!fs.existsSync(`./${config.output}`))
        ? csvWriter({ headers: ['title', 'text', 'label'] })
        : csvWriter({ sendHeaders: false });
    writer.pipe(fs.createWriteStream(config.output, { flags: 'a' }));
    data.map(n => writer.write(n));
    writer.end();
    console.log('Data stored');
}

const upload_data = async (data) => {
    const blobServiceClient = BlobServiceClient.fromConnectionString(config.azure.connection);
    const containerClient = blobServiceClient.getContainerClient(config.azure.container);

    const blockBlobClient = containerClient.getBlockBlobClient(`data-${moment().format('YYYY-MM-DD')}.json`);

    const json = JSON.stringify(data)
    await blockBlobClient.upload(json, json.length);
}

module.exports = { run_date, run_number, upload_data }