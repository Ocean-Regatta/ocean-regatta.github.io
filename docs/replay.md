# 3D Playback & Analysis (`gz sim --playback`) 🎥

A core feature of **Ocean Regatta** is the ability to replay and scrutinize any evaluated run in full 3D inside **Gazebo Jetty**, exactly as if standing on the shoreline.

---

## 📥 1. Downloading Your Replay

1. Open your Pull Request on GitHub.
2. Navigate to the **Actions** tab (or click the artifact link in the referee comment).
3. Download the `gz-replay-pr-<num>.zip` archive.
4. Unpack the archive on your local workstation:
   ```bash
   unzip gz-replay-pr-42.zip -d ./my_replay
   ```

---

## 🕹️ 2. Starting Playback in Gazebo

Run in your terminal:

```bash
gz sim --playback ./my_replay/replay
```

Gazebo starts in read-only playback mode. Every physical entity (boat, waves, buoys, capsules) is reproduced with micro-step precision.

---

## 🎛️ 3. Interactive Playback Controls

| Action | Shortcut / Control | Description |
| :--- | :--- | :--- |
| **Play / Pause** | Spacebar | Pause or resume playback. |
| **Playback Speed** | Bottom timeline slider | Speed up to $4\times$ or slow down to $0.25\times$ for detailed maneuver inspection. |
| **Time Seek** | Timeline cursor | Scrub immediately to any moment of the race. |
| **Follow Drone** | Right-click BlueBoat $\rightarrow$ *Follow* | Camera locks onto and tracks the moving catamaran. |
| **Orbit Camera** | Left-click + drag | Rotate the 3D perspective around any scene point. |

---

## 🔍 4. Key Visual Indicators

### A. Dynamic Capsule Waypoint Accuracy
Each capsule starts as **vibrant Red**:
* If your boat center passes within $< 50 \text{ cm}$, the capsule snaps to **pure Green** (100% points).
* Between 50 cm and 1 m, watch the **smooth dynamic color fade (Red $\rightarrow$ Green)** reflecting your exact score ratio!

### B. Mooring Drift & Wavelet Animation
Notice how buoys drift with the ocean current and sway continuously with surface wavelets. This visually illustrates why open-loop dead reckoning fails and closed-loop perception is essential.

### C. Pier Wall Standoff & Sonar Lock
Verify your vessel's alignment when passing through the pier entry gate ($X = 55 \text{ m}$) and confirm that the Ping2 beam maintains an uninterrupted orthogonal lock onto the wall.
