const today = new Date()
const defaultConfig = {
    output: 'test.csv',
    azure: {
        connection: '<AZURE-KEY>',
        container: 'data-scrapped'
    },
    sources: [
        {
            label: 'waterfordwhispersnews',
            type: 'date',
            endpoint: 'https://waterfordwhispersnews.com',
            from: today,
            to: today,
            scrapper: 'water',
            truth: false
        },
        {
            label: 'metro',
            type: 'date',
            from: today,
            to: today,
            endpoint: 'https://metro.co.uk',
            scrapper: 'metro',
            truth: true
        },
        // {
        //     label: 'snopes',
        //     type: 'number',
        //     endpoint: 'https://www.snopes.com/fact-check/rating/false/page',
        //     scrapper: 'snopes',
        //     truth: false,
        //     max: 458
        // },
        // {
        //     label: 'snopes',
        //     type: 'number',
        //     endpoint: 'https://www.snopes.com/fact-check/rating/true/page',
        //     scrapper: 'snopes',
        //     truth: true,
        //     max: 157
        // }
    ]
}

module.exports = defaultConfig
