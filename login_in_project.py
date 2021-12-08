from flask import Flask, render_template, request
import psycopg2


app = Flask(__name__)
#  Connection to the database
try:
    connection = psycopg2.connect(host="localhost", user="postgres", password="admin", database="continents")
    connection.autocommit = True
    cursor = connection.cursor()
except Exception as _ex:
    print(f"Error with PostgreSQL: {_ex}")


def fetching_data(continent, db = cursor):
    data = []
    db.execute(f"SELECT * FROM continents WHERE continent = '{continent}';")
    for i in range(9):
        data.append(db.fetchone())
    return data


user_data = {"email": "admin", "password": "admin"}


@app.route("/", methods=["GET", "POST"])
def home_page():
    email = request.form.get("email")
    password = request.form.get("password")
    if email and password:
        if email == user_data["email"] and password == user_data["password"]:
            asia = fetching_data("Азия")
            america = fetching_data("Америка")
            africa = fetching_data("Африка")
            europe = fetching_data("Европа")
            return render_template("tables.html", title="Tables", continent1=asia, continent2=america, continent3=africa, continent4=europe)
        else:
            return render_template("authorisation.html", title="Authorisation")
    else:
        return render_template("authorisation.html", title="Authorisation")


if __name__ == "__main__":
    app.run()
    if connection:
        connection.close()
        cursor.close()