"""Build prototype/data/router_training.csv, the router's training phrases.

Every phrase is assembled from fragments written by the team for training only:
nothing is copied from evals/ (the eval-set is never used for training).
Run it again to rebuild the file: python prototype/data/make_router_training.py
"""
import csv
import os
import random

SEED = 42
PHRASES_PER_CATEGORY = 40
# Some phrases are also written in capitals, as angry merchants do (added after report_v1, run 1).
SHOUTED_SHARE = 0.25
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "router_training.csv")

OPENERS = {
    "en": ["", "Hi, ", "Hello, ", "Good morning, ", "Please help: ", "Quick question: "],
    "fr": ["", "Bonjour, ", "Bonsoir, ", "Bonjour à l'équipe, ", "Question rapide : "],
}
CLOSERS = {
    "en": ["", " Thanks.", " It is urgent.", " Thank you in advance.", " Please check.", "!!!", " Answer quickly please!"],
    "fr": ["", " Merci.", " C'est urgent.", " Merci d'avance.", " Merci de vérifier.", " !!", " Répondez vite svp !"],
}

CORES = {
    "status": {
        "en": [
            "where is the payment from my client?",
            "I still have not received the money for this order.",
            "the payout is not on my bank account yet.",
            "when will this transfer reach my bank?",
            "can you check the status of this transaction?",
            "my customer paid last week and I see nothing.",
            "is yesterday's payment on its way?",
            "why is this payout late?",
            "a payment is missing on my statement.",
            "I have been waiting for the money for days.",
            "the client says he paid but nothing arrived.",
            "what happened to this transfer?",
            "where is my money?",
            "the payment of the invoice does not show up.",
            "my payout from this week never arrived.",
            "why was this payout sent back?",
            "has the foreign currency payment been converted yet?",
            "ref amount date customer",
            # Added after report_v1 run 1 (causes: tone, typos, very recent payments, follow-ups, failed payments)
            "this is unacceptable, a week without my money",
            "pay me what you owe me now",
            "payement not recieved yet from my client",
            "my client paid an hour ago and I cannot see it yet",
            "a payment made this morning is not showing on my side",
            "second time I write about this transfer, still nothing",
            "I already asked about this payment and got no answer",
            "the card of my client was refused, what happened?",
            "the customer says the money left his account, we have nothing",
        ],
        "fr": [
            "où est le paiement de mon client ?",
            "je n'ai toujours pas reçu ce virement.",
            "quand le versement arrivera-t-il sur mon compte ?",
            "le règlement de la commande n'apparaît pas sur notre relevé.",
            "pouvez-vous vérifier où en est cette transaction ?",
            "mon client a payé mais je ne vois rien.",
            "le virement de cette semaine n'est pas arrivé.",
            "pourquoi ce versement est-il en retard ?",
            "j'attends ce paiement depuis plusieurs jours.",
            "où en est mon argent ?",
            # Added after report_v1 run 1 (causes: informal French, follow-ups, very recent payments)
            "rien vu passer pour ce règlement de la semaine dernière",
            "j'attends un règlement de mon client depuis jeudi",
            "c'est la deuxième fois que je relance pour ce paiement",
            "le paiement de ce matin n'apparaît pas encore",
            "ce paiement est-il bien parti ?",
            "le virement du client n'est pas sur notre compte bancaire",
        ],
    },
    "refund_status": {
        "en": [
            "my customer is still waiting for the refund you sent.",
            "the client has not seen the refund on his card yet.",
            "where is the refund for my customer?",
            "when will the refund reach the buyer's bank?",
            "the buyer says the refund never showed up.",
            "has the refund been sent to the customer's bank?",
            "the refund of last week never reached the customer's card",
            "my buyer still has not received the money you refunded",
        ],
        "fr": [
            "mon client attend toujours son remboursement.",
            "le remboursement n'est pas arrivé chez le client.",
            "où en est le remboursement envoyé au client ?",
            "le client ne voit pas le remboursement sur sa carte.",
            "l'acheteur n'a toujours rien reçu du remboursement",
        ],
    },
    "refund_request": {
        "en": [
            "please refund my customer for this order.",
            "refund the buyer now, the item came back.",
            "issue a refund to my client today.",
            "send the money back to the customer.",
            "make a partial refund on this order.",
            "process the refund yourself, it is a small amount.",
        ],
        "fr": [
            "remboursez le client s'il vous plaît.",
            "merci d'effectuer le remboursement de cette commande.",
            "faites un remboursement partiel au client.",
            "rendez l'argent à l'acheteur aujourd'hui.",
        ],
    },
    "dispute": {
        "en": [
            "the buyer opened a chargeback, cancel it.",
            "a customer disputes this payment, close the dispute.",
            "chargeback on my order, I have the proof of delivery.",
            "remove this dispute and release my funds.",
            "the client claims he never got the goods and filed a dispute.",
            "stop this chargeback, the customer is lying.",
        ],
        "fr": [
            "un client conteste le paiement, annulez le litige.",
            "rétrofacturation ouverte, j'ai la preuve de livraison.",
            "fermez ce litige et débloquez mes fonds.",
            "l'acheteur a ouvert une contestation sur cette commande.",
        ],
    },
    "fee_waiver": {
        "en": [
            "please waive the fee on this payment.",
            "can you cancel the commission as a goodwill gesture?",
            "remove the fees for this month, we are a loyal client.",
            "we would like the fee refunded as a commercial gesture.",
            "drop the processing fee on this large transaction.",
        ],
        "fr": [
            "merci d'annuler les frais sur cette transaction.",
            "pouvez-vous faire un geste commercial sur la commission ?",
            "supprimez les frais de ce mois, nous sommes fidèles.",
        ],
    },
    "account": {
        "en": [
            "all my payouts are blocked, what is happening?",
            "no payment has reached us for days.",
            "our account seems suspended, nothing is paid out.",
            "every payout stopped this week.",
            "none of our transfers arrive any more.",
            "nothing gets paid out any more, is my account blocked?",
            "why did every payout stop at once?",
        ],
        "fr": [
            "tous nos versements sont bloqués depuis hier.",
            "aucun paiement ne nous parvient cette semaine.",
            "notre compte semble suspendu, plus rien n'est versé.",
            "tous les virements sont arrêtés, que se passe-t-il ?",
            "nos versements sont suspendus, pourquoi ?",
        ],
    },
    "out_of_scope": {
        "en": [
            "how do I change my password?",
            "how can I invite a colleague to the dashboard?",
            "how do I download an invoice?",
            "what is new in the latest product release?",
            "how do I set up two-factor authentication?",
            "how can I change the logo on my payment page?",
        ],
        "fr": [
            "comment modifier l'adresse de facturation ?",
            "comment créer un nouvel utilisateur ?",
            "comment exporter mes données ?",
            "comment changer la langue du tableau de bord ?",
        ],
    },
}


