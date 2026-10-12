from __future__ import annotations

from pathlib import Path
import calendar
from io import BytesIO

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Hotel Booking Dashboard",
    page_icon="🏨",
    layout="wide",
)


@st.cache_data
def load_data(file_bytes: bytes | None, file_path: str) -> pd.DataFrame:
    if file_bytes is not None:
        df = pd.read_csv(BytesIO(file_bytes))
    else:
        df = pd.read_csv(file_path)

    df.columns = df.columns.str.strip().str.lower()

    required_columns = {
        "hotel",
        "is_canceled",
        "arrival_date_year",
        "arrival_date_month",
        "stays_in_weekend_nights",
        "stays_in_week_nights",
    }
    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError("CSV 缺少必要字段：" + ", ".join(sorted(missing)))

    df["is_canceled"] = pd.to_numeric(df["is_canceled"], errors="coerce")
    df["arrival_date_year"] = pd.to_numeric(
        df["arrival_date_year"], errors="coerce"
    )

    month_numbers = {
        calendar.month_name[i]: i for i in range(1, 13)
    }
    month_numbers.update({
        calendar.month_abbr[i]: i for i in range(1, 13)
    })

    df["arrival_month_num"] = df["arrival_date_month"].map(month_numbers)
    df["arrival_month"] = pd.to_datetime(
        {
            "year": df["arrival_date_year"],
            "month": df["arrival_month_num"],
            "day": 1,
        },
        errors="coerce",
    )

    for column in [
        "stays_in_weekend_nights",
        "stays_in_week_nights",
    ]:
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)

    df["room_nights"] = (
        df["stays_in_weekend_nights"]
        + df["stays_in_week_nights"]
    )

    return df


st.title("🏨 酒店预订与取消概览｜团队名称请替换")
st.caption(
    "面向酒店收益经理：查看不同酒店和入住月份的取消情况，"
    "辅助复核预订渠道与政策。"
)

data_path = Path(__file__).resolve().parent / "hotel_bookings.csv"
uploaded_file = None

if not data_path.exists():
    st.info("请将 hotel_bookings.csv 放在 app.py 同一文件夹，或在下方上传。")
    uploaded_file = st.file_uploader(
        "上传 hotel_bookings.csv",
        type=["csv"],
    )

    if uploaded_file is None:
        st.stop()

try:
    file_bytes = uploaded_file.getvalue() if uploaded_file else None
    df = load_data(file_bytes, str(data_path))
except Exception as error:
    st.error(f"无法读取数据：{error}")
    st.stop()


valid_dates = df["arrival_month"].dropna()

if valid_dates.empty:
    st.error("无法根据入住年份和月份生成日期。")
    st.stop()

start_period = valid_dates.min().strftime("%b %Y")
end_period = valid_dates.max().strftime("%b %Y")


with st.sidebar:
    st.header("筛选")

    hotel_options = [
        "全部酒店",
        *sorted(df["hotel"].dropna().unique().tolist()),
    ]
    selected_hotel = st.selectbox("酒店类型", hotel_options)

    years = sorted(
        df["arrival_date_year"].dropna().astype(int).unique().tolist()
    )
    selected_years = st.multiselect(
        "入住年份",
        years,
        default=years,
    )


filtered = df.copy()

if selected_hotel != "全部酒店":
    filtered = filtered[filtered["hotel"] == selected_hotel]

if selected_years:
    filtered = filtered[
        filtered["arrival_date_year"].isin(selected_years)
    ]
else:
    filtered = filtered.iloc[0:0]


total_bookings = len(filtered)

if total_bookings:
    cancellation_rate = filtered["is_canceled"].mean()
else:
    cancellation_rate = 0

confirmed_bookings = filtered[filtered["is_canceled"] == 0]
confirmed_room_nights = int(confirmed_bookings["room_nights"].sum())


col1, col2, col3 = st.columns(3)

col1.metric("预订记录", f"{total_bookings:,}")
col2.metric("取消率", f"{cancellation_rate:.1%}")
col3.metric("未取消预订间夜数", f"{confirmed_room_nights:,}")


st.subheader("取消率随入住月份的变化")

monthly = (
    filtered.dropna(subset=["arrival_month"])
    .groupby("arrival_month")
    .agg(
        取消率=("is_canceled", "mean"),
        预订数=("is_canceled", "size"),
    )
    .sort_index()
)

if monthly.empty:
    st.warning("当前筛选条件下没有可绘制的月份数据。")
else:
    st.line_chart(
        monthly["取消率"],
        y_label="取消率",
        x_label="入住月份",
    )


if "market_segment" in filtered.columns:
    st.subheader("不同预订市场的取消情况")

    segment = (
        filtered.dropna(subset=["market_segment"])
        .groupby("market_segment")
        .agg(
            取消率=("is_canceled", "mean"),
            预订数=("is_canceled", "size"),
        )
        .sort_values("取消率", ascending=False)
    )

    if not segment.empty:
        st.bar_chart(
            segment["取消率"],
            y_label="取消率",
            x_label="预订市场",
        )


st.caption(
    f"数据期间：{start_period} – {end_period}（Kaggle 历史快照）。"
    "生产环境建议每日刷新；收益经理每周查看，旺季或取消率异常时复查。"
)

st.caption(
    "口径说明：取消率按预订记录计算；未取消预订间夜数不等于入住率或实际收入。"
    "房型代码经过匿名处理，不代表可识别的具体房型。"
)