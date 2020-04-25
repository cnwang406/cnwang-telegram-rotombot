# Rotom406_bot - telegram bot for search nearest mask pharmacies

![Platform][platform-image]
![Python][python-image]
[![NPM Version][npm-image]][npm-url]
[![Build Status][travis-image]][travis-url]

telegram chat bot.
search for masks

datasource is from gov.tw, and reference from https://github.com/kiang/pharmacies

wish to filtered out the nearst pharmacies which satisified for at-least certain quantites masks.

## execute

host on *heroku* or ◊local by `ngrok http 8443`

## Usage
host files at heroku.
at telergram, use `@rotom406_bot`  to inline query.
or invite @rotom406_bot to chat.

after push or build, use
```sh
ngrok http 8443
```
and
`https://api.telegram.org/bot{TOKEN}/setWebhook?url={URL_to_webhook}/hook`

## Known Issues


## Wish list
-
## Release History

- 2020.04.23 Ver 0.6
    * remove token in database.py
    * repo to github, and manual deploy to heroku

- 2020.04.18 Ver 0.5
    * host at heroku
- 2020.04.12 Ver 0.1
    * move to telegram, with chatroom.


## Meta

chun nan wang – [@cnwang406](https://twitter.com/cnwang406) – cnwang406@gmail.com

Distributed under the XYZ license. See ``LICENSE`` for more information.

[https://github.com/yourname/github-link](https://github.com/dbader/)


<!-- Markdown link & img dfn's -->
[npm-image]: https://img.shields.io/badge/version-0.6.0-orange
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/badge/build-working-red
[travis-url]: https://img.shields.io/badge/build-working-red
[wiki]: https://github.com/yourname/yourproject/wiki
[platform-image]:https://img.shields.io/badge/platform-heroku-orange
[python-image]:https://img.shields.io/badge/python-3.6%20%7C%203.7-blue
[snapshot-img]:file://resources/snapshot.jpg
