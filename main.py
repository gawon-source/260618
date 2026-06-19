import streamlit as st
import random

# 페이지 설정
st.set_page_config(
    page_title="MBTI 진로 추천 🌈",
    page_icon="🚀",
    layout="wide"
)

# CSS 꾸미기
st.markdown("""
<style>
.main {
    background: linear-gradient(to bottom right, #f9f7ff, #e3f2fd);
}
.big-title {
    font-size: 48px;
    font-weight: bold;
    text-align: center;
    color: #6a1b9a;
}
.sub-title {
    font-size: 24px;
    text-align: center;
    color: #1565c0;
}
.result-box {
    background-color: #ffffff;
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.15);
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# MBTI별 직업 데이터
career_data = {
    "INTJ": ["🧠 데이터 과학자", "💻 AI 개발자", "📊 전략 컨설턴트"],
    "INTP": ["🔬 연구원", "💡 발명가", "👨‍💻 프로그래머"],
    "ENTJ": ["🏢 CEO", "📈 경영 컨설턴트", "⚖️ 변호사"],
    "ENTP": ["🚀 창업가", "📢 마케터", "🎤 방송인"],

    "INFJ": ["🩺 상담사", "✍️ 작가", "🎓 교육 전문가"],
    "INFP": ["🎨 디자이너", "🎬 콘텐츠 크리에이터", "📚 작가"],
    "ENFJ": ["👩‍🏫 교사", "🎤 강사", "🤝 HR 전문가"],
    "ENFP": ["🎭 배우", "📢 광고기획자", "🌟 크리에이터"],

    "ISTJ": ["🏦 회계사", "📋 공무원", "⚙️ 엔지니어"],
    "ISFJ": ["💉 간호사", "🏥 의료 코디네이터", "📖 사서"],
    "ESTJ": ["📊 관리자", "🏛️ 행정가", "🏗️ 프로젝트 매니저"],
    "ESFJ": ["👩‍⚕️ 간호사", "🎓 교사", "🤗 사회복지사"],

    "ISTP": ["🔧 기계 엔지니어", "🚗 자동차 전문가", "🛠️ 기술자"],
    "ISFP": ["🎨 아티스트", "📷 사진작가", "🎼 음악가"],
    "ESTP": ["💼 영업 전문가", "🏅 스포츠 코치", "🎤 이벤트 플래너"],
    "ESFP": ["🎬 연예인", "🎵 가수", "🎉 행사 기획자"]
}

# 헤더
st.markdown('<div class="big-title">🌈 MBTI 진로 추천 웹앱 🚀</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">학생들의 미래 직업을 추천해드려요! 💼✨</div>', unsafe_allow_html=True)

st.write("")
st.balloons()

# 사이드바
st.sidebar.header("📌 사용 방법")
st.sidebar.write("""
1️⃣ 자신의 MBTI를 선택하세요  
2️⃣ 추천 버튼을 누르세요  
3️⃣ 나에게 맞는 직업을 확인하세요 🚀  
""")

# MBTI 선택
mbti_list = list(career_data.keys())

selected_mbti = st.selectbox(
    "🧩 당신의 MBTI를 선택하세요!",
    mbti_list
)

# 버튼
if st.button("✨ 직업 추천 받기 ✨"):
    jobs = career_data[selected_mbti]
    recommended = random.sample(jobs, min(3, len(jobs)))

    st.markdown(f"""
    <div class="result-box">
        <h2 style="color:#6a1b9a;">🎯 {selected_mbti} 추천 직업</h2>
    </div>
    """, unsafe_allow_html=True)

    for job in recommended:
        st.success(job)

    st.write("")
    st.markdown("### 🌟 진로 조언")
    
    advice = {
        "I": "혼자 깊게 생각하는 능력이 뛰어나요 🧠",
        "E": "사람들과 소통하며 에너지를 얻어요 🤝",
        "S": "현실적이고 실용적인 감각이 좋아요 📌",
        "N": "창의적이고 미래지향적이에요 💡",
        "T": "논리적인 판단이 강점이에요 📊",
        "F": "공감 능력이 뛰어나요 ❤️",
        "J": "계획적이고 체계적이에요 📅",
        "P": "유연하고 적응력이 좋아요 🌊"
    }

    for char in selected_mbti:
        st.info(advice[char])

# 하단
st.write("")
st.markdown("---")
st.markdown("### 💖 오늘도 멋진 미래를 준비하는 여러분을 응원합니다! 🚀")
