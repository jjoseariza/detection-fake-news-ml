const moment = require('moment');
const { BlobServiceClient } = require('@azure/storage-blob');
const config = require('./config')
const converter = require('json-2-csv');

const read_data = async () => {
    const blobService = BlobServiceClient.fromConnectionString(config.azure.connection);
    const containerClient = blobService.getContainerClient(config.azure.fromContainer);

    const init = moment().subtract(1, 'month');
    const finish = moment().subtract(1, 'day');

    let records = []
    for (let date = init; date.diff(finish, 'days') <= 0; date.add(1, 'days')) {
        const file = `data-${date.format('YYYY-MM-DD')}.json`;
        const data = await get_text_data(containerClient, file)

        // FIX: to clean old data
        if (need_clean(date)) {
            data.forEach(d => {
                d.title = clean_text(d.title)
                d.text = clean_text(d.text)
            })
        }

        records = records.concat(data)
    }

    console.log('data grouped: ', records.length)

    // store data grouped
    await upload_data(blobService, records);
}

const get_text_data = async (containerClient, file) => {
    try {
        console.log('Fetching file', file)

        const blockBlobClient = containerClient.getBlockBlobClient(file);
        const downloadBlockBlobResponse = await blockBlobClient.download(0);

        const data = await streamToString(downloadBlockBlobResponse.readableStreamBody)

        return JSON.parse(data) || []
    } catch (err) {
        console.log('Error fetching ', file, err.message || '')
        return []
    }
}

const upload_data = async (blobService, records) => {
    const containerClient = blobService.getContainerClient(config.azure.toContainer);
    const blockBlobClient = containerClient.getBlockBlobClient(`data-${moment().format('YYYY-MM')}.csv`);

    const csv = await to_csv(records)

    await blockBlobClient.upload(csv, csv.length);
}

const streamToString = async (readableStream) =>
    new Promise((resolve, reject) => {
        const chunks = [];
        readableStream.on("data", (data) => {
            chunks.push(data.toString());
        });
        readableStream.on("end", () => {
            resolve(chunks.join(""));
        });
        readableStream.on("error", reject);
    });

const to_csv = (json) => new Promise((resolve, reject) =>
    converter.json2csv(json, (err, csv) => {
        if (err) return reject(err)
        resolve(csv)
    }))

const need_clean = (date) => date < moment('2021/08/30', 'YYYY-MM-DD')
const clean_text = (text) => text.replace(/(\r\n|\r?\n|\n|\r|\t)/g, '');

module.exports = { read_data }