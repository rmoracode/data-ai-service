import polars as pl
import os

class FileService:

    def csv_to_parquet(self, path_csv: str):
        df = pl.read_csv(path_csv)
        parquet_path = path_csv.replace(".csv", ".parquet")
        df.write_parquet(parquet_path)
        return parquet_path
