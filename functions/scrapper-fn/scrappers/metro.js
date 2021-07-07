const axios = require('axios');
const cheerio = require('cheerio');
const { clean_text } = require('./helper')

const content = async (url) => {
    const response = await axios.get(url);
    $ = cheerio.load(response.data);
    const article = $('#post-content article').first();
    const title = $(article).find('header h1').text();

    const texts = $(article).find('.article-body p');
    let body = '';
    $(texts).each((_, text) => {
        body = body + ' ' + $(text).text();
    });
    return { title: clean_text(title), text: clean_text(body) };
}

const fetch = async (url) => {
    const response = await axios.get(url);
    $ = cheerio.load(response.data);
    const articles = $('#content article.teaser');
    const news = [];
    for (let article of $(articles)) {
        const linkToNew = $(article).find('.meta a.title').attr('href');
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