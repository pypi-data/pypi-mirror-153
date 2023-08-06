# rss2gab
Takes an RSS feed and auto posts to gab

There is 100% test coverage on this codebase. So if the unit tests pass on your platform then
the system will work correctly.

# Tests

To run all linting and unit test, please install `tox` and run it, like so:

Install:
```
> python -m pip install tox
```

Then run `tox`:
```
> tox
```


## Platform Unit Tests

[![Actions Status](https://github.com/zackees/rss2gab/workflows/MacOS_Tests/badge.svg)](https://github.com/zackees/rss2gab/actions/workflows/test_macos.yml)
[![Actions Status](https://github.com/zackees/rss2gab/workflows/Win_Tests/badge.svg)](https://github.com/zackees/rss2gab/actions/workflows/test_win.yml)
[![Actions Status](https://github.com/zackees/rss2gab/workflows/Ubuntu_Tests/badge.svg)](https://github.com/zackees/rss2gab/actions/workflows/test_ubuntu.yml)


# Building an app

`pythony build_app.py` and follow the prompts

# Versions

  * 1.0.3: Adds include_author_in_content