import pandas as pd

df = pd.read_csv('/home/tingjung/cmdm/NPS/BBB/DeePred-BBB/DeePred-BBB_predictions.csv')
df['x'] = df['Name'].str.extract(r'(\d+)$').astype(int)
df = df.sort_values(by='x').drop(columns=['x']).reset_index(drop=True)
df.to_csv('/home/tingjung/cmdm/NPS/BBB/DeePred-BBB/DeePred-BBB_predictions_sorted.csv', index=False)