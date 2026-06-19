import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="서울 기후 타임머신",
    page_icon="🌏",
    layout="wide"
)

st.title("🌏 서울 기후 타임머신")
st.markdown("특정 날짜를 선택하면 **1907년 / 1950년 / 2026년 서울 기온**을 비교합니다.")

# -----------------------------
# 데이터 로드
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("ta_20260619190504.csv", encoding="utf-8")

    # 컬럼명 자동 감지
    col_map = {}

    for col in df.columns:
        if "날짜" in col or "일시" in col:
            col_map[col] = "date"
        elif "지점" in col:
            col_map[col] = "station"
        elif "평균" in col:
            col_map[col] = "avg_temp"
        elif "최저" in col:
            col_map[col] = "min_temp"
        elif "최고" in col:
            col_map[col] = "max_temp"

    df = df.rename(columns=col_map)

    # 날짜 처리
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day

    # 숫자 변환
    for col in ["avg_temp", "min_temp", "max_temp"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


df = load_data()

# -----------------------------
# 날짜 선택
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    month = st.selectbox("월", list(range(1, 13)), index=5)

with col2:
    day = st.selectbox("일", list(range(1, 32)), index=18)

selected = df[(df["month"] == month) & (df["day"] == day)]

target_years = [1907, 1950, 2026]
filtered = selected[selected["year"].isin(target_years)]

# -----------------------------
# 기온 비교
# -----------------------------
st.subheader(f"📅 {month}월 {day}일 기온 비교")

cols = st.columns(3)

for i, year in enumerate(target_years):
    row = filtered[filtered["year"] == year]

    with cols[i]:
        st.markdown(f"## {year}")

        if not row.empty:
            avg = row.iloc[0]["avg_temp"]
            min_t = row.iloc[0]["min_temp"]
            max_t = row.iloc[0]["max_temp"]

            st.metric("평균기온", f"{avg:.1f}°C")
            st.metric("최저기온", f"{min_t:.1f}°C")
            st.metric("최고기온", f"{max_t:.1f}°C")
        else:
            st.warning("데이터 없음")

# -----------------------------
# 전체 변화 그래프
# -----------------------------
st.subheader("📈 연도별 평균기온 변화")

chart_df = selected[["year", "avg_temp"]].dropna()

if not chart_df.empty:
    fig = px.line(
        chart_df,
        x="year",
        y="avg_temp",
        markers=True,
        title=f"{month}월 {day}일 평균기온 변화"
    )
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# 온난화 분석
# -----------------------------
temp_1907 = filtered[filtered["year"] == 1907]["avg_temp"]
temp_2026 = filtered[filtered["year"] == 2026]["avg_temp"]

if not temp_1907.empty and not temp_2026.empty:
    diff = temp_2026.iloc[0] - temp_1907.iloc[0]

    if diff > 0:
        st.success(
            f"🔥 {month}월 {day}일 서울은 1907년보다 "
            f"{diff:.2f}°C 더 따뜻합니다."
        )
    else:
        st.info(
            f"❄️ {month}월 {day}일 서울은 1907년보다 "
            f"{abs(diff):.2f}°C 더 낮습니다."
        )
