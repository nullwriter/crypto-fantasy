## Crypto-Fantasy

Donate to contribute with the project:

BTC 1FCP2Qrkkexf3zSCKu8bnxZGtbbzfkU8m7 \
ETH 0x32dB252572840D6Ab1D51E3FD2EDadc8C6C87935 \
ETC 0x8a36E1385FF1210c98cc57B0411D79E323E8d677 \
DASH XhCPHypCspaPNrqnCL99Fxkm4feM2tt8bW \
LTC LYtUzgsJwQEdJe8WLLmpdf7VrpKUNmSJQS


## Crypto fantasy trading bot for Whatsapp

Crypto-Fantasy is a cryptocurrency fantasy trading game written in Python which you play in Whatsapp (props to [Yowsup](https://github.com/tgalal/yowsup) library). It excells at multiplayer games with your friends in whatsapp groups. Using realtime data from CoinMarketCap, the objective is to trade and compete with your friends to see who makes the most money throughout a week, with a fixed starting money amount of $10,000.

Its a great way to practice trading, as well as keeping up with prices and trends. If you're into cryptocurrency, you'll love this.

## Feature list

 * help
 * tutorial
 * tick / ticker <symbol\>: returns information about the coin; price, % change, etc.
 * top <number\>: returns a list of top cryptocurrencies with prices and % change
 * buy <amount_usd> <symbol\>
 * sell $<amount_usd> <symbol\> or sell <coin_amount> <symbol\>
 * leaderboard
 * join \ play: joins the current round. Must be registered before.
 * portfolio
 * register <name\>
 * transactions (WIP)

## Installation

### One step Docker installation (recommended)

Build image:
```
docker-compose up -d
```

### Manual installation

 * Requires python 2.6+, or python3.0+
 * Required python packages: python-dateutil,
 * Required python packages for end-to-end encryption: protobuf, pycrypto, python-axolotl-curve25519
 * Requires pip
 * Requires yowsup

Install yowsup:

```
pip install yowsup2
```

Run setup.py:

```
python setup.py install
```

## Usage

* Requires mobile phone number from SIM card

First you need to [follow Yowsup's registration process](https://github.com/tgalal/yowsup/wiki/yowsup-cli-2.0#yowsup-cli-registration) to register your phone number and obtain the Whatsapp password.

Copy and rename ```credentials.txt.example``` to ```credentials.txt``` and add your login details (phone number and password provided by previous step).

Only if using Docker:

```
docker exec -it <container_id> bash
```

Then:
```
cd app
```

And type this to run on Whatsapp:
```
python3 run.py
```

Or this to run in command line for tests:
```
python3 run-cli.py
```

This will create the sqlite3 database and start the game loop. From this point, you should be able to talk to the bot. Start by sending ```help``` through whatsapp to check the commands available.


## License

crypto-fantasy is licensed under the GPLv3+: http://www.gnu.org/licenses/gpl-3.0.html.
