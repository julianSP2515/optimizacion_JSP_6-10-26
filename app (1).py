import streamlit as st
import numpy as np
from scipy.optimize import linprog

st.set_page_config(page_title="LP & IP Optimizer", layout="centered")

st.title("🧮 Interactive Linear & Integer Programming Solver")
st.write("Customize the parameters below to solve the maximization problem in real-time.")

st.sidebar.header("1. Optimization Goal")
problem_type = st.sidebar.selectbox("Variable Type", ["Binary (0-1)", "General Integer (>=0)", "Continuous (>=0)"])

# Dynamic default bounds & integrality based on selection
if problem_type == "Binary (0-1)":
    default_bounds = (0.0, 1.0)
    integrality_flag = 1
elif problem_type == "General Integer (>=0)":
    default_bounds = (0.0, None)
    integrality_flag = 1
else:
    default_bounds = (0.0, None)
    integrality_flag = 0

st.header("Objective Function")
st.write("Maximize: $c_1 x_1 + c_2 x_2 + c_3 x_3 + c_4 x_4$")
col1, col2, col3, col4 = st.columns(4)
with col1:
    c1 = st.number_input("c1 (x1 coeff)", value=14.0)
with col2:
    c2 = st.number_input("c2 (x2 coeff)", value=5.0)
with col3:
    c3 = st.number_input("c3 (x3 coeff)", value=7.0)
with col4:
    c4 = st.number_input("c4 (x4 coeff)", value=3.0)

st.header("Constraints")
st.write("Subject to: $w_1 x_1 + w_2 x_2 + w_3 x_3 + w_4 x_4 \\le B$")
col5, col6, col7, col8 = st.columns(4)
with col5:
    w1 = st.number_input("w1 (x1 weight)", value=8.0)
with col6:
    w2 = st.number_input("w2 (x2 weight)", value=3.0)
with col7:
    w3 = st.number_input("w3 (x3 weight)", value=4.0)
with col8:
    w4 = st.number_input("w4 (x4 weight)", value=2.0)

B = st.number_input("Constraint Limit (B)", value=9.0)

# Prepare linprog input parameters
c = [-c1, -c2, -c3, -c4]  # Negative for maximization
A = [[w1, w2, w3, w4]]
b = [B]
bounds = [default_bounds] * 4
integrality = [integrality_flag] * 4

if st.button("⚡ Run Optimization", type="primary"):
    res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, integrality=integrality, method='highs')
    
    if res.success:
        st.success("Optimization terminated successfully!")
        
        st.header("Results")
        col_r1, col_r2, col_r3, col_r4 = st.columns(4)
        with col_r1:
            st.metric("x1", value=round(res.x[0], 4))
        with col_r2:
            st.metric("x2", value=round(res.x[1], 4))
        with col_r3:
            st.metric("x3", value=round(res.x[2], 4))
        with col_r4:
            st.metric("x4", value=round(res.x[3], 4))
            
        st.subheader(f"Maximized Objective Value: **{round(-res.fun, 4)}**")
        
        # Verification
        slack_used = w1*res.x[0] + w2*res.x[1] + w3*res.x[2] + w4*res.x[3]
        st.info(f"Total Capacity Used: {round(slack_used, 4)} out of {B}")
    else:
        st.error(f"Optimization failed: {res.message}")
