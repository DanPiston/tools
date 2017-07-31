import argparse
from urllib.parse import parse_qs

from colorama import Fore
from colorama import Style

'''Tool for parsing Paypal IPN messages when troubleshooting our PayPal integration'''

class PayPalIPN(object):
    subscribe_txn_type = ['cart',
                          'express_checkout',
                          'masspay',
                          'subscr_signup',
                          'recurring_payment_profile_created',
                          'virtual_terminal',
                          'web_accept']

    unsubscribe_txn_type = ['subscr_cancel',
                            'subscr_eot']

    def __init__(self, ipn_string):
        self.ipn_string = ipn_string
        self.data = parse_qs(self.ipn_string)

        for attr in self.data:
            val = self.data[attr]
            if isinstance(val, list) and len(val) == 1:
                val = val[0]

            setattr(self, attr, val)

    @property
    def action(self):
        if self.txn_type in self.subscribe_txn_type:
            return 'subscribe'
        elif self.txn_type in self.unsubscribe_txn_type:
            return 'unsubscribe'
        else:
            return None

    def __str__(self):
        return '\n'.join([f'{Fore.RED}Action{Style.RESET_ALL}: {Fore.YELLOW}"{Style.RESET_ALL}{self.action}{Fore.YELLOW}"',
                          f'{Fore.GREEN}Email{Style.RESET_ALL}:  {Fore.YELLOW}"{Style.RESET_ALL}{self.payer_email}{Fore.YELLOW}"',
                          f'{Fore.BLUE}Item{Style.RESET_ALL}:   {Fore.YELLOW}"{Style.RESET_ALL}{self.item_name}{Fore.YELLOW}"'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('ipn_string')
    args = parser.parse_args()

    ipn = PayPalIPN(args.ipn_string)
    print(ipn)


if __name__ == '__main__':
    main()
