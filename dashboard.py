import streamlit as st
import pandas as pd
import cv2
import numpy as np

st.set_page_config(page_title="Traffic Dashboard", layout="wide")

st.title("🚦 AI Traffic Control Dashboard")

video_path = "traffic.mp4"
cap = cv2.VideoCapture(video_path)

if "data" not in st.session_state:
    st.session_state.data = []

frame_placeholder = st.empty()
stats_placeholder = st.empty()

run = st.button("▶ Start")

if run:
    for _ in range(300):
        ret, frame = cap.read()

        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        frame = cv2.resize(frame, (800, 500))

        frame = frame[0:380, :]

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower = np.array([0, 50, 50])
        upper = np.array([180, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)

        kernel = np.ones((5,5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        height, width, _ = frame.shape
        lane_width = width // 8

        lanes = [0]*8
        total = 0

        for cnt in contours:
            area = cv2.contourArea(cnt)

            if area < 200 or area > 5000:
                continue

            x, y, w, h = cv2.boundingRect(cnt)

            if w < 10 or h < 10:
                continue

            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

            cx = x + w//2
            lane_index = min(cx // lane_width, 7)

            lanes[lane_index] += 1
            total += 1

        for i in range(1,8):
            cv2.line(frame, (i*lane_width, 0), (i*lane_width, height), (255,0,0), 1)

        max_lane = max(lanes)

        signal_time = 5 + (max_lane * 3)

        if signal_time < 10:
            density = "LOW"
            color = "🟢"
        elif signal_time < 20:
            density = "MEDIUM"
            color = "🟡"
        else:
            density = "HIGH"
            color = "🔴"

        st.session_state.data.append(total)

        frame_placeholder.image(frame, channels="BGR")

        with stats_placeholder.container():
            st.subheader("📊 Live Traffic Status")

            cols = st.columns(4)
            for i in range(4):
                cols[i].metric(f"Lane {i+1}", lanes[i])

            cols2 = st.columns(4)
            for i in range(4):
                cols2[i].metric(f"Lane {i+5}", lanes[i+4])

            st.markdown("---")

            col1, col2 = st.columns(2)
            col1.metric("Total Vehicles", total)
            col2.metric("Signal Time (sec)", signal_time)

            st.markdown(f"## {color} {density} Traffic")

            st.markdown("---")

            df = pd.DataFrame(st.session_state.data, columns=["Vehicles"])
            st.line_chart(df)