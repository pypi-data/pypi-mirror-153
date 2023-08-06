# FreeFortniteAPI
![PyPI Python Version](https://img.shields.io/pypi/pyversions/fortnite-api?label=python%20version&logo=python&logoColor=yellow)
[![discord server invite](https://discordapp.com/api/guilds/881251978951397396/embed.png)](https://discord.com/invite/pFUTyqqcUx)
Easy to use FreeFortniteAPI module.

## Installing

Python 3.5 or higher is required

```
pip install FreeFortniteAPI
```

## Documentation

To get started we first need to import the api and initialize the client.

```
import FreeFortniteAPI

api = FreeFortniteAPI.FortniteAPI
```

## Aes
```
api.aes.build()
api.aes.main_key()
api.aes.updated()
```

## News
```
api.news.image_gif()
api.news.date()
api.news.hash()
```

## Creator Code
```
api.creator_code.code("{creator code}")
api.creator_code.status("{creator code}")
```

## Creative Mode Island
```
api.creative_mode_island.title("{island code}")
api.creative_mode_island.description("{island code}")
api.creative_mode_island.published_date("{island code}")
api.creative_mode_island.image("{island code}")
api.creative_mode_island.creator("{island code}")
```

## Cosmetics By ID
```
api.cosmetics.fetch_by_id.id("{id of the cosmetic}")
api.cosmetics.fetch_by_id.name("{id of the cosmetic}")
api.cosmetics.fetch_by_id.description("{id of the cosmetic}")
api.cosmetics.fetch_by_id.type("{id of the cosmetic}")
api.cosmetics.fetch_by_id.rarity("{id of the cosmetic}")
api.cosmetics.fetch_by_id.image("{id of the cosmetic}")
api.cosmetics.fetch_by_id.introduction("{id of the cosmetic}")
api.cosmetics.fetch_by_id.file("{id of the cosmetic}")
```

## Map
```
api.map.all_locations()
api.map.image()
```

## Playlists
```
api.playlists.all_playlists()
api.playlists.image()
```