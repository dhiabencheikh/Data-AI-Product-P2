import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Synthetic training data for Ledgerly ticket routing (Rung 2: Classical ML)
TRAINING_DATA = [
    ("Where is my payment TX-90112?", "status"),
    ("Still haven't received this payment of €640", "status"),
    ("When will I get my GBP payout?", "status"),
    ("Payment never arrived from customer", "status"),
    ("Payout still not on our bank account", "status"),
    ("Client paid 1,560 EUR this morning, not showing yet", "status"),
    ("WHERE IS MY MONEY 3 days now", "status"),
    ("Status of payment from Maison Leroux", "status"),
    ("Please refund my customer, he returned the item", "refund"),
    ("My customer says he never got the €120 refund", "refund"),
    ("Please issue a partial refund of €100 right now", "refund"),
    ("Client still hasn't seen the €75 refund from last week", "refund"),
    ("My customer opened a dispute, close this dispute and release my money", "dispute"),
    ("A buyer filed a chargeback, cancel it immediately", "dispute"),
    ("Chargeback opened on order, I have proof of delivery", "dispute"),
    ("None of my payments arrived this week, payouts suspended", "account_flag"),
    ("All our payouts stopped since Tuesday, what is going on", "account_flag"),
    ("Contract ended, payment never came", "account_flag"),
    ("Please waive the 1.9% fee on this transaction", "fee_waiver"),
    ("Why did you take a 1.9% fee instead of 1.5%?", "status"),
    ("How do I export my monthly statement as a CSV?", "out_of_scope"),
    ("How do I add a new team member to my dashboard?", "out_of_scope"),
    ("Where are the October payments of all three shops M-0412, M-0413, M-0420?", "out_of_scope"),
    ("Hola, ¿dónde está mi pago de 500 euros de ayer?", "out_of_scope"),
]

class TicketRouter:
    def __init__(self):
        df = pd.DataFrame(TRAINING_DATA, columns=["text", "category"])
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), lowercase=True)
        X = self.vectorizer.fit_transform(df["text"])
        self.model = LogisticRegression(random_state=42)
        self.model.fit(X, df["category"])

    def predict(self, ticket_text: str) -> dict:
        X_test = self.vectorizer.transform([ticket_text])
        probs = self.model.predict_proba(X_test)[0]
        best_idx = probs.argmax()
        return {
            "category": self.model.classes_[best_idx],
            "confidence": round(float(probs[best_idx]), 3),
        }

if __name__ == "__main__":
    router = TicketRouter()
    sample = "Still haven't received payment TX-90112"
    print(router.predict(sample))
