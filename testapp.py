import streamlit as st
import random
import json
import pickle

# --- Page Config ---
st.set_page_config(page_title="Keyword Recommender", page_icon="🔍", layout="wide")

# --- Inject CSS for toggle button styling ---
st.markdown("""
<style>
    /* Selected keyword button style */
    div[data-testid="stButton"] button.selected-btn {
        background-color: #6C63FF !important;
        color: white !important;
        border: 2px solid #6C63FF !important;
        border-radius: 20px !important;
    }

    div[data-testid="stButton"] > button {
        border-radius: 20px;
        padding: 0.4rem 1.2rem;
        font-size: 0.9rem;
        transition: all 0.2s ease;
        border: 2px solid #ccc;
        background-color: #f0f0f0;
        color: #333;
    }

    div[data-testid="stButton"] > button:hover {
        border-color: #6C63FF;
        color: #6C63FF;
    }

    .recommend-card {
        background: linear-gradient(135deg, #667eea22, #764ba222);
        border-left: 4px solid #6C63FF;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin-bottom: 1rem;
    }

    .recommend-card h4 {
        margin: 0 0 0.3rem 0;
        color: #333;
    }

    .recommend-card p {
        margin: 0;
        color: #555;
        font-size: 0.9rem;
    }

    .tag {
        display: inline-block;
        background-color: #6C63FF22;
        color: #6C63FF;
        border-radius: 12px;
        padding: 2px 10px;
        font-size: 0.78rem;
        margin: 2px;
        border: 1px solid #6C63FF55;
    }

    .selected-summary {
        background-color: #6C63FF11;
        border: 1px dashed #6C63FF;
        border-radius: 10px;
        padding: 0.6rem 1rem;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)


# --- Sample Data: Keyword Pool & Item Catalog ---
# KEYWORD_POOL = [
#     "Machine Learning", "Python", "Data Science", "Deep Learning", "NLP",
#     "Computer Vision", "Robotics", "Cloud Computing", "Blockchain", "Cybersecurity",
#     "Web Development", "Mobile Apps", "API Design", "DevOps", "Databases",
#     "JavaScript", "React", "Docker", "Kubernetes", "Open Source",
#     "Productivity", "Finance", "Health", "Travel", "Gaming",
#     "Music", "Photography", "Design", "Writing", "Marketing"
# ]

with open('keywords.pkl', 'rb') as f:
    keywords = json.loads(pickle.load(f))

KEYWORD_POOL = [kw for kw in keywords if keywords[kw] > 100]


CATALOG = [
    {"title": "Neural Networks from Scratch", "desc": "Build deep learning models step by step.", "tags": ["Machine Learning", "Deep Learning", "Python"]},
    {"title": "Advanced NLP with Transformers", "desc": "Master modern NLP using BERT and GPT.", "tags": ["NLP", "Deep Learning", "Python"]},
    {"title": "Computer Vision Masterclass", "desc": "Object detection, segmentation, and more.", "tags": ["Computer Vision", "Machine Learning", "Python"]},
    {"title": "Cloud Architecture on AWS", "desc": "Design scalable, fault-tolerant cloud systems.", "tags": ["Cloud Computing", "DevOps", "Databases"]},
    {"title": "Blockchain Development Guide", "desc": "Build decentralized apps on Ethereum.", "tags": ["Blockchain", "Web Development", "Open Source"]},
    {"title": "Ethical Hacking & Pentesting", "desc": "Learn offensive security from experts.", "tags": ["Cybersecurity", "Networking", "Open Source"]},
    {"title": "Full-Stack React & Node.js", "desc": "Build modern web apps end-to-end.", "tags": ["React", "JavaScript", "Web Development", "API Design"]},
    {"title": "Docker & Kubernetes in Production", "desc": "Container orchestration for real workloads.", "tags": ["Docker", "Kubernetes", "DevOps", "Cloud Computing"]},
    {"title": "Data Science with Python", "desc": "Pandas, NumPy, Matplotlib — the essentials.", "tags": ["Data Science", "Python", "Machine Learning"]},
    {"title": "Mobile App Dev with React Native", "desc": "Cross-platform iOS and Android apps.", "tags": ["Mobile Apps", "JavaScript", "React"]},
    {"title": "Personal Finance 101", "desc": "Budgeting, investing, and financial freedom.", "tags": ["Finance", "Productivity"]},
    {"title": "Travel Photography Guide", "desc": "Capture stunning photos around the world.", "tags": ["Travel", "Photography", "Design"]},
    {"title": "Music Production for Beginners", "desc": "From loops to full tracks in your DAW.", "tags": ["Music", "Design", "Productivity"]},
    {"title": "Content Marketing Playbook", "desc": "Grow your brand through strategic content.", "tags": ["Marketing", "Writing", "Productivity"]},
    {"title": "Game Development with Unity", "desc": "Build 2D and 3D games from scratch.", "tags": ["Gaming", "Design", "Mobile Apps"]},
    {"title": "Robotics with ROS", "desc": "Program autonomous robots using ROS2.", "tags": ["Robotics", "Python", "Machine Learning"]},
    {"title": "Health & Wellness Habits", "desc": "Science-backed routines for a better life.", "tags": ["Health", "Productivity"]},
    {"title": "API Design Best Practices", "desc": "REST, GraphQL, and beyond.", "tags": ["API Design", "Web Development", "JavaScript"]},
    {"title": "SQL & NoSQL Databases", "desc": "Master relational and document databases.", "tags": ["Databases", "Data Science", "Cloud Computing"]},
    {"title": "Open Source Contribution Guide", "desc": "Start contributing to real-world projects.", "tags": ["Open Source", "Python", "JavaScript", "DevOps"]},
]


# --- Session State Init ---
if "selected_keywords" not in st.session_state:
    st.session_state.selected_keywords = {}

if "keyword_display_set" not in st.session_state:
    st.session_state.keyword_display_set = random.sample(KEYWORD_POOL, 12)

if "recommendations" not in st.session_state:
    st.session_state.recommendations = []


# --- Recommender Logic ---
def get_recommendations(selected_kws):
    if not selected_kws:
        return []
    scored = []
    for item in CATALOG:
        score = sum(1 for kw in selected_kws if kw in item["tags"])
        if score > 0:
            scored.append((score, item))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [(score, item) for score, item in scored[:6]]


# --- UI ---
st.title("🔍 Keyword Recommender")
st.markdown("Pick the keywords that interest you, then hit **Recommend** to discover relevant content.")

st.divider()

# --- Keyword Buttons ---
st.subheader("🏷️ Choose Your Keywords")

cols = st.columns(6)
for i, kw in enumerate(st.session_state.keyword_display_set):
    with cols[i % 6]:
        is_selected = kw in st.session_state.selected_keywords

        # Button label shows ✓ if selected
        label = f"✓ {kw}" if is_selected else kw

        if st.button(label, key=f"kw_{kw}", use_container_width=True):
            if is_selected:
                del st.session_state.selected_keywords[kw]
            else:
                st.session_state.selected_keywords[kw] = True
            st.rerun()

# Shuffle button
st.markdown("")
if st.button("🔀 Shuffle Keywords", use_container_width=False):
    st.session_state.keyword_display_set = random.sample(KEYWORD_POOL, 12)
    # Deselect keywords no longer shown
    shown = set(st.session_state.keyword_display_set)
    st.session_state.selected_keywords = {
        k: v for k, v in st.session_state.selected_keywords.items() if k in shown
    }
    st.rerun()

st.divider()

# --- Selected Summary ---
selected_list = list(st.session_state.selected_keywords.keys())

if selected_list:
    tags_html = " ".join([f'<span class="tag">{kw}</span>' for kw in selected_list])
    st.markdown(
        f'<div class="selected-summary">🎯 <strong>Selected ({len(selected_list)}):</strong> {tags_html}</div>',
        unsafe_allow_html=True
    )
else:
    st.info("No keywords selected yet. Click any keyword above to select it.")

# --- Recommend Button ---
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("🚀 Recommend", type="primary", use_container_width=True, disabled=not selected_list):
        st.session_state.recommendations = get_recommendations(selected_list)

with col2:
    if st.button("🗑️ Clear All", use_container_width=False):
        st.session_state.selected_keywords = {}
        st.session_state.recommendations = []
        st.rerun()

# --- Results ---
if st.session_state.recommendations:
    st.divider()
    st.subheader(f"✨ Top Recommendations for you")

    for score, item in st.session_state.recommendations:
        tags_html = " ".join([f'<span class="tag">{t}</span>' for t in item["tags"]])
        match_text = f"{'⭐' * score} {score} keyword match{'es' if score > 1 else ''}"
        st.markdown(f"""
        <div class="recommend-card">
            <h4>{item['title']}</h4>
            <p>{item['desc']}</p>
            <br/>
            {tags_html} &nbsp;&nbsp; <small style="color:#999">{match_text}</small>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.get("recommendations") == [] and selected_list:
    st.warning("No matches found for your selected keywords. Try different ones!")