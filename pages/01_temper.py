import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="서울 기후 타임머신", layout="wide")

st.title("🌏 서울 기후 타임머신")
st.write("특정 날짜를 선택하면 서울의 과거와 현재 기온을 비교합니다.")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("ta_20260619190504.csv", encoding="utf-8")
    except:
        df = pd.read_csv("ta_20260619190504.csv", encoding="cp949")

    # 컬럼 자동 인식
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
target_years = [1907, 1950, 2026]

# ======================
# 1. 상단 카드 비교
# ======================
st.subheader(f"📅 {month}월 {day}일 기온 비교")

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

# ======================
# 2. 얼마나 더워졌을까?
# ======================
st.subheader("🔥 서울은 얼마나 더워졌을까?")

compare_df = selected[selected["year"].isin(target_years)]

if not compare_df.empty:
    fig = px.bar(
        compare_df,
        x="year",
        y="avg_temp",
        text="avg_temp",
        title=f"{month}월 {day}일 평균기온 비교"
    )
    st.plotly_chart(fig, use_container_width=True)

    temp_1907 = compare_df[compare_df["year"] == 1907]["avg_temp"]
    temp_2026 = compare_df[compare_df["year"] == 2026]["avg_temp"]

    if not temp_1907.empty and not temp_2026.empty:
        diff = temp_2026.iloc[0] - temp_1907.iloc[0]
        st.success(
            f"1907년 대비 2026년 서울은 평균 {diff:.2f}°C 더 따뜻해졌습니다."
        )

# ======================
# 3. 역대 TOP10 더운 해
# ======================
st.subheader("🏆 역대 가장 더웠던 해 TOP 10")

top10 = selected.sort_values("avg_temp", ascending=False).head(10)

if not top10.empty:
    fig2 = px.bar(
        top10,
        x="year",
        y="avg_temp",
        text="avg_temp",
        title=f"{month}월 {day} 기준 역대 가장 더운 해"
    )
    st.plotly_chart(fig2, use_container_width=True)

    hottest = top10.iloc[0]
    st.info(
        f"역대 가장 더웠던 {month}월 {day}은 "
        f"{int(hottest['year'])}년 ({hottest['avg_temp']:.1f}°C) 입니다."
    )
