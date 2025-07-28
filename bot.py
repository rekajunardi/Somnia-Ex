import requests
from web3 import Web3
import time
import json
import random
from eth_account.messages import encode_defunct
import config
from colorama import init, Fore
from rich.console import Console
from rich.panel import Panel
from config import *
import datetime
import sys

console = Console()


w3 = Web3(Web3.HTTPProvider(config.RPC_URL))
CHAIN_ID = config.CHAIN_ID
EXPLORER = config.EXPLORER
DELAY_BETWEEN_TX = getattr(config, "DELAY_BETWEEN_TX", 30)


ERC20_ABI = config.ERC20_ABI
POSITION_MANAGER_ABI = config.POSITION_MANAGER_ABI
SWAP_ROUTER_ABI = config.SWAP_ROUTER_ABI


WSTT_ADDRESS = config.WSTT_ADDRESS
NIA_ADDRESS = config.NIA_ADDRESS
USDTg_ADDRESS = config.USDTg_ADDRESS
POSITION_MANAGER_ADDRESS = config.POSITIONMANAGER_ADDRESS
SWAP_ROUTER_ADDRESS = config.SWAP_ROUTER_ADDRESS
QUOTER_ADDRESS = config.QUOTER
NIA_POOL_ADDRESS = config.NIA_POOL_ADDRESS
USDTg_POOL_ADDRESS = config.USDTg_POOL_ADDRESS


API_URL = "https://api.somnia.exchange"
BASE_URL = API_URL

def tampil_banner():
    banner = """[bold red]
===================================
 Somnia Exchange Auto Swap 
===================================
Powered : Hikari Projects
[/bold red]"""
    console.print(Panel.fit(banner, title="[bold yellow]Testnet Tools - Somnnia Testnet[/bold yellow]"))
def load_proxies(file_path="proxy.txt"):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

proxies_list = load_proxies()

def generate_random_address():
    return w3.eth.account.create().address

def acak_angka(min_val, max_val):
    return round(random.uniform(min_val, max_val), 6)

def sign_message(private_key, message="somnia"):
    acct = w3.eth.account.from_key(private_key)
    msg = encode_defunct(text=message)
    signed = acct.sign_message(msg)
    return signed.signature.hex()

def login_with_private_key(private_key):
    address = w3.eth.account.from_key(private_key).address
    signature = sign_message(private_key)
    url = f"{API_URL}/user/login?address={address}&signature={signature}"
    headers = {"Origin": "https://somnia.exchange", "Referer": "https://somnia.exchange"}
    try:
        response = requests.post(url, headers=headers)
        data = response.json()
        return data.get("data", {}).get("jwt")
    except Exception as e:
        print(f"Failed get data : {e}")
        return None


## fitur swap

def swap_token(private_key):
    jumlah = acak_angka(0.01, 0.02)
    amount_in_wei = w3.to_wei(jumlah, 'ether')
    account = w3.eth.account.from_key(private_key)
    address = account.address
    nonce = w3.eth.get_transaction_count(address)
    token = w3.eth.contract(address=WSTT_ADDRESS, abi=ERC20_ABI)
    router = w3.eth.contract(address=SWAP_ROUTER_ADDRESS, abi=SWAP_ROUTER_ABI)
    
    approve_tx = token.functions.approve(SWAP_ROUTER_ADDRESS, amount_in_wei).build_transaction({
    'from': address,
    'nonce': nonce,
    'gasPrice': w3.eth.gas_price,
    'chainId': CHAIN_ID
})

    try:
        estimated_gas_approve = w3.eth.estimate_gas(approve_tx)
        approve_tx['gas'] = estimated_gas_approve + 10000
    except Exception as e:
        approve_tx['gas'] = 60000

    signed_approve = w3.eth.account.sign_transaction(approve_tx, private_key)
    w3.eth.send_raw_transaction(signed_approve.rawTransaction)
    time.sleep(5)

    params = {
        "tokenIn": WSTT_ADDRESS,
        "tokenOut": NIA_ADDRESS,
        "fee": 500,
        "recipient": address,
        "amountIn": amount_in_wei,
        "amountOutMinimum": 1,
        "sqrtPriceLimitX96": 0
    }
    
    tx = router.functions.exactInputSingle(params).build_transaction({
    'from': address,
    'nonce': nonce + 1,
    'gasPrice': w3.eth.gas_price,
    'chainId': CHAIN_ID
    })

    try:
        estimated_gas_swap = w3.eth.estimate_gas(tx)
    
        tx['gas'] = estimated_gas_swap + 50000 
    except Exception as e:
        tx['gas'] = 300000

    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"Success Swap! TX Has: {EXPLORER}{tx_hash.hex()}")



def get_pool_contract(token0, token1, fee):
    return None

