import pandas as pd

df = pd.read_csv(
    "data/SMSSpamCollection",
    sep="\t",
    header=None,
    names=["label", "message"]
)

print(df.head())

print("\nDataset shape:")
print(df.shape)

print("\nClass distribution:")
print(df["label"].value_counts())
print("\nMissing values:")
print(df.isnull().sum())

print("\nRows with missing values:")
print(df[df.isnull().any(axis=1)])
print("\nExample HAM messages:")
print(df[df["label"] == "ham"]["message"].head(5).to_string(index=False))

print("\nExample SPAM messages:")
print(df[df["label"] == "spam"]["message"].head(5).to_string(index=False))
import re


def clean_text(text):
    # Convert everything to lowercase
    text = text.lower()

    # Replace URLs with the word URL
    text = re.sub(r"http\S+|www\S+", " URL ", text)

    # Remove punctuation and special characters
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


# Apply cleaning to every SMS
df["message"] = df["message"].apply(clean_text)

print("\nCleaned examples:")
print(df.head(10).to_string(index=False))
from sklearn.model_selection import train_test_split

X = df["message"]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))
from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer()

X_train_vectors = vectorizer.fit_transform(X_train)
X_test_vectors = vectorizer.transform(X_test)

print("\nTraining feature matrix shape:")
print(X_train_vectors.shape)

print("\nTesting feature matrix shape:")
print(X_test_vectors.shape)
from sklearn.naive_bayes import MultinomialNB

model = MultinomialNB()

model.fit(X_train_vectors, y_train)

print("\nModel training completed!")
# Make predictions on the test data
y_pred = model.predict(X_test_vectors)

print("\nPredictions completed!")
print(y_pred[:10])
from sklearn.metrics import accuracy_score

accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy:", accuracy)
print("Accuracy percentage:", accuracy * 100, "%")
from sklearn.metrics import classification_report

print("\nClassification Report:")
print(classification_report(y_test, y_pred))
from sklearn.metrics import confusion_matrix

cm = confusion_matrix(y_test, y_pred)

print("\nConfusion Matrix:")
print(cm)
import joblib

joblib.dump(model, "model/spam_model.pkl")
joblib.dump(vectorizer, "model/vectorizer.pkl")

print("\nModel and vectorizer saved!")