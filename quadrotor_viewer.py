import mujoco
import mujoco.viewer
import time
import glfw

XML_PATH = "x2.xml"

model = mujoco.MjModel.from_xml_path(XML_PATH)
data = mujoco.MjData(model)

# Hover condition from instructor XML
hover_thrust = 3.2495625

# Start at hover position
data.qpos[:] = [0, 0, 0.3, 1, 0, 0, 0]

# Start all four motors at hover thrust
data.ctrl[:] = hover_thrust

# Amount of thrust difference for movement
delta = 0.3


def keyboard_callback(key):

    # Forward / backward
    if key == glfw.KEY_W:
        data.ctrl[0] = hover_thrust + delta
        data.ctrl[1] = hover_thrust + delta
        data.ctrl[2] = hover_thrust - delta
        data.ctrl[3] = hover_thrust - delta

    elif key == glfw.KEY_S:
        data.ctrl[0] = hover_thrust - delta
        data.ctrl[1] = hover_thrust - delta
        data.ctrl[2] = hover_thrust + delta
        data.ctrl[3] = hover_thrust + delta

    # Left / right
    elif key == glfw.KEY_A:
        data.ctrl[0] = hover_thrust - delta
        data.ctrl[1] = hover_thrust + delta
        data.ctrl[2] = hover_thrust + delta
        data.ctrl[3] = hover_thrust - delta

    elif key == glfw.KEY_D:
        data.ctrl[0] = hover_thrust + delta
        data.ctrl[1] = hover_thrust - delta
        data.ctrl[2] = hover_thrust - delta
        data.ctrl[3] = hover_thrust + delta

    # Increase / decrease altitude
    elif key == glfw.KEY_UP:
        data.ctrl[:] = hover_thrust + delta

    elif key == glfw.KEY_DOWN:
        data.ctrl[:] = hover_thrust - delta

    # Reset to hover
    elif key == glfw.KEY_SPACE:
        data.ctrl[:] = hover_thrust


with mujoco.viewer.launch_passive(
    model, data, key_callback=keyboard_callback
) as viewer:

    while viewer.is_running():

        mujoco.mj_step(model, data)

        viewer.sync()
        time.sleep(0.01)
