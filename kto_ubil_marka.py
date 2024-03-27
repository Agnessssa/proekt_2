import pandas as pd
import markovify

provs = pd.read_csv('corpus.csv', sep='\t', encoding='utf-8')

shuffled = provs.sample(frac=1)
train = ' '.join(shuffled.Column1)
m = markovify.Text(train)