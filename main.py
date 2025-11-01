import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


def polar_to_cartesian(angle_degrees, radius):
    """
    Convert polar coordinates to Cartesian coordinates.

    Parameters:
        angle_degrees (float): The angle in degrees.
        radius (float): The radius.

    Returns:
        tuple: (x, y) coordinates
    """
    x = radius * np.sin(np.radians(angle_degrees))
    y = radius * np.cos(np.radians(angle_degrees))
    return x, y


def draw_point_cloud(ax, n_point_lines, code, color):
    # Generate points based on the raster pattern (clockwise, starting at 0 degrees)
    points = []
    max_radius = max([int(x) for x in code])
    for r in range(1, max_radius+1):  # Distance from center (based on code numbers)
        angles = np.linspace(0, 360, n_point_lines, endpoint=False)  # Divide circle into equal parts, clockwise
        for angle in angles:
            x_coord, y_coord = polar_to_cartesian(angle, r)
            points.append((x_coord, y_coord, r, angle))  # Include the radius and angle for matching

    # Draw all points in the raster
    for x_coord, y_coord, r, angle in points:
        ax.plot(x_coord, y_coord, 'o', color=color, markersize=5)
    
    return angles


def draw_art(n_angles, codes, colors):
    # Validate inputs
    if not codes or not all(
        code is None or
        code == "" or
        code.isdigit()
        # and len(set(c)) == len(c)
        and all(int(d) >= 1 for d in code) for code in codes
    ):
        st.error("Invalid codes or input.")
        return

    # Plot the graph
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')
    ax.axis('off')

    # Draw the center point
    ax.plot(0, 0, 'ro', label="Center")

    # Draw the lines based on codes
    for i_code, code in enumerate(codes):
        color = colors[i_code]
        n_angle = n_angles[i_code]

        if code is None or code == "":  # Empty string occurs due to queary params
            draw_point_cloud(ax, n_angle, [4], color)
            continue

        code = [int(c) for c in code]
        angles = draw_point_cloud(ax, n_angle, code, color)

        visited = set()  # Track visited (current_radius, current_angle) to detect repetition
        
        i = 0
        while True and i < 1000:
            current_radius = code[i % len(code)]
            next_radius = code[(i+1) % len(code)]

            current_angle = angles[i % len(angles)]
            next_angle = angles[(i+1) % len(angles)]
            
            current_point = polar_to_cartesian(current_angle, current_radius)
            next_point = polar_to_cartesian(next_angle, next_radius)

              # Stop drawing if a repetition is detected
            if (current_radius, current_angle, i % len(code)) in visited:
                break
            visited.add((current_radius, current_angle, i % len(code)))

            # Draw the line
            ax.plot([current_point[0], next_point[0]], [current_point[1], next_point[1]], color)

            i += 1

    st.pyplot(fig, width=400)


st.set_page_config(layout="wide")
col1, col2 = st.columns([4, 5])  # Allocate more space to col2 (graph)
if not st.query_params:
    st.query_params.from_dict({
        "ck1": "True", "ang1": "8", "code1": "52413", "cl1": "#FF0000",
        "ck2": "False", "ang2": "8", "code2": "", "cl2": "#00FF00",
        "ck3": "False", "ang3": "8", "code3": "", "cl3": "#0000FF"
    })

# Streamlit Dashboard
with col1:
    # First row
    row1 = st.columns(4)
    with row1[0]:
        checkbox1 = st.checkbox("Enable", label_visibility="hidden", value=st.query_params["ck1"]=="True", key="ck1")
    with row1[1]:
        n_angles1 = st.number_input("N Angles", min_value=2, value=int(st.query_params["ang1"]), step=1, key="ang1")
    with row1[2]:
        code1 = st.text_input("code", value=st.query_params["code1"], key="code1")
    with row1[3]:
        color1 = st.color_picker("Color", value=st.query_params["cl1"], key="cl1")

    # Second row
    row2 = st.columns(4)
    with row2[0]:
        checkbox2 = st.checkbox("Enable", label_visibility="hidden", value=st.query_params["ck2"]=="True", key="ck2")
    with row2[1]:
        n_angles2 = st.number_input("N Angles", min_value=2, value=int(st.query_params["ang2"]), step=1, key="ang2")
    with row2[2]:
        code2 = st.text_input("code", value=st.query_params["code2"], key="code2")
    with row2[3]:
        color2 = st.color_picker("Color", value=st.query_params["cl2"], key="cl2")

    # Third row
    row3 = st.columns(4)
    with row3[0]:
        checkbox3 = st.checkbox("Enable", label_visibility="hidden", value=st.query_params["ck3"]=="True", key="ck3")
    with row3[1]:
        n_angles3 = st.number_input("N Angles", min_value=2, value=int(st.query_params["ang3"]), step=1, key="ang3")
    with row3[2]:
        code3 = st.text_input("code", value=st.query_params["code3"], key="code3")
    with row3[3]:
        color3 = st.color_picker("Color", value=st.query_params["cl3"], key="cl3")

# Set parameters that are configured:
st.query_params.from_dict({
    "ck1": str(checkbox1), "ang1": str(n_angles1), "code1": code1, "cl1": color1,
    "ck2": str(checkbox2), "ang2": str(n_angles2), "code2": code2, "cl2": color2,
    "ck3": str(checkbox3), "ang3": str(n_angles3), "code3": code3, "cl3": color3
})

# Prepare the input data
codes = [code for chk, code in [(checkbox1, code1), (checkbox2, code2), (checkbox3, code3)] if chk]
colors = [color for chk, color in [(checkbox1, color1), (checkbox2, color2), (checkbox3, color3)] if chk]
n_angles = [angle for chk, angle in [(checkbox1, n_angles1), (checkbox2, n_angles2), (checkbox3, n_angles3)] if chk]

with col2:
    # st.title("Mathematical Art Dashboard")
    draw_art(n_angles, codes, colors)
