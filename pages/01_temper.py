import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="서울 기후 변화 대시보드", layout="wide")

st.title("🌏 서울 기후 변화 대시보드")
st.write("특정 날짜를 선택하면 서울의 과거와 현재 기온을 비교합니다.")

# ---------------------------
# 데이터 로드
# ---------------------------
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

# ---------------------------
# 날짜 선택
# ---------------------------
col1, col2 = st.columns(2)

with col1:
    month = st.selectbox("월 선택", list(range(1, 13)), index=5)

with col2:
    day = st.selectbox("일 선택", list(range(1, 32)), index=18)

selected = df[(df["month"] == month) & (df["day"] == day)].copy()

if selected.empty:
    st.warning("선택한 날짜의 데이터가 없습니다.")
    st.stop()

# ---------------------------
# 데이터 계산
# ---------------------------
past_avg = selected[(selected["year"] >= 1961) & (selected["year"] <= 1990)]["avg_temp"].mean()
recent_avg = selected[(selected["year"] >= 1991) & (selected["year"] <= 2020)]["avg_temp"].mean()

current = selected[selected["year"] == 2026]
current_temp = current["avg_temp"].iloc[0] if not current.empty else None

# ===========================
# 1. 상단 카드
# ===========================
st.subheader(f"📅 {month}월 {day}일 서울 기온 비교")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("과거 평균 (1961–1990)", f"{past_avg:.1f}°C")

with c2:
    st.metric("최근 평균 (1991–2020)", f"{recent_avg:.1f}°C")

with c3:
    if current_temp is not None:
        st.metric("현재 (2026)", f"{current_temp:.1f}°C")
    else:
        st.metric("현재 (2026)", "데이터 없음")

# ===========================
# 2. 순위 분석
# ===========================
st.subheader("🏆 2026년 선택 날짜 순위 분석")

all_temps = selected["avg_temp"].dropna().sort_values(ascending=False)

if current_temp is not None:
    rank = (all_temps > current_temp).sum() + 1
    percentile = rank / len(all_temps) * 100
    avg_temp = all_temps.mean()
    diff = current_temp - avg_temp

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("역대 순위", f"{rank}위")

    with c2:
        st.metric("상위 Percentile", f"{percentile:.1f}%")

    with c3:
        st.metric("평균 대비", f"{diff:.2f}°C")

# ===========================
# 3. Temperature Distribution
# ===========================
st.subheader("📊 Temperature Distribution")

fig_dist = px.histogram(
    selected,
    x="avg_temp",
    nbins=20,
    title=f"{month}월 {day}일 평균기온 분포"
)

st.plotly_chart(fig_dist, use_container_width=True)

# ===========================
# 4. 10년 단위 변화
# ===========================
st.subheader("📈 10년 단위 평균 변화")

selected["decade"] = (selected["year"] // 10) * 10
decade_avg = selected.groupby("decade")["avg_temp"].mean().reset_index()

fig_decade = px.line(
    decade_avg,
    x="decade",
    y="avg_temp",
    markers=True
)

st.plotly_chart(fig_decade, use_container_width=True)

# ===========================
# 5. 폭염 빈도
# ===========================
st.subheader("🔥 폭염 빈도 분석")

hot_25 = (selected["max_temp"] >= 25).sum()
hot_30 = (selected["max_temp"] >= 30).sum()

c1, c2 = st.columns(2)

with c1:
    st.metric("25°C 이상", f"{hot_25}일")

with c2:
    st.metric("30°C 이상", f"{hot_30}일")

# ===========================
# 6. TOP 10 더운 해
# ===========================
st.subheader("🏆 역대 가장 더웠던 해 TOP 10")

top10 = selected.sort_values("avg_temp", ascending=False).head(10)

fig_top10 = px.bar(
    top10,
    x="year",
    y="avg_temp",
    text="avg_temp",
    title=f"{month}월 {day} 기준 역대 가장 더운 해"
)

st.plotly_chart(fig_top10, use_container_width=True)

if not top10.empty:
    hottest = top10.iloc[0]
    st.info(
        f"역대 가장 더웠던 {month}월 {day}은 "
        f"{int(hottest['year'])}년 ({hottest['avg_temp']:.1f}°C) 입니다."
    )
