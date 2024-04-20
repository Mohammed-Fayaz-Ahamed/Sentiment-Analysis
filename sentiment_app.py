import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import pickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

# Load your pre-trained random forest model
with open("/content/random_forest_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

# Load the CountVectorizer used during training
with open("/content/random_forest_vec.pkl", "rb") as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

# Initialize NLTK tools for preprocessing
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    """Preprocesses the text data."""
    # Tokenization
    tokens = word_tokenize(text)
    # Remove stop words and non-alphanumeric tokens
    tokens = [token.lower() for token in tokens if token.lower() not in stop_words and token.isalnum()]
    # Lemmatization
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return " ".join(lemmatized_tokens)

def predict_sentiment(comment):
    """Predicts the sentiment of a comment using the loaded model."""
    preprocessed_comment = preprocess_text(comment)
    vectorized_comment = vectorizer.transform([preprocessed_comment])
    prediction = model.predict(vectorized_comment)[0]
    return prediction

def main():
    """
    Streamlit app to analyze user comments and classify sentiment.
    """
    st.title("Sentiment Analysis App")

    comment = st.text_area("Enter your comment here:")

    if st.button("Analyze"):
        if comment:
            prediction = predict_sentiment(comment)
            sentiment = {
                0: "Positive",
                1: "Negative",
                
            }[prediction]
            st.write(f"Sentiment: {sentiment}")
        else:
            st.warning("Please enter a comment to analyze.")

if __name__ == "__main__":
    main()
