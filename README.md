# Somnia Exchange Auto Bot
---

## FITUR UTAMA

| Fitur              | Keterangan                                                                               |
|--------------------|------------------------------------------------------------------------------------------|
| Auto Swap          | Swap token menggunakan smart contract (real transaction)                                 |
| Multi Wallet       | Bisa jalankan banyak wallet sekaligus                                                    |
| TX Explorer          | Tampilkan link TX langsung ke explorer (https://http://shannon-explorer.somnia.network/) |

---

## STRUKTUR FILE

| File              | Deskripsi                                                               |
|-------------------|-------------------------------------------------------------------------|
| `bot.py`          | File utama bot, sudah all-in-one                                        |
| `privateKeys.txt` | List private key (1 wallet per baris)                                   |

---

## PERSIAPAN SEBELUM RUNNING

### 1. Install Python 3.10+
Download & install dari: [https://www.python.org/downloads/](https://www.python.org/downloads/)

> Jangan lupa centang opsi `Add Python to PATH` saat install!

---

### 2. Install Modul Wajib

```
git clone https://github.com/rekajunardi/Somnia-Ex.git
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
