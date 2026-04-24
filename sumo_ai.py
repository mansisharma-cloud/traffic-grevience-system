import traci
from rl_model import TrafficRL
import matplotlib.pyplot as plt
import time

# SUMO command (GUI mode)
sumo_cmd = ["sumo-gui", "-c", "sumo_files/simple.sumocfg", "--start", "--quit-on-end"]

# start SUMO
traci.start(sumo_cmd)
traci.gui.setZoom("View #0", 500)
traci.gui.setOffset("View #0", 50, 50)
# 🔥 FORCE VIEW FIX
traci.gui.setSchema("View #0", "real world")
traci.gui.setZoom("View #0", 1000)
traci.gui.setOffset("View #0", 0, 0)

# AI model
rl = TrafficRL()

# data for graph
vehicle_data = []
signal_data = []

step = 0
max_steps = 200   # increased for better graph

while step < max_steps:
    traci.simulationStep()

    # get vehicle count
    vehicle_count = traci.vehicle.getIDCount()

    # store data
    vehicle_data.append(vehicle_count)

    # AI decision
    state = vehicle_count
    signal_time = rl.get_action(state)
    signal_data.append(signal_time)

    reward = -vehicle_count
    next_state = vehicle_count

    rl.update(state, signal_time, reward, next_state)

    # get traffic light id
    tls_id = traci.trafficlight.getIDList()[0]

    # AI decision
    if vehicle_count < 3:
        phase = 0   # green
    elif vehicle_count < 6:
        phase = 1   # yellow
    else:
        phase = 2   # red

    # apply to SUMO
    traci.trafficlight.setPhase(tls_id, phase)

    print(f"Step: {step} | Vehicles: {vehicle_count} | Signal: {phase}")
    step += 1

    # small delay (for visibility)
    time.sleep(0.05)

# close SUMO
traci.close()

# 📊 PLOT 1: Vehicle count
plt.figure()
plt.plot(vehicle_data)
plt.title("Vehicle Count Over Time")
plt.xlabel("Time Step")
plt.ylabel("Vehicles")
plt.grid()

# 📊 PLOT 2: Signal timing
plt.figure()
plt.plot(signal_data)
plt.title("Signal Timing Over Time")
plt.xlabel("Time Step")
plt.ylabel("Signal Time")
plt.grid()

plt.show()