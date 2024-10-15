# TikTok Live Comment Listener

Program ini menggunakan library [TikTokLive](https://github.com/isaackogan/TikTokLive) untuk terhubung ke live stream TikTok dan mengumpulkan komentar dari penonton. Komentar yang diterima akan disimpan dalam file CSV untuk analisis lebih lanjut. 

## 1. Dependencies

Pastikan Anda menginstall dependensi yang diperlukan:

```bash
pip install TikTokLive pandas
```

## 2. Import Library

Di bawah ini adalah persiapan 

```python
import asyncio
from TikTokLive import TikTokLiveClient
from TikTokLive.client.logger import LogLevel
import datetime
import pandas as pd
from datetime import datetime
from TikTokLive.events import ConnectEvent, CommentEvent
```
- `asyncio` : Library bawaan Python untuk asynchronous programming.
- `TikTokLiveClient`: Client utama yang digunakan untuk terhubung dan berinteraksi dengan TikTok live stream.
- `LogLevel`: Mengatur tingkat logging dari aktivitas TikTokLiveClient.
- `datetime`: Mengelola waktu dan tanggal.
- `pandas`: Library untuk manipulasi data, digunakan untuk membaca dan menulis file CSV.
- `ConnectEvent` dan `CommentEvent`: Event yang di-trigger ketika terhubung ke live stream dan ketika menerima komentar.

## 3. Memuat Data dan Menyiapkan Struktur untuk Komentar

```python
df_komentar = pd.read_csv('komentar.csv')

komentar = {
    'datetime': [],
    'nickname': [],
    'komentar': []
}

target = '3mongkis'

```
- `df_komentar`: Membaca data komentar yang sudah ada dari file komentar.csv menggunakan pandas.
- `komentar`: Dictionary yang menyimpan data baru berupa waktu, nama pengguna, dan isi komentar yang diterima selama live.
- `target`: Username TikTok yang akan dimonitor untuk live stream, dalam contoh ini adalah `'3mongkis'`.

## 4. Fungsi untuk Menyimpan Komentar ke CSV

```python
client: TikTokLiveClient = TikTokLiveClient(
    unique_id=target
)
```

- `client`: Membuat instance TikTokLiveClient yang terhubung ke live stream pengguna TikTok berdasarkan target yang ditentukan.

## 5. Event: Saat Berhasil Terhubung

```python
@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    client.logger.info(f"Connected to @{event.unique_id}!")
    await asyncio.sleep(3600)
    for end in range(10):
        time = 10 - end
        print(f'Client will disconnect in {time}')
    await client.disconnect()
    
    save(df_komentar, komentar, 'komentar.csv')
```

- Ketika terhubung ke live stream, program akan menunggu selama satu jam ( `await asyncio.sleep(3600)` ) sebelum mulai menghitung mundur untuk memutus koneksi.
- Data komentar disimpan ke file CSV menggunakan fungsi `save`.

## 6. Event: Saat Menerima Komentar Baru

```python
@client.on(CommentEvent)
async def on_comment(event: CommentEvent) -> None:
    print(f"{datetime.now()} -> {event.user.nickname} -> {event.comment}")
    komentar['datetime'].append(datetime.now())
    komentar['nickname'].append(f'{event.user.nickname}')
    komentar['komentar'].append(f'{event.comment}')
```

- Setiap kali ada komentar baru, waktu, nama pengguna, dan isi komentar akan ditambahkan ke dictionary `komentar`.
- Komentar juga akan ditampilkan di terminal menggunakan `print`.

## 7. Memeriksa Status Live Stream

```python
async def check_loop(client):
    while True:
        while not await client.is_live():
            client.logger.info(f'{datetime.now()} -> {target} is currently not live')
            await asyncio.sleep(60)

        client.logger.info(f'{datetime.now()} -> {target} is live!')
        await client.connect()
```

Fungsi **check_loop** secara berkala memeriksa apakah pengguna `target` sedang live. Jika tidak live, akan menunggu selama 60 detik sebelum memeriksa ulang. Ketika live stream dimulai, program akan menghubungkan client ke stream tersebut.

## 8. Menjalankan Program
```python
if __name__ == '__main__':
    client.logger.setLevel(LogLevel.INFO.value)
    
    try:
        asyncio.run(check_loop(client))
    except:
        save(df_komentar, komentar, 'komentar.csv')
```

- Mengatur tingkat logging untuk menampilkan informasi penting.
- Menjalankan fungsi check_loop untuk memulai pengecekan status live.
- Jika terjadi kesalahan selama eksekusi, komentar yang sudah diterima akan disimpan ke CSV.

