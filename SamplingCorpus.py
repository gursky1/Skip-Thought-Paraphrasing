# Importing packages
import pandas as pd

# Importing TextCorpus data
df = pd.read_csv('TextCorpus.csv',encoding='utf8')
df.sample(10000).to_csv('TextCorpusSample.csv',encoding='utf8',index=False)