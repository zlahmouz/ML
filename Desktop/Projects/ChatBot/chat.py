import streamlit as st
import psycopg2
from streamlit_lottie import st_lottie
import requests

# Fonction pour se connecter à la base de données PostgreSQL
def connect_db():
    conn = psycopg2.connect(
        dbname="wxcqkqvn",
        user="wxcqkqvn",
        password="1MmU3atbUECYw4sp3Aq21Xu417JJN9HU",
        host="flora.db.elephantsql.com"
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


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# Use local CSS
#def local_css(file_name):
 #   with open(file_name) as f:
  #      st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Création de la table si elle n'existe pas
create_table()

# Interface utilisateur avec Streamlit
st.title("Système de Login/Signup avec PostgreSQL et Streamlit")

action = st.sidebar.selectbox("Action", ["Login", "Signup"])

if action == "Login":
    st.subheader("Connexion")
    username=st.text_input("username")
    email = st.text_input("Email")
    mot_de_passe = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        utilisateur = login(email, mot_de_passe)
        if utilisateur:
            st.success(f"Connecté en tant que {utilisateur[1]}")
            st.title('Chatbot for C code generation')
            lottie_coding = load_lottieurl("https://lottie.host/d86275a4-8cc5-4463-a8d1-03071f02f7ee/UnwrqECWFD.json")
            st_lottie(lottie_coding, height=300, key="coding")


            with st.sidebar:
                # Create a sidebar
                st.title("Hello "+ username)
                st.sidebar.header("Send your feedback to enhance the application")
                st.sidebar.write("##")

                contact_form = """
                <form action="https://formsubmit.co/zakarialahmouz@gmail.com" method="POST">
                    <input type="hidden" name="_captcha" value="false">
                    <input type="text" name="name" placeholder="Your name" required>
                    <input type="email" name="email" placeholder="Your email" required>
                    <textarea name="message" placeholder="Your message here" required></textarea>
                    <button type="submit">Send</button>
                </form>
                """
                st.markdown(contact_form, unsafe_allow_html=True)
            #local_css("style.css")

            # Add logout button to the sidebar
            
                #st.warning("You have logged out.")
                # Add logout logic here (e.g., redirect to login page, clear session data, etc.)
            #authenticator.logout("Logout","sidebar")
        

            # Charger le modèle
            from transformers import GPT2LMHeadModel, GPT2Tokenizer
            tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

            # Charger le modèle
            model = GPT2LMHeadModel.from_pretrained("gpt2")

            # load the quantized settings, we're doing 4 bit quantization

            #from transformers import AutoModelForCausalLM, AutoTokenizer

            # Charger le tokenizer et le modèle DialoGPT
            #tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
            #model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
            # Replicate Credentials
        

            # Store LLM generated responses
            if "messages" not in st.session_state.keys():
                st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

            # Display or clear chat messages
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

            def clear_chat_history():
                st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
            st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

            # Function for generating LLaMA2 response
            def generate_llama2_response(prompt):
                inputs = tokenizer.encode(prompt, return_tensors="pt", max_length=50, truncation=True)
                outputs = model.generate(inputs, max_length=100, num_return_sequences=1, temperature=0.7)
                generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
                return(generated_text)

            # User-provided prompt
            if prompt := st.chat_input():
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.write(prompt)

            # Generate a new response if last message is not from assistant
            if st.session_state.messages[-1]["role"] != "assistant":
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        response = generate_llama2_response(prompt)
                        placeholder = st.empty()
                        full_response = ''
                        for item in response:
                            full_response += item
                            placeholder.markdown(full_response)
                        placeholder.markdown(full_response)
                message = {"role": "assistant", "content": full_response}
                st.session_state.messages.append(message)
                    
        else:
            st.error("Email ou mot de passe incorrect")

elif action == "Signup":
    st.subheader("Inscription")
    nom = st.text_input("username")
    email = st.text_input("Email")
    mot_de_passe = st.text_input("Mot de passe", type="password")

    if st.button("S'inscrire"):
        signup(nom, email, mot_de_passe)
        st.success("Inscription réussie. Vous pouvez maintenant vous connecter.")
