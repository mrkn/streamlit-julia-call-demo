import streamlit as st
from streamlit_julia_call import julia_eval, julia_display

with st.spinner("Initializing Julia runtime environment..."):
    julia_eval("using Colors, Images")
    julia_eval("using PlotUtils: cgrad")
    julia_eval("""
        function mandel(x, y, maxiter)
            count = 0
            c = complex(x, y)
            z = zero(c)
            for i in 1:maxiter
                count += 1
                z = z^2 + c
                if abs(z) >= 2
                    break
                end
            end
            return count
        end
    """)
    julia_eval("""
        default_palette = cgrad([
            :black,
            :blue,
            :lightblue,
            :white,
            :white,
            :orange,
            :orange,
            :black
        ])
    """)
    julia_eval("""
        function render_mandel(width, height;
                               xlim=(-2.0, 1.0), ylim=(-1.2, 1.2),
                               maxiter=100,
                               palette=default_palette)
            x0, y0 = xlim[1], ylim[1]
            α = (xlim[2] - x0) / width
            β = (ylim[2] - y0) / height

            ary = Array{Float64}(undef, (3, height, width))

            Threads.@threads for y in 1:height
                v = β*(height - y) + y0
                for x in 1:width
                    u = α*x + x0

                    count = mandel(u, v, maxiter)

                    color = palette[count/maxiter]
                    r, g, b = color.r, color.g, color.b
                    ary[:, y, x] .= (r, g, b)
                end
            end

            return colorview(RGB, ary)
        end
    """)

with st.spinner("Rendering Mandelbrot set.."):
    julia_display("render_mandel(1600, 1200)")
