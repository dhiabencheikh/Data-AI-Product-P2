import csv
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Step 1 · Router (rung 2: classical ML, TF-IDF + logistic regression).
# It reads ONLY what the merchant wrote (message, or the form fields when there is no message),
# never the ledger rows: account data is the job of the routing rule and the drafter.
#
# Training phrases live in data/router_training.csv, built by data/make_router_training.py.
# None of them is copied from the eval-set (the eval-set is never used for training).
TRAINING_PATH = os.path.join(os.path.dirname(__file__), "data", "router_training.csv")

# Inverse regularisation strength, chosen by 5-fold cross-validation on the training phrases only
# (C = 20: 327/346 right, 305 above the 0.70 gate, 2 confident errors).
REGULARISATION_C = 20.0


def load_training_data(path: str = TRAINING_PATH) -> tuple:
    """Read the training phrases and their categories."""
    texts = []
    labels = []
    with open(path, encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            texts.append(row["text"])
            labels.append(row["category"])
    return texts, labels


class TicketRouter:
    """Classify the merchant's words into one of the routing categories."""

    def __init__(self, training_path: str = TRAINING_PATH):
        texts, labels = load_training_data(training_path)
        # Character n-grams cope with typos, capitals and French/English spelling variants.
        self.vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), lowercase=True, sublinear_tf=True)
        features = self.vectorizer.fit_transform(texts)
        self.model = LogisticRegression(C=REGULARISATION_C, max_iter=2000, random_state=42)
        self.model.fit(features, labels)

    def predict(self, merchant_words: str) -> dict:
        """Return the most likely category and the model's confidence in it."""
        features = self.vectorizer.transform([merchant_words])
        probabilities = self.model.predict_proba(features)[0]
        best_index = probabilities.argmax()
        return {
            "category": str(self.model.classes_[best_index]),
            "confidence": round(float(probabilities[best_index]), 3),
        }


if __name__ == "__main__":
    router = TicketRouter()
    print(router.predict("I still have not received the payment from Atelier Brun"))
    print(router.predict("Please refund the customer"))
