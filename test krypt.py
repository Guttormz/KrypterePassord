import tkinter as tk
from tkinter import *
from tkinter import messagebox
import sqlite3 as sq
import csv
import string
import random
from cryptography.fernet import Fernet

conn = sq.connect('personer.db') # Oppretter en database

c = conn.cursor() # Oppretter en cursor

if c.execute("SELECT name FROM sqlite_schema WHERE type='table' AND name='kunde'"): # Sjekker om tabellen post eksisterer
    try: 
        c.execute("DROP TABLE kunde") # Prøver å slette tabellen post
    except:
       sq.OperationalError # Hvis tabellen ikke eksisterer, så vil den ikke bli slettet

c.execute('CREATE TABLE IF NOT EXISTS kunde (brukernavn TEXT, passord TEXT)') # Oppretter tabellen post

#c.execute('DELETE FROM kunde WHERE brukernavn = "brukernavn"') # Sletter den første linjen i tabellen kunde

conn.commit() # Lagrer endringene

# Define the number of rows to read from the file
num_rows = 10

# Generate a random password for each user and write it to a new file
with open("randoms.csv", "r") as file_in, open("randoms_with_passwords.csv", "w", newline="") as file_out:
    reader = csv.reader(file_in)
    writer = csv.writer(file_out)

    # Write the headers to the new file
    headers = next(reader)
    headers.append("password")
    writer.writerow(headers)

    for i, row in enumerate(reader):
        if i < num_rows:
            # Generate a random password
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            # Add the password to the current row
            row.append(password)

            decrypted_data = password
            print(decrypted_data)

            passord = "passord"

            nok = Fernet.generate_key()

            fernet = Fernet(nok)


            encrypted_data = fernet.encrypt(passord.encode())

            # Decrypt the data
            decrypted_data = fernet.decrypt(encrypted_data).decode()
            row[-1] = encrypted_data

            # Write the row to the new file
            writer.writerow(row)
        else:
            break
f = open('randoms_with_passwords.csv', 'r') # Åpner filen randoms_with_passwords.csv i read
for line in f: # Går gjennom hver linje i filen
    c.execute('INSERT INTO kunde VALUES (?,?)', (line.split(',')[0], line.split(',')[1])) # Legger til hver linje i tabellen post
    
conn.commit() # Lagrer endringene

def admin(): 
    def logout():
        root.destroy() # Lukker vinduet
        hovedside() # Åpner hovedsiden

    root = tk.Tk() # Oppretter et vindu
    root.geometry("800x900") # Setter størrelsen på vinduet
    root.resizable(False, False) # Gjør det umulig å endre størrelsen på vinduet

    logout_button = tk.Button(root, text="Logout", padx=0, pady=0, font=("Arial", 50), command=lambda: [logout(), root.destroy()]) # Oppretter en logoutknapp
    logout_button.place(x=550, y=0) # Plasserer logoutknappen øverst til høyre på skjermen

    avslutt_button = tk.Button(root, text="Avslutt", bg="red", fg="white", padx=0, pady=0, font=("Arial", 50), command=root.destroy) # Oppretter en avsluttknapp
    avslutt_button.place(x=540, y=770) # Plasserer avsluttknappen nederst til høyre på skjermen

def log():
    def login():
        username = username_entry.get() # Henter brukernavnet fra brukernavnfeltet
        password = password_entry.get() # Henter passordet fra passordfeltet

        # Henter brukernavn og passord fra databasen
        c.execute("SELECT * FROM kunde WHERE brukernavn = ?", (username,))
        result = c.fetchone()

        if result: # Hvis brukernavnet finnes i databasen
            encrypted_password = result[1] # Henter det krypterte passordet fra databasen
            print(encrypted_password)

            passord = "passord"

            nok = Fernet.generate_key()

            fernet = Fernet(nok)

            encrypted_password = fernet.encrypt(passord.encode())

            decrypted_password = fernet.decrypt(encrypted_password).decode()

            if password == decrypted_password: # Hvis passordet er riktig
                root.destroy() # Lukker vinduet
                admin() # Åpner adminvinduet
            else: # Hvis passordet er feil
                messagebox.showerror("Error", "Feil brukernavn eller passord") # Viser en feilmelding
        else: # Hvis brukernavnet ikke finnes i databasen
            messagebox.showerror("Error", "Feil brukernavn eller passord") # Viser en feilmelding


    root = tk.Tk() # Oppretter et vindu
    root.geometry("800x900") # Setter størrelsen på vinduet
    root.resizable(False, False) # Gjør det umulig å endre størrelsen på vinduet

    username_label = tk.Label(root, text="Username:", font=("Arial", 40)) # Oppretter en label med teksten "Username:"
    password_label = tk.Label(root, text="Password:", font=("Arial", 40)) # Oppretter en label med teksten "Password:"
    username_entry = tk.Entry(root, font=("Arial", 40)) # Oppretter et brukernavnfelt
    password_entry = tk.Entry(root, show="*", font=("Arial", 40)) # Oppretter et passordfelt
    login_button = tk.Button(root, text="Login", bg="green", fg="white", command=login, font=("Arial", 40)) # Oppretter en loginknapp

    username_label.pack(pady=10) # Plasserer brukernavnlabelen øverst på skjermen
    username_entry.pack(pady=5) # Plasserer brukernavnfeltet under brukernavnlabelen
    password_label.pack(pady=10) # Plasserer passordlabelen under brukernavnfeltet
    password_entry.pack(pady=5) # Plasserer passordfeltet under passordlabelen
    login_button.pack(pady=10) # Plasserer loginknappen under passordfeltet
    return username_entry # Returnerer brukernavnfeltet

def hovedside():
    root = tk.Tk() # Oppretter et vindu
    root.geometry("800x900") # Setter størrelsen på vinduet
    root.resizable(False, False) # Gjør det umulig å endre størrelsen på vinduet

    login_button = tk.Button(root, bg="green", fg="white", text="Login", padx=0, pady=0, font=("Arial", 50), command=lambda: [log(), root.destroy()]) # Oppretter en loginknapp
    login_button.place(x=300, y=0) # Plasserer loginknappen øverst i midten på skjermen

    avslutt_button = tk.Button(root, text="Avslutt", bg="red", fg="white", padx=0, pady=0, font=("Arial", 50), command=root.destroy) # Oppretter en avsluttknapp
    avslutt_button.place(x=540, y=770) # Plasserer avsluttknappen nederst til høyre på skjermen


    root.mainloop() # Starter hovedløkken

hovedside()