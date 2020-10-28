#!/usr/bin/python3

# Utility script to find staking-payouts information
# for a _Stash_ account

# Usage:
#   pendingPayout.py [-s <sidecarUrl>] [-a <accountId>] [-d <depth>] [-e <era>] [-c]
#       <sidecarUrl> : the url of the sidecar instance (default is http://127.0.0.1:8080)
#       <accountId> : the staking account id (default is the last block author)
#       <depth> : the number of eras to query for payouts of (default is 5)
#       -c : query all payouts (default queries only unclaimed payouts)
#

import requests
import getopt
import json
import sys

CFG_DEF_SIDECAR_URL = 'http://127.0.0.1:8080'
CFG_DEF_DEPTH = 8

CFG_DEF_TOKEN_SYMB = 'KSM'
CFG_DEF_TOKEN_DECIMAL = 12

# ==============================================================================================
# Sidecar IO functions
# ==============================================================================================
class SidecarIO:

    def __init__(self, sidecar_url, account_id, depth, era, unclaimed_only):
        self.sidecar_url = sidecar_url
        self.account_id = account_id
        self.depth = depth
        self.era = era
        self.unclaimed_only = unclaimed_only
        self.calcu_payouts = {
                "valid": False,
                "claimed_total_payout": 0,
                "unclaimed_total_payout": 0,
                "total_payout": 0,
                "payouts_number": 0
            }

    def request_sidecar(self, req_endpoint ):
        sidecar_response = requests.get( req_endpoint )
        if sidecar_response.status_code == 200:
            return json.loads(sidecar_response.text)
        print(f'Sidecar request { req_endpoint } returns {sidecar_response.status_code}. Exiting.')
        sys.exit(sidecar_response.status_code)

    def request_last_block_author(self):
        return self.request_sidecar(f'{self.sidecar_url}/blocks/head')['authorId']

    def request_staking_payouts(self):
        print(f'Loading pending payouts of account {self.account_id} ...')
        request_params = f'depth={self.depth}&unclaimedOnly={str(self.unclaimed_only).lower()}'
        if self.era != -1:
            request_params += f'&era={self.era}'
        return self.request_sidecar(f'{self.sidecar_url}/accounts/{self.account_id}/staking-payouts?{request_params}')

    def check_ioparams(self):
        if len(self.account_id) == 0:
            print('Get address of last block ...')
            self.account_id = self.request_last_block_author()

    # ==============================================================================================
    # Request, Receive & Process the Payout Info
    # ==============================================================================================
    def process_payouts(self):
        try:
            staking_payouts = self.request_staking_payouts()
            eras_payouts = staking_payouts['erasPayouts']
            for era_payout in eras_payouts:
                payouts = era_payout['payouts']
                for payout in payouts:
                    payout_value = int(payout['nominatorStakingPayout'])
                    self.calcu_payouts["payouts_number"] += 1
                    self.calcu_payouts["total_payout"] += payout_value
                    if payout['claimed']:
                        self.calcu_payouts["claimed_total_payout"] += payout_value
                    else:
                        self.calcu_payouts["unclaimed_total_payout"] += payout_value
            self.calcu_payouts["valid"] = True
        except:
            print("Something went wrong")
            self.calcu_payouts["valid"] = False

    # ==============================================================================================
    # Payout Info Format & Display
    # ==============================================================================================
    def format_payout(self, payout):
        one_token = 10 ** CFG_DEF_TOKEN_DECIMAL
        one_milli_token = 10 ** (CFG_DEF_TOKEN_DECIMAL - 3)
        if payout >= one_token:
            return "%.3f%s" % (payout / one_token, CFG_DEF_TOKEN_SYMB)
        return "%.3fm%s" % (payout / one_milli_token, CFG_DEF_TOKEN_SYMB)

    def display_results(self):
        print(f'Account {self.account_id} received {self.calcu_payouts["payouts_number"]} payouts for {self.depth} era(s).')
        if self.unclaimed_only:
            print(f'Total payout unclaimed is {self.format_payout(self.calcu_payouts["unclaimed_total_payout"])}')
        else:
            print(f'Total payout is {self.format_payout(self.calcu_payouts["total_payout"])}')
            print(f'{self.format_payout(self.calcu_payouts["claimed_total_payout"])} has been claimed.')
            print(f'Still {self.format_payout(self.calcu_payouts["unclaimed_total_payout"])} to claimed.')

# ==============================================================================================
# Generic Util functions
# ==============================================================================================
def help_message(exit_code=0):
    print('pendingPayout.py [-s <sidecarUrl>] [-a <accountId>] [-d <depth>] [-e <era>] [-c]')
    sys.exit(exit_code)

def get_cli_options(argv):
    sidecar_url = CFG_DEF_SIDECAR_URL
    account_id = ''
    depth = CFG_DEF_DEPTH
    era = -1
    unclaimed_only = True
    try:
        opts, args = getopt.getopt(argv, "hs:a:d:e:c", ["sidecar=", "accountId=", "depth=", "era=", "all"])
    except getopt.GetoptError:
        help_message(2)
    for opt, arg in opts:
        if opt == '-h':
            help_message()
        elif opt in ("-s", "--sidecar"):
            sidecar_url = arg
        elif opt in ("-c", "--all"):
            unclaimed_only = False
        elif opt in ("-a", "--accountId"):
            account_id = arg
        elif opt in ("-d", "--depth"):
            depth = arg
        elif opt in ("-e", "--era"):
            era = arg
    return sidecar_url, account_id, depth, era, unclaimed_only

# ==============================================================================================
# Generic Util functions :: main
# ==============================================================================================
if __name__ == "__main__":
    sidecar_url, account_id, depth, era, unclaimed_only = get_cli_options(sys.argv[1:])
    handle_sidecario = SidecarIO( sidecar_url, account_id, depth, era, unclaimed_only )
    handle_sidecario.check_ioparams( )
    handle_sidecario.process_payouts( )

    if handle_sidecario.calcu_payouts["valid"] is True:
        handle_sidecario.display_results()
    else:
        print('Sidecar query failed ...')
