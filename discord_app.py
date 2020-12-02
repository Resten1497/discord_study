import discord

import json
import requests
from bs4 import BeautifulSoup

hdr =  {'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
'User-Agent' : ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'), }


client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.author.bot:  # discord.User.bot 프로퍼티가 참일 때
        return

    if message.content.startswith('!ping'):
        #await message.channel.send('pong')
        e = discord.Embed(title='foo')
        await message.channel.send('Hello', embed=e)
    if message.content.startswith('!유저정보'):
        #await message.channel.send('pong')
        if "$" not in message.content:
            await message.channel.send('값이 잘못 요청되었습니다!')
            await message.channel.send('!유저정보$<유저이름>')

        else :
            userName = message.content.split("$")[1]
            result = getUserData(userName)
            embed = discord.Embed(title=result["tierRank"], color=0xc81e1e)
            embed.set_author(name="유저 조회 결과")
            embed.set_thumbnail(url=result["userImage"])
            for i in result['result']:
                embed.add_field(name=i['ChampName']+" - "+i["GameResult"], value=i["Kill"]+" / "+i["Death"]+" / "+i["assist"], inline=False)
            await message.channel.send(embed=embed)


def getUserData (userName):
    print(userName)
    response = requests.get("https://www.op.gg/summoner/userName=" + userName, headers=hdr)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # print(soup)

    result = []
    dictResult = {}

    item = soup.select('.GameItemList')
    for i in range(0, 12):
        dictValue = {}
        dictValue["GameResult"] = item[0].select('.GameResult')[i].text.strip()
        dictValue["ChampName"] = item[0].select('.ChampionName')[i].text.strip()
        dictValue["Kill"] = item[0].select('.KDA')[i * 2].select('.KDA ')[0].select_one('.Kill').text
        dictValue["Death"] = item[0].select('.KDA ')[i * 2].select('.KDA ')[0].select_one('.Death').text
        dictValue["assist"] = item[0].select('.KDA ')[i * 2].select('.KDA ')[0].select_one('.Assist').text
        result.append(dictValue)
    dictResult["userName"] = userName
    dictResult["userImage"] = "https:" + soup.select(".ProfileIcon > img")[0].attrs['src']
    dictResult["tierRank"] = soup.find('div', class_='TierRank').text.strip()
    dictResult["result"] = result

    json_val = json.dumps(dictResult, ensure_ascii=False)
    result = json.loads(json_val)
    return result

client.run('token')
