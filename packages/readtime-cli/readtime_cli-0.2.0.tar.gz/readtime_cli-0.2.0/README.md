<h1 align="center">
  📖 Readtime-CLI
</h1>
<p align="center">
    <a href="https://github.com/guedesfelipe/readtime_cli/actions/workflows/ci.yml" target="_blank">
        <img src="https://github.com/guedesfelipe/readtime_cli/actions/workflows/ci.yml/badge.svg?branch=main" />
    </a>
    <a href="https://github.com/guedesfelipe/readtime_cli/actions/workflows/security.yml" target="_blank">
        <img src="https://github.com/guedesfelipe/readtime_cli/actions/workflows/security.yml/badge.svg?branch=main" />
    </a>
    <a href="https://codecov.io/gh/guedesfelipe/readtime_cli" target="_blank">
      <img src="https://codecov.io/gh/guedesfelipe/readtime_cli/branch/main/graph/badge.svg" />
    </a>
    <a href="https://pypi.org/project/readtime-cli/" target="_blank">
      <img src="https://img.shields.io/pypi/v/readtime-cli?color=%2334D058&label=pypi%20package" />
    </a>
    <a href="" target="_blank">
      <img src="https://img.shields.io/pypi/pyversions/readtime-cli.svg?color=%2334D058&logo=python&logoColor=yellow" />
    </a>
</p>

<p align="center">
  <em>CLI to calculates the time some text takes the average human to read, based on Medium's <a href="https://help.medium.com/hc/en-us/articles/214991667-Read-time" target="_blank">read time forumula</a>.</em>
</p>


## 🧮 Algorithm

Medium's Help Center says,

> Read time is based on the average reading speed of an adult (roughly 265 WPM). We take the total word count of a post and translate it into minutes, with an adjustment made for images. For posts in Chinese, Japanese and Korean, it's a function of number of characters (500 characters/min) with an adjustment made for images.

[Source](https://help.medium.com/hc/en-us/articles/214991667-Read-time)

Double checking with real articles, the English algorithm is:

    seconds = num_words / 265 * 60 + img_weight * num_images

With `img_weight` starting at `12` and decreasing one second with each image encountered, with a minium `img_weight` of `3` seconds.


## Requirements

MacOS or Linux

Python 3.9+

Readtime-CLI stands on the shouders of giants:

* [Typer](https://github.com/tiangolo/typer)
* [Readtime](https://github.com/alanhamlett/readtime)


## 🛠 Installation

### Poetry

    poetry add readtime-cli

### Pip

    virtualenv venv
    . venv/bin/activate
    pip install readtime-cli


## 💻 Usage


### Version

```sh
readtime version
```

### Calculate Read time Markdown files

```sh
readtime md FILE_PATH [OPTIONS]
```

### Calculate Read time HTML files

```sh
readtime html FILE_PATH [OPTIONS]
```

### Calculate Read time Text files

```sh
readtime text FILE_PATH [OPTIONS]
```

### Options for all commands

    --wpm INTEGER          Word Per Minute  [default: 265]
    --language [en|pt-br]  [default: Languages.en]
    --help                 Show this message and exit.
