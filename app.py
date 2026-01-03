from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()

    if "message" not in update:
        return "ok"

    chat_id = update["message"]["chat"]["id"]
    text = update["message"].get("text", "")

    number = "".join(filter(str.isdigit, text))

    if len(number) < 10:
        reply = "❌ 10 digit number bhejo"
    else:
        url = f"https://numberimfo.vishalboss.sbs/api.php?number={number}&key={API_KEY}"
        r = requests.get(url)
        reply = f"📱 Number: {number}\n\n{r.text}"

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": reply}
    )

    return "ok"
