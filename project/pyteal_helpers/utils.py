from algosdk import account,mnemonic
from algosdk.future import transaction
from algosdk.kmd import KMDClient
from algosdk.v2client.algod import AlgodClient
import json

MICRO_ALGO = 1
ALGO = MICRO_ALGO * (10 ** 6)


def get_kmd_client(address="http://localhost:4002", token="a" * 64) -> KMDClient:
    return KMDClient(token, address)


def get_keys_from_wallet(
    kmd_client: KMDClient, wallet_name="unencrypted-default-wallet", wallet_password=""
) -> list[str] | None:
    wallets = kmd_client.list_wallets()

    handle = None
    for wallet in wallets:
        if wallet["name"] == wallet_name:
            handle = kmd_client.init_wallet_handle(wallet["id"], wallet_password)
            break

    if handle is None:
        raise Exception("Could not find wallet")

    private_keys = None
    try:
        addresses = kmd_client.list_keys(handle)
        private_keys = [
            kmd_client.export_key(handle, wallet_password, address)
            for address in addresses
        ]
    finally:
        kmd_client.release_wallet_handle(handle)

    return private_keys


def get_algod_client(address="http://localhost:4001", token="a" * 64):
    return AlgodClient(token, address)


def generate_account():
    (private_key, _) = account.generate_account()
    return private_key


def make_atomic(
    signing_keys=[], transactions=[]
) -> list[transaction.SignedTransaction]:
    return [
        tx.sign(key)
        for key, tx in zip(
            signing_keys, transaction.assign_group_id(transactions), strict=True
        )
    ]

def generate_algorand_keypair():
    private_key, address = account.generate_account()
    print("My address: {}".format(address))
    print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))

if __name__ == "__main__":
    acct = account.generate_account()
    address1 = acct[1]
    print("Account 1")
    print(address1)
    mnemonic1 = mnemonic.from_private_key(acct[0])

    print("Account 2")
    acct = account.generate_account()
    address2 = acct[1]
    print(address2)
    mnemonic2 = mnemonic.from_private_key(acct[0])

    print("Account 3")
    acct = account.generate_account()
    address3 = acct[1]
    print(address3)
    mnemonic3 = mnemonic.from_private_key(acct[0])
    print ("")
    print("Copy off accounts above and add TestNet Algo funds using the TestNet Dispenser at https://bank.testnet.algorand.network/")
    print("copy off the following mnemonic code for use later")
    print("")
    print("mnemonic1 = \"{}\"".format(mnemonic1))
    print("mnemonic2 = \"{}\"".format(mnemonic2))
    print("mnemonic3 = \"{}\"".format(mnemonic3))