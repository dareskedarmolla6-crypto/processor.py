class MarketFeed:
    """
    FSE Production Market Feed Layer

    Receives real market data
    through exchange adapters.
    """

    def __init__(
        self,
        adapter
    ):
        self.adapter = adapter


    def get_data(
        self
    ):

        data = self.adapter.fetch()

        if not data:
            raise RuntimeError(
                "Empty market data received"
            )

        return data
