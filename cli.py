import fire

from alphalib.dataset import Dataset


class AlphaLib(object):
    def download(self, country="united states"):
        dataset = Dataset(country=country)
        dataset.download(continue_from_last_download=True, start_pos=1905)


if __name__ == "__main__":
    alphalib = AlphaLib()
    fire.Fire(alphalib)
