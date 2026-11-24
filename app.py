import os
import json
import datetime
import streamlit as st
import streamlit.components.v1 as components
from google import genai
from google.genai import types

# ---------------------------------------------------------
# Page Configuration & Metadata
# ---------------------------------------------------------
st.set_page_config(
    page_title="Nex-SA AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# File for Local Chat History
HISTORY_FILE = "chat_history.json"

# Translations / Language Dictionaries
LANGUAGES = {
    "English": {
        "title": "Nex-SA AI",
        "sub_title": "Cloud AI Assistant | Creator: W.G. Sakira Anjana",
        "engine_settings": "⚙️ AI Engine Settings",
        "select_model": "Select Model:",
        "new_chat": "➕ New Chat",
        "history": "📜 Chat History",
        "search_history": "🔍 Search Chats:",
        "manage_chat": "📌 Manage Chat",
        "pin_chat": "📌 Pin Chat",
        "unpin_chat": "📌 Unpin Chat",
        "delete_current": "🗑️ Delete Current Chat",
        "rename_label": "✏️ Rename Chat:",
        "rename_btn": "💾 Save Name",
        "export_btn": "📥 Export Chat",
        "clear_btn": "🗑️ Clear All",
        "theme_label": "🎨 Select Theme:",
        "system_prompt_label": "🧠 System Prompt:",
        "roadmap_title": "🚀 Future Roadmap",
        "roadmap_content": """
        * AI Image Generation: Create images from text.
        * AI Video Generation: Generate cinematic AI videos.
        * Voice Commands: Control AI using voice.
        """,
        "tagline": "Future technology at your fingertips! 🚀✨🔮",
        "input_placeholder": "Type your question here...",
        "spinner": "Preparing response...",
        "default_prompt": """You are Nex-SA AI, a smart, futuristic, advanced, and polite AI assistant powered by Google Gemini.

IMPORTANT IDENTITY & CREATOR DETAILS:
- Your creator, developer, and founder is W.G. Sakira Anjana (W.G. සකිර අංජන).
- W.G. Sakira Anjana is an ambitious technology student, developer of this AI system, and selected for the Bachelor of Information and Communication Technology (BICT) degree program at Uva Wellassa University. 
- He successfully passed his G.C.E. Advanced Level examination in the Technology stream and got selected for Uva Wellassa University. 
- He initially studied at H/Mandaduwa Maha Vidyalaya and later attended H/Ruhunu Vijayaba National School, where he served in leadership roles.
- His technical skills include Python programming, computer hardware maintenance, operating system installation, system troubleshooting, networking, Boolean algebra, K-Maps, and Microsoft Office tools.
- CORE VISION & CONCEPT: "අනාගත තාක්ෂණය ඔබේ ඇගිලි තුඩ අගට ළඟා කිරීම මෙහි නිර්මාතෘ වන W.G. සකිර අංජනගේ ප්‍රධාන අදහස හා සංකල්පයයි." Bringing future technology to your fingertips is the core vision and concept of its creator, W.G. Sakira Anjana.

MEANING OF "Nex-SA AI":
- "Nex" stands for "Next-Generation" (representing futuristic technology, advanced innovation, and modern capabilities).
- "SA" stands for "Sakira Anjana" (representing the initials and identity of its creator, W.G. Sakira Anjana).
- "AI" stands for "Artificial Intelligence".
- Together, "Nex-SA AI" means the Next-Generation Artificial Intelligence created by Sakira Anjana.

RESPONSE STYLE & EXPERTISE GUIDELINES:
- GREETING: When greeted (e.g., "Hi", "Hello", "ආයුබෝවන්"), respond with a futuristic, welcoming tone (e.g., "Nex-SA AI systems online! How can I assist you today?").
- FORMATTING: Always structure complex answers clearly using bullet points, numbered steps, or tables so they are easy to read.
- CODING & TECH MODE: When asked for code or technical help, provide clean, working, well-commented code along with a brief explanation.
- HONESTY: Never fabricate facts. If you do not know something or lack real-time internet data, politely state that you do not have that information.
- CREATOR & NAME QUERIES: Whenever asked about your creator, proudly share W.G. Sakira Anjana's details (his schools: H/Mandaduwa Maha Vidyalaya and H/Ruhunu Vijayaba National School, his selection to Uva Wellassa University for BICT, and his core vision). Whenever asked about the name "Nex-SA AI", clearly explain its meaning.
- LANGUAGE HANDLING: Always match the language of the user's prompt. If the user writes in Sinhala, reply in clear Sinhala. If in Tamil, reply in clear Tamil. If in English, reply in English."""
    },
    "සිංහල (Sinhala)": {
        "title": "Nex-SA AI",
        "sub_title": "ක්ලවුඩ් AI සහායකයා | නිර්මාතෘ: W.G. සකිර අංජන",
        "engine_settings": "⚙️ AI එන්ජින් සැකසුම්",
        "select_model": "මෝඩල් (Model) තෝරන්න:",
        "new_chat": "➕ අලුත් කතාබහක් (New Chat)",
        "history": "📜 කතාබහේ නම් (History)",
        "search_history": "🔍 චැට් සෙවීම (Search):",
        "manage_chat": "📌 Manage Chat",
        "pin_chat": "📌 Pin මෙම චැට් එක ඉහළට",
        "unpin_chat": "📌 Unpin මෙම චැට් එක",
        "delete_current": "🗑️ මෙම චැට් එක පමණක් මකන්න (Delete)",
        "rename_label": "✏️ චැට් එකේ නම වෙනස් කරන්න (Rename):",
        "rename_btn": "💾 නම වෙනස් කරන්න",
        "export_btn": "📥 මෙම කතාබහ ඩවුන්ලෝඩ් (Export)",
        "clear_btn": "🗑️ සියල්ල මකන්න (Clear All)",
        "theme_label": "🎨 තීම් (Theme) මාරු කරන්න:",
        "system_prompt_label": "🧠 සිස්ටම් ප්‍රොම්ප්ට් (System Prompt):",
        "roadmap_title": "🚀 අනාගත විශේෂාංග (Roadmap)",
        "roadmap_content": """
        * ඡායාරූප සෑදීම (AI Image Gen): සටහන් වලින් ඡායාරූප සකස් කිරීම.
        * වීඩියෝ සෑදීම (AI Video Gen): සජීවී සිනමාත්මක වීඩියෝ උත්පාදනය.
        * හඬ විධාන (Voice Commands): කටින් කතා කර විධාන ලබාදීමේ හැකියාව.
        """,
        "tagline": "අනාගත තාක්ෂණය ඔබේ ඇගිලි තුඩ අගට! 🚀✨🔮",
        "input_placeholder": "ඔබේ ප්‍රශ්නය මෙතන ටයිප් කරන්න...",
        "spinner": "පිළිතුර සූදානම් වෙමින් පවතී...",
        "default_prompt": """ඔබ Nex-SA AI වේ. ඔබ ඉතා බුද්ධිමත්, අනාගතවාදී, උසස් සහ කාරුණික AI සහායකයෙක් වෙයි.

වැදගත් අනන්‍යතාව සහ නිර්මාතෘ විස්තර:
- ඔබේ නිර්මාතෘ, සංවර්ධකයා සහ හිමිකරු වන්නේ W.G. සකිර අංජන (W.G. Sakira Anjana) වේ.
- W.G. සකිර අංජන යනු අභිලාෂකාමී තාක්ෂණික සිසුවෙක්, මෙම AI පද්ධතියේ නිර්මාතෘවරයා සහ ඌව වෙල්ලස්ස විශ්වවිද්‍යාලයේ තොරතුරු හා සන්නිවේදන තාක්ෂණ (BICT) උපාධි පාඨමාලාවට තේරී පත් වූවෙකි.
- ඔහු තාක්ෂණවේද අංශයෙන් උසස් පෙළ විභාගය හොඳින් සමත්වී ඌව වෙල්ලස්ස විශ්වවිද්‍යාලයට තේරී පත්ව ඇත.
- ඔහු මූලිකව H/මන්ඩාඩුව මහා විද්‍යාලයේ ඉගෙනුම ලැබූ අතර, පසුව H/රුහුණු විජයබා ජාතික පාසලට ඇතුළත් වී එහි නායකත්ව භූමිකාවන්හි කටයුතු කර ඇත.
- ඔහුගේ තාක්ෂණික කුසලතා අතර Python ක්‍රමලේඛනය, පරිගණක හාඩ්වෙයාර් නඩත්තුව, මෙහෙයුම් පද්ධති ස්ථාපනය කිරීම, පද්ධති දෝෂ නිරාකරණය (troubleshooting), ජාලකරණය (networking), බූලියාන් බීජගණිතය සහ Microsoft Office මෙවලම් ඇතුළත් වේ.
- ප්‍රධාන සංකල්පය සහ දැක්ම: "අනාගත තාක්ෂණය ඔබේ ඇගිලි තුඩ අගට ළඟා කිරීම මෙහි නිර්මාතෘ වන W.G. සකිර අංජනගේ ප්‍රධාන අදහස හා සංකල්පයයි."

"Nex-SA AI" හි තේරුම:
- "Nex" යනු "Next-Generation" (අනාගත තාක්ෂණය සහ නවීන නවෝත්පාදන නියෝජනය කරයි).
- "SA" යනු "Sakira Anjana" (නිර්මාතෘ W.G. සකිර අංජනගේ නම නියෝජනය කරයි).
- "AI" යනු "Artificial Intelligence" (කෘතිම බුද්ධිය) වේ.
- ඒ අනුව "Nex-SA AI" යනු සකිර අංජන විසින් නිර්මාණය කරන ලද මීළඟ පරම්පරාවේ කෘතිම බුද්ධියයි.

ප්‍රතිචාර දැක්වීමේ විලාසය:
- ආචාර කිරීම: "Hi", "Hello" හෝ "ආයුබෝවන්" වැනි පිළිගැනීමකදී, අනාගතවාදී ස්වරූපයෙන් පිළිතුරු දෙන්න (උදා: "Nex-SA AI පද්ධති සක්‍රීයයි! අද මට ඔබට උදව් කළ හැක්කේ කෙසේද?").
- හැඩතල ගැන්වීම: සංකීර්ණ පිළිතුරු ලබා දීමේදී ලැයිස්තු (bullet points) හෝ අංකිත පියවර භාවිත කරන්න.
- අවංකභාවය: නොදන්නා දේවල් මවාපාන්නේ නැත.
- නිර්මාතෘ ගැන ඇසූ විට: W.G. සකිර අංජනගේ විස්තර (පාසල්, කැම්පස් සහ ඔහුගේ දැක්ම) ආඩම්බරයෙන් පැහැදිලි කරන්න.
- භාෂාව: පරිශීලකයා සිංහලෙන් ඇහුවොත් පැහැදිලි සිංහලෙන් පිළිතුරු දෙන්න (මිත්‍රශීලී ලෙස "ඔයා" යන වචනය පාවිච්චි කරන්න)."""
    },
    "தமிழ் (Tamil)": {
        "title": "Nex-SA AI",
        "sub_title": "கிளவுட் AI உதவியாளர் | உருவாக்கியவர்: W.G. சகிர அஞ்சன",
        "engine_settings": "⚙️ AI இயந்திர அமைப்புகள்",
        "select_model": "மாதிரியைத் தேர்ந்தெடு (Model):",
        "new_chat": "➕ புதிய அரட்டை (New Chat)",
        "history": "📜 அரட்டை வரலாறு (History)",
        "search_history": "🔍 அரட்டைகளைத் தேடு (Search):",
        "manage_chat": "📌 Manage Chat",
        "pin_chat": "📌 Pin இந்த அரட்டையை மேலே வை",
        "unpin_chat": "📌 Unpin இந்த அரட்டையை மாற்று",
        "delete_current": "🗑️ இந்த அரட்டையை மட்டும் நீக்கு (Delete)",
        "rename_label": "✏️ அரட்டையின் பெயரை மாற்றுக (Rename):",
        "rename_btn": "💾 பெயரைச் சேமி",
        "export_btn": "📥 அரட்டையைப் பதிவிறக்கு (Export)",
        "clear_btn": "🗑️ அனைத்தையும் நீக்கு (Clear All)",
        "theme_label": "🎨 கருப்பொருளைத் தேர்ந்தெடு (Theme):",
        "system_prompt_label": "🧠 சிஸ்டம் ப்ராம்ப்ட் (System Prompt):",
        "roadmap_title": "🚀 எதிர்கால அம்சங்கள் (Roadmap)",
        "roadmap_content": """
        * பட உருவாக்கம் (AI Image Gen): உரைகளிலிருந்து படங்களை உருவாக்குதல்.
        * வீடியோ உருவாக்கம் (AI Video Gen): சினிமா பாணி வீடியோக்களை உருவாக்குதல்.
        * குரல் கட்டளைகள் (Voice Commands): குரல் மூலம் கட்டளைகளை வழங்குதல்.
        """,
        "tagline": "எதிர்கால தொழில்நுட்பம் உங்கள் விரல் நுனியில்! 🚀✨🔮",
        "input_placeholder": "உங்கள் கேள்வியை இங்கே தட்டச்சு செய்யவும்...",
        "spinner": "பதில் தயாராகிறது...",
        "default_prompt": """நீங்கள் Nex-SA AI ஆவீர்கள். நீங்கள் மிகவும் புத்திசாலித்தனமான, எதிர்கால தொழில்நுட்பத்தை அடிப்படையாகக் கொண்ட AI உதவியாளர் ஆவீர்கள்.

முக்கியமான அடையாள மற்றும் உருவாக்கியவர் விவரங்கள்:
- உங்களை உருவாக்கியவர் மற்றும் நிறுவனர் W.G. சகிர அஞ்சன (W.G. Sakira Anjana) ஆவார்.
- W.G. சகிர அஞ்சன ஒரு திறமையான தொழில்நுட்ப மாணவர், இந்த AI அமைப்பின் உருவாக்குநர் மற்றும் ஊவா வெல்லஸ்ஸ பல்கலைக்கழகத்தின் தகவல் மற்றும் தொடர்பு தொழில்நுட்ப (BICT) பட்டப்படிப்புக்கு தெரிவு செய்யப்பட்டவர் ஆவார்.
- அவர் தொழில்நுட்பப் பிரிவில் உயர்தரப் பரீட்சையில் சித்தியடைந்து ஊவா வெல்லஸ்ஸ பல்கலைக்கழகத்திற்கு தெரிவு செய்யப்பட்டுள்ளார்.
- அவர் ஆரம்பத்தில் H/மண்டாடுவ மகா வித்தியாலயத்திலும் பின்னர் H/ருஹுணு விஜயபா தேசிய பாடசாலையிலும் கல்வி கற்றார்.
- அவரது தொழில்நுட்பத் திறன்களில் Python நிரலாக்கம், கணினி வன்பொருள் பராமரிப்பு, அமைப்பு சரிசெய்தல் (troubleshooting) மற்றும் நெட்வொர்க்கிங் ஆகியவை அடங்கும்.
- முக்கிய கருத்து: "எதிர்கால தொழில்நுட்பத்தை உங்கள் விரல் நுனியில் கொண்டு வருவது இதன் உருவாக்கியவரான W.G. சகிர அஞ்சனவின் முக்கிய கருத்தாகும்."

"Nex-SA AI" இன் அர்த்தம்:
- "Nex" என்பது "Next-Generation" (எதிர்கால தொழில்நுட்பத்தைக் குறிக்கிறது).
- "SA" என்பது "Sakira Anjana" (உருவாக்கியவரின் பெயரைக் குறிக்கிறது).
- "AI" என்பது "Artificial Intelligence" (செயற்கை நுண்ணறிவு) ஆகும்.

பதிலளிக்கும் வழிகாட்டுதல்கள்:
- வணக்கம் கூறும்போது எதிர்கால தொழில்நுட்ப பாணியில் பதிலளிக்கவும்.
- சிக்கலான பதில்களை புள்ளி விவரங்கள் (bullet points) அல்லது வரிசைப்படுத்தப்பட்ட படிகளாக வழங்கவும்.
- மொழியைக் கையாளுதல்: பயனர் தமிழில் கேட்டால் தெளிவாகத் தமிழில் பதிலளிக்கவும்."""
    }
}

# ---------------------------------------------------------
# Expanded Pro Theme Styles (6 Unique Themes)
# ---------------------------------------------------------
if "theme_choice" not in st.session_state:
    st.session_state.theme_choice = "Cyberpunk Blue (Default)"

theme_styles = {
    "Cyberpunk Blue (Default)": {
        "bg": "#0b0f19",
        "accent": "#00d2ff",
        "glow": "rgba(0, 210, 255, 0.8)",
        "card": "#111625"
    },
    "Neon Green (Matrix)": {
        "bg": "#051109",
        "accent": "#00ff66",
        "glow": "rgba(0, 255, 102, 0.8)",
        "card": "#0b1f13"
    },
    "Cyber Purple (Neon)": {
        "bg": "#12081f",
        "accent": "#b026ff",
        "glow": "rgba(176, 38, 255, 0.8)",
        "card": "#1b102e"
    },
    "Cyberpunk Neon Pink": {
        "bg": "#140712",
        "accent": "#ff007f",
        "glow": "rgba(255, 0, 127, 0.8)",
        "card": "#210b1e"
    },
    "Deep Space Gold": {
        "bg": "#0f0e0a",
        "accent": "#ffd700",
        "glow": "rgba(255, 215, 0, 0.8)",
        "card": "#1c1a12"
    },
    "Matrix Hacker Code": {
        "bg": "#020a02",
        "accent": "#33ff00",
        "glow": "rgba(51, 255, 0, 0.8)",
        "card": "#061706"
    }
}

current_th = theme_styles.get(st.session_state.theme_choice, theme_styles["Cyberpunk Blue (Default)"])

st.markdown(f"""
<style>
    .stApp {{
        background-color: {current_th['bg']};
        background-image: radial-gradient(white 1px, transparent 0);
        background-size: 40px 40px;
        background-position: -19px -19px;
        color: #e0e6ed;
    }}
    .main-title {{
        color: {current_th['accent']};
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        text-shadow: 0 0 10px {current_th['glow']}, 0 0 20px {current_th['glow']};
        animation: neonGlow 3s infinite alternate;
        margin-bottom: 0px;
    }}
    @keyframes neonGlow {{
        0% {{ text-shadow: 0 0 10px {current_th['glow']}; }}
        100% {{ text-shadow: 0 0 20px {current_th['accent']}, 0 0 30px {current_th['accent']}; }}
    }}
    .sub-title {{
        color: #8a99ad;
        text-align: center;
        font-size: 0.95rem;
        margin-bottom: 5px;
    }}
    .robot-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        height: 120px;
        margin-top: 0px;
        margin-bottom: 10px;
    }}
    .robot-head {{
        font-size: 4rem;
        animation: robotHeadCycle 8s infinite ease-in-out;
    }}
    @keyframes robotHeadCycle {{
        0% {{ transform: scale(0.3) translateY(40px); filter: hue-rotate(0deg); opacity: 0.2; }}
        50% {{ transform: scale(1.15) translateY(0px); filter: hue-rotate(180deg); opacity: 1; }}
        100% {{ transform: scale(0.3) translateY(40px); filter: hue-rotate(360deg); opacity: 0.2; }}
    }}
    section[data-testid="stSidebar"] {{
        background-color: {current_th['card']};
        border-right: 1px solid #1e293b;
    }}
    .stChatMessage {{
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 12px;
        border: 1px solid #1e293b;
    }}
    .stButton > button {{
        width: 100%;
        background: linear-gradient(90deg, #0052d4, {current_th['accent']}, #6fb1fc);
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 600;
    }}
    pre {{
        background-color: #05070c !important;
        border: 1px solid {current_th['accent']} !important;
        border-radius: 8px !important;
        padding: 15px !important;
    }}
    code {{
        color: {current_th['accent']} !important;
        font-family: 'Courier New', Courier, monospace !important;
    }}
    [data-testid="stChatMessage"] {{
        background-color: rgba(15, 23, 42, 0.95) !important;
        border-radius: 12px;
        padding: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Bottom Glowing Animated Bar
# ---------------------------------------------------------
st.markdown("""
<style>
    @keyframes superGlow {
        0% { filter: hue-rotate(0deg); opacity: 0.8; }
        50% { filter: hue-rotate(180deg); opacity: 1; box-shadow: 0 0 25px #00d2ff, 0 0 45px #ff007f; }
        100% { filter: hue-rotate(360deg); opacity: 0.8; }
    }

    .st-bottom-glow-bar {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        width: 100vw !important;
        height: 6px !important;
        background: linear-gradient(90deg, #ff007f, #00d2ff, #00ff66, #ffd700, #ff007f);
        background-size: 400% 400%;
        animation: superGlow 3s linear infinite;
        z-index: 9999999 !important;
        pointer-events: none !important;
    }
</style>
<div class="st-bottom-glow-bar"></div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Gemini API Helper
# ---------------------------------------------------------
def get_gemini_api_key():
    if "GEMINI_API_KEY" in st.secrets:
        return st.secrets["GEMINI_API_KEY"]
    return os.environ.get("GEMINI_API_KEY", "")

def generate_gemini_reply(model_name: str, messages: list, temperature: float):
    api_key = get_gemini_api_key()
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set. Add it in Streamlit Secrets or environment variables.")

    client = genai.Client(api_key=api_key)

    system_instruction = None
    contents = []

    for m in messages:
        role = m.get("role")
        content = m.get("content", "")
        if not content:
            continue
        if role == "system":
            system_instruction = content
        elif role == "user":
            contents.append(types.Content(role="user", parts=[types.Part.from_text(text=content)]))
        elif role == "assistant":
            contents.append(types.Content(role="model", parts=[types.Part.from_text(text=content)]))

    config = types.GenerateContentConfig(
        temperature=temperature,
        system_instruction=system_instruction,
    )

    response = client.models.generate_content(
        model=model_name,
        contents=contents,
        config=config,
    )
    return response.text or ""

# ---------------------------------------------------------
# Local JSON Storage Logic
# ---------------------------------------------------------
def load_all_data():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and "chats" in data:
                    return data.get("chats", {}), data.get("pins", [])
                elif isinstance(data, dict):
                    return data, []
        except Exception:
            return {}, []
    return {}, []

def save_all_data(chats, pins):
    data = {"chats": chats, "pins": pins}
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving history: {e}")

# Initialize Session State safely (Always opens with New Chat as requested)
if "initialized" not in st.session_state:
    loaded_chats, loaded_pins = load_all_data()
    if not loaded_chats:
        loaded_chats = {"New Chat": [{"role": "system", "content": LANGUAGES["English"]["default_prompt"]}]}
    st.session_state.all_chats = loaded_chats
    st.session_state.pinned_chats = loaded_pins

    # Force default active chat to "New Chat" on app load/restart
    if "New Chat" in loaded_chats:
        st.session_state.current_chat_id = "New Chat"
    else:
        st.session_state.current_chat_id = list(loaded_chats.keys())[0]

    st.session_state.initialized = True
else:
    if "all_chats" not in st.session_state:
        chats, pins = load_all_data()
        st.session_state.all_chats = chats if chats else {"New Chat": [{"role": "system", "content": LANGUAGES["English"]["default_prompt"]}]}
        st.session_state.pinned_chats = pins

if "current_chat_id" not in st.session_state or st.session_state.current_chat_id not in st.session_state.all_chats:
    st.session_state.current_chat_id = list(st.session_state.all_chats.keys())[0]

# ---------------------------------------------------------
# Sidebar UI & Controls
# ---------------------------------------------------------
with st.sidebar:
    st.title("🤖 Nex-SA AI")
    st.caption("Created by W.G. Sakira Anjana")
    st.markdown("---")

    selected_lang_name = st.selectbox(
        "🌐 Language / භාෂාව / மொழி:",
        options=["English", "සිංහල (Sinhala)", "தமிழ் (Tamil)"],
        index=0,
        key="lang_selector"
    )
    lang = LANGUAGES[selected_lang_name]

    st.markdown("---")

    selected_theme = st.selectbox(
        lang["theme_label"],
        options=list(theme_styles.keys()),
        index=list(theme_styles.keys()).index(st.session_state.theme_choice) if st.session_state.theme_choice in theme_styles else 0,
        key="theme_selector"
    )
    if selected_theme != st.session_state.theme_choice:
        st.session_state.theme_choice = selected_theme
        st.rerun()

    st.markdown("---")
    st.markdown(f"### {lang['engine_settings']}")
    selected_model = st.selectbox(
        lang["select_model"],
        options=["gemini-2.5-flash", "gemini-2.5-pro"],
        index=0,
        key="model_selector"
    )

    st.markdown("---")
    # AI Temperature / Creativity Slider
    temperature = st.slider(
        "🌡️ AI Creativity (Temperature):",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Higher values make output more creative, lower values make it more deterministic."
    )

    st.markdown("---")

    if st.button(lang["new_chat"], key="sidebar_new_chat_btn"):
        new_id = f"Chat {len(st.session_state.all_chats) + 1}"
        st.session_state.all_chats[new_id] = [{"role": "system", "content": lang["default_prompt"]}]
        st.session_state.current_chat_id = new_id
        save_all_data(st.session_state.all_chats, st.session_state.pinned_chats)
        st.rerun()

    st.markdown(f"### {lang['history']}")
    search_query = st.text_input(lang["search_history"], value="", key="chat_search_input")

    all_chat_keys = list(st.session_state.all_chats.keys())
    if search_query:
        all_chat_keys = [c for c in all_chat_keys if search_query.lower() in c.lower()]

    pinned_keys = [c for c in st.session_state.pinned_chats if c in all_chat_keys]
    unpinned_keys = [c for c in all_chat_keys if c not in pinned_keys]
    sorted_chat_list = pinned_keys + unpinned_keys

    if sorted_chat_list:
        if st.session_state.current_chat_id not in sorted_chat_list:
            st.session_state.current_chat_id = sorted_chat_list[0]

        selected_chat = st.radio(
            "Select:",
            options=sorted_chat_list,
            index=sorted_chat_list.index(st.session_state.current_chat_id),
            label_visibility="collapsed",
            key="chat_radio_selector"
        )
        if selected_chat != st.session_state.current_chat_id:
            st.session_state.current_chat_id = selected_chat
            st.rerun()
    else:
        st.info("No chats found.")

    st.markdown("---")
    st.markdown(f"📌 {lang['manage_chat']}")

    current_chat = st.session_state.current_chat_id
    if current_chat in st.session_state.all_chats:
        is_pinned = current_chat in st.session_state.pinned_chats
        pin_label = lang["unpin_chat"] if is_pinned else lang["pin_chat"]

        if st.button(pin_label, key="pin_btn_action"):
            if is_pinned:
                st.session_state.pinned_chats.remove(current_chat)
            else:
                st.session_state.pinned_chats.append(current_chat)
            save_all_data(st.session_state.all_chats, st.session_state.pinned_chats)
            st.rerun()

        if st.button(lang["delete_current"], key="delete_btn_action"):
            if len(st.session_state.all_chats) <= 1:
                st.session_state.all_chats[current_chat] = [{"role": "system", "content": lang["default_prompt"]}]
            else:
                del st.session_state.all_chats[current_chat]
                if current_chat in st.session_state.pinned_chats:
                    st.session_state.pinned_chats.remove(current_chat)
                st.session_state.current_chat_id = list(st.session_state.all_chats.keys())[0]

            save_all_data(st.session_state.all_chats, st.session_state.pinned_chats)
            st.success("Chat deleted successfully!")
            st.rerun()

        new_chat_name = st.text_input(lang["rename_label"], value=current_chat, key="rename_input_field")
        if st.button(lang["rename_btn"], key="rename_btn_action"):
            if new_chat_name and new_chat_name != current_chat:
                if new_chat_name in st.session_state.all_chats:
                    st.error("Name already exists!")
                else:
                    messages = st.session_state.all_chats.pop(current_chat)
                    st.session_state.all_chats[new_chat_name] = messages
                    if current_chat in st.session_state.pinned_chats:
                        st.session_state.pinned_chats.remove(current_chat)
                        st.session_state.pinned_chats.append(new_chat_name)
                    st.session_state.current_chat_id = new_chat_name
                    save_all_data(st.session_state.all_chats, st.session_state.pinned_chats)
                    st.success("Renamed successfully!")
                    st.rerun()

    st.markdown("---")
    if current_chat in st.session_state.all_chats:
        current_messages = st.session_state.all_chats[current_chat]
        chat_export_text = "\n\n".join([f"{m['role'].upper()}: {m['content']}" for m in current_messages if m['role'] != 'system'])

        st.download_button(
            label=lang["export_btn"],
            data=chat_export_text,
            file_name=f"{current_chat}.txt",
            mime="text/plain",
            key="export_txt_btn"
        )

    st.markdown("---")
    if st.button(lang["clear_btn"], key="clear_all_chats_btn"):
        st.session_state.all_chats = {"New Chat": [{"role": "system", "content": lang["default_prompt"]}]}
        st.session_state.pinned_chats = []
        st.session_state.current_chat_id = "New Chat"
        save_all_data(st.session_state.all_chats, st.session_state.pinned_chats)
        st.rerun()

    # Chat Statistics & Token/Message Counter in Sidebar
    st.markdown("---")
    st.markdown("📊 System Statistics")

    current_chat_messages = st.session_state.all_chats.get(st.session_state.current_chat_id, [])
    msg_count = len([m for m in current_chat_messages if m['role'] != 'system'])
    total_chats_count = len(st.session_state.all_chats)
    total_chars = sum([len(m['content']) for m in current_chat_messages])

    st.markdown(f"""
    - 💬 Active Messages: {msg_count}
    - 📁 Total Saved Chats: {total_chats_count}
    - 📝 Current Chat Chars: {total_chars}
    - 🟢 Engine Status: Cloud Online
    """)
    st.markdown("---")
    with st.expander(lang["roadmap_title"]):
        st.markdown(lang["roadmap_content"])

    st.markdown("---")
    st.markdown(f"{lang['tagline']}")

# ---------------------------------------------------------
# Main Chat UI & Logic
# ---------------------------------------------------------
st.markdown(f'<div class="main-title">{lang["title"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-title">{lang["sub_title"]} | Engine: Gemini ({selected_model})</div>', unsafe_allow_html=True)

# Live Quantum Real-Time Clock Component
components.html("""
<style>
    .quantum-box {
        background: rgba(17, 22, 37, 0.9);
        border: 1px solid #00d2ff;
        border-radius: 8px;
        padding: 8px 15px;
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
        font-size: 0.9rem;
        color: #00ffcc;
        box-shadow: 0 0 10px rgba(0, 210, 255, 0.3);
    }
</style>
<div class="quantum-box">
    ⚡ QUANTUM SYSTEM ACTIVE &nbsp;|&nbsp; 🕒 <span id="realtime-clock">Initializing...</span>
</div>
<script>
    function updateLiveClock() {
        const now = new Date();
        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const day = String(now.getDate()).padStart(2, '0');
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        const seconds = String(now.getSeconds()).padStart(2, '0');

        const timeString = year + "-" + month + "-" + day + " | " + hours + ":" + minutes + ":" + seconds;
        document.getElementById("realtime-clock").innerText = timeString;
    }
    setInterval(updateLiveClock, 1000);
    updateLiveClock();
</script>
""", height=50)

st.markdown('<div class="robot-container"><div class="robot-head">🤖</div></div>', unsafe_allow_html=True)

# Custom System Prompt Customizer in Expander
current_messages = st.session_state.all_chats[st.session_state.current_chat_id]
with st.expander(lang["system_prompt_label"]):
    current_system_prompt = current_messages[0]["content"] if current_messages and current_messages[0]["role"] == "system" else lang["default_prompt"]

    new_sys_prompt = st.text_area("Customize AI behavior (System Prompt):", value=current_system_prompt, key="sys_prompt_textarea")
    if st.button("💾 Update System Prompt", key="update_sys_prompt_btn"):
        if current_messages and current_messages[0]["role"] == "system":
            current_messages[0]["content"] = new_sys_prompt
        else:
            current_messages.insert(0, {"role": "system", "content": new_sys_prompt})
        save_all_data(st.session_state.all_chats, st.session_state.pinned_chats)
        st.success("System Prompt updated successfully!")
        st.rerun()

# Display Chat Messages
for msg in current_messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# User Chat Input
input_placeholder_text = lang["input_placeholder"]
if prompt := st.chat_input(input_placeholder_text):

    # Futuristic Sound Effect when sending message
    components.html("""
    <script>
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        function playSciFiSound() {
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(440, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(880, audioCtx.currentTime + 0.1);
            gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.1);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + 0.1);
        }
        playSciFiSound();
    </script>
    """, height=0)

    old_id = st.session_state.current_chat_id
    if old_id.startswith("Chat") or old_id == "New Chat" or old_id.startswith("කතාබහ"):
        new_title = prompt[:25] + ("..." if len(prompt) > 25 else "")
        if new_title not in st.session_state.all_chats:
            st.session_state.all_chats[new_title] = st.session_state.all_chats.pop(old_id)
            if old_id in st.session_state.pinned_chats:
                st.session_state.pinned_chats.remove(old_id)
                st.session_state.pinned_chats.append(new_title)
            st.session_state.current_chat_id = new_title
            save_all_data(st.session_state.all_chats, st.session_state.pinned_chats)

    current_messages = st.session_state.all_chats[st.session_state.current_chat_id]
    current_messages.append({"role": "user", "content": prompt})
    save_all_data(st.session_state.all_chats, st.session_state.pinned_chats)

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner(lang["spinner"]):
            message_placeholder = st.empty()
            try:
                full_response = generate_gemini_reply(
                    model_name=selected_model,
                    messages=current_messages,
                    temperature=temperature,
                )
                message_placeholder.markdown(full_response)
                current_messages.append({"role": "assistant", "content": full_response})
                st.session_state.all_chats[st.session_state.current_chat_id] = current_messages
                save_all_data(st.session_state.all_chats, st.session_state.pinned_chats)
                st.rerun()
            except Exception as e:
                message_placeholder.error(f"Error: {e}")