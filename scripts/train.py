import pandas as pd
import sys
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
import joblib

input_file = sys.argv[1]
output_model = sys.argv[2]

df = pd.read_csv(input_file)
X = df['text']
y = df['label']

vectorizer = CountVectorizer()
X_vec = vectorizer.fit_transform(X)

model = LogisticRegression()
model.fit(X_vec, y)

joblib.dump((model, vectorizer), output_model)
print(f"Model saved to {output_model}")
