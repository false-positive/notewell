import numpy as np
import pandas as pd
import json


dataset = open("dataset.txt")
p_dataset = pd.read_excel("Physics.xlsx")
x = p_dataset.iloc[:,  0].values
dataset_lines = []

for line in dataset:
    dataset_lines.append(json.loads(line))

for article in x:
    print(article)
