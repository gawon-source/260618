import streamlit as st
import random
import time

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Foodstagram 🍽️", page_icon="🍽️", layout="wide")

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
menu_data = [
    ("🍕 피자", "치즈 폭발!", "★★★★★"),
    ("🍔 햄버거", "든든한 한끼!", "★★★★"),
    ("🍣 초밥", "신선함 MAX", "★★★★★"),
    ("🍜 라멘", "국물 맛집", "★★★★"),
    ("🍗 치킨", "오늘은 치킨각", "★★★★★"),
    ("🥩 스테이크", "고기 is love", "★★★★★"),
    ("🍝 파스타", "분위기까지 완벽", "★★★★"),
    ("🌮 타코", "색다른 맛", "★★★★"),
    ("🍛 카레", "호불호 없는 맛", "★★★★"),
    ("🍲 샤브샤브", "건강 + 맛", "★★★★★"),
    ("🍚 비빔밥", "한식 최고", "★★★★"),
    ("🍜 떡볶이", "매콤달콤", "★★★★★"),
]

comments = [
    "이 메뉴 오늘 딱인데요 😋",
    "와... 지금 너무 먹고 싶어요 🤤",
    "맛집 가야겠어요 🔥",
    "오늘 저녁은 이걸로 결정 💯"
]

dm_messages = [
    "오늘은 맛있는 하루가 될 것 같아요 🍀",
    "먹는 순간 행복해질 메뉴예요 💕",
    "후회 없는 선택입니다 😎"
]

# -------------------------------
# SESSION
# -------------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "likes" not in st.session_state:
    st.session_state.likes = random.randint(100, 999)

# -------------------------------
# HOME
# -------------------------------
if st.session_state.page == "home":

    st.markdown('<div class="title">🍽️ Foodstagram</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">오늘 뭐 먹지? 룰렛이 골라드려요 🎰✨</div>', unsafe_allow_html=True)

    name = st.text_input("👤 닉네임 입력", placeholder="예: foodie123")

    food_type = st.selectbox(
        "🍴 먹고 싶은 종류",
        ["전체", "한식", "양식", "일식", "패스트푸드"]
    )

    if st.button("🎰 메뉴 추천 시작"):
        if name:
            st.session_state.name = name
            st.session_state.food_type = food_type
            st.session_state.page = "result"
            st.session_state.likes = random.randint(100, 999)
            st.rerun()
        else:
            st.warning("닉네임을 입력해주세요!")

# -------------------------------
# RESULT
# -------------------------------
if st.session_state.page == "result":

    name = st.session_state.name
    followers = random.randint(100, 5000)

    st.markdown('<div class="title">🍽️ Foodstagram</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
    <h2>👤 {name}</h2>
    <p>❤️ Likes {st.session_state.likes} | 👥 Followers {followers}</p>
    <p><b>오늘의 메뉴 탐험가 🍴✨</b></p>
    </div>
    """, unsafe_allow_html=True)

    placeholder = st.empty()

    for _ in range(12):
        rolling = random.choice(menu_data)[0]
        placeholder.info(f"🎰 {rolling}")
        time.sleep(0.15)

    menu, desc, rating = random.choice(menu_data)
    match = random.randint(85, 99)

    placeholder.markdown(f"""
    <div class="feed">
    <h2>📸 Food Feed</h2>
    <h1>{menu}</h1>
    <h3>💖 만족도 {match}%</h3>
    <h3>⭐ 평점 {rating}</h3>
    <p><b>{desc}</b></p>
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

    st.markdown("### ✉️ Food DM")
    st.success(random.choice(dm_messages))

    st.markdown("### 🔥 Trending Menus")
    st.write("""
    #1 🍗 치킨  
    #2 🍕 피자  
    #3 🍜 떡볶이  
    #4 🍣 초밥  
    #5 🍔 햄버거  
    """)

    st.balloons()

    if st.button("🏠 처음으로 돌아가기"):
        st.session_state.page = "home"
        st.rerun()
