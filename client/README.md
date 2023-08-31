# ringling-cli
Command-line interface for the Ringling model management service

## Installing ringling-cli
Ringling-cli requires Python 3.8 or higher, and interfaces with [Ringling](https://github.com/msoe-dise-project/ringling)

## Getting ringling-cli
Download Ringling-cli by cloning the git repository:

```bash
$ git clone https://github.com/msoe-dise-project/ringling-cli
```

## Option 1. Install in Virtual Environment
If you would prefer to use a virtual environment instead of installing system wide, you can:

#### Linux:
```bash
$ cd ringling-cli
$ python3 -m venv venv
$ source venv/Scripts/activate
$ python3 setup.py install
```

Ringling-cli will install the script located under `venv/bin` system wide.  The binary will be on your path when the virtual environment is activated.

## Option 2. Install System-Wide
You can install Ringling-cli using Python's setup tools:

#### Linux:
```bash
$ cd ringling-cli
$ sudo python3 setup.py install
```


Ringling-cli will install the script located under `bin/` system wide.

## What Next?
Now that Ringling-cli is installed, make sure you have [Ringling](https://github.com/msoe-dise-project/ringling)'s REST service running before using
