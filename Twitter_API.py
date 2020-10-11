import requests
import json

class Wrapper(object):
    """docstring for Wrapper."""

    def __init__(self, api_key, api_secret_key, access_token, access_secret, bearer):
        self.api_key = api_key
        self.api_secret_key = api_secret_key
        self.access_token = access_secret
        self.access_secret = access_secret
        self.bearer = bearer
        self.headers = {"authorization": "Bearer {BEARER_TOKEN}"}
        self.headers["authorization"] = self.headers["authorization"].format(BEARER_TOKEN=bearer)
        self.base = "https://api.twitter.com/1.1/"
    def get_reverse_location(self, lat, long):
        """
        Comment: returns location data as Name, Country, woeid and more
        Input: Name of Instance, latitude, longitude
        Output: Json Object with details for a location
        Special: Returns Location data as Json
        """
        url = self.base + "trends/closest.json"
        params = {"lat":lat, "long":long}
        headers = self.headers
        r = requests.get(url, params=params, headers=headers)
        return json.loads(r.content)

    def get_trends_woeid(self, woeid):
        """
        Comment: returns nearest trends by a woeid
        Input: name of Instance, woeid
        Output: Json object with trends
        Special: Nothing special
        """
        url = self.base + "trends/place.json"
        params = {"id":woeid}
        headers = self.headers
        r = requests.get(url, params=params, headers=headers)
        return json.loads(r.content)

    def get_sorted_trends(self, woeid):
        """
        Comment: returns a sorted list of twitter trends, descending from the Trend with most volume
        Input: name of Instance, woeid
        Output: Sorted Json List with Twitter Trends by woeid
        Special: Propably not the most efficient way of sorting but it works
        """
        trends_raw = self.get_trends_woeid(woeid)[0]["trends"]
        trends_sorted = sort_dict(trends_raw, "tweet_volume")
        return trends_sorted

    global sort_dict
    def sort_dict(dict, key_value, reverse=True):
        out = sorted(dict, key=lambda i: i[key_value], reverse=reverse)
        return out

    def get_user_info(self, username):
        """
        Comment: Get USer info by his name
        Input: Name of Instance, UserName
        Output: Details as Json
        Special: Nothing Special
        """
        url = self.base + "users/lookup.json"
        params = {"screen_name" : username}
        headers = self.headers
        r = requests.get(url, params=params, headers=headers)
        return json.loads(r.content)
    def get_statusses(self, arg):
        pass


def main():
    tokens = json.load(open("tokens.json", "r"))
    berlin_woeid = 638242
    parent_id = 23424829
    test = Wrapper(tokens["key"], tokens["secret_key"], tokens["access"], tokens["acces_secret"], tokens["bearer"])
    res = test.get_user_info("RealDonaldTrump")
    print res
    json.dump(res, open("out.json", "w"))
if __name__ == '__main__':
    main()
