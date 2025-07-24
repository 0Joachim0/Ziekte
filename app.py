from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = "data.xlsx"
DATE_FORMAT = "%Y-%m-%d"

def initialize_excel():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=[
            "Naam", "Startdatum", "Arbeidsongeval", "dagen afwezig", 
            "Kaartje verstuurd", "Zorgteam verwittigd", "Trakakast afgesloten", "Beterschaps mandje"
        ])
        df.to_excel(DATA_FILE, index=False)

@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")

@app.route("/api/list", methods=["GET"])
def get_list():
    df = pd.read_excel(DATA_FILE)
    for idx, row in df.iterrows():
        start = datetime.strptime(str(row["Startdatum"]), DATE_FORMAT)
        dagen = (datetime.now() - start).days
        df.at[idx, "dagen afwezig"] = dagen
    df.to_excel(DATA_FILE, index=False)
    return df.to_dict(orient="records")

@app.route("/api/add", methods=["POST"])
def add_person():
    data = request.json
    if not data or "naam" not in data or "startdatum" not in data or "arbeidsongeval" not in data:
        return jsonify({"error": "Ongeldige data"}), 400

    df = pd.read_excel(DATA_FILE)
    new_row = {
        "Naam": data["naam"],
        "Startdatum": data["startdatum"],
        "Arbeidsongeval" : data["arbeidsongeval"],
        "dagen afwezig": 0,
        "Zorgteam verwittigd": "nee",
        "Kaartje verstuurd": "nee",
        "Trakakast afgesloten": "nee",
        "Beterschaps mandje": "nee"
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_excel(DATA_FILE, index=False)
    return jsonify({"success": True}), 201

@app.route("/api/update/<int:index>", methods=["PATCH"])
def update_person(index):
    data = request.json
    if not data:
        return jsonify({"error": "Geen data meegegeven"}), 400

    df = pd.read_excel(DATA_FILE)

    if index < 0 or index >= len(df):
        return jsonify({"error": "Ongeldige index"}), 404

    # Verwijderen van persoon
    if data.get("verwijderen"):
        df = df.drop(index).reset_index(drop=True)
        df.to_excel(DATA_FILE, index=False)
        return jsonify({"success": True, "message": "Persoon verwijderd"})

    # Updaten van velden (bijv. Kaartje verstuurd, etc.)
    update_fields = ["Kaartje verstuurd", "Zorgteam verwittigd", "Trakakast afgesloten", "Beterschaps mandje"]
    updated = False
    for veld in update_fields:
        if veld in data:
            waarde = data[veld]
            # Zet "ja" of "nee" afhankelijk van bool / string
            if isinstance(waarde, bool):
                df.at[index, veld] = "ja" if waarde else "nee"
            elif isinstance(waarde, str) and waarde.lower() in ["ja", "nee"]:
                df.at[index, veld] = waarde.lower()
            else:
                return jsonify({"error": f"Ongeldige waarde voor {veld}"}), 400
            updated = True

    if updated:
        df.to_excel(DATA_FILE, index=False)
        return jsonify({"success": True, "message": "Status bijgewerkt"})

    return jsonify({"error": "Geen geldige velden om te updaten"}), 400


if __name__ == "__main__":
    initialize_excel()
    app.run(debug=True)
