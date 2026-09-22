# ============================================================
# 영화 데이터 그래프 도감 2 - 분포와 관계
# ------------------------------------------------------------
# - KOBIS 박스오피스 10위권에 든 영화 중, 이 기간에 개봉한 216편의
#   요약 데이터를 가지고 "분포"와 "관계"를 보여주는 그래프들을 모아둔
#   도감입니다.
# - 앞으로 그래프가 계속 늘어날 예정이라, 그래프마다 번호가 붙은
#   구역(section)으로 나눠뒀습니다. 새 그래프를 추가할 땐 그 구역
#   패턴을 그대로 복사해서 아래에 이어 붙이면 됩니다.
# - 초보자를 위해 곳곳에 한국어 주석을 달아두었습니다.
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------------------------
# 0. 기본 설정
# ------------------------------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide",
)

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


# ------------------------------------------------------------
# 1. 데이터 불러오기
# ------------------------------------------------------------
# st.cache_data : 한 번 불러온 데이터는 저장해두고 재사용해서,
# 페이지를 새로고침해도 매번 인터넷에서 다시 받아오지 않습니다.
@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_URL)

    # 'openDt' 열은 20250903처럼 하이픈 없는 여덟 자리 숫자로 되어 있습니다.
    # 문자열로 바꾼 뒤 진짜 날짜(datetime) 타입으로 변환합니다.
    df["openDt"] = pd.to_datetime(df["openDt"].astype(str), format="%Y%m%d")

    # 'genre' 열은 "드라마|코미디"처럼 세로막대(|) 기호로 여러 장르가
    # 적혀 있는 경우가 있습니다. 여기서는 첫 번째 장르만 대표 장르로 씁니다.
    df["대표장르"] = df["genre"].astype(str).str.split("|").str[0]

    return df


df = load_data()

# ------------------------------------------------------------
# 2. 화면 제목
# ------------------------------------------------------------
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.markdown(
    "이 기간에 개봉한 216편의 영화 데이터를 가지고, "
    "**장르·국가 같은 분포**와 **숫자들 사이의 관계**를 보여주는 그래프 모음입니다."
)

st.divider()

# ============================================================
# 구역 1. 장르별 영화 편수
# ============================================================
st.header("① 장르별 영화 편수")
st.markdown(
    "영화마다 대표 장르(여러 장르가 적혀 있으면 첫 번째 장르) 하나를 기준으로, "
    "장르별로 몇 편씩 있는지 도넛 그래프로 보여줍니다."
)

genre_counts = (
    df["대표장르"]
    .value_counts()
    .reset_index()
)
genre_counts.columns = ["대표장르", "편수"]

fig1 = px.pie(
    genre_counts,
    names="대표장르",
    values="편수",
    hole=0.45,
    title="장르별 영화 편수",
)
fig1.update_traces(
    hovertemplate="장르: %{label}<br>편수: %{value}편<br>비율: %{percent}<extra></extra>"
)
fig1.update_layout(legend_title_text="장르")

st.plotly_chart(fig1, width="stretch", key="chart_1")

# '이 그래프로 알 수 있는 것' 문구를 적어 넣을 자리입니다.
# 그래프를 보고 알게 된 점을 한 문장으로 직접 적어보세요.
st.text_input(
    "📝 이 그래프로 알 수 있는 것",
    placeholder="예: 이 기간 박스오피스 10위권 영화 중 드라마 장르가 가장 많았다.",
    key="insight_1",
)

st.divider()

# ============================================================
# 구역 2. 장르 안에 영화가 들어있는 트리맵
# ============================================================
st.header("② 장르별 영화 트리맵 (총 관객 기준)")
st.markdown(
    "큰 칸이 장르, 그 안의 작은 칸이 영화 한 편입니다. "
    "칸의 크기는 그 영화의 총 관객(total_audi) 수에 비례합니다."
)

fig2 = px.treemap(
    df,
    path=["대표장르", "movieNm"],
    values="total_audi",
    title="장르별 영화 트리맵 (칸 크기 = 총 관객)",
)
fig2.update_traces(
    hovertemplate="%{label}<br>총 관객: %{value:,}명<extra></extra>"
)

st.plotly_chart(fig2, width="stretch", key="chart_2")

st.text_input(
    "📝 이 그래프로 알 수 있는 것",
    placeholder="예: 애니메이션 장르 안에서도 한두 편이 총 관객을 대부분 차지한다.",
    key="insight_2",
)

st.divider()

