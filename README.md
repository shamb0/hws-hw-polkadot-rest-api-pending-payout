# Demo on Polkadot REST API | Pending payout

# [ADVANCED CHALLENGE] REST APIs - Read an account's pending payouts | Trace Logs

---

## HOWTO use the script

```shell
$ python3 ./sol001-py-pendingpayout/pendingPayout.py --help
pendingPayout.py [-s <sidecarUrl>] [-a <accountId>] [-d <depth>] [-e <era>] [-c]

```

---

## Verification on Local dev net

### Launch polkadot node in dev mode

![](https://i.imgur.com/OIb1Yg7.png)

### Launch Substrate REST API server

```shell
  master ±  NODE_ENV=local yarn start
yarn run v1.22.4
$ yarn run build && yarn run main
$ rimraf build/ && tsc
$ node ./build/src/main.js
SAS:
  📦 LOG:
     ✅ LEVEL: "info"
     ✅ JSON: false
     ✅ FILTER_RPC: false
     ✅ STRIP_ANSI: false
  📦 SUBSTRATE:
     ✅ WS_URL: "ws://127.0.0.1:9944"
  📦 EXPRESS:
     ✅ BIND_HOST: "127.0.0.1"
     ✅ PORT: 8080
2020-10-27 20:47:36 info: Connected to chain Development on the parity-polkadot client at ws://127.0.0.1:9944
2020-10-27 20:47:36 info: Listening on http://127.0.0.1:8080/
```

### Verification of node status on polkadot.js UI

![](https://i.imgur.com/Qy8ShGh.png)

### Verification of pending payout utility script

```shell
$ python3 ./sol001-py-pendingpayout/pendingPayout.py -a 5GNJqTPyNqANBkUVMN1LPPrxXnFouWXoe2wNSmmEoLctxiZY -d 5
Loading pending payouts of account 5GNJqTPyNqANBkUVMN1LPPrxXnFouWXoe2wNSmmEoLctxiZY ...
Account 5GNJqTPyNqANBkUVMN1LPPrxXnFouWXoe2wNSmmEoLctxiZY received 0 payouts for 5 era(s).
Total payout unclaimed is 0.000mKSM
```


---

## Verification on kusama mainnet

### Launch Substrate REST API server

![](https://i.imgur.com/91gC3lt.png)

### Verification of pending payout utility script

```shell
python3 ./sol001-py-pendingpayout/pendingPayout.py --all
Get address of last block ...
Loading pending payouts of account FFdDXFK1VKG5QgjvqwxdVjo8hGrBveaBFfHnWyz1MAmLL82 ...
Account FFdDXFK1VKG5QgjvqwxdVjo8hGrBveaBFfHnWyz1MAmLL82 received 8 payouts for 8 era(s).
Total payout is 618.312mKSM
0.000mKSM has been claimed.
Still 618.312mKSM to claimed.
```
