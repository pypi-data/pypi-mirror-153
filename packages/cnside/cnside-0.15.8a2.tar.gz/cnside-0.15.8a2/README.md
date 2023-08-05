# cnside CLI
[![Python](https://img.shields.io/badge/Python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-blue)](https://pypi.org/project/cnside/)
[![illustria](https://img.shields.io/badge/Home-illustria-blue)](https://illustria.io/)
[![Slack](https://img.shields.io/badge/Slack-illustriacommunity.slack.com-blue)](https://illustriacommunity.slack.com)

## What is cnside?
Your gateway to a safer world of [Open Source Software](https://en.wikipedia.org/wiki/Open-source_software).
Using _cnside_, you can securely download and install open source packages on your projects. 

## What do we do?
Using our amazing CLI client, we wrap your package managers and redirect all your requests to our service. 
We perform a series of advanced security examinations to the libraries you want to download, and let you do so **only** if they passed all our validations.

## What are we protecting you from?
Every encounter with Open-Source-Components reflects high risk that can threat your environment. Protect yourself from common open-source based supply-chain attacks such as:
* [TypoSquatting](https://en.wikipedia.org/wiki/Typosquatting)
* [Dependency Confusion](https://medium.com/@alex.birsan/dependency-confusion-4a5d60fec610)
* [Backdoors](https://medium.com/@alex.birsan/dependency-confusion-4a5d60fec610)
* And many more...

By using our services when letting new libraries into your environment.

## Supported Package Managers
* pip
* npm

Will be added soon:
* Maven
* Nuget

---

# Using cnside CLI

## Installation
You have several options for installing the cnside cli client:
### Using pip
```bash
$ pip install cnside
```

### Cloning from git
```bash
$ git clone git@gitlab.com:illustria/cnside-cli.git
$ cd cnside-cli
$ python setup.py
```

## Usage
### Authentication
Run the `auth` command:
```bash
$ cnside illustria auth
```
You'll be directed to our login page, where you can sign in or login with existing user.

### Downloading new packages
Just wrap your ordinary installation command with our client by adding the `cnside` prefix:

```bash
$ cnside [ pip | npm | maven | nuget ] [ flags ] [ package_name ]
```
And get going!

![illustria cnside-cli install Django](docs/assets/illustria-demo.gif)

## Troubleshooting
No troubles yet!
