import fire
import pandas as pd

from alphalib.dataset.finance_database import prepare_stock_dataset
from alphalib.dataset.yahooquery_downloader import Dataset


class AlphaLib:
    def stock_database(self) -> pd.DataFrame:
        dataset = prepare_stock_dataset(save=True)
        return dataset

    def stock_stats(self):
        dataset = Dataset()
        dataset.stock_stats()

    def stock_selection(self):
        ...


if __name__ == "__main__":
    alphalib = AlphaLib()
    fire.Fire(alphalib)
