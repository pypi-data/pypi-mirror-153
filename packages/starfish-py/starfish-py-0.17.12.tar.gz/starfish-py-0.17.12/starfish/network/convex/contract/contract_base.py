"""


Contract Base

"""

import re

from convex_api import API

from starfish.network.convex.contract.convex_registry import ConvexRegistry


class ContractBase:
    def __init__(self, convex: API):
        self._convex = convex
        self._name = None
        self._version = None
        self._address = None
        self._owner_address = None

    def send(self, transaction, account):
        if not self.address:
            raise ValueError(f'No contract address found for {self._name}')
        return self._convex.send(f'(call #{self.address} {transaction})', account)

    def query(self, transaction, account_address=None):
        if account_address is None:
            account_address = self.address
        if not self.address:
            raise ValueError(f'No contract address found for {self._name}')
        return self._convex.query(f'(call #{self.address} {transaction})', account_address)

    def resolve_address(self, name):
        registry = ConvexRegistry(self._convex)
        self._address = registry.resolve_address(name)
        if self._address:
            self._owner_address = registry.resolve_owner(name)
            self._name = name
        return self._address

    @property
    def deploy_version(self):
        if self.address:
            result = self.query('(version)')
            if result and 'value' in result:
                return result['value']

    @property
    def address(self):
        return self._address

    @property
    def owner_address(self):
        return self._owner_address

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version

    @staticmethod
    def escape_string(text):
        escape_text = re.sub('\\\\', '\\\\\\\\', text)
        escape_text = re.sub('"', '\\"', escape_text)
        return escape_text
