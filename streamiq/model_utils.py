# streamiq/model_utils.py
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

# Simple demo model
vectorizer = CountVectorizer()
model = LogisticRegression()

# Train with toy data (replace with real later)
X_train = vectorizer.fit_transform(["billing issue", "technical problem", "account query"])
y_train = ["billing", "technical", "account"]
model.fit(X_train, y_train)

def predict_intent(text: str):
    """
    Predict intent category from text.
    """
    X_test = vectorizer.transform([text])
    return model.predict(X_test)[0]
