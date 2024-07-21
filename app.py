from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,
    initial-scale=1.0">
    <title>Simple Frontend</title>
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            height: 100vh;
            margin: 0;
            padding: 20px;
            background-color: #f4f4f4;
        }
        .container {
            width: 80%;
            max-width: 800px;
            text-align: center;
            margin-top: 20px;
            background-color: #fff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
        }
        textarea {
            width: 100%;
            margin-bottom: 10px;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ddd;
        }
        button {
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
            background-color: #007BFF;
            color: #fff;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        button:hover {
            background-color: #0056b3;
        }
        pre {
            white-space: pre-wrap;
            word-wrap: break-word;
            text-align: left;
            background-color: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
        }
        h1 {
            font-family: 'Roboto', sans-serif;
            color: #333;
        }
        .form-container {
            max-height: 300px; /* Adjust as needed */
            overflow-y: auto;
        }
        textarea {
            resize: none;
            max-width: 90%;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Medical Note Redaction Service</h1>
        <form id="redactForm" class="form-container">
            <textarea id="text" name="text" rows="10" 
            placeholder="Enter medical note here...">
            </textarea><br>
            <button type="button" onclick="submitForm()">
            Redact
            </button>
        </form>
        <h2>Redacted Note:</h2>
        <pre id="redactedText"></pre>
    </div>

    <script>
        async function submitForm() {
            const text = document.getElementById('text').value;
            const response = await fetch('/redact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text }),
            });
            if (response.ok) {
                const data = await response.json();
                document.getElementById('redactedText')
                .textContent = data.redacted_text;
            } else {
                document.getElementById('redactedText')
                .textContent = 'An error occurred during redaction.';
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

url = "http://host.docker.internal:8080/v1"
api_key = "sk-no-key-required"

client = OpenAI(base_url=url, api_key=api_key)

context = (
    "You are a system that removes PHI information from the given "
    "medical note. "
    "You are given a text and you need to replace all PHI information "
    "from it with the word <REDACTED>. "
    "You must return the text exactly as it was given, but with all "
    "PHI information redacted.\n"
    "PHI Information includes the following:\n"
    "- Names\n"
    "- Addresses\n"
    "- Phone Numbers\n"
    "- Email Addresses\n"
    "- Medical Record Numbers\n"
    "- Health Plan Beneficiary Numbers\n"
    "- Social Security Numbers\n"
    "- IP Addresses\n"
    "Please find below a sample input and output for your reference:\n"
    "### SAMPLE INPUT 1 ###\n"
    "Michael Johnson, residing at 789 Pine Road, Gotham, NJ 07030, born "
    "on 12/10/1985, visited the clinic. "
    "He reports mild chest pain lasting for two days. "
    "### SAMPLE OUTPUT 1 ###\n"
    "<REDACTED>, residing at <REDACTED>, born on <REDACTED>, visited the "
    "clinic. He reports mild chest pain lasting for two days.\n"
    "### SAMPLE INPUT 2 ###\n"
    "Hi my name is Josephine Smith and I really need my medication shipped to "
    "Gotham, NJ 07030. "
    "You can also reach me at 123-565-1222 or at jsmith@gmail.com.\n"
    "### SAMPLE OUTPUT 2 ###\n"
    "Hi my name is <REDACTED> and I really need my medication shipped to "
    "<REDACTED>. "
    "You can also reach me at <REDACTED> or at <REDACTED>.\n"
    "### SAMPLE INPUT 3 ###\n"
    "Jane Watson with medical number MRN123456789, health plan beneficiary "
    "number HPB123456789, and social security number 123-45-6789, "
    "visited the clinic.\n"
    "She reports a sore throat lasting for two days.\n"
    "### SAMPLE OUTPUT 3 ###\n"
    "<REDACTED> with medical number <REDACTED>, health plan beneficiary "
    "number <REDACTED>, and social security number <REDACTED>, "
    "visited the clinic.\n"
    "She reports a sore throat lasting for two days.\n"
)

@app.route("/redact", methods=["POST"])
def redact():
    data = request.get_json()
    if "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    text = data["text"]

    completion = client.chat.completions.create(
        model="LLaMA_CPP",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": text},
        ],
    )

    response = completion.choices[0].message.content
    return jsonify({"redacted_text": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
