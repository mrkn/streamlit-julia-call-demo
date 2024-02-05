import streamlit as st
from streamlit_julia_call import julia_eval, julia_display

with st.spinner("Loading libraries..."):
    julia_eval("import CairoMakie as cm")
    julia_eval("using CSV, DataFrames")

with st.spinner("Rendering a figure by CairoMakie..."):
    julia_display("""
f = cm.Figure()
ax = cm.Axis(f[1, 1])
x = range(0, 10, length=100)
y = cos.(x)
cm.lines!(ax, x, y)
f
""")

with st.spinner("Loading housing.csv..."):
    julia_display("""CSV.read("housing.csv", DataFrame)""")
