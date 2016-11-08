#get feature dicts from .p file
from application.pickles import pickledData

pData = pickledData()
metadata = pData.metadata
feature_dicts = pData.feature_dicts

print(metadata)
