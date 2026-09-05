import joblib

# Load the trained model
model = joblib.load("model/spam_model.pkl")

# Load the Bag-of-Words vectorizer
vectorizer = joblib.load("model/vectorizer.pkl")

print("Model and vectorizer loaded successfully!")
# Get an SMS from the user
message = input("\nEnter an SMS to check: ")

# Convert the SMS into the same format used during training
message_vector = vectorizer.transform([message])

# Predict whether it is ham or spam
prediction = model.predict(message_vector)[0]

# Get prediction probabilities
probabilities = model.predict_proba(message_vector)[0]

# Find the probability of the predicted class
class_index = list(model.classes_).index(prediction)
confidence = probabilities[class_index]

print("\nPrediction:", prediction.upper())
print("Confidence:", round(confidence * 100, 2), "%")