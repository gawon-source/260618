import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="서울 기후 변화 대시보드", layout="wide")

st.title("🌏 서울 기후 변화 대시보드")
st.write("특정 날짜를 선택하면 과거와 현재의 서울 기온을 비교합니다.")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("ta_20260619190504.csv", encoding="utf-8")
    except:
        df = pd.read_csv("ta_20260619190504.csv", encoding="cp949")

    col_map = {}

    for col in df.columns:
        if "날짜" in col or "일시" in col:
            col_map[col] = "date"
        elif "평균" in col:
            col_map[col] = "avg_temp"
        elif "최저" in col:
            col_map[col] = "min_temp"
        elif "최고" in col:
            col_map[col] = "max_temp"

    df = df.rename(columns=col_map)

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day

    for col in ["avg_temp", "min_temp", "max_temp"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


df = load_data()

# ----------------------
# 날짜 선택
# ----------------------
col1, col2 = st.columns(2)

with col1:
    month = st.selectbox("월 선택", list(range(1, 13)), index=5)

with col2:
    day = st.selectbox("일 선택", list(range(1, 32)), index=18)

selected = df[(df["month"] == month) & (df["day"] == day)]

# ----------------------
# 그룹별 평균 계산
# ----------------------
past_avg = selected[(selected["year"] >= 1961) & (selected["year"] <= 1990)]["avg_temp"].mean()
recent_avg = selected[(selected["year"] >= 1991) & (selected["year"] <= 2020)]["avg_temp"].mean()

current = selected[selected["year"] == 2026]
current_temp = current["avg_temp"].iloc[0] if not current.empty else None

# ======================
# 1. 상단 카드
# ======================
st.subheader(f"📅 {month}월 {day}일 서울 기온 비교")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("과거 평균 (1961–1990)", f"{past_avg:.1f}°C")

with col2:
    st.metric("최근 평균 (1991–2020)", f"{recent_avg:.1f}°C")

with col3:
    if current_temp is not None:
        st.metric("현재 (2026)", f"{current_temp:.1f}°C")
    else:
        st.metric("현재 (2026)", "데이터 없음")

# ======================
# 2. Bar Chart
# ======================
st.subheader("🔥 서울은 얼마나 더워졌을까?")

compare_df = pd.DataFrame({
    "period": ["1961-1990", "1991-2020", "2026"],
    "temp": [past_avg, recent_avg, current_temp]
})

fig = px.bar(
    compare_df,
    x="period",
    y="temp",
    text="temp"
)

st.plotly_chart(fig, use_container_width=True)

if current_temp is not None:
    diff = current_temp - past_avg
    st.success(f"1961–1990 대비 서울은 평균 {diff:.2f}°C 더 따뜻해졌습니다.")

# ======================
# 3. 역대 TOP10
# ======================
st.subheader("🏆 역대 가장 더웠던 해 TOP 10")

top10 = selected.sort_values("avg_temp", ascending=False).head(10)

fig2 = px.bar(
    top10,
    x="year",
    y="avg_temp",
    text="avg_temp"
)

st.plotly_chart(fig2, use_container_width=True)

if not top10.empty:
    hottest = top10.iloc[0]
    st.info(
        f"역대 가장 더웠던 {month}월 {day}은 "
        f"{int(hottest['year'])}년 ({hottest['avg_temp']:.1f}°C) 입니다."
    )
