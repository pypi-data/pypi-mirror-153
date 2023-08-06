import os

import pandas as pd

dir_name = "/Users/ashok/Downloads/TradingData"
file_paths = {}
for path, currentDirectory, files in os.walk(dir_name):
    for file in files:
        if "csv" in os.path.join(path, file):
            file_location = os.path.join(path, file)

            if file not in file_paths:
                file_paths[file] = [file_location]
            else:
                file_paths[file].append(file_location)


for file_name in file_paths:
    li = []

    if "NIFTY21N" not in file_name:
        continue

    for file_loc in file_paths[file_name]:
        df = pd.read_csv(file_loc, index_col=None, header=0)
        li.append(df)

    df = pd.concat(li, axis=0, ignore_index=True)

    df.loc[:, "date"] = df["<date>"] + " " + df["<time>"]
    df.loc[:, "date"] = pd.to_datetime(df.date)

    df = df.drop_duplicates(subset=["date"])

    assert len(df) == len(df.date.unique())

    df.rename(
        columns={
            "<ticker>": "symbol",
            "<open>": "open",
            "<close>": "close",
            "<low>": "low",
            "<high>": "high",
            "<volume>": "volume",
        },
        inplace=True,
    )
    df = df[["date", "open", "high", "low", "close", "volume", "symbol"]]

    print("saving file {}".format(file_name))
    df.sort_values(["date"]).reset_index(drop=True).to_csv(
        "~/.quantplay/NSE_OPT/minute/{}".format(file_name), index=False
    )
