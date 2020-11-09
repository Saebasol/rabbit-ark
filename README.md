# Rabbit Ark

[![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)

> Scalable downloader that downloads asynchronously

- [Rabbit Ark](#rabbit-ark)
  - [Description](#description)
    - [Download](#download)
    - [How to use](#how-to-use)
  - [Supported Sites](#supported-sites)
  - [Script](#script)
  - [Special Thanks](#special-thanks)

## Description

This program is inspired by [YouTube-dl](https://github.com/ytdl-org/youtube-dl/) and [Hitomi Downloader](https://github.com/KurtBestor/Hitomi-Downloader)

The download is processed using the [aiomultiprocess](https://github.com/omnilib/aiomultiprocess) module.

### Download

You can Download in [here](https://github.com/Saebasol/rabbit-ark/releases)

### How to use

First you shoud specify which extractor to use

```sh
rabbitark pixiv
```

Then provide downloadable information, such as a link, via the --downloadable argument.

```sh

rabbitark pixiv --downloadable pixiv-artwork-url
```

After a while, you can see that the folder is created and the images are down.

For more information, check the -h argument.

## Supported Sites

|     Site      | URL                 | Extractor release life cycle |
| :-----------: | ------------------- | ---------------------------- |
| **Hitomi.la** | <https://hitomi.la> | Alpha                        |
|   **Pixiv**   | <https://pixiv.net> | Alpha                        |
| **Youtube.com**| <https://youtube.com> | Alpha|

## Script

You can learn how to write it in detail [here](https://github.com/Saebasol/rabbit-ark/wiki/Script).

If you want to publish the script after writing it, add it to the extractor folder and open the Pull Request.

## Special Thanks

Thank you very much to [Kurt Bester](https://github.com/KurtBestor) for providing the source for Hitomi Downloader.

It was very helpful in the structure and concept.
