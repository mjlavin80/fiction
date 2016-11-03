from application.selective_features import make_feature_list

top_genre_terms = make_feature_list("lavin_lexicon/features_correlation_with_genre_all.csv", "spearman", 500)
