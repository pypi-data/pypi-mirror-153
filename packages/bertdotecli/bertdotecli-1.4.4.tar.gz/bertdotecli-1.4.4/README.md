<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Overview](#overview)
- [Design](#design)
    - [Features](#features)
- [Plugin Architecture](#plugin-architecture)
    - [Creating Plugins](#creating-plugins)
    - [Installing Plugins](#installing-plugins)
- [Usage examples](#usage-examples)
    - [Usage examples - Utilizing Windows Credentials Manager](#usage-examples---utilizing-windows-credentials-manager)
- [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [ecli](#ecli)
- [Appendix](#appendix)
    - [Sub-Command naming logic](#sub-command-naming-logic)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

<a name="top"></a>
<a name="overview"></a>

# Overview

As systems engineers, we spend much of our time on our command-line terminals
interacting with a myriad of systems in support of the overarching infrastructure.

Our daily tasks can often be repetitive, 
which is why we often find ourselves utilizing 
or creating automation to lessen our keystrokes.

This brings us to a question:

- _What do you get when each member of a team of engineers has an affinity
  for creating their own little scripts to make their lives easier?_<br />
  Hint: It's something messy.
  
The *ecli* app aims to clean up this proclivity for command-line mess in the team setting
by unifying disparate pieces of automation into a single entrypoint, thus 
creating a homogenous command-line experience.

This is accomplished by a modular design that can accomodate just about any executable
piece of code.

The following sections go over this in detail.

<a name="design"></a>
# Design

The *ecli* app is made up of two major components:

- A base command module written in python
- Plugins that extend the base command module

The plugin system essentially allows contributers to 
define namespaces of commands, along with their corresponding 
subcommands.

<a name="features"></a>
## Features

  - Commands are executables organized by subfolders in a given plugin directory<br />
    (See the Appendix for list of supported executable types)
  - Subfolders are interpreted as the namespace name for<br />
    the given scripts/executables contained therein
  - Subcommands follow a dot-notation style of reference, e.g.<br />
    _pluginfolder.namespace.command_<sup> [1](#sub-command-naming-logic)</sup>

<a name="installation"></a>
# Installation

<a name="prerequisites"></a>
## Prerequisites

You'll need python3 & pip for the pip distribution.

To install,

* For Windows:
    * <a href="https://community.chocolatey.org/" target="_blank">choco</a>
        1. Start an elevated powershell prompt and run the following commands:
        1. `Set-Variable -Name "ChocolateyInstall" -Value "$(Join-Path -Path $Env:LocalAppData -ChildPath chocolatey)"`
        1. `New-Item $ChocolateyInstall -Type Directory -Force`
        1. `[Environment]::SetEnvironmentVariable("ChocolateyInstall", $ChocolateyInstall)`
        1. `Set-ExecutionPolicy Bypass -Scope Process iex ((new-object net.webclient).DownloadString('https://chocolatey.org/install.ps1'))`
    * Microsoft C++ Build Tools: `choco install visualstudio2017buildtools`<br />
      Or Install the latest from the Microsoft Website: [https://visualstudio.microsoft.com/visual-cpp-build-tools/](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
    * python 3.7.x: `choco install python --version=3.7.4` <br />
* For Linux, just install python3 via your distro's package manager.
* For OSX, if not already present, I recommend you install 
  python3 via the `brew` package manager

[Back to Top](#top)
<a name="ecli"></a>
## Installing ecli

There are two distributions of the `ecli`

1. python package: Installed via 
   `pip3 install bertdotecli`
1. The Windows bundled executable, available via [Releases](https://github.com/berttejeda/bert.ecli/releases)<br />
   Note that the bundled executable can be slow to initialize.<br />
   This is because python itself is bundled into the ecli binary<br />
   The python package runs much faster, as there<br />
   is no need unpacking resources.<br />
   Also, it has a much slower release cadence.
1. If you are behind a corporate proxy, and get SSL errors 
   when installing, try your installation command with 
   the `--trusted-host` flags, as with:<br />
```bash
pip3 install \
--trusted-host=pypi.org \
--trusted-host=github.com \
--trusted-host=files.pythonhosted.org \
git+https://github.com/berttejeda/bert.ecli.git
```

The next section will cover Plugins.

[Back to Top](#top)
<a name="plugin-architecture"></a>
# Plugin Architecture

As mentioned before, the ecli plugins extend the base command module.
That is, for every plugin detected, a new ecli subcommand is made available.

<a name="creating-plugins"></a>
## Creating Plugins

Plugins are really easy to create, as they are simply executable 
files neatly organized into folders bearing the name of 
the plugin's namespace.

You need only enough proficiency to write a script in either bash,<br /> 
python, powershell, or ruby to get started. 
I will eventually add binaries (e.g. golang, Windows .exe's) 
and rust to the mix.

<a name="installing-plugins"></a>
## Installing Plugins

Invoke the `plugins.install` built-in subcommand to install a 
given plugin repo. The syntax is `ecli plugins.install -S -r <gitrepo>`.

You can install my plugin repo to start:

`ecli plugins.install -S -r https://github.com/berttejeda/bert.ecli.plugins.git -a ecli.plugins`

Once you've installed a plugin repo, run `ecli` to get 
the list of newly available subcommands 

The usage examples in the following sections 
assume you've installed the plugin repository above.

[Back to Top](#top)
# Usage examples

<a name="usage-examples---utilizing-windows-credentials-manager"></a>
## Usage examples - Utilizing Windows Credentials Manager

We'll be demonstrating ecli's integration with 
Windows Credential Manager.

The first step is to create Windows Generic Credentials 
a given subcommand.

You can do that by launching credential 
manager via ecli: `ecli system.launcher -n cred-mgr`

Once the Windows Credential manager is in view,

- Click Windows Credentials
- Then click Add generic credential
  - Internet or network address: {{ name_of_subcommand }}
  - User name: {{ username }}
  - Password: {{ password }}

With these populated, ecli should be able to read 
from the Windows credential store when you
call the given subcommand with the `--use-cred-mgr flag`.

Doing so will populate variables _$username_ and  _$password_ during command runtime.

[Back to Top](#top)
<a name="appendix"></a>
# Appendix

<a name="sub-command-naming-logic"></a>
## Sub-Command naming logic

As mentioned in the previous sections, commands follow a dot-notation style of reference,<br />
e.g. _pluginfolder.namespace.command_.

Of note is that the _pluginfolder_ prefix only takes effect for<br />
plugin folders not bearing a name similar to _ecli.plugins_ e.g. a plugin folder<br />
named _foo_ will yield plugins conforming to _foo.namespace.command_.

However, if a plugin folder name matches the regular expression _ecli.plugins[\W]+?|ecli.plugins_, <br />
its effective name will be stripped of that pattern, i.e. the following plugin folders:<br />

- ecli.plugins
- ecli.plugins-fork
- ecli.plugins01
- ecli.plugins-02
- ecli.plugins.new

will yield sub-commands with the following dot-notation (respectively):

- _namespace.command_
- _fork.namespace.command_
- _01.namespace.command_
- _02.namespace.command_
- _new.namespace.command_