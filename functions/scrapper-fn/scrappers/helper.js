const clean_text = (text) => text.replace(/(\r\n|\r?\n|\n|\r|\t)/g, '');

module.exports = { clean_text }