import pandas as pd


def fox():
    x = [{'z': 1, 'y': 2},
         {'z': 2, 'y': 4},
         {'z': 3, 'y': 6},
         {'z': 4, 'y': 8}, ]
    df = pd.DataFrame(x)
    print(df.head())