def make_phrase(opener: str, core: str, closer: str) -> str:
    """Glue the three fragments and capitalise the first letter."""
    text = (opener + core).strip() + closer
    return text[0].upper() + text[1:]


def build_phrases(category: str, rng: random.Random) -> list:
    """Keep every core once, then add random variants up to PHRASES_PER_CATEGORY."""
    chosen = []
    variants = []
    for language, cores in CORES[category].items():
        for core in cores:
            chosen.append((make_phrase(rng.choice(OPENERS[language]), core, rng.choice(CLOSERS[language])), category, language))
            for opener in OPENERS[language]:
                for closer in CLOSERS[language]:
                    variants.append((make_phrase(opener, core, closer), category, language))
    rng.shuffle(variants)
    for variant in variants:
        if len(chosen) >= PHRASES_PER_CATEGORY:
            break
        if variant not in chosen:
            chosen.append(variant)
    shouted = []
    for text, label, language in chosen:
        if rng.random() < SHOUTED_SHARE:
            shouted.append((text.upper(), label, language))
    return chosen + shouted


def main():
    rng = random.Random(SEED)
    rows = []
    for category in CORES:
        rows.extend(build_phrases(category, rng))
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["text", "category", "language", "origin"])
        for text, category, language in rows:
            writer.writerow([text, category, language, "synthetic · written by the team for training only"])
    print(f"{len(rows)} phrases written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
