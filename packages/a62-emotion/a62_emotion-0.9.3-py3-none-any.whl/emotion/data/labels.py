from pathlib import Path

import pandas as pd
from emotion import root_dir
from emotion.utils import create_csv

LABELS_DIR = Path(root_dir / "data/raw/labels")
CSV_FILES = LABELS_DIR.iterdir()
EMOTIONS = ["anger", "disgust", "fear", "happiness", "sadness", "surprise"]
EMOTIONS_COLS = [f"Answer.{emotion}" for emotion in EMOTIONS]
SENTIMENT_COL = "Answer.sentiment"
SENTIMENT = "sentiment"


def merge_intensity(df: pd.DataFrame) -> pd.DataFrame:
    """
    Use 0 or 1 for presence of emotion and -1, 0 or 1 for polarity.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to transform.

    Returns
    -------
    pd.DataFrame

    """
    return pd.concat(
        [
            df[EMOTIONS].applymap(lambda v: v > 0 and 1 or 0),
            df[SENTIMENT].map(lambda v: v < 0 and -1 or v > 0 and 1 or 0),
        ],
        axis=1,
    )


def merge_agreement(by: str, df: pd.DataFrame) -> pd.DataFrame:
    """
    Select only segments from which there is at most a disagreeement of 1 ordinality
    and take the median/mode as the 'winning' modality.

    Parameters
    ----------
    by: str
        column to group by.
    df : pd.DataFrame
        DataFrame to process.

    Returns
    -------
    pd.DataFrame
        The transformed DataFrame.
    """
    groupped = df.groupby(by=by)
    all_modalities = groupped[EMOTIONS + [SENTIMENT]]

    return all_modalities.median()[(all_modalities.std(0) < 0.48).all(axis=1)]


def main():
    dfs = {csv_file.stem: pd.read_csv(csv_file) for csv_file in CSV_FILES}

    # Standardize 'Input.VIDEO_ID' for `pom_extra_sqa_mono_results` dataset
    dfs["pom_extra_sqa_mono_results"]["Input.VIDEO_ID"] = dfs[
        "pom_extra_sqa_mono_results"
    ]["Input.VIDEO_ID"].map(lambda x: x.split("/")[1])

    # Merge all dataframes
    df_init = pd.concat(dfs.values())

    # Relevant columns
    ids = (
        df_init["Input.VIDEO_ID"].astype(str) + "_" + df_init["Input.CLIP"].astype(str)
    )
    ids.rename("id", inplace=True)
    df = pd.concat([ids, df_init[EMOTIONS_COLS + [SENTIMENT_COL]]], axis=1)
    df = df.rename(
        columns=dict(zip(EMOTIONS_COLS, EMOTIONS), **{SENTIMENT_COL: "sentiment"})
    )
    df = df.set_index("id")

    # Drop missing values
    missing = df[df.isnull().any(axis=1)]
    df = df.drop(index=missing.index)

    df_merged_intensity = merge_intensity(df)
    df_merged_agreement = merge_agreement("id", df_merged_intensity).astype(int)

    create_csv(root_dir / "data/interim/labels" / "labels.csv", df_merged_agreement)

    return df_merged_agreement


if __name__ == "__main__":
    main()
