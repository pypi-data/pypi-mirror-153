from pathlib import Path

import pandas as pd


def create_csv(path: Path, df: pd.DataFrame) -> None:
    df.to_csv(path)
