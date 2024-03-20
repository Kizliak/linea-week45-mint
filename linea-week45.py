from web3 import Web3
import time, random, requests, json
from decimal import Decimal
from loguru import logger
from tqdm import tqdm
from sys import stderr
from random import (
    randint,
    uniform,
)

############################## Config #################################################

time_delay_min = 60  # Min delay between accs in mili seceonds
time_delay_max = 180  # Max delay between accs in mili seceonds

#######################################################################################

logger.remove()
logger.add(stderr, format="<lm>{time:YYYY-MM-DD HH:mm:ss}</lm> | <level>{level: <8}</level>| <lw>{message}</lw>")
web3 = Web3(Web3.HTTPProvider('https://linea.blockpi.network/v1/rpc/public'))

def add_gas_limit(tx):
    try:
        tx['gas'] = web3.eth.estimate_gas(tx)
    except:
        tx['gas'] = random.randint(220000, 250000)
    return tx

def mintNFT(private_key, address_wallet, data, toContract, quest):
    txData = {
        'from': address_wallet,
        'to': Web3.to_checksum_address(toContract),
        'nonce': web3.eth.get_transaction_count(address_wallet),
        'gasPrice': int(web3.eth.gas_price * uniform(1.01, 1.02)),
        'value': 0,
        'gas': 0,
        'data': data
        }    
    add_gas_limit(txData)
    signed_tx = web3.eth.account.sign_transaction(txData, private_key)
    
    try:
        raw_tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_hash = web3.to_hex(raw_tx_hash)
        tx_receipt = web3.eth.wait_for_transaction_receipt(raw_tx_hash, timeout=600)
        status = tx_receipt.status
        if status == 1:
            logger.success(f'Minted {quest} NFT https://lineascan.build/tx/{tx_hash}\n')
            return True
        else:
            if getTxStatus(tx_hash): 
                logger.success(f'Minted {quest} NFT https://lineascan.build/tx/{tx_hash}\n')
                return True
            else:
                logger.error(f'Mint {quest} NFT failed. TX status = {status} \n')
                return False
    except Exception as e:
        logger.error(f'Mint {quest} NFT failed: {e}\n')
        return False
        
def getTxStatus(tx_hash):
    time.sleep(30)
    tx_receipt = web3.eth.get_transaction_receipt(tx_hash)
    status = tx_receipt.status
    returnStatus = True if status == 1 else False
    return returnStatus

def main():
    print()
    print('This script will mint Linea NFT for 3 quests in week-4 and week-5: Omnizone Attraction, Battlemon and LuckyCat')
    print()

    with open("private_key.txt", "r") as f:
        keys_list = [row.strip() for row in f]
        
    count_wallets = len(keys_list)
    number_wallets = 0

    while keys_list:
        key = keys_list.pop(0)
        number_wallets += 1
        address_wallet = web3.eth.account.from_key(key).address
        print(f'{number_wallets}/{count_wallets} - {address_wallet}\n')
        mintNFT(key, address_wallet, '0x6871ee40', '0x578705c60609c9f02d8b7c1d83825e2f031e35aa', 'battlemon') # battlemon https://lineascan.build/address/0x578705c60609c9f02d8b7c1d83825e2f031e35aa
        time.sleep(15)
        mintNFT(key, address_wallet, '0x1249c58b', '0x7136abb0fa3d88e4b4d4ee58fc1dfb8506bb7de7', 'omnizone') # omnizone https://lineascan.build/address/0x7136abb0fa3d88e4b4d4ee58fc1dfb8506bb7de7
        time.sleep(15)
        mintNFT(key, address_wallet, '0x70245bdc', '0xc577018b3518cd7763d143d7699b280d6e50fdb6', 'adoptCat') # adoptCat https://lineascan.build/address/0xc577018b3518cd7763d143d7699b280d6e50fdb6
        time.sleep(15)
            
        sleepDelay = random.randint(time_delay_min, time_delay_max)
        for i in tqdm(range(sleepDelay), desc='sleep ', bar_format='{desc}: {n_fmt}/{total_fmt}'):
            time.sleep(1)
        print()
    print('Done! Subscribe if you want more https://t.me/legalcrypt')
main()