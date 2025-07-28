# Somnia Exchange Auto Bot
---

## FITUR UTAMA

| Fitur              | Keterangan                                                             |
|--------------------|------------------------------------------------------------------------|
| Auto Swap        | Swap token menggunakan smart contract (real transaction)              |
| Auto Transfer    | Kirim token ke wallet random                                           |
| Multi Wallet     | Bisa jalankan banyak wallet sekaligus                                  |
| TX Explorer Link | Tampilkan link TX langsung ke explorer (https://testnet.pharosscan.xyz) |

---

## STRUKTUR FILE

| File              | Deskripsi                                                               |
|-------------------|-------------------------------------------------------------------------|
| `bot.py`          | File utama bot, sudah all-in-one                                        |
| `privateKeys.txt` | List private key (1 wallet per baris)                                   |
| `abi.txt`         | ABI smart contract (token, router, staking)                             |

---

## PERSIAPAN SEBELUM RUNNING

### 1. Install Python 3.10+
Download & install dari: [https://www.python.org/downloads/](https://www.python.org/downloads/)

> Jangan lupa centang opsi `Add Python to PATH` saat install!

---

### 2. Install Modul Wajib

```
git clone https://github.com/rekajunardi/SOMNIA.git
```
```
cd Somnia-Ex
```
```
pip install web3 eth-account requests colorama rich
```
```
python bot.py
```

CATATAN
Semua transaksi menggunakan testnet, aman & tanpa biaya

Transaksi dilakukan langsung ke smart contract menggunakan Web3 

Script ini 100% open-source, dikembangkan bersama komunitas
