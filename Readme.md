# Xserverpy

[![Build Status](https://travis-ci.org/oarrabi/xserverpy.svg?branch=master)](https://travis-ci.org/oarrabi/xserverpy)  [![PyPI version](https://badge.fury.io/py/xserverpy.svg)](http://badge.fury.io/py/xserverpy)

Xserverpy makes it possible to use Xcode bots from the command line.
<br/>

![Preview](https://raw.githubusercontent.com/oarrabi/xserverpy/master/assets/preview.gif)

# Use cases
- Running Xcode server tasks, like new integration (ie. Build project) or list bots, without the need to install or run Xcode.
- Build Xcode bots from another CI tool like Jenkins (see [Future milestones and improvements](#future-milestones-and-improvements).
- You love ASCII progress bars (or Nikola Tesla's inventions)

# Installation

## Using brew (recommended)
    brew tap oarrabi/tap
    brew install xserverpy

## Using pip
    pip install xserverpy

# Usage

## Authentication and Host information
All of xserverpy command accept authentication and Xcode server host/port as flags. For example, in order to list all the bots you would run:

    xserverpy bots --host HOST --port PORT --user USER --pass PASS

To reduce duplication in calling consequent or future commands, you can run `init` subcommand to store these configuration on your machine.

    xserverpy init --host HOST --port PORT --user USER --pass PASS    

Now that you stored them, you can call all of xcserverpy subcommands without passing these stored arguments:

    xserverpy bots
    xserverpy integrations list

xserverpy init flags:

     --host HOST          Xcode server host
     --port PORT          Xcode server host port, default 443
     --user USER          Username to use for authentication
     --password PASSWORD  Password to use for authentication
     --local              Store configuration file in the local directory

Note: 
- Running `init` sotres a configuration file at `~/.xserverpy`. 
- Using `init --local` stores the configuration in the current directory

## Bots
List all bots [Demo](http://showterm.io/1e0d25570e5c65ab57cd0)

    xserverpy bots # pass host/user info or load from stored

## Integrations
List integrations per bot [Demo](http://showterm.io/5899725079c80c3026d9d)

    xserverpy integrations list --bot <Bot name or ID>
---
Integrate (build project) [Demo](http://showterm.io/bb69e715ba165d147edf5)

    xserverpy integrations new --bot <Bot name or ID>
---
Integrate and wait [Demo](http://showterm.io/4b61beb417fe4a5b1ba25)

    xserverpy integrations new --bot <Bot name or ID> --wait
---
Show running integrations [Demo](http://showterm.io/eae3a3cabf806cc9fd84d)

    xserverpy integrations running
---
Cancel integrations (build project) [Demo](http://showterm.io/9bbb138149c147ca1c103)

    xserverpy integrations cancel --id <Integration ID>

## Note on integrate and wait
When using `xserverpy integrations new --wait`, xserverpy keeps polling Xcode server for updates on the running integrations. The default interval is .5s, you can control the behavior and the format of the progress using the following flags:

    --interval INTERVAL  Interval to poll the server for updates, default .5s
    --no-tty             Force non tty progress reporting

# Future milestones and improvements
- Create Jenkins plugin to embed Xcode server tasks in Jenkins
- Implement show all pending integrations
- Improve code coverage

# Author
Omar Abdelhafith 
[nsomar](http://nsomar.com), [nsomar medium](https://medium.com/@nsomar), [@ifnottrue](https://twitter.com/ifnottrue)

