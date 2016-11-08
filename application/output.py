import pandas as import pd

def save_labels(sklearn_instance, filename, columns_data_dictionary):
    """
    A generalized function that automates a fe commonly repeated steps in sklearn testing and output.
    Columns data dictionary will have column names and data for column, such as "docid", "group_label", "genres", "year", etc.
    """
    labels = sklearn_instance.labels_

    #convert to pandas df (terms and counts)
    columns= list(columns_data_dictionary.keys())

    #This list comprehension approach with ensure that grouping and columns are in the same order. Groupings will be a list of lists.
    groupings = [columns_data_dictionary[i] for i in columns]
    df = pd.DataFrame(groupings, columns=columns)
    #Save as csv in lavin_results folder
    df.to_csv("lavin_results/" + filename)

if __name__ == "__main__":
        pass
