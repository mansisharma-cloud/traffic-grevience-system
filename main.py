import cv2
from vehicle_counter import count_vehicles, get_density
from rl_model import TrafficRL

# create RL model
rl = TrafficRL()

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Step 1: get traffic data
    count = count_vehicles(frame)
    density = get_density(count)

    # Step 2: RL decision
    state = count
    action = rl.get_action(state)
    signal_time = action

    # Step 3: reward (less traffic is better)
    reward = -count
    next_state = count

    # Step 4: update learning
    rl.update(state, action, reward, next_state)

    # Step 5: display results
    cv2.putText(frame, f"Vehicles: {count}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.putText(frame, f"Density: {density}", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.putText(frame, f"AI Signal: {signal_time} sec", (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("AI Traffic System", frame)

    # press 'q' to stop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()