def add_liquidity(w3, private_key, token0_address, token1_address, amount0, amount1, position_manager, position_manager_abi, fee):
    wallet = w3.eth.account.from_key(private_key)
    address = wallet.address

    token0 = w3.eth.contract(address=token0_address, abi=ERC20_ABI)
    token1 = w3.eth.contract(address=token1_address, abi=ERC20_ABI)
    position_manager_contract = w3.eth.contract(address=position_manager, abi=position_manager_abi)

    nonce = w3.eth.get_transaction_count(address)

    tx1 = token0.functions.approve(position_manager, amount0).build_transaction({
        'from': address,
        'nonce': nonce,
        'gas': 200000,
        'gasPrice': w3.eth.gas_price
    })
    signed_tx1 = w3.eth.account.sign_transaction(tx1, private_key)
    w3.eth.send_raw_transaction(signed_tx1.rawTransaction)
    time.sleep(3)

    tx2 = token1.functions.approve(position_manager, amount1).build_transaction({
        'from': address,
        'nonce': nonce + 1,
        'gas': 200000,
        'gasPrice': w3.eth.gas_price
    })
    signed_tx2 = w3.eth.account.sign_transaction(tx2, private_key)
    w3.eth.send_raw_transaction(signed_tx2.rawTransaction)
    time.sleep(3)

    deadline = int(time.time()) + 600
    tick_lower = -60000
    tick_upper = 60000

    mint_params = {
        "token0": token0_address,
        "token1": token1_address,
        "fee": fee,
        "tickLower": tick_lower,
        "tickUpper": tick_upper,
        "amount0Desired": amount0,
        "amount1Desired": amount1,
        "amount0Min": 0,
        "amount1Min": 0,
        "recipient": address,
        "deadline": deadline
    }

    tx3 = position_manager_contract.functions.mint(mint_params).build_transaction({
        'from': address,
        'nonce': nonce + 2,
        'value': 0,
        'gas': 800000,
        'gasPrice': w3.eth.gas_price
    })
    signed_tx3 = w3.eth.account.sign_transaction(tx3, private_key)
    tx_hash3 = w3.eth.send_raw_transaction(signed_tx3.rawTransaction)
    print("Sending Add LP")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash3)
    return tx_hash3.hex()

def main(jumlah_tx=1, jumlah_swap=1, jumlah_lp=1, show_banner=True):
    if show_banner:
        tampil_banner()
    print(Fore.GREEN + "Bot dimulai...\n")

    try:
        with open("privateKeys.txt", "r") as f:
            private_keys = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("File privateKeys.txt tidak ditemukan.")
        return

    proxies_list = load_proxies()

    for i, pk in enumerate(private_keys):
        print("=" * 50)
        print(f"Wallet #{i+1}")

        if not pk.startswith("0x"):
            pk = "0x" + pk

        proxy = proxies_list[i % len(proxies_list)] if proxies_list else None
        proxies = {"http": proxy, "https": proxy} if proxy else None

        try:
            w3 = Web3(Web3.HTTPProvider(RPC_URL, request_kwargs={'proxies': proxies} if proxies else {}))
            account = w3.eth.account.from_key(pk)
            address = account.address
            print(f"Wallet Address: {address}")
        except Exception as e:
            print(f"Private key tidak valid / RPC Failed: {e}")
            continue

        for sxi in range(1, jumlah_swap + 1):
            print(f"\nSwap Token ke {sxi}")
            try:
                swap_token(pk)
                time.sleep(5)
            except Exception as e:
                print(f"❗ Gagal swap: {e}")

        for lpi in range(1, jumlah_lp + 1):
            print(f"\nAdd LP #{lpi}")
            try:
                amount0 = w3.to_wei(0.01, "ether")
                amount1 = w3.to_wei(0.01, "ether")

                tx_hash = add_liquidity(
                    w3,
                    pk,
                    WSTT_ADDRESS,
                    NIA_ADDRESS,
                    amount0,
                    amount1,
                    POSITION_MANAGER_ADDRESS,
                    POSITION_MANAGER_ABI,
                    3000
                )
                print(f"Add LP Done: {EXPLORER}{tx_hash}")
                time.sleep(DELAY_BETWEEN_TX)
            except Exception as e:
                print(f"Failed Add LP: {str(e)}")
                time.sleep(5)

        print("=" * 50)


import sys
import time

def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

if __name__ == "__main__":
    INTERVAL = 43200  
    jumlah_swap = 2
    jumlah_lp = 2
    total_runs = 9999999  # total looping 

    for run_count in range(1, total_runs + 1):
        print(f"\n===== Looping ke-{run_count} =====")
        if run_count == 1:
            main(jumlah_swap, jumlah_lp)
        else:
            main(jumlah_swap, jumlah_lp)

    print(f"\n⏳ Semua looping selesai. Countdown {format_time(INTERVAL)} sebelum running bot berikutnya...\n")

    for remaining in range(INTERVAL, 0, -1):
        sys.stdout.write(f"\rCountdown: {format_time(remaining)}")
        sys.stdout.flush()
        time.sleep(1)
    print("\rMemulai ulang bot!         \n")
