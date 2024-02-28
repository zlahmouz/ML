import streamlit as st
import requests
from streamlit_lottie import st_lottie
import pickle
from pathlib import Path
import hashlib

# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	  c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	  data = c.fetchall()
	  return data

def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


##User authentification
st.set_page_config(page_title="ProjetLong", page_icon=":tada:", layout="wide")
choice=st.sidebar.selectbox("select",["login","signup"])
if choice=="login":

  #names=["lahmouz","trevor"]
  #usernames=["Zlh","pyr"]
  #passwords=["XXXXXX","XXX"]
  #load hashed passwords

  #file_path=Path(__file__).parent / "hashed_pw.pkl"

  #with file_path.open("rb") as file :
  # hashed_passwords=pickle.load(file)
  #credentials = {"usernames":{}}
          
  #for uname,name,pwd in zip(usernames,names,passwords):
  #   user_dict = {"name": name, "password": pwd}
    #  credentials["usernames"].update({uname: user_dict})
          
  #authenticator = stauth.Authenticate(credentials, "cokkie_name", "random_key", cookie_expiry_days=30)

  #authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "sales_dashboard", "abcdef", cookie_expiry_days=7)

  #name,authentication_status,usernames = authenticator.login()


  #if authentication_status ==False:
  # st.error("erreur username/password")

  username=st.sidebar.text_input("username",type="email")
  password=st.sidebar.text_input("password",type="password")
  if st.sidebar.checkbox("login"):
    create_usertable()
    hashed_pswd = make_hashes(password)

    if login_user(username,check_hashes(password,hashed_pswd)):
        st.success("Login successful")
        st.title('Chatbot for C code generation')
        lottie_coding = load_lottieurl("https://lottie.host/d86275a4-8cc5-4463-a8d1-03071f02f7ee/UnwrqECWFD.json")
        st_lottie(lottie_coding, height=300, key="coding")


        with st.sidebar:
            # Create a sidebar
            st.title('Info')
            st.write("---")
            st.sidebar.header("Get In Touch With Me!")
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
            local_css("/content/style.css")

            # Add logout button to the sidebar
            
                #st.warning("You have logged out.")
                # Add logout logic here (e.g., redirect to login page, clear session data, etc.)
            #authenticator.logout("Logout","sidebar")
        import streamlit as st
        model_name = "NousResearch/Llama-2-7b-chat-hf"
        import torch
        from transformers import (
            AutoTokenizer,
            AutoModelForCausalLM,
            BitsAndBytesConfig,
            pipeline,
            logging,
        )

        # load the quantized settings, we're doing 4 bit quantization
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=False,
        )

        # Load base model
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=bnb_config,
            # use the gpu
            device_map={"": 0}
        )

        # don't use the cache
        model.config.use_cache = False

        model.config.pretraining_tp = 1
        # Load the tokenizer from the model (llama2)
        tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True, use_fast=False)
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.padding_side = "right"
        # App title

        @st.cache_resource()
        def ChatModel(temperature, top_p):
            return AutoModelForCausalLM.from_pretrained(
                model_name, 
                model_type='llama',
                temperature=temperature, 
                top_p = top_p)

        # Replicate Credentials
        with st.sidebar:
            st.title('🦙💬 Llama 2 Chatbot')

            # Refactored from <https://github.com/a16z-infra/llama2-chatbot>
            st.subheader('Models and parameters')
            
            temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=2.0, value=0.1, step=0.01)
            top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
            # max_length = st.sidebar.slider('max_length', min_value=64, max_value=4096, value=512, step=8)
            chat_model =model
            # st.markdown('📖 Learn how to build this app in this [blog](#link-to-blog)!')

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
            pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=200)
            result = pipe(f"<s>[INST] {prompt} [/INST]")
            return(result[0]['generated_text'])

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
if choice=="signup":
   new_user=st.sidebar.text_input("username")
   new_password=st.sidebar.text_input("password",type="password")
   if st.sidebar.checkbox("signup"):
      create_usertable()
      add_userdata(new_user,make_hashes(new_password))
      st.success("You have successfully created an account.Go to the Login Menu to login")




      