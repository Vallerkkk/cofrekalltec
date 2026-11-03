import os
from pathlib import Path

from flask import Flask, jsonify, send_from_directory

BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__, static_folder=None)


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
