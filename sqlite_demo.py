import sqlite3
import csv
import json
import smtplib
import ssl
from string import Template

conn = sqlite3.connect(':memory:')  # create a DB in memory
c = conn.cursor()  # c will allow us to run commands in the DB

# creating the DB table "sometable"
c.execute("""CREATE TABLE sometable (
            dbname text,
            omail text,
            mmail text,
            cat text
            )""")


# function to insert a full entry to the "sometable" table
def insert_entry(entry):
    with conn:
        c.execute("INSERT INTO sometable VALUES (:dbname, :omail, :mmail, :cat)",
                  {'dbname': entry.dbname, 'omail': entry.omail, 'mmail': entry.mmail,
                   'cat': entry.cat})


# function to insert a partial entry to the DB. FOR THE CSV DATA
def insert_partial_entry(dbname, omail, mmail):
    with conn:
        c.execute("INSERT INTO sometable VALUES (:dbname, :omail, :mmail, NULL)",
                  {'dbname': dbname, 'omail': omail, 'mmail': mmail})


# function to update the DB entry and append the CAT.
def update_cat(dbname, cat):
    with conn:
        c.execute("""UPDATE sometable SET cat = :cat
                    WHERE dbname = :dbname""",
                  {'cat': cat, 'dbname': dbname})


# show all entries in the "sometable" table
def get_all_entries():
    c.execute("SELECT * FROM sometable;")
    return c.fetchall()


# get the owner of the DB
def get_owner(dbname):
    fetch = c.execute("SELECT omail FROM sometable WHERE dbname = :dbname", {"dbname": dbname}).fetchall()
    return fetch[0][0]


# setting up mail config and input data
port = 465  # For SSL
password = input("Type your email password and press enter: ")  # for login
context = ssl.create_default_context()  # create a secure SSL context
sender_email = "bo.testing.addr.ml@gmail.com"  # From we'll be sending mail.
message = """\
Subject: Validacion criticidad base de datos activos de informacion

Estimado $owner,
Junto con saludar, me comunico para solicitar su validacion respecto de la criticidad para la base de datos '$dbname'.
Asi, la criticidad asociada a la base de datos corresponde a: '$cat'.
Quedamos atentos a su confirmacion a traves de esta linea de correo.
Saludos cordiales,
Equipo Seguridad Informatica ML"""
msg_template = Template(message)  # setting up "message" as the template we'll use later

# process CSV Data and add it to DB
with open('CSV_Data.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')  # Setting delimiter character
    line_count = 0
    for row in csv_reader:
        if line_count == 0:  # first line/row are the headers of the file
            line_count += 1
        else:
            insert_partial_entry(row[0], row[1], row[3])  # Inserting data into DB
            line_count += 1

# Process JSON data and add it to db
with open('JSON_Data.txt') as json_file:
    local_json = json.load(json_file)
    for db in local_json["clasificacion-bd"]:
        temp_db = db.get("base-de-datos")  # getting db name from JSON file
        temp_cat = db.get("clasificacion")  # getting cat from JSON file
        update_cat(temp_db, temp_cat)  # updating cat in DB
        if temp_cat == "high":
            temp_owner = get_owner(temp_db)
            owner_mail = temp_owner + '@gmail.com'  # could be something like '@mercado-libre.cl'
            official_msg = msg_template.substitute(owner=temp_owner, dbname=temp_db, cat=temp_cat) # getting custom msg
            print("sending mail to... " + owner_mail + " owner of DB: " + temp_db + " with cat of: " + temp_cat)
            with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                server.login("bo.testing.addr.ml@gmail.com", password)  # login with input password
                server.sendmail(sender_email, owner_mail, official_msg)  # sending mail

print(get_all_entries())  # prints all entries in the memory database
conn.close()
