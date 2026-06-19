import streamlit as st
import random
import time

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="CareerGram 📸", page_icon="📸", layout="wide")

# -------------------------------
# CSS
# -------------------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #ffd6e8, #d9c8ff, #c9f1ff);
}

.title {
    text-align:center;
    font-size:56px;
    font-weight:800;
    color:white;
}

.subtitle {
    text-align:center;
    font-size:20px;
    color:white;
    margin-bottom:30px;
}

.card {
    background:white;
    padding:25px;
    border-radius:25px;
    box-shadow:0px 8px 24px rgba(0,0,0,0.15);
    margin-top:20px;
}

.feed {
    background:white;
    padding:30px;
    border-radius:25px;
    box-shadow:0px 8px 24px rgba(0,0,0,0.15);
    margin-top:20px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# DATA
# -------------------------------
career_data = {
    "INTJ": [("AI 개발자", "9000만원", "SSS"), ("데이터 과학자", "8800만원", "SS"), ("전략 컨설턴트", "8500만원", "S")],
    "INTP": [("연구원", "7000만원", "S"), ("개발자", "8500만원", "SS"), ("발명가", "9000만원", "SSS")],
    "ENTJ": [("CEO", "1.2억원", "SSS"), ("변호사", "9000만원", "S"), ("기획자", "7500만원", "S")],
    "ENTP": [("창업가", "1억원", "SSS"), ("PD", "7000만원", "S"), ("마케터", "6500만원", "S")],
    "INFJ": [("상담사", "5000만원", "A"), ("교사", "5500만원", "A"), ("작가", "6000만원", "S")],
    "INFP": [("디자이너", "6500만원", "S"), ("작가", "6000만원", "S"), ("크리에이터", "8000만원", "SS")],
    "ENFP": [("크리에이터", "9000만원", "SS"), ("배우", "1억원", "SSS"), ("광고기획자", "7000만원", "S")],
    "ISTJ": [("공무원", "6000만원", "A"), ("회계사", "8000만원", "SS"), ("엔지니어", "7500만원", "S")],
    "ESFP": [("연예인", "1억원", "SSS"), ("가수", "9000만원", "SS"), ("MC", "7000만원", "S")]
}

comments = [
    "이 직업 진짜 잘 어울려요 🔥",
    "미래 유망 직업이에요 🚀",
    "성격과 궁합 최고 💯",
    "숨겨진 재능 발견 👀"
]

dm_messages = [
    "당신은 잠재력이 큰 사람입니다 🚀",
    "성장 가능성이 매우 높아요 🌟",
    "미래가 기대되는 인재예요 💫"
]

# 없는 MBTI 보완
all_mbti = ["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP","ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]
for m in all_mbti:
    if m not in career_data:
        career_data[m] = [("AI 개발자", "9000만원", "SS"), ("기획자", "7000만원", "S"), ("디자이너", "6500만원", "S")]

# -------------------------------
# SESSION STATE
# -------------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "likes" not in st.session_state:
    st.session_state.likes = random.randint(100, 999)

# -------------------------------
# HOME PAGE
# -------------------------------
if st.session_state.page == "home":

    st.markdown('<div class="title">📸 CareerGram</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">SNS처럼 즐기는 MBTI 진로 탐색 ✨</div>', unsafe_allow_html=True)

    name = st.text_input("👤 이름 입력", placeholder="예: 김민준")
    mbti = st.selectbox("🧩 MBTI 선택", all_mbti)

    if st.button("🚀 진로 추천 시작"):
        if name:
            st.session_state.name = name
            st.session_state.mbti = mbti
            st.session_state.page = "result"
            st.session_state.likes = random.randint(100, 999)
            st.rerun()
        else:
            st.warning("이름을 입력해주세요!")

# -------------------------------
# RESULT PAGE
# -------------------------------
if st.session_state.page == "result":

    name = st.session_state.name
    mbti = st.session_state.mbti

    followers = random.randint(100, 5000)

    st.markdown('<div class="title">📸 CareerGram</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
    <h2>👤 {name}</h2>
    <p>🧩 {mbti}</p>
    <p>❤️ Likes {st.session_state.likes} | 👥 Followers {followers}</p>
    <p><b>미래를 설계하는 특별한 인재 🚀</b></p>
    </div>
    """, unsafe_allow_html=True)

    placeholder = st.empty()
    jobs = career_data[mbti]

    for _ in range(10):
        rolling = random.choice(jobs)[0]
        placeholder.info(f"🎰 {rolling}")
        time.sleep(0.15)

    job, salary, tier = random.choice(jobs)
    match = random.randint(80, 99)

    placeholder.markdown(f"""
    <div class="feed">
    <h2>📸 Career Feed</h2>
    <h1>🚀 {job}</h1>
    <h3>❤️ 궁합 {match}%</h3>
    <h3>💸 평균 연봉 {salary}</h3>
    <h3>🔥 티어 {tier}</h3>
    </div>
    """, unsafe_allow_html=True)

    st.progress(match)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("❤️ 좋아요"):
            st.session_state.likes += 1
            st.rerun()

    with col2:
        st.metric("현재 좋아요", f"❤️ {st.session_state.likes}")

    st.markdown("### 💬 댓글")
    for c in random.sample(comments, 3):
        st.info(c)

    st.markdown("### ✉️ Career DM")
    st.success(random.choice(dm_messages))

    st.markdown("### 🔥 Trending Careers")
    st.write("""
    #1 AI 개발자 🤖  
    #2 콘텐츠 크리에이터 🎬  
    #3 UX 디자이너 🎨  
    #4 데이터 분석가 📊  
    #5 게임 개발자 🎮  
    """)

    st.balloons()

    if st.button("🏠 처음으로 돌아가기"):
        st.session_state.page = "home"
        st.rerun()
