#open lovecraft_bib
import pandas as pd
df = pd.read_csv('../lavin_meta/lovecraft_bib.csv', encoding='latin-1')

#read groupings
groups = list(set(list(df["Group"].dropna())))
groups.sort()
#loop groups, for each ...
for i in groups:
    full_text = []
    #get associated file_names
    new_df = df.loc[df['Group'] == i]
    roots = list(set(list(new_df['file_name'].dropna())))
    for r in roots:
        file_loc = "".join(["/Users/matthewlavin/lovecraft_horror/", r, ".txt"])
        #open lovecraft_horror folder
        with open(file_loc) as f:
            text = f.read()
        #group
        full_text.append(text)
    outfile = "".join(["../lavin_additional_texts/", i, ".txt"])
    with open(outfile, 'a') as out:
        #make new files
        for t in full_text:
            #save files in lavin_additional_texts
            out.write(t)
            out.write(" ")

#generate initial values for lavin_meta.csv
df_meta = pd.DataFrame.from_records([[i] for i in groups], columns=["docid"])
df_meta.to_csv("../lavin_meta/lavin_meta.csv")
