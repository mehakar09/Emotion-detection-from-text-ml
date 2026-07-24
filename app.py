import streamlit as st
from predict import predict_emotion

# Page configuration
st.set_page_config(
    page_title="Emotion Detection from Text",
    page_icon="😊",
    layout="centered"
)

# Title
st.title("🧠 Emotion Detection from Text")

st.write(
    "Enter a sentence below and the model will predict the emotion."
)

# Text input
user_input = st.text_area(
    "Enter your text",
    height=150,
    placeholder="Example: I am feeling really excited today!"
)

# Predict button
if st.button("Predict Emotion"):

    if user_input.strip() == "":
        st.warning("Please enter some text.")
    else:

        emotion, confidence, probabilities = predict_emotion(user_input)

        st.success(f"**Predicted Emotion:** {emotion.capitalize()}")

        st.info(f"Confidence: {confidence*100:.2f}%")

        st.subheader("Prediction Probabilities")

        emotion_names = [
            "anger",
            "fear",
            "joy",
            "love",
            "sadness",
            "surprise"
        ]

        chart_data = {
            "Emotion": emotion_names,
            "Probability": probabilities
        }

        st.bar_chart(
            data=chart_data,
            x="Emotion",
            y="Probability"
        )
