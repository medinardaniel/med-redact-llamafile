import string
from nltk.translate.bleu_score import sentence_bleu

true_notes = [
    "Born on <REDACTED>, <REDACTED> lives at <REDACTED>. Contact number "
    "<REDACTED>, and email <REDACTED>. Reports chest pain for three days, "
    "taking Metformin 500 mg twice daily, no allergies.",
    "<REDACTED> mentions a persistent cough and shortness of breath for a "
    "week. Residing at <REDACTED>, contact <REDACTED>, email <REDACTED>, "
    "born on <REDACTED>. On Atorvastatin 10 mg nightly, allergic to "
    "penicillin.",
    "<REDACTED>, address <REDACTED>, phone (<REDACTED>), email <REDACTED>, "
    "describes severe headaches and nausea for two days. Born on <REDACTED>, "
    "currently taking Levothyroxine 50 mcg daily, no drug allergies.",
    "Reports joint pain and swelling for a week, <REDACTED>, residing at "
    "<REDACTED>. Born on <REDACTED>, contact <REDACTED>, email <REDACTED>. "
    "Takes Losartan 25 mg daily, allergic to ibuprofen.",
    "Address <REDACTED>, phone <REDACTED>, and email <REDACTED>, <REDACTED> "
    "reports dizziness and fatigue for five days. Born on <REDACTED>, "
    "currently taking Hydrochlorothiazide 12.5 mg daily, no allergies.",
    "<REDACTED>, with contact number <REDACTED>, email <REDACTED>, residing "
    "at <REDACTED>. Born on <REDACTED>, mentions a persistent fever and "
    "chills for three days. On Amlodipine 5 mg daily, allergic to latex.",
    "Frequent migraines and light sensitivity for a week reported by "
    "<REDACTED>, phone <REDACTED>, address <REDACTED>. Born on <REDACTED>, "
    "email <REDACTED>. Takes Sertraline 50 mg daily, no drug allergies.",
    "<REDACTED>, severe back pain and muscle spasms for five days. Address "
    "<REDACTED>, contact <REDACTED>, born on <REDACTED>, email <REDACTED>. "
    "On Simvastatin 20 mg daily, allergic to aspirin.",
    "Chronic fatigue and joint stiffness for a week, <REDACTED>, phone "
    "<REDACTED>, address <REDACTED>, email <REDACTED>. Born on <REDACTED>, "
    "taking Metoprolol 50 mg daily, no known allergies.",
    "Severe abdominal pain and nausea for three days described by <REDACTED>, "
    "address <REDACTED>, contact <REDACTED>, email <REDACTED>. Born on "
    "<REDACTED>, on Lisinopril 10 mg daily, allergic to sulfa drugs."
]

predicted_notes = [
    "<REDACTED>, born on <REDACTED>, lives at <REDACTED>. Contact number "
    "<REDACTED>, and email <REDACTED>. Reports chest pain for three days, "
    "taking Metformin 500 mg twice daily, no allergies.",
    "<REDACTED> mentions a persistent cough and shortness of breath for a "
    "week. Residing at <REDACTED>, contact <REDACTED>, email <REDACTED>, "
    "born on <REDACTED>. On Atorvastatin 10 mg nightly, allergic to "
    "penicillin.",
    "<REDACTED>, address <REDACTED>, phone (<REDACTED>), email <REDACTED>, "
    "describes severe headaches and nausea for two days. Born on <REDACTED>, "
    "currently taking Levothyroxine 50 mcg daily, no drug allergies.",
    "<REDACTED> reports joint pain and swelling for a week. <REDACTED>, "
    "residing at <REDACTED>, born on <REDACTED>. Contact <REDACTED>. Email "
    "<REDACTED>. Takes Losartan 25 mg daily. <REDACTED> is allergic to "
    "ibuprofen.",
    "<REDACTED>, residing at <REDACTED>, phone (<REDACTED>), and email "
    "<REDACTED>, Sophia Martinez reports dizziness and fatigue for five days. "
    "Born on <REDACTED>, currently taking Hydrochlorothiazide 12.5 mg daily, "
    "no allergies.",
    "<REDACTED>, with contact number <REDACTED>, email <REDACTED>, residing "
    "at <REDACTED>. Born on <REDACTED>, mentions a persistent fever and "
    "chills for three days. On Amlodipine 5 mg daily, allergic to latex.",
    "<REDACTED> reported frequent migraines and light sensitivity for a week. "
    "<REDACTED>, phone <REDACTED>, address <REDACTED>, born on <REDACTED>, "
    "email <REDACTED>. Takes Sertraline 50 mg daily, no drug allergies.",
    "<REDACTED>, severe back pain and muscle spasms for five days. "
    "<REDACTED>, contact <REDACTED>, born on <REDACTED>, email <REDACTED>. "
    "On Simvastatin 20 mg daily, allergic to aspirin.",
    "<REDACTED>, chronic fatigue and joint stiffness for a week, "
    "<REDACTED>, phone <REDACTED>, address <REDACTED>, email <REDACTED>. Born "
    "on <REDACTED>, taking Metoprolol 50 mg daily, no known allergies.",
    "<REDACTED>, residing at <REDACTED>, contact <REDACTED>, email "
    "<REDACTED>. Born on <REDACTED>, taking Lisinopril 10 mg daily, "
    "allergic to sulfa drugs. Describes severe abdominal pain and "
    "nausea lasting for three days"
]


def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text


def calculate_bleu_scores(true_notes, predicted_notes):
    true_notes_preprocessed = [
        preprocess_text(note) for note in true_notes
    ]
    predicted_notes_preprocessed = [
        preprocess_text(note) for note in predicted_notes
    ]

    bleu_scores = [
        sentence_bleu([t.split()], p.split())
        for t, p in zip(true_notes_preprocessed, predicted_notes_preprocessed)
    ]

    return bleu_scores


bleu_scores = calculate_bleu_scores(true_notes, predicted_notes)

average_bleu_score = sum(bleu_scores) / len(bleu_scores)
sorted_scores = sorted(bleu_scores)
median_index = len(sorted_scores) // 2
median_bleu_score = sorted_scores[median_index]
min_bleu_score = min(bleu_scores)
max_bleu_score = max(bleu_scores)

print(f"Average BLEU score: {average_bleu_score}")
print(f"Median BLEU score: {median_bleu_score}")
print(f"Minimum BLEU score: {min_bleu_score}")
print(f"Maximum BLEU score: {max_bleu_score}")
