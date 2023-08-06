"""

    Network class to provide basic functionality for convex network

"""
from convex_api import (
    API,
    KeyPair
)

from starfish.network.convex.convex_account import ConvexAccount
from starfish.network.network_base import NetworkBase
from starfish.types import AccountAddress

DEFAULT_PACKAGE_NAME = 'starfish.network.convex.contract'

DID_CONTRACT_NAME = 'starfish.did'
PROVENANCE_CONTRACT_NAME = 'starfish.provenance'


class ConvexNetwork(NetworkBase):
    def __init__(self, url: str, contract_names=None) -> None:
        NetworkBase.__init__(self, url)
        self._convex = API(url)
        self._contract_names = contract_names or {}
        from starfish.network.convex.contract.contract_manager import ContractManager
        self._manager = ContractManager(self._convex, DEFAULT_PACKAGE_NAME)

    def create_account(self, key_pair: KeyPair = None) -> ConvexAccount:
        return self._convex.create_account(key_pair)

    def load_account(self, name, key_pair: KeyPair) -> ConvexAccount:
        return self._convex.setup_account(name, key_pair)

    def setup_account(self, name, key_pair: KeyPair) -> ConvexAccount:
        return self._convex.setup_account(name, key_pair)

    def register_account_name(self, name, account: ConvexAccount) -> ConvexAccount:
        return self._convex.setup_account(name, account)

    """

    Register DID with a DDO and resolve DID to a DDO

    """
    def register_did(self, account: ConvexAccount, did: str, ddo_text: str) -> bool:
        ddo_registry_contract = self._manager.load(
            'DIDContract',
            self._contract_names.get('DIDContract', DID_CONTRACT_NAME)
        )
        if ddo_registry_contract:
            return ddo_registry_contract.register_did(did, ddo_text, account)

    def resolve_did(self, did: str, account_address: AccountAddress = None) -> str:
        ddo_registry_contract = self._manager.load(
            'DIDContract',
            self._contract_names.get('DIDContract', DID_CONTRACT_NAME)
        )
        if account_address is None:
            account_address = ddo_registry_contract.address
        if ddo_registry_contract:
            return ddo_registry_contract.resolve(did,  account_address)
        return None

    """

    Register Provenance

    """
    def register_provenance(self, account: ConvexAccount, asset_id: str, data: str):
        provenance_contract = self._manager.load(
            'ProvenanceContract',
            self._contract_names.get('ProvenanceContract', PROVENANCE_CONTRACT_NAME)
        )
        result = provenance_contract.register(asset_id, data, account)
        return result

    def get_provenance_event_list(self, asset_id: str):
        provenance_contract = self._manager.load(
            'ProvenanceContract',
            self._contract_names.get('ProvenanceContract', PROVENANCE_CONTRACT_NAME)
        )
        return provenance_contract.event_list(asset_id, provenance_contract.address)

    @property
    def convex(self):
        return self._convex
