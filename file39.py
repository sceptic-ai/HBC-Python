"""
Invoking the smart contract:

testinvoke 0x60a7ed582c6885addf1f9bec7e413d01abe54f1a register ["f572f8ce40
bf97b56bad1c6f8d62552b8b066039a9835f294ea4826629278df3","AK2nJJpJr6o664CWJKi1QRXj
qeic2zRp8y"]

testinvoke 0x60a7ed582c6885addf1f9bec7e413d01abe54f1a transfer ["f572f8ce40
bf97b56bad1c6f8d62552b8b066039a9835f294ea4826629278df3","AZ81H31DMWzbSnFDLFkzh9v
HwaDLayV7fU"]

testinvoke 0x60a7ed582c6885addf1f9bec7e413d01abe54f1a query ["f572f8ce40
bf97b56bad1c6f8d62552b8b066039a9835f294ea4826629278df3"]

import contract swiggy/supply_chain.avm 0710 05 True False

"""

from boa.interop.Neo.Runtime import Log, Notify
from boa.interop.Neo.Storage import Get, Put, GetContext
from boa.interop.Neo.Runtime import GetTrigger,CheckWitness
from boa.builtins import concat


def main(operation, args):
    nargs = len(args)
    if nargs == 0:
        print("No asset id supplied")
        return 0

    if operation == 'query':
        asset_id = args[0]
        return query_asset(asset_id)

    elif operation == 'delete':
        asset_id = args[0]
        return delete_asset(asset_id)

    elif operation == 'register':
        if nargs < 2:
            print("required arguments: [asset_id] [owner]")
            return 0
        asset_id = args[0]
        owner = args[1]
        info = args[2]
        return register_asset(asset_id, owner, info)

    elif operation == 'transfer':
        if nargs < 2:
            print("required arguments: [asset_id] [to_address]")
            return 0
        asset_id = args[0]
        to_address = args[1]
        info = args[2]
        asset_list = args[3]
        return transfer_asset(asset_id, to_address, info, asset_list)

    elif operation == 'query_asset_list':
        address = args[0]
        return query_asset_list(address)



def query_asset(asset_id):
    msg = concat("QueryAsset: ", asset_id)
    Notify(msg)

    context = GetContext()
    owner = Get(context, asset_id)
    info = Get(context, asset_id+'info')
    if not owner:
        Notify("Asset is not yet registered")
        return False

    Notify(owner)
    return info

def query_asset_list(address):

    context = GetContext()
    asset_list = Get(context, address)

    if not asset_list:
        Notify("No assets found for user")
        return False

    return asset_list


def register_asset(asset_id, owner, info):
    msg = concat("RegisterAsset: ", asset_id)
    Notify(msg)

    # removing witness check for hackathon
    if not CheckWitness(owner):
        Notify("Owner argument is not the same as the sender")
        return False

    context = GetContext()
    exists = Get(context, asset_id)
    if exists:
        Notify("Asset is already registered")
        return False

    Put(context, asset_id, owner)
    Put(context, asset_id+'info', info)
    return True


def transfer_asset(asset_id, to_address, info, asset_list):
    msg = concat("TransferAsset: ", asset_id)
    Notify(msg)

    context = GetContext()
    owner = Get(context, asset_id)
    if not owner:
        Notify("Asset is not yet registered")
        return False

    # removing witness check for hackathon
    if not CheckWitness(owner):
        Notify("Sender is not the owner, cannot transfer")
        return False

    if not len(to_address) != 34:
        Notify("Invalid new owner address. Must be exactly 34 characters")
        return False

    Put(context, asset_id, to_address)
    Put(context, asset_id+'info', info)
    Put(context, to_address, asset_list)
    return True


def delete_asset(asset_id):
    msg = concat("DeleteAsset: ", asset_id)
    Notify(msg)

    context = GetContext()
    owner = Get(context, asset_id)
    if not owner:
        Notify("Asset is not yet registered")
        return False

    if not CheckWitness(owner):
        Notify("Sender is not the owner, cannot transfer")
        return False

    Delete(context, asset_id)
    return True
