import pandas as pd
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

df = pd.read_csv(input_file)
# Simple preprocessing: lowercase text
df['text'] = df['text'].str.lower()
df.to_csv(output_file, index=False)
print(f"Preprocessed data saved to {output_file}")
