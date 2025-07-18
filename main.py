import csv
import os
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox, simpledialog, Checkbutton, IntVar

DATA_FILE = "verzuim_data.csv"
DATE_FORMAT = "%Y-%m-%d"

# Zorg dat het CSV-bestand bestaat
def initialize_csv():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Naam", "Startdatum", "Kaartje_verstuurd", "Mandje_besteld"])

# Voeg een nieuwe persoon toe
def add_person():
    naam = simpledialog.askstring("Nieuwe Afwezigheid", "Naam:")
    startdatum_str = simpledialog.askstring("Startdatum", "Startdatum (YYYY-MM-DD):")

    try:
        datetime.strptime(startdatum_str, DATE_FORMAT)
    except ValueError:
        messagebox.showerror("Fout", "Verkeerde datumformaat!")
        return

    with open(DATA_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([naam, startdatum_str, "nee", "nee"])

    messagebox.showinfo("Toegevoegd", f"{naam} toegevoegd met startdatum {startdatum_str}.")

# Controleer op meldingen en pop-ups
def check_dates():
    updated_rows = []

    with open(DATA_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            naam = row["Naam"]
            startdatum = datetime.strptime(row["Startdatum"], DATE_FORMAT)
            dagen_weg = (datetime.now() - startdatum).days

            kaartje_verstuurd = row["Kaartje_verstuurd"] == "ja"
            mandje_besteld = row["Mandje_besteld"] == "ja"

            if dagen_weg >= 21 and not kaartje_verstuurd:
                response = messagebox.askyesno("Herinnering", f"{naam} is al 3 weken afwezig. Kaartje al verstuurd?")
                if response:
                    row["Kaartje_verstuurd"] = "ja"

            if dagen_weg >= 45:
                messagebox.showinfo("Trakakast", f"{naam} is 45 dagen afwezig. Overweeg afsluiting in Trakakast.")

            if dagen_weg >= 60 and not mandje_besteld:
                response = messagebox.askyesno("Beterschapsmandje", f"{naam} is 2 maanden afwezig. Mandje besteld?")
                if response:
                    row["Mandje_besteld"] = "ja"

            updated_rows.append(row)

    # Schrijf de aangepaste data terug
    with open(DATA_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Naam", "Startdatum", "Kaartje_verstuurd", "Mandje_besteld"])
        writer.writeheader()
        writer.writerows(updated_rows)

# GUI opstarten
def start_gui():
    root = tk.Tk()
    root.withdraw()  # geen hoofdvenster

    check_dates()

    if messagebox.askyesno("Nieuwe Invoer", "Wil je een nieuwe persoon toevoegen?"):
        add_person()

# Main
if __name__ == "__main__":
    initialize_csv()
    start_gui()