import streamlit as st
import random
import time

# -------------------------------
# 기본 설정
# -------------------------------
st.set_page_config(
    page_title="CareerGram 📸",
    page_icon="📸",
    layout="wide"
)

# -------------------------------
# CSS
# -------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #FEC8D8, #D5AAFF, #B5EAEA);
}

.main-title {
    text-align: center;
    font-size: 52px;
    font-weight: bold;
    color: white;
}

.sub-title {
    text-align: center;
    font-size: 20px;
    color: white;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.15);
    margin-top: 15px;
}

.feed-card {
    background: white;
    padding: 30px;
    border-radius: 25px;
    box-shadow: 0px 8px 20px rgba(0,0,0,0.15);
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# 데이터
# -------------------------------
career_data = {
    "INTJ": [("AI 개발자", "9000만원", "SSS"), ("전략 컨설턴트", "8500만원", "S"), ("데이터 과학자", "8800만원", "SS")],
    "INTP": [("연구원", "7000만원", "S"), ("개발자", "8500만원", "SS"), ("발명가", "9000만원", "SSS")],
    "ENTJ": [("CEO", "1.2억원", "SSS"), ("변호사", "9000만원", "S"), ("기획자", "7500만원", "S")],
    "ENTP": [("창업가", "1억원", "SSS"), ("마케터", "6500만원", "S"), ("PD", "7000만원", "S")],
    "INFJ": [("상담사", "5000만원", "A"), ("작가", "6000만원", "S"), ("교사", "5500만원", "A")],
    "INFP": [("디자이너", "6500만원", "S"), ("작가", "6000만원", "S"), ("크리에이터", "8000만원", "SS")],
    "ENFJ": [("교사", "5500만원", "A"), ("강사", "6500만원", "S"), ("HR 전문가", "7000만원", "S")],
    "ENFP": [("크리에이터", "9000만원", "SS"), ("광고기획자", "7000만원", "S"), ("배우", "1억원", "SSS")],
    "ISTJ": [("공무원", "6000만원", "A"), ("회계사", "8000만원", "SS"), ("엔지니어", "7500만원", "S")],
    "ISFJ": [("간호사", "6000만원", "A"), ("사서", "4500만원", "A"), ("교사", "5500만원", "A")],
    "ESTJ": [("관리자", "8000만원", "SS"), ("행정가", "7000만원", "S"), ("PM", "8500만원", "SS")],
    "ESFJ": [("간호사", "6000만원", "A"), ("교사", "5500만원", "A"), ("사회복지사", "5000만원", "A")],
    "ISTP": [("기계 엔지니어", "8000만원", "SS"), ("자동차 전문가", "7500만원", "S"), ("기술자", "6500만원", "S")],
    "ISFP": [("아티스트", "7000만원", "S"), ("사진작가", "6500만원", "S"), ("음악가", "8000만원", "SS")],
    "ESTP": [("영업 전문가", "8500만원", "SS"), ("코치", "7000만원", "S"), ("이벤트 플래너", "6500만원", "S")],
    "ESFP": [("연예인", "1억원", "SSS"), ("가수", "9000만원", "SS"), ("MC", "7000만원", "S")]
}

comments = [
    "이 직업 진짜 잘 어울려요 🔥",
    "미래 유망 직업이에요 🚀",
    "성격과 궁합 최고 💯",
    "숨겨진 재능이 보이네요 👀"
]

dm_messages = [
    "당신은 잠재력이 큰 사람입니다 🚀",
    "꾸준히 성장하면 큰 성공을 만들 수 있어요 🌟",
    "미래가 정말 기대되는 타입이에요 💫"
]

# -------------------------------
# 헤더
# -------------------------------
st.markdown('<p class="main-title">📸 CareerGram</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">SNS처럼 즐기는 MBTI 진로 탐색 ✨</p>', unsafe_allow_html=True)

# -------------------------------
# 입력
# -------------------------------
name = st.text_input("👤 이름 입력", placeholder="예: 김민준")
mbti = st.selectbox("🧩 MBTI 선택", list(career_data.keys()))

if name:
    likes = random.randint(500, 5000)
    followers = random.randint(100, 3000)

    st.markdown(f"""
    <div class="card">
    <h2>👤 {name}</h2>
    <p>🧩 {mbti}</p>
    <p>❤️ Likes {likes} | 👥 Followers {followers}</p>
    <p><b>미래를 설계하는 특별한 인재 🚀</b></p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.markdown("### 📷 Stories")
    col1, col2, col3, col4 = st.columns(4)
    col1.button("🤖 AI")
    col2.button("🎨 Design")
    col3.button("🚀 Future")
    col4.button("💸 Salary")

    if st.button("🎰 직업 추천 받기"):
        placeholder = st.empty()
        jobs = career_data[mbti]

        for _ in range(12):
            rolling = random.choice(jobs)[0]
            placeholder.info(f"🎰 {rolling}")
            time.sleep(0.15)

        job, salary, tier = random.choice(jobs)
        match = random.randint(80, 99)

        placeholder.markdown(f"""
        <div class="feed-card">
        <h2>📸 Career Feed</h2>
        <h1>🚀 {job}</h1>
        <h3>❤️ 궁합 {match}%</h3>
        <h3>💸 평균 연봉 {salary}</h3>
        <h3>🔥 티어 {tier}</h3>
        <p><b>"당신과 매우 잘 맞는 직업입니다!"</b></p>
        </div>
        """, unsafe_allow_html=True)

        st.progress(match)

        if st.button("❤️ 좋아요"):
            st.success("좋아요 +1 ❤️")

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
