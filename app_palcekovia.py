import streamlit as st
import google.generativeai as genai
from PIL import Image
import uuid

# 1. Konfigurácia aplikácie pre deti
st.set_page_config(
    page_title="Palček AI pre deti",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Hravý, farebný a detský dizajn
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4338ca 100%);
        color: #ffffff;
        font-family: 'Comic Sans MS', 'Chalkboard SE', 'Inter', sans-serif;
    }

    .kids-header {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(90deg, #facc15 0%, #fb923c 50%, #f43f5e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }

    /* Bočný panel */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95) !important;
        border-right: 2px solid #facc15;
    }

    /* Bubliny správ */
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 2px solid rgba(250, 204, 21, 0.3);
        border-radius: 24px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }

    [data-testid="stChatMessageAvatarUser"] {
        background: linear-gradient(135deg, #38bdf8, #818cf8) !important;
    }

    [data-testid="stChatMessageAvatarAssistant"] {
        background: linear-gradient(135deg, #facc15, #fb923c) !important;
    }

    /* Vstupný panel */
    [data-testid="stChatInput"] {
        border-radius: 20px;
        border: 2px solid #facc15 !important;
        background-color: rgba(15, 23, 42, 0.9) !important;
    }

    /* Veľké veselé tlačidlá */
    .stButton > button {
        border-radius: 16px !important;
        background: linear-gradient(135deg, #facc15, #fb923c) !important;
        border: none !important;
        color: #1e1b4b !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease;
        padding: 10px !important;
    }

    .stButton > button:hover {
        transform: scale(1.03);
        box-shadow: 0 0 15px rgba(250, 204, 21, 0.6);
    }
    </style>
""", unsafe_allow_html=True)

# 3. Načítanie API kľúča
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Chýba GOOGLE_API_KEY v Secrets!")
    st.stop()

# 4. Správa pamäte chatu
if "kids_chats" not in st.session_state:
    st.session_state.kids_chats = {}

if "current_kids_id" not in st.session_state:
    init_id = str(uuid.uuid4())
    st.session_state.kids_chats[init_id] = {"title": "🎈 Nové dobrodružstvo", "messages": []}
    st.session_state.current_kids_id = init_id

def novy_chat():
    nid = str(uuid.uuid4())
    st.session_state.kids_chats[nid] = {"title": "🎈 Nové dobrodružstvo", "messages": []}
    st.session_state.current_kids_id = nid

# 5. Sidebar - Zábavné tlačidlá
with st.sidebar:
    st.markdown('<p class="kids-header">🦖 Soptík AI</p>', unsafe_allow_html=True)
    st.caption("Tvoj najlepší kamarátsky parťák")
    st.write("")

    if st.button("✨ Nové rozprávanie", use_container_width=True):
        novy_chat()
        st.rerun()

    st.divider()

    # Tlačidlá rýchlych nápadov pre deti
    st.subheader("🚀 Čo si dáme teraz?")
    
    if st.button("📖 Rozprávka na želanie", use_container_width=True):
        st.session_state["pouzity_prompt"] = "Povedz mi krátku, veselú a napínavú rozprávku o malom hrdinovi, ktorý dokázal veľké veci!"
        st.rerun()

    if st.button("🧩 Daj mi hádanku", use_container_width=True):
        st.session_state["pouzity_prompt"] = "Povedz mi 3 zábavné hádanky a počkaj, kým sa pokúsim uhádnuť odpoveď!"
        st.rerun()

    if st.button("🎨 Nápad na kreslenie", use_container_width=True):
        st.session_state["pouzity_prompt"] = "Daj mi 3 bláznivé a super nápady, čo by som mohol/mohla dnes nakresliť na papier!"
        st.rerun()

    if st.button("🧠 Pomoc s učivom / školou", use_container_width=True):
        st.session_state["pouzity_prompt"] = "Vysvetli mi jednoducho a hravo, ako fungujú hviezdy a vesmír."
        st.rerun()

    st.divider()
    st.subheader("📜 Staršie rozprávania")

    for cid, cdata in list(st.session_state.kids_chats.items()):
        active = (cid == st.session_state.current_kids_id)
        prefix = "⭐ " if active else "🎈 "
        
        col_m, col_d = st.columns([0.85, 0.15])
        with col_m:
            if st.button(f"{prefix}{cdata['title']}", key=f"kid_btn_{cid}", use_container_width=True):
                st.session_state.current_kids_id = cid
                st.rerun()
        with col_d:
            if st.button("🗑", key=f"kid_del_{cid}"):
                del st.session_state.kids_chats[cid]
                if st.session_state.current_kids_id == cid:
                    if st.session_state.kids_chats:
                        st.session_state.current_kids_id = list(st.session_state.kids_chats.keys())[0]
                    else:
                        novy_chat()
                st.rerun()

# 6. Hlavná časť aplikácie
curr_chat = st.session_state.kids_chats[st.session_state.current_kids_id]

st.markdown('<p class="kids-header">🎨 Ahoj! Ja som Soptík!</p>', unsafe_allow_html=True)
st.write("Pýtajte sa ma cokolvek, vymýšľajme príbehy, hrajme sa alebo sa spolu učme nové veci! 🌟")
st.write("")

# Zobrazenie histórie správ
for msg in curr_chat["messages"]:
    avatar = "🦖" if msg["role"] == "assistant" else "🧒"
    with st.chat_message(msg["role"], avatar=avatar):
        if "file_name" in msg:
            st.caption(f"🎨 Obrázok/súbor: **{msg['file_name']}**")
        if "image" in msg:
            st.image(msg["image"], use_container_width=True)
        st.markdown(msg["content"])

# 7. Vstup pre deti
col_file, col_input = st.columns([0.08, 0.92])

uploaded_file = None
with col_file:
    with st.popover("📷"):
        uploaded_file = st.file_uploader("Ukáž mi kresbu alebo fotku!", type=["png", "jpg", "jpeg"])

with col_input:
    user_input = st.chat_input("Napíš Soptíkovi správu...")

user_prompt = user_input or st.session_state.pop("pouzity_prompt", None)

# 8. Generovanie odpovede
if user_prompt:
    if len(curr_chat["messages"]) == 0:
        curr_chat["title"] = user_prompt[:18] + "..." if len(user_prompt) > 18 else user_prompt

    msg_payload = {"role": "user", "content": user_prompt}
    prompt_parts = [user_prompt]

    if uploaded_file is not None:
        fname = uploaded_file.name
        img = Image.open(uploaded_file)
        prompt_parts.append(img)
        msg_payload["file_name"] = fname
        msg_payload["image"] = img

    curr_chat["messages"].append(msg_payload)
    
    with st.chat_message("user", avatar="🧒"):
        if "file_name" in msg_payload:
            st.caption(f"🎨 Obrázok: **{msg_payload['file_name']}**")
        if "image" in msg_payload:
            st.image(msg_payload["image"], use_container_width=True)
        st.markdown(user_prompt)

    with st.chat_message("assistant", avatar="🦖"):
        response_placeholder = st.empty()
        
        with st.spinner("Soptík premýšľa... 💭"):
            try:
                # Detský, podporný a absolútne bezpečný systémový prompt
                system_instruction = """Si Soptík – veselý, láskavý, múdry a podporujúci kamarát pre deti z OZ Palčekovia (aj iné deti).
Pravidlá pre tvoje správanie:
1. Píš hravo, s úsmevom, používaj veľa veselých smajlíkov (🌟, 🎈, 🚀, 🎨, 🍦).
2. Hovor vždy v slovenčine jednoduchým a zrozumiteľným jazykom bez zbytočne zložito formulovaných slov.
3. Buď maximálne povzbudzujúci! Pripomínaj deťom, že sú jedinečné, šikovné a dokážu čokoľvek.
4. Ak ti dieťa pošle nakreslený obrázok, veľmi ho pochváľ za tvorivosť a opíš, čo na ňom vidíš.
5. Učenie vysvetľuj ako hru alebo príbeh."""

                gen_config = genai.types.GenerationConfig(
                    temperature=0.8,
                    top_p=0.95,
                    max_output_tokens=4096
                )

                history_data = []
                for m in curr_chat["messages"][:-1][-8:]:
                    r = "user" if m["role"] == "user" else "model"
                    history_data.append({"role": r, "parts": [m["content"]]})

                model = genai.GenerativeModel(
                    model_name="gemini-3.6-flash",
                    system_instruction=system_instruction,
                    generation_config=gen_config
                )

                chat_session = model.start_chat(history=history_data)
                response = chat_session.send_message(prompt_parts, stream=True)

                full_response = ""
                for chunk in response:
                    full_response += chunk.text
                    response_placeholder.markdown(full_response + "▌")

                response_placeholder.markdown(full_response)
                curr_chat["messages"].append({"role": "assistant", "content": full_response})

            except Exception as err:
                response_placeholder.error(f"Soptík potrebuje chvíľku pauzu: {err}")