import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="UFO Sighting Predictor", page_icon="🛸")

st.title("🛸 UFO Appearance Prediction")
st.write("根据目击持续时间和地理坐标，预测 UFO 在哪个国家被目击。")
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    seconds = st.number_input(
        "持续时间（秒）",
        min_value=1,
        max_value=60,
        value=10,
        help="UFO 目击持续秒数，范围 1~60 秒"
    )

with col2:
    latitude = st.number_input(
        "纬度 Latitude",
        min_value=-90.0,
        max_value=90.0,
        value=44.0,
        step=0.1,
        format="%.4f",
        help="目击地点的纬度，范围 -90 到 90"
    )

with col3:
    longitude = st.number_input(
        "经度 Longitude",
        min_value=-180.0,
        max_value=180.0,
        value=-100.0,
        step=0.1,
        format="%.4f",
        help="目击地点的经度，范围 -180 到 180"
    )

st.markdown("---")

if st.button("🔍 预测目击国家", use_container_width=True):
    with st.spinner("正在预测..."):
        try:
            response = requests.post(
                f"{BACKEND_URL}/predict",
                json={
                    "seconds": seconds,
                    "latitude": latitude,
                    "longitude": longitude,
                },
                timeout=5,
            )
            if response.status_code == 200:
                result = response.json()
                st.success(f"🌍 预测结果：**{result['country']}**")
            else:
                st.error(f"后端返回错误：{response.status_code}")
        except requests.exceptions.ConnectionError:
            st.error("❌ 无法连接到后端，请确认已运行：`uvicorn backend:app --reload`")
        except requests.exceptions.Timeout:
            st.error("❌ 请求超时，请检查后端服务是否正常运行")

st.markdown("---")
st.caption("数据来源：NUFORC（美国国家 UFO 报告中心），约 8 万条目击记录 | 模型：逻辑回归，精度约 96%")
