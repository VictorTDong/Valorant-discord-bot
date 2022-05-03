import aiohttp
import json
import traceback

async def get_rank(username, tag):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.henrikdev.xyz/valorant/v1/mmr/na/{username}/{tag}") as r: data = json.loads(await r.text())

            # print(data)
            currenttierpatched = data["data"]["currenttierpatched"]
            name = data["data"]["name"]
            ranking_in_tier = data["data"]["ranking_in_tier"]
            elo = data["data"]["elo"]
            mmr_change_to_last_game = data["data"]["mmr_change_to_last_game"]

            DATA = dict(
                currenttierpatched = currenttierpatched,
                elo = elo,
                mmr_change_to_last_game = mmr_change_to_last_game,
                name = name,
                ranking_in_tier = ranking_in_tier,
            )

            return DATA
    except:
        print(traceback.format_exc())