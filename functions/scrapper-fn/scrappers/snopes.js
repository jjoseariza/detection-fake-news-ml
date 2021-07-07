const axios = require('axios');
const cheerio = require('cheerio');

const content = async (url) => {
    const response = await axios.get(url);
    $ = cheerio.load(response.data);
    const article = $('main article').first();
    const title = $(article).find('header h1.title').text();

    const texts = $(article).find('div.single-body p');
    let body = '';
    $(texts).each((_, text) => {
        body = body + ' ' + $(text).text();
    });
    return { title: clean_text(title), text: clean_text(body) };
}

const fetch = async (url) => {
    const response = await axios.get(url);
    $ = cheerio.load(response.data);
    const articles = $('div.list-archive div.list-group article');
    const news = [];
    for (let article of $(articles)) {
        const linkToNew = $(article).find('a.stretched-link').attr('href');
        news.push(await content(linkToNew));
    }
    return news;
}

const run = async (config, page) => {
    const url = `${config.endpoint}/${page}`;
    console.log('url', url)
    const news = await fetch(url);
    return news.map(n => ({ ...n, label: config.truth }));
};

module.exports = { run };