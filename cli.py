import fire

from alphalib.dataset.yahooquery_downloader import Dataset


class AlphaLib:
    def stock_stats(self):
        dataset = Dataset()
        dataset.stock_stats()


if __name__ == "__main__":
    alphalib = AlphaLib()
    fire.Fire(alphalib)
