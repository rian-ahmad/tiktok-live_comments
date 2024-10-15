import asyncio

from TikTokLive import TikTokLiveClient
from TikTokLive.client.logger import LogLevel
import datetime
import pandas as pd
from datetime import datetime
from TikTokLive.events import ConnectEvent, CommentEvent

df_komentar = pd.read_csv('komentar.csv')

komentar = {
    'datetime': [],
    'nickname': [],
    'komentar': []
}

target = '3mongkis'


def save(old_row, new_row, file):
    new_df = pd.DataFrame(new_row)
    df = pd.concat([old_row, new_df], ignore_index=True)
    df.to_csv(file, index=False, encoding='utf-8')


client: TikTokLiveClient = TikTokLiveClient(
    unique_id=target
)

@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    client.logger.info(f"Connected to @{event.unique_id}!")
    await asyncio.sleep(3600)
    for end in range(10):
        time = 10 - end
        print(f'Client will disconnect in {time}')
    await client.disconnect()
    
    save(df_komentar, komentar, 'komentar.csv')

    
@client.on(CommentEvent)
async def on_comment(event: CommentEvent) -> None:
    print(f"{datetime.now()} -> {event.user.nickname} -> {event.comment}")
    komentar['datetime'].append(datetime.now())
    komentar['nickname'].append(f'{event.user.nickname}')
    komentar['komentar'].append(f'{event.comment}')


async def check_loop(client):
    while True:
        while not await client.is_live():
            client.logger.info(f'{datetime.now()} -> {target} is currently not live')
            await asyncio.sleep(60)

        client.logger.info(f'{datetime.now()} -> {target} is live!')
        await client.connect()

if __name__ == '__main__':
    client.logger.setLevel(LogLevel.INFO.value)
    
    try:
        asyncio.run(check_loop(client))
    except:
        save(df_komentar, komentar, 'komentar.csv')
    
