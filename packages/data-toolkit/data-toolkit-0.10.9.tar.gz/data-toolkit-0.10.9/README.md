# ML & data helper code!
Jakub Langr (c) 2021

This is a CLI utility for speeding up basic Data Engineering/Data Science tasks

Namely there are several functions: 
```
sub-commands:
  {cai,config,ec2,fls,gcp,gh,hist,load,monitor,nf,py,run,s3,sftp,sg,ssh,td,viz}
    cai                 Ops with Codex AI from OpenAI.
    config              Operations with config.
    ec2                 AWS EC2 helper commands.
    fls                 Display all available Fluidstack nodes.
    gcp                 GCP VM Instances helper commands.
    gh                  All Github related operations
    hist                Operations on CLI hist
    load                Appends defaults: from zshrc.txt to ~/.bashrc or
                        ~/.zshrc or tmux conf
    monitor             Monitor lack of GPU activity. When there is none, runs
                        -job
    nf                  Displays the number of files
    py                  Execute a Python command across all files in current
                        dir.
    run                 Operations with snippets
    s3                  Operations with s3 bucket creationlabs-raw-data
    sftp                Operations to easily work with remote servers /
                        devices
    sg                  AWS Security Groups helper functions
    ssh                 Operations on the SSH config
    td                  Manage TODOs using Google Keep
    viz                 Basic viz using streamlit for image comparisons

```
The screen above can be called using:
```
dt -h
```

The commands above can be generally called in the pattern:
```
dt command sub-command [args]
``` 

For example, to run to list the running ec2 isntances run 

```
dt ec2 ls --profile <profile>
```

## Installation

```
$ pip install data-toolkit
```

## Development

This project includes a number of helpers in the `Makefile` to streamline common development tasks.

### Environment Setup

The following demonstrates setting up and working with a development environment:

```
### create a virtualenv for development

$ make virtualenv

$ source env/bin/activate


### run dt cli application

$ dt --help


### run pytest / coverage

$ make test
```