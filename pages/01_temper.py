import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="서울 기후 타임머신", layout="wide")

st.title("🌏 서울 기후 타임머신")
st.write("특정 날짜의 서울 기온을 1907년 / 1950년 / 2026년과 비교합니다.")

# -------------------------
# CSV 로드
# -------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("ta_20260619190504.csv", encoding="utf-8")
    except:
        df = pd.read_csv("ta_20260619190504.csv", encoding="cp949")

    st.write("컬럼명 확인:", df.columns.tolist())

    # 컬럼명 자동 매핑
    date_col = None
    avg_col = None
    min_col = None
    max_col = None

    for col in df.columns:
        if "날짜" in col or "일시" in col:
            date_col = col
        if "평균" in col:
            avg_col = col
        if "최저" in col:
            min_col = col
        if "최고" in col:
            max_col = col

    if date_col is None:
        st.error("날짜 컬럼을 찾을 수 없습니다.")
        st.stop()

    df = df.rename(columns={
        date_col: "date",
        avg_col: "avg_temp",
        min_col: "min_temp",
        max_col: "max_temp"
    })

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day

    for col in ["avg_temp", "min_temp", "max_temp"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


df = load_data()

# -------------------------
# 날짜 선택
# -------------------------
col1, col2 = st.columns(2)

with col1:
    month = st.selectbox("월", list(range(1, 13)), index=5)

with col2:
    day = st.selectbox("일", list(range(1, 32)), index=18)

selected = df[(df["month"] == month) & (df["day"] == day)]

target_years = [1907, 1950, 2026]

st.subheader(f"{month}월 {day}일 서울 기온 비교")

cols = st.columns(3)

for i, year in enumerate(target_years):
    row = selected[selected["year"] == year]

    with cols[i]:
        st.markdown(f"## {year}")

        if row.empty:
            st.warning("데이터 없음")
        else:
            st.metric("평균기온", f"{row.iloc[0]['avg_temp']:.1f}°C")
            st.metric("최저기온", f"{row.iloc[0]['min_temp']:.1f}°C")
            st.metric("최고기온", f"{row.iloc[0]['max_temp']:.1f}°C")

# -------------------------
# 그래프
# -------------------------
st.subheader("📈 연도별 평균기온 변화")

chart_df = selected[["year", "avg_temp"]].dropna()

if not chart_df.empty:
    fig = px.line(chart_df, x="year", y="avg_temp", markers=True)
    st.plotly_chart(fig, use_container_width=True)
