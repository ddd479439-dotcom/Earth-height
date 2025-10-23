import streamlit as st
import plotly.graph_objects as go
import numpy as np

# ---------------------------
# 표준 대기 모델 계산 함수
# ---------------------------
def atmosphere_properties(alt_km):
    alt = alt_km * 1000
    if alt < 11000:
        T = 288.15 - 0.0065 * alt
        P = 101325 * (T / 288.15) ** (-9.80665 / (-0.0065 * 287.05))
        region = "대류권 (Troposphere)"
    elif alt < 20000:
        T = 216.65
        P = 22632 * np.exp(-9.80665 * (alt - 11000) / (287.05 * T))
        region = "성층권 하부 (Stratosphere)"
    elif alt < 32000:
        T = 196.65 + 0.001 * (alt - 20000)
        P = 5474.9 * (T / 216.65) ** (-9.80665 / (0.001 * 287.05))
        region = "성층권 중부 (Stratosphere)"
    elif alt < 47000:
        T = 228.65 + 0.0028 * (alt - 32000)
        P = 868.02 * (T / 228.65) ** (-9.80665 / (0.0028 * 287.05))
        region = "성층권 상부 (Stratosphere)"
    elif alt < 51000:
        T = 270.65
        P = 110.91 * np.exp(-9.80665 * (alt - 47000) / (287.05 * T))
        region = "중간권 하부 (Mesosphere)"
    elif alt < 71000:
        T = 270.65 - 0.0028 * (alt - 51000)
        P = 66.94 * (T / 270.65) ** (-9.80665 / (-0.0028 * 287.05))
        region = "중간권 상부 (Mesosphere)"
    else:
        T = 214.65
        P = 3.96 * np.exp(-9.80665 * (alt - 71000) / (287.05 * T))
        region = "열권 (Thermosphere)"
    rho = P / (287.05 * T)
    return T, P / 1000, rho, region

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="지구 대기 고도 시각화", layout="wide")

st.title("🌍 지구 대기 고도 시각화")
st.write("입력한 고도에서의 온도, 압력, 밀도, 대기권 단계를 보여주는 프로그램입니다.")

alt_input = st.slider("고도 입력 (km)", 0.0, 100.0, 1.0, step=0.5)
T, P, rho, region = atmosphere_properties(alt_input)

# ---------------------------
# 3D 지구 모델
# ---------------------------
R_earth = 6371
theta, phi = np.mgrid[0:np.pi:100j, 0:2*np.pi:100j]
x = R_earth * np.sin(theta) * np.cos(phi)
y = R_earth * np.sin(theta) * np.sin(phi)
z = R_earth * np.cos(theta)

# 고도 위치 점
x_p = 0
y_p = 0
z_p = R_earth + alt_input

fig = go.Figure()
fig.add_trace(go.Surface(
    x=x, y=y, z=z,
    colorscale="Blues", opacity=0.9, showscale=False
))
fig.add_trace(go.Scatter3d(
    x=[x_p], y=[y_p], z=[z_p],
    mode="markers+text",
    marker=dict(size=6, color="red"),
    text=[f"{alt_input:.1f} km"],
    textposition="top center"
))
fig.update_layout(
    scene=dict(
        xaxis_title="X (km)",
        yaxis_title="Y (km)",
        zaxis_title="Z (km)",
        aspectmode="data",
        camera=dict(eye=dict(x=1.5, y=1.5, z=1))
    ),
    margin=dict(l=0, r=0, t=0, b=0)
)

# ---------------------------
# 출력 정보
# ---------------------------
st.plotly_chart(fig, use_container_width=True)
st.markdown(f"""
### 🛰️ 고도 {alt_input:.1f} km 정보
- 구간: **{region}**  
- 온도: **{T:.1f} K**  
- 압력: **{P:.2f} kPa**  
- 밀도: **{rho:.4f} kg/m³**
""")
