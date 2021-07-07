const axios = require('axios');
const cheerio = require('cheerio');

const content = async (url) => {
    const response = await axios.get(url);
    $ = cheerio.load(response.data);
    const article = $('#main article').first();
    const title = $(article).find('header h1').text();

    const texts = $(article).find('section p');
    let body = '';
    $(texts).each((_, text) => {
        body = body + ' ' + $(text).text();
    });
    return { title: clean_text(title), text: clean_text(body) };
}

const fetch = async (url) => {
    const response = await axios.get(url);
    $ = cheerio.load(response.data);
    const articles = $('#main article');
    const news = [];
    for (let article of $(articles)) {
        const linkToNew = $(article).find('header h2 a').attr('href');
        news.push(await content(linkToNew));
    }
    return news;
}

const run = async (config, date) => {
    const url = `${config.endpoint}/${date.year()}/${date.month() + 1}/${date.date()}`;
    console.log('url', url)
    const news = await fetch(url);
    return news.map(n => ({ ...n, label: config.truth }));
};

module.exports = { run };