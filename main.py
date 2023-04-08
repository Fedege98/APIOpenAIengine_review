from flask import Flask, render_template, request, redirect, url_for
import openai
import smtplib
from googletrans import Translator

app = Flask(__name__)

# Configura le API di OpenAI
openai.api_key = "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"

# Configura l'email di invio
email = "federicogemmo@gmail.com"
password = "F9GCesare_98**"

# Configura il server SMTP
'''server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(email, password)'''

translator = Translator()


def generate_review(keywords, sector, company_name):
    prompt = f"Scrivi una recensione per l'azienda {company_name} nel settore {sector} utilizzando le parole chiave: {', '.join(keywords)}"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keywords = request.form.get('keywords').split(',')
        sector = request.form.get('sector')
        company_name = request.form.get('company_name')
        review = generate_review(keywords, sector, company_name)
        return render_template('review.html', review=review, company_name=company_name)

    return render_template('index.html')


@app.route('/send_email', methods=['POST'])
def send_email():
    review = request.form.get('review')
    company_name = request.form.get('company_name')
    recipient = request.form.get('recipient')

    translated = translator.translate(review, dest='en')
    sentiment = "Positivo" if translated.sentiment.polarity > 0 else "Negativo"

    subject = f"Recensione {sentiment} per {company_name}"
    message = f"Subject: {subject}\n\n{review}"

    server.sendmail(email, recipient, message)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
