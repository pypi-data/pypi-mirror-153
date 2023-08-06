import requests
import urllib.request
import glob

class FortniteAPI:
    #aes
    class aes:
        def build():
            try:
                return requests.get("https://fortnite-api.com/v2/aes").json()["data"]["build"]
            except:
                print("ERROR : can't connect to API please try again later.")

        def main_key():
            try:
                return requests.get("https://fortnite-api.com/v2/aes").json()["data"]["mainKey"]
            except:
                print("ERROR : can't connect to API please try again later.")

        def updated():
            try:
                return requests.get("https://fortnite-api.com/v2/aes").json()["data"]["updated"]
            except:
                print("ERROR : can't connect to API please try again later.")


    #news
    class news:
        def image_gif():
            try:
                return requests.get("https://fortnite-api.com/v2/news/br").json()["data"]["image"]
            except:
                print("ERROR : can't connect to API please try again later.")

        def date():
            try:
                return requests.get("https://fortnite-api.com/v2/news/br").json()["data"]["date"]
            except:
                print("ERROR : can't connect to API please try again later.")

        def hash():
            try:
                return requests.get("https://fortnite-api.com/v2/news/br").json()["data"]["hash"]
            except:
                print("ERROR : can't connect to API please try again later.")


    #creator code
    class creator_code:
        def code(code):
            try:
                return requests.get(f"https://fortnite-api.com/v2/creatorcode?name={code}").json()["data"]["code"]
            except:
                print("ERROR : can't connect to API please try again later.")

        def status(code):
            try:
                return requests.get(f"https://fortnite-api.com/v2/creatorcode?name={code}").json()["data"]["status"]
            except:
                print("ERROR : can't connect to API please try again later.")


    #creative mode island
    class creative_mode_island:
        def title(code):
            try:
                return requests.get(f"https://fortniteapi.io/v1/creative/island?code={code}",
                headers = {
                    "Authorization": "f3295740-a9367ef5-9bc9935a-40dbfcd2"}).json()["island"]["title"]
            except:
                print("ERROR : can't connect to API please try again later.")

        def description(code):
            try:
                return requests.get(f"https://fortniteapi.io/v1/creative/island?code={code}",
                headers = {
                    "Authorization": "f3295740-a9367ef5-9bc9935a-40dbfcd2"}).json()["island"]["description"]
            except:
                print("ERROR : can't connect to API please try again later.")

        def published_date(code):
            try:
                return requests.get(f"https://fortniteapi.io/v1/creative/island?code={code}",
                headers = {
                    "Authorization": "f3295740-a9367ef5-9bc9935a-40dbfcd2"}).json()["island"]["publishedDate"]
            except:
                print("ERROR : can't connect to API please try again later.")

        def image(code):
            try:
                return requests.get(f"https://fortniteapi.io/v1/creative/island?code={code}",
                headers = {
                    "Authorization": "f3295740-a9367ef5-9bc9935a-40dbfcd2"}).json()["island"]["image"]
            except:
                print("ERROR : can't connect to API please try again later.")

        def creator(code):
            try:
                return requests.get(f"https://fortniteapi.io/v1/creative/island?code={code}",
                headers = {
                    "Authorization": "f3295740-a9367ef5-9bc9935a-40dbfcd2"}).json()["island"]["creator"]
            except:
                print("ERROR : can't connect to API please try again later.")


    #cosmetics
    class cosmetics:
        class fetch_by_id:
            def id(id):
                try:
                    return requests.get(f"https://fortnite-api.com/v2/cosmetics/br/{id}").json()["data"]["id"]
                except:
                    print("ERROR : can't connect to API please try again later.")

            def name(id):
                try:
                    return requests.get(f"https://fortnite-api.com/v2/cosmetics/br/{id}").json()["data"]["name"]
                except:
                    print("ERROR : can't connect to API please try again later.")

            def description(id):
                try:
                    return requests.get(f"https://fortnite-api.com/v2/cosmetics/br/{id}").json()["data"]["description"]
                except:
                    print("ERROR : can't connect to API please try again later.")

            def type(id):
                try:
                    return requests.get(f"https://fortnite-api.com/v2/cosmetics/br/{id}").json()["data"]["type"]["displayValue"]
                except:
                    print("ERROR : can't connect to API please try again later.")

            def rarity(id):
                try:
                    return requests.get(f"https://fortnite-api.com/v2/cosmetics/br/{id}").json()["data"]["rarity"]["displayValue"]
                except:
                    print("ERROR : can't connect to API please try again later.")

            def image(id):
                try:
                    return requests.get(f"https://fortnite-api.com/v2/cosmetics/br/{id}").json()["data"]["images"]["icon"]
                except:
                    print("ERROR : can't connect to API please try again later.")

            def introduction(id):
                try:
                    return requests.get(f"https://fortnite-api.com/v2/cosmetics/br/{id}").json()["data"]["introduction"]["text"]
                except:
                    print("ERROR : can't connect to API please try again later.")

            def file(id):
                try:
                    return requests.get(f"https://fortnite-api.com/v2/cosmetics/br/{id}").json()["data"]["path"]
                except:
                    print("ERROR : can't connect to API please try again later.")


    #map
    class map:
        def all_locations():
            try:
                request = requests.get("https://fortnite-api.com/v1/map").json()["data"]["pois"]
                data = ""
                for data1 in request:
                    data += str(f"{data1['name']}, ")
                return data
            except:
                print("ERROR : can't connect to API please try again later.")

        def image():
            try:
                return requests.get("https://fortnite-api.com/v1/map").json()["data"]["images"]["pois"]
            except:
                print("ERROR : can't connect to API please try again later.")


    #playlists
    class playlists:
        def all_playlists():
            try:
                request = requests.get("https://fn-api.com/api/playlists/active").json()["data"]
                allplaylists = ""
                for playlists in request:
                    allplaylists += f"{playlists['name']}, "
                return allplaylists
            except:
                print("ERROR : can't connect to API please try again later.")

        def image():
            try:
                request = requests.get("https://fn-api.com/api/playlists/active").json()["data"]
                for playlists in request:
                    if playlists["image"] == None:
                        urllib.request.urlretrieve("https://i.imgur.com/H0r1dfk.jpg", f"cache/playlists/{playlists['id']}.jpg")
                    else:
                        urllib.request.urlretrieve(playlists["image"], f"cache/playlists/{playlists['id']}.jpg")
                
                for images in glob.glob("cache/playlists"):
                    return images
            except:
                print("ERROR : can't connect to API please try again later.")