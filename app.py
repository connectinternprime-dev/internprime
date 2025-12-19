from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = "internprime_secret_key"

def get_db():
    return sqlite3.connect("internprime.db")

@app.route("/")
def index():
    return render_template("index.html")

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        if password != confirm:
            flash("❌ Passwords do not match", "danger")
            return redirect(url_for("register"))

        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, password)
            )
            db.commit()
            db.close()

            flash("✅ Registration successful. Please login.", "success")
            return redirect(url_for("login"))

        except Exception as e:
            flash("❌ Email already exists", "danger")
            return redirect(url_for("register"))

    return render_template("register.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )
        user = cursor.fetchone()
        db.close()

        if user:
            session["user"] = email
            flash("✅ Login successful", "success")
            return redirect(url_for("apply"))
        else:
            flash("❌ Invalid login credentials", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")


# ---------------- APPLY (PROTECTED) ----------------
@app.route("/apply", methods=["GET", "POST"])
def apply():
    if "user" not in session:
        flash("⚠ Please login first", "warning")
        return redirect(url_for("login"))

    if request.method == "POST":
        fullname = request.form.get("fullname")
        email = request.form.get("email")
        course = request.form.get("course")
        message = request.form.get("message")

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO applications (user_email, course) VALUES (?, ?)",
            (session["user"], course)
        )
        db.commit()
        db.close()

        flash("🎉 Application submitted successfully", "success")
        return redirect(url_for("apply"))

    return render_template("apply.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("👋 Logged out successfully", "info")
    return redirect(url_for("login"))

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

