import os
import time
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

CONFIG = {
    "keywords": ["gpu"],
    "webhook_url": "",
    "interval": 120,
    "seen_ids": set()
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>TradeMe Bot Dashboard</title></head>
<body>
    <h1>TradeMe Bot Settings</h1>
    <form method=\"POST\">
        <label>Discord Webhook URL:</label><br>
        <input type=\"text\" name=\"webhook\" value=\"{{ config.webhook_url }}\" style=\"width:80%\"><br><br>
        <label>Keywords (one per line):</label><br>
        <textarea name=\"keywords\" rows=\"5\" style=\"width:80%\">{{ config.keywords | join("\
") }}</textarea><br><br>
        <label>Polling Interval (seconds):</label><br>
        <input type=\"number\" name=\"interval\" value=\"{{ config.interval }}\"><br><br>
        <button type=\"submit\">Save & Restart Bot</button>
    </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        CONFIG["webhook_url"] = request.form.get("webhook")
        CONFIG["keywords"] = [k.strip() for k in request.form.get("keywords").split("\
") if k.strip()]
        CONFIG["interval"] = int(request.form.get("interval", 120))
        return redirect(url_for("dashboard"))
    return render_template_string(HTML_TEMPLATE, config=CONFIG)

if __name__ == "__main__":
    # In a real deployment, the bot logic would run in a background thread
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
