def confusion_from_csv(csv, genre_type):
    import pandas as pd
    df = pd.read_csv(csv)

    #depending on genre_type, get cluster index and appropriate genre
    if genre_type == "lavin":
        genres = list(df["lavin_genres"])
    else:
        genres = list(df["big_genres"])

    clusters = [str(i) for i in list(df["labels"])]

    y_actu = pd.Series(genres, name='Human Coded')
    y_pred = pd.Series(clusters, name='Inferred')

    df_confusion = pd.crosstab(y_pred, y_actu)
    filename = csv.replace("lavin_results/", "").replace(".csv", "_confusion_"+genre_type)
    df_confusion.to_csv("viz/"+ filename +".csv")
import glob
csvs = glob.glob("lavin_results/*.csv")
for csv in csvs:
    if "horror" not in csv:
        confusion_from_csv(csv, genre_type="big")
for csv in csvs:
    confusion_from_csv(csv, genre_type="lavin")