# ============================================================
# 구역 3. 총 관객 히스토그램
# ============================================================
st.header("③ 총 관객 히스토그램")
st.markdown("영화들의 총 관객(total_audi)이 어떤 구간에 많이 몰려 있는지 보여줍니다.")

fig3 = px.histogram(
    df,
    x="total_audi",
    nbins=30,
    title="총 관객 분포",
)
fig3.update_traces(
    marker_color="#457b9d",
    hovertemplate="총 관객 구간: %{x}<br>영화 편수: %{y}편<extra></extra>",
)
fig3.update_layout(
    xaxis_title="총 관객(명)",
    yaxis_title="영화 편수",
    bargap=0.05,
)

st.plotly_chart(fig3, width="stretch", key="chart_3")

# 대부분의 영화가 몰려 있는 구간과, 가장 관객이 많은 영화를 자동으로 계산해서
# 그래프 아래에 문구로 보여줍니다.
bin_edges = pd.cut(df["total_audi"], bins=30)
most_common_bin = bin_edges.value_counts().idxmax()
top_movie_row = df.loc[df["total_audi"].idxmax()]

# pd.cut은 최솟값을 포함시키려고 맨 첫 구간의 왼쪽 경계를 실제보다
# 살짝(전체 범위의 0.1%) 더 낮게 잡습니다. 관객수는 음수가 될 수 없으므로
# 화면에 보여줄 때는 0보다 작으면 0으로 맞춰줍니다.
bin_left = max(0, int(most_common_bin.left))
bin_right = int(most_common_bin.right)

st.info(
    f"📊 가장 많은 영화가 몰려 있는 구간은 **{bin_left:,}명 ~ "
    f"{bin_right:,}명** 사이입니다. "
    f"가장 총 관객이 많은 영화는 **'{top_movie_row['movieNm']}'**"
    f"(총 {int(top_movie_row['total_audi']):,}명)입니다."
)

st.text_input(
    "📝 이 그래프로 알 수 있는 것",
    placeholder="예: 대부분의 영화는 관객 수가 적은 편이고, 소수의 영화만 크게 흥행한다.",
    key="insight_3",
)

st.divider()

# ============================================================
# 구역 4. 개봉일 스크린수와 총 관객의 관계
# ============================================================
st.header("④ 개봉일 스크린수와 총 관객의 관계")
st.markdown(
    "점 하나가 영화 한 편입니다. 개봉일에 스크린을 많이 잡을수록 "
    "총 관객도 많은지 살펴보세요. 색은 대표 장르를 나타냅니다."
)

fig4 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="대표장르",
    hover_name="movieNm",
    title="개봉일 스크린수 vs 총 관객",
)
fig4.update_traces(
    hovertemplate="영화명: %{hovertext}<br>개봉일 스크린수: %{x:,}관<br>총 관객: %{y:,}명<extra></extra>"
)
fig4.update_layout(
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객(명)",
    legend_title_text="대표 장르",
)

st.plotly_chart(fig4, width="stretch", key="chart_4")

st.text_input(
    "📝 이 그래프로 알 수 있는 것",
    placeholder="예: 개봉일 스크린수가 많을수록 대체로 총 관객도 많은 경향이 있다.",
    key="insight_4",
)

st.divider()

# ============================================================
# 구역 5. 장르별 총 관객 박스플롯 (영화 10편 이상 장르만)
# ============================================================
st.header("⑤ 장르별 총 관객 박스플롯 (10편 이상인 장르만)")
st.markdown(
    "영화가 10편 이상 있는 장르만 뽑아서, 장르별 총 관객의 분포를 상자 그림으로 보여줍니다. "
    "상자 밖으로 튀어나온 점(이상치)에 마우스를 올리면 영화명이 보여요."
)

genre_counts_all = df["대표장르"].value_counts()
genres_10plus = genre_counts_all[genre_counts_all >= 10].index
box_df = df[df["대표장르"].isin(genres_10plus)]

fig5 = px.box(
    box_df,
    x="대표장르",
    y="total_audi",
    hover_name="movieNm",
    points="outliers",
    title="장르별 총 관객 박스플롯 (10편 이상 장르만)",
)
fig5.update_traces(
    hovertemplate="영화명: %{hovertext}<br>총 관객: %{y:,}명<extra></extra>"
)
fig5.update_layout(
    xaxis_title="대표 장르",
    yaxis_title="총 관객(명)",
)

st.plotly_chart(fig5, width="stretch", key="chart_5")

st.text_input(
    "📝 이 그래프로 알 수 있는 것",
    placeholder="예: 애니메이션 장르는 총 관객의 편차가 크고, 일부 영화가 크게 튄다.",
    key="insight_5",
)

