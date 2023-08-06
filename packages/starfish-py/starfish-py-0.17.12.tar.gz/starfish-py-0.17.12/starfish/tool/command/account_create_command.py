"""

    Tool command Account Create


"""
import logging
import os
from typing import Any

from convex_api import KeyPair

from .command_base import CommandBase

logger = logging.getLogger(__name__)


class AccountCreateCommand(CommandBase):

    def __init__(self, sub_parser: Any = None) -> None:
        super().__init__('create', sub_parser)

    def create_parser(self, sub_parser):
        parser = sub_parser.add_parser(
            self._name,
            description='Create a new account',
            help='Create a new account'

        )
        parser.add_argument(
            'password',
            help='Password of new account'
        )

        parser.add_argument(
            'keyfile',
            nargs='?',
            help='Optional name of the keyfile to write the account key data to'
        )
        return parser

    def execute(self, args: Any, output: Any) -> None:
        network = self.get_network(args.url)
        key_pair = None
        if args.password and args.keyfile:
            key_pair = KeyPair.import_from_file(args.keyfile, args.password)
        else:
            key_pair = KeyPair()
        account = network.create_account(key_pair)
        logger.debug(f'create new account {account.address}')
        if args.keyfile and not os.path.exists(args.keyfile):
            logger.debug(f'writing key file to {args.keyfile}')
            account.key_pair.export_to_file(args.keyfile, args.password)
        else:
            logger.debug('writing key file to ouptut')
            output.add_line(account.key_pair.export_to_text(args.password))
        output.add_line(account.address)
        output.set_value('public_key', account.public_key)
        output.set_value('export_key', account.key_pair.export_to_text(args.password))
        output.set_value('address', account.address)
