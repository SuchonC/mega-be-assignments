# ERC20 Helper

A CLI program for accessing some functionalities of Ethereum block chain.

This program requires a URL endpoint to a running Ethereum node

It also uses etherscan's API to retrieve contracts' ABI

---

## Requirements

***Ethereum node URL***

You can either launch your own Ethereum node or use a public node for development purpose such as [Infura](https://infura.io/)

***API key of etherscan.io***

This program needs this API key to be able to obtain contrains' ABI and function properly.
    
You can get one by heading to [etherscan.io](https://etherscan.io/) and create a free account, from then you will have access to the API key

***Python Version***

Python 3.0+ is preferred, this program was tested on Python 3.88 and 3.7.4

---

## Installation

Clone this repository to your local machine

``` sh
git clone https://github.com/SuchonC/mega-be-assignments.git
cd ./mega-be-assignments
```

Install all the dependencies

``` sh
pip install -r requirements.txt
```

Note :

If you are using Windows you may encounter a "Microsoft visual c++ 14.0 or greater is required" error, you can follow a link [here](https://exerror.com/error-microsoft-visual-c-14-0-is-required-get-it-with-microsoft-visual-c-build-tools/) to fix the error

Next, put your Ethereum node URL and Etherscan API key in environment variables

For your node's URL, you can use ***either*** HTTP or Websocket URL.

If both are set, Websocket URL will be used

```sh
export ETHER_NODE_HTTP_URL=your_http_url
export ETHER_NODE_WEBSOCKET_URL=your_websocket_url
export ETHER_SCAN_API_KEY=your_ether_scan_api_key
```

From here you should be able to run the program

```sh
python main.py --help
```

The output should be similar to the below

```txt
Usage: main.py [OPTIONS] COMMAND [ARGS]...

  ...

Options:
  --help  Show this message and exit.

Commands:
  balance-of  Get total balance of target address in a contract
  detail      Get name, symbol and decimals of a contract
  holders     Get top N holders of a contract
  latest-tx   Get latest N transactions of a contract
  watch-tx    Watch for new transactions in a contract
```