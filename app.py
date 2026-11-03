import os
import threading
import time
import urllib.request
from pathlib import Path

from flask import Flask, jsonify, send_from_directory

BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__, static_folder=None)

KEEP_ALIVE_URL = os.environ.get("KEEP_ALIVE_URL") or (
    "https://{}/healthz".format(
        os.environ.get("RENDER_EXTERNAL_HOSTNAME", "cofrekalltec.onrender.com")
    )
    if os.environ.get("RENDER")
    else ""
)
KEEP_ALIVE_SECONDS = int(os.environ.get("KEEP_ALIVE_SECONDS", "600"))


def keep_alive():
    # A instância free do Render dorme após 15 min sem tráfego.
    while True:
        time.sleep(KEEP_ALIVE_SECONDS)
        try:
            with urllib.request.urlopen(KEEP_ALIVE_URL, timeout=60) as res:
                res.read()
            app.logger.info("keep-alive ok")
        except Exception as exc:
            app.logger.warning("keep-alive falhou: %s", exc)


if KEEP_ALIVE_URL:
    threading.Thread(target=keep_alive, daemon=True).start()


@app.get("/")
def intro():
    return send_from_directory(BASE_DIR, "cofre_kalltec_intro.html")


@app.get("/cofre")
def vault():
    return send_from_directory(BASE_DIR, "index.html")


@app.get("/config")
def config():
    # Chaves ficam nas variáveis de ambiente do Render, fora do HTML.
    return jsonify({
        "supabaseUrl": os.environ.get("SUPABASE_URL", ""),
        "supabaseKey": os.environ.get("SUPABASE_PUBLISHABLE_KEY", ""),
        "authEmail": os.environ.get("AUTH_EMAIL", ""),
        "accessUser": os.environ.get("ACCESS_USER", "kalltec"),
    })


@app.get("/healthz")
def healthz():
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
