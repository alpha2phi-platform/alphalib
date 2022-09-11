import fire

from alphalib.dataset import Dataset


class AlphaLib(object):
    def stock_info(self, country="united states"):
        dataset = Dataset(country=country)
        dataset.stock_info(continue_last_download=True)

    def stock_dividends(self, country="united states"):
        dataset = Dataset(country=country)
        dataset.stock_dividends(continue_from_last_download=True)


if __name__ == "__main__":
    alphalib = AlphaLib()
    fire.Fire(alphalib)
