import re
import pickle
import joblib
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from nltk.corpus import stopwords
import nltk

# Download stopwords if not already present
nltk.download('stopwords')

# Load stopwords
stop_words = set(stopwords.words('english'))

# Load saved files
model = load_model("model/lstm_emotion_model.h5")

with open("model/tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

label_encoder = joblib.load("model/label_encoder.pkl")

MAX_LEN = 100


def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#\w+", "", text)
    text = re.sub(r"[^a-z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    # Remove stopwords
    text = " ".join(
        [word for word in text.split() if word not in stop_words]
    )

    return text


def predict_emotion(text):
    cleaned_text = clean_text(text)

    sequence = tokenizer.texts_to_sequences([cleaned_text])

    padded = pad_sequences(
        sequence,
        maxlen=MAX_LEN,
        padding="post",
        truncating="post"
    )

    prediction = model.predict(padded, verbose=0)

    predicted_index = np.argmax(prediction)

    emotion = label_encoder.inverse_transform([predicted_index])[0]

    confidence = float(np.max(prediction))

    return emotion, confidence, prediction[0]
