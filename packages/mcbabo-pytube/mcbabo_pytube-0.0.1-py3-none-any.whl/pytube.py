import httpx


class PyTube:
    """
    PyTube class for basic utils
    Attributes
    -----------
    api_key: :class:`str`
        Personal Google API Key
    latitude: :class:`str`
        Latitude of your search location
    longitude: :class:`str`
        Longitude of your search location
    radius: :class:`str`
        Search radius of your location
    region_code: :class:`str`
        Country Code ISO 3166 Alpha 2
    """

    def __init__(self, api_key: str, **kwargs: str) -> None:
        self.api_key = api_key
        self.latitude = kwargs.get("latitude", "")
        self.longitude = kwargs.get("longitude", "")
        self.radius = kwargs.get("radius", "")
        self.region_code = kwargs.get("region_code", "")
        self.url = "https://www.googleapis.com/youtube/v3/"
        self.session = httpx.AsyncClient()

    async def get_channel_statistics(self, channel_id: str) -> dict:
        """
        Get statistics of a youtube channel with id
        Attributes
        -----------
        channel_id: :class:`str`
            Channel ID of youtube channel
        """

        url = self.url + f'channels?part=statistics&id={channel_id}&key={self.api_key}'
        data = await self.fetch(url)
        print(url)
        return data

    async def get_videos(self, search: str, count: int = 8, order: str = "relevance") -> dict:
        """
        Get video data of search
        -----------
        search :class:`str`
            Keywords you search for
        count :class:`str`
            Amount of fetched videos
        order :class:`str`
            Search order (date, relevance, viewCount, rating, title)
        """
        url = self.url + f'search?part=snippet&q="{search}"&maxResults={count}&key={self.api_key}&type=video&region={self.region_code}&order={order}'
        data = await self.fetch(url)
        return data

    async def fetch(self, url) -> dict:
        resp = await self.session.get(url)
        return resp.json()
