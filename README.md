# Zsh History

[![GitHub Release](https://img.shields.io/github/v/release/nobbmaestro/zhis)](github-release)
[![GitHub last commit](https://img.shields.io/github/last-commit/nobbmaestro/zhis/development)](github-last-commit)
[![GitHub commits since](https://img.shields.io/github/commits-since/nobbmaestro/zhis/v0.1.2/development)](githut-commits-since)
![License](https://img.shields.io/github/license/nobbmaestro/zhis)

zhis: Command history with a database twist

`TODO: Add short demo video`

## Table of contents

- [Installation](#installation)
  - [Install via pipx](#pipx)
  - [Install via pip](#pip)
  - [Manual](#manual)
  - [Configure zsh](#configure-zsh)
- [Feature Roadmap](#feature-roadmap)
- [Customization](#customization)
- [Alternatives](#alternatives)

## Installation

### Pipx (Recommended)

```sh
pipx install zhis
```

### Pip

```sh
pip install zhis
```

### Manual

```sh
git clone git@github.com:nobbmaestro/zhis.git
cd zhis
make
```

## Configure zsh

```sh
echo 'eval "$(zhis init zsh)"' >> ~/.zshrc
```

## Feature Roadmap

- [x] Customizable GUI theme
- [x] Support for inline GUI mode
- [ ] Edit history entries via GUI
- [ ] Delete history entries via GUI
- [ ] Delete selected history entries via GUI
- [ ] Copy to clipboard via GUI
- [ ] Fuzzy-finder search strategy in GUI
- [ ] Filter history by context via GUI
- [ ] Add doctor CLI command for verifying shell configuration
- [ ] Add prune CLI command for removing history based on ignore pattern
- [ ] Add generate shell-completions CLI command
- [ ] Add export CLI command for exporting to HISTFILE
- [ ] Add support for command execution duration
- [ ] Customizable keybindings

## Customization

Check out the [configuration docs](docs/config.md).

## Alternatives

If you find that `zhis` does not quite satisfy your needs, following may be a better fit:

- [Atuin](https://github.com/atuinsh/atuin)
