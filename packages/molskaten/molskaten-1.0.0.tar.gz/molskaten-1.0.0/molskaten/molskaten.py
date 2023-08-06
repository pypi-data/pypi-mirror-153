import json
from datetime import datetime

import requests
import xmltodict


class Molskaten:
    def __init__(self, school: str, baseUrl="https://skolmaten.se"):
        self.endpoint = "{}/{}/rss".format(baseUrl, school)
        self.school = school

    def getData(self):
        r = requests.get(self.endpoint)
        food = []

        if r.status_code == 200:
            # First we need to parse the xml data from the request, then we convert it to json
            data = json.dumps(xmltodict.parse(r.text))

            # Then we convert it to dict, we need to do this to avoid OrderedDict. :(
            data = json.loads(data)["rss"]["channel"]

            for i in data["item"]:

                # This parses the date from the rss.
                pubDate = i["pubDate"].split(" ")

                # This fixes the date parsed to "DAY MONTH YEAR".
                fixedDate = "{} {} {}".format(pubDate[1], pubDate[2], pubDate[3])

                # Then this makes it eaiser to use the date.
                date = datetime.strptime(fixedDate, "%d %b %Y")

                # Then we append it to the food array.
                food.append({"date": date, "food": i["description"].split("<br/>")})

            return food
        else:
            return []
