import streamlit as st
from streamlit_login_auth_ui.widgets import __login__
from ai71 import AI71
import requests
from streamlit_lottie import st_lottie
import re
from background import BackgroundCSSGenerator
from datetime import datetime

st.set_page_config(page_title="Edu-Bot", page_icon="📚", layout="wide")

img1_path = r"Main_bg.jpg"
img2_path = r"Main_bg.jpg"
background_generator = BackgroundCSSGenerator(img1_path, img2_path)
page_bg_img = background_generator.generate_background_css()
st.markdown(page_bg_img, unsafe_allow_html=True)

header = st.empty()
header.title("Edu-Bot: Your Personalized Educational Assistant 🎓")

# Login functionality
__login__obj = __login__(auth_token= st.secrets['Courier'],
                         company_name="Edu-Bot: A Personalized Educational Assistant",
                         width=300, height=350,
                         logout_button_name='Logout', hide_menu_bool=True,
                         hide_footer_bool=True,
                         lottie_url='https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

LOGGED_IN = __login__obj.build_login_ui()

if LOGGED_IN:
    # Set the API key
    header.empty()
    AI71_API_KEY = st.secrets['LLM']
    client = AI71(AI71_API_KEY)

    # Function to load Lottie animations
    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    # Lottie animations
    lottie_education = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_t2xm9bsw.json")
    lottie_robot = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_xh83pj1c.json")

    # Initialize session states
    if "user_info" not in st.session_state:
        st.session_state.user_info = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_started" not in st.session_state:
        st.session_state.chat_started = False
    if "response" not in st.session_state:
        st.session_state.response = None

    # Function to create system prompt
    def create_system_prompt(user_info):
        return f"""You are EduBot, an AI educational assistant tailored for {user_info['name']}, a {user_info['age']}-year-old {user_info['education_level']} student currently at the {user_info['study_level']} level. 
        Their main interests are {', '.join(user_info['interests'])}. Their learning style is {user_info['learning_style']} and they prefer {user_info['communication_style']} communication.
        Adjust your language and depth of explanations accordingly. Their career aspiration is to become a {user_info['career_aspiration']}.
        Provide informative, engaging, and age-appropriate responses to help them learn and explore their interests.
        Occasionally, suggest resources or activities that might enhance their understanding or skills in their areas of interest.
        Your responses should be concise yet informative, aiming for 2-3 paragraphs at most."""

    def clean_response(response):
        cleaned = re.split(r'\s*User:', response)[0]
        return cleaned.strip()

    # Function to call the Falcon API
    def call_falcon_api(messages):
        content = ""
        for chunk in client.chat.completions.create(
            messages=messages,
            model="tiiuae/falcon-180b-chat",
            stream=True,
        ):
            delta_content = chunk.choices[0].delta.content
            if delta_content:
                content += delta_content
        return clean_response(content)

    # Sidebar content
    def sidebar_content():
        with st.sidebar:
            st.warning("Press the Above button to Logout 🛑")
            st.divider()
            st.header("Edubot: A Personalized AI Mentor 🤖", divider='gray')

            if st.session_state.user_info:
                st.subheader(f"Welcome, {st.session_state.user_info['name']} 👋!")
                st.warning("Application is still under development. 🚧")
                st.error("Warning: Pressing this button will erase your session. ⚠️")
                if st.button("Start a New Session 🔄"):
                    st.session_state.chat_started = False
                    st.session_state.messages = []
                    st.rerun()
            with st.container(border=True):
             if lottie_robot:
                st_lottie(lottie_robot, height=200, key="robot")
                st.error("Did you know fear drives AI confinement? 😱")
            st.markdown("---")
            st.markdown("**Made with ❤️ by Your Amazing Team [ERROR 404]**")

    # User Input Page
    def user_input_page():
        with st.sidebar:
            st.error("Press the Above button to Logout 🛑")
            st.warning("Application is still under development. 🚧")
            st.divider()
            st.markdown("**Made with ❤️ by Your Amazing Team [ERROR 404]**")
        st.toast("Login Successful ✅", icon='✅')
        st.header(":rainbow-background[Welcome to EduBot: Your Personal Learning Companion! 🌟]", divider="gray")

        col1, col2 = st.columns([2, 1.2])

        with col1:
            st.markdown("**Let's personalize your learning experience. Tell us about yourself! ✨**")

            name = st.text_input("Your Name ✍️", placeholder="Ex: Adam")
            c1, c2 = st.columns([1, 1])
            with c1:
                age = st.number_input("Your Age 🎂", min_value=5, max_value=100, value=18)
            with c2:
                last_date = st.date_input("Date of Birth 📅", value=datetime.today())

            gender = st.selectbox("Gender 🚻", ['Male', 'Female', 'Prefer Not to Say'])
            c3, c4 = st.columns([1, 1])
            with c3:
                education_level = st.selectbox("Your Highest Level of Education 🎓",
                                               ["Elementary", "Middle School", "High School", "Undergraduate", "Graduate", "Doctorate"])
            with c4:
                study_level = st.selectbox("Your Current Level of Study 📚",
                                           ["School", "Diploma", "Undergraduate", "Postgraduate", "Doctorate"])
            interests = st.multiselect("Your Fields of Interest 🌟",
                                       ["Mathematics", "Physics", "Chemistry", "Biology", "Computer Science",
                                        "Literature", "History", "Art", "Music", "Psychology", "Economics"])
            c5, c6 = st.columns([1, 1])
            with c5:
                learning_style = st.selectbox("Your Preferred Learning Style 🧠",
                                              ["Visual", "Auditory", "Reading/Writing", "Kinesthetic"])
            with c6:
                communication_style = st.selectbox("Your Preferred Communication Style 💬",
                                                   ["Formal", "Casual", "Direct", "Storytelling"])
            career_aspiration = st.text_input("Your Career Aspiration 🚀", placeholder="Ex: Scholar, Dancer")

            if st.button("Start Your Learning Journey! 🎉"):
                if name and interests and career_aspiration:
                    st.session_state.user_info = {
                        "name": name,
                        "age": age,
                        "interests": interests,
                        "education_level": education_level,
                        "study_level": study_level,
                        "learning_style": learning_style,
                        "communication_style": communication_style,
                        "career_aspiration": career_aspiration
                    }
                    st.session_state.chat_started = True
                    st.session_state.messages.append({"role": "assistant", "content": f"Hi {name} 👋! Let's start your personalized learning experience, shall we? 🎓🚀"})
                    st.rerun()
                else:
                    st.warning("Please fill in all required fields (Name, Interests, and Career Aspiration).")

        with col2:
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            if lottie_education:
                st_lottie(lottie_education, height=400, key="education")
                st.warning("Did You Know 🤔: The American flag has 50 stars and 13 stripes.")

    # Chat Page
    @st.dialog("Terms and Condition 🧑‍🏫", width="large")
    def pop_up():
        st.markdown("Please understand that this application is under development and it doesn't have strict guardrails or a setup that makes it stick to the context, so please use it with caution and responsibly.")
        lets_do_that = st.button("Ok 👍")

        if lets_do_that:
            st.session_state.response = "Lets go"
            st.rerun()

    def chat_page():
        
        if st.session_state.response != "Lets go":
         pop_up()

        sidebar_content()

        st.header("Your Personal Learning Session 🧑‍🏫", divider='gray')

        # Initialize messages with system prompt if not already
        if not st.session_state.messages:
            system_prompt = create_system_prompt(st.session_state.user_info)
            st.session_state.messages.append({"role": "system", "content": system_prompt})
            st.session_state.messages.append({"role": "assistant", "content": f"Hi {st.session_state.user_info['name']} 👋! Welcome to EduBot. How can I assist you today? 🌟"})

        # Display chat history (excluding system prompt)
        for message in st.session_state.messages:
            if message["role"] != "system":
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        # User input at the bottom
        user_input = st.chat_input("Ask EduBot anything you'd like to learn about!")

        # Handle user input
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})

            with st.chat_message("user"):
                st.markdown(user_input)

            # Display toast while generating response
            st.toast("EduBot is thinking... ⏳", icon='⌛')

            # Generate the assistant response
            assistant_message = call_falcon_api(st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": assistant_message})

            with st.chat_message("assistant"):
                st.markdown(assistant_message)

    if not st.session_state.chat_started:
        user_input_page()
    else:
        chat_page()
