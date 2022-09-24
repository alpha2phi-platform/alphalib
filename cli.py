import fire

from alphalib.dataset import Dataset


class AlphaLib(object):
    def stock_info(self):
        dataset = Dataset()
        dataset.stock_info()

    def stock_stats(self):
        dataset = Dataset()
        dataset.stock_stats()

    def stock_dividends(self):
        dataset = Dataset()
        dataset.stock_dividends()


if __name__ == "__main__":
    alphalib = AlphaLib()
    fire.Fire(alphalib)
