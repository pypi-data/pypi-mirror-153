"""

    Account class to provide basic functionality for convex network

"""
from typing import Any

from convex_api import Account as ConvexAPIAccount

from starfish.network.account_base import AccountBase


class ConvexAccount(ConvexAPIAccount, AccountBase):

    def sign_transaction(self, transaction: Any) -> Any:
        return self.sign(transaction)
