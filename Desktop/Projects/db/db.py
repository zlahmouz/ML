import streamlit as st
import psycopg2

# Fonction pour se connecter à la base de données PostgreSQL
def connect_db():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="azert12345AB+",
        host="zlahmouz"
    )
    return conn

# Fonction pour créer la table si elle n'existe pas
def create_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS utilisateurs
               (id SERIAL PRIMARY KEY,
               nom VARCHAR(255) NOT NULL,
               email VARCHAR(255) UNIQUE NOT NULL,
               mot_de_passe VARCHAR(255) NOT NULL)''')
    conn.commit()
    conn.close()

# Fonction pour inscrire un utilisateur
def signup(nom, email, mot_de_passe):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO utilisateurs (nom, email, mot_de_passe) VALUES (%s, %s, %s)", (nom, email, mot_de_passe))
    conn.commit()
    conn.close()

# Fonction pour vérifier les informations de connexion
def login(email, mot_de_passe):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM utilisateurs WHERE email=%s AND mot_de_passe=%s", (email, mot_de_passe))
    utilisateur = cur.fetchone()
    conn.close()
    return utilisateur

# Création de la table si elle n'existe pas
create_table()

# Interface utilisateur avec Streamlit
st.title("Système de Login/Signup avec PostgreSQL et Streamlit")

action = st.sidebar.selectbox("Action", ["Login", "Signup"])

if action == "Login":
    st.subheader("Connexion")
    email = st.text_input("Email")
    mot_de_passe = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        utilisateur = login(email, mot_de_passe)
        if utilisateur:
            st.success(f"Connecté en tant que {utilisateur[1]}")
        else:
            st.error("Email ou mot de passe incorrect")

elif action == "Signup":
    st.subheader("Inscription")
    nom = st.text_input("Nom")
    email = st.text_input("Email")
    mot_de_passe = st.text_input("Mot de passe", type="password")

    if st.button("S'inscrire"):
        signup(nom, email, mot_de_passe)
        st.success("Inscription réussie. Vous pouvez maintenant vous connecter.")