st.divider()

# ============================================================
# 구역 6. 개봉일 스크린수와 총 관객의 관계 (버블 그래프)
# ============================================================
st.header("⑥ 개봉일 스크린수와 총 관객의 관계 (버블 그래프)")
st.markdown(
    "④번 산점도와 같은 x축·y축·색이지만, 이번에는 점 크기로 "
    "개봉 첫 주 관객(first_week_audi)까지 함께 보여줍니다. "
    "점이 클수록 첫 주에 많은 관객이 들었다는 뜻이에요."
)

fig6 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="대표장르",
    hover_name="movieNm",
    size_max=45,
    title="개봉일 스크린수 vs 총 관객 (점 크기 = 첫 주 관객)",
)
fig6.update_traces(
    hovertemplate=(
        "영화명: %{hovertext}<br>"
        "개봉일 스크린수: %{x:,}관<br>"
        "총 관객: %{y:,}명<br>"
        "첫 주 관객: %{marker.size:,}명"
        "<extra></extra>"
    )
)
fig6.update_layout(
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객(명)",
    legend_title_text="대표 장르",
)

st.plotly_chart(fig6, width="stretch", key="chart_6")

st.text_input(
    "📝 이 그래프로 알 수 있는 것",
    placeholder="예: 첫 주 관객이 많았던 영화는 대체로 총 관객도 많다.",
    key="insight_6",
)

st.divider()

# ============================================================
# 구역 7. 제작 국가 → 장르 선버스트
# ============================================================
st.header("⑦ 제작 국가 → 장르 선버스트")
st.markdown(
    "안쪽 고리가 제작 국가(nation), 바깥쪽 고리가 그 국가에서 만든 영화의 대표 장르입니다. "
    "칸의 크기는 영화 편수에 비례합니다."
)

sun_df = df.copy()
sun_df["건수"] = 1

fig7 = px.sunburst(
    sun_df,
    path=["nation", "대표장르"],
    values="건수",
    title="제작 국가 → 장르 선버스트 (칸 크기 = 영화 편수)",
)
fig7.update_traces(
    hovertemplate="%{label}<br>편수: %{value}편<extra></extra>"
)

st.plotly_chart(fig7, width="stretch", key="chart_7")

st.text_input(
    "📝 이 그래프로 알 수 있는 것",
    placeholder="예: 한국 영화는 드라마 비중이 크고, 미국 영화는 장르가 다양하게 퍼져 있다.",
    key="insight_7",
)

st.divider()

# ============================================================
# 구역 8. 10위권에 들어간 대작들과 개봉 첫 주 관객 또한 많았는가
# ============================================================
st.header("⑧ 10위권에 들어간 대작들과 개봉 첫 주 관객 또한 많았는가")
st.markdown(
    "가로축은 10위권에 머문 날수(days_in_top10), 세로축은 개봉 첫 주 관객(first_week_audi)입니다. "
    "오래 버틴 영화가 처음부터 관객이 많았는지 살펴보세요."
)

fig8 = px.scatter(
    df,
    x="days_in_top10",
    y="first_week_audi",
    hover_name="movieNm",
    title="10위권에 들어간 대작들과 개봉 첫 주 관객 또한 많았는가",
)
fig8.update_traces(
    marker_color="#457b9d",
    hovertemplate="영화명: %{hovertext}<br>10위권 체류일수: %{x}일<br>첫 주 관객: %{y:,}명<extra></extra>",
)
fig8.update_layout(
    xaxis_title="10위권 체류일수(일)",
    yaxis_title="개봉 첫 주 관객(명)",
)

st.plotly_chart(fig8, width="stretch", key="chart_8")

st.text_input(
    "📝 이 그래프로 알 수 있는 것",
    placeholder="예: 10위권에 오래 머문 영화라고 해서 꼭 첫 주 관객이 많았던 것은 아니다.",
    key="insight_8",
)

st.divider()

# ============================================================
# 구역 9. (다음 그래프를 추가할 자리)
# ------------------------------------------------------------
# 새로운 그래프를 추가하려면 아래 패턴을 그대로 따라 하면 됩니다.
#
# st.header("⑨ 그래프 제목")
# st.markdown("그래프에 대한 간단한 설명")
# ... (데이터 가공 + plotly 그래프 그리기) ...
# st.plotly_chart(fig9, width="stretch", key="chart_9")
# st.text_input("📝 이 그래프로 알 수 있는 것", key="insight_9")
# st.divider()
# ============================================================
