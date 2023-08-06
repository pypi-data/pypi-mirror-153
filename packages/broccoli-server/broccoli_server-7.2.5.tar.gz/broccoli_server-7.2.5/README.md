# broccoli-server
[![Build Status](https://travis-ci.org/k-t-corp/broccoli-server.svg?branch=master)](https://travis-ci.org/k-t-corp/broccoli-server)
[![PyPI version](https://badge.fury.io/py/broccoli-server.svg)](https://badge.fury.io/py/broccoli-server)

A Python framework to build web scraping applications.

## Problem Statement
* I want to
    * Scrape contents (images, texts, etc) from places on the web (RSS, Twitter, parsing HTML, etc)
    * Moderate and modify them internally on a web UI
    * Expose them in a public API
* Without having to re-implement, for different scraping applications
    * Reliable "cron" jobs that scrape the content
    * A pipeline that processes the contents stage by stage
    * Internal web UIs that allow human to moderate the contents as a pipeline stage


## Solution
This is a Python framework that extracts out common components in the scraping, processing and moderating of web contents,
and provides interfaces for programmers to implement "business logic" with, so that they can build reliable and easy-to-use web scraping applications in less time.

## Getting started
WIP (https://github.com/k-t-corp/broccoli-server/issues/124)

## Development
### Prerequisites
* `Python 3.9`
* `Make`

### Prepare virtualenv
```bash
make venv
```

### Develop
```bash
make deps
```

### Test
```bash
make test
```
