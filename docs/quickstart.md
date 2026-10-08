# Student Quick Start Guide 🚀

This step-by-step guide walks you from cloning your team repository to your first officially ranked run on the Live Scoreboard.

---

## 📋 Prerequisites

Choose between two development workflows:

=== "Option 1: Docker (Recommended)"
    * **Operating System:** Linux (Ubuntu/Debian), macOS, or Windows 10/11 with WSL2.
    * **Requirements:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) or standard Docker engine.
    * **Benefit:** No robotics toolchain, ROS, or C++ dependencies needed on your host machine!

=== "Option 2: Native Setup"
    * **Operating System:** Ubuntu 24.04 LTS (Noble).
    * **Requirements:** Gazebo Jetty (`gz-sim9`), Python 3.10+, `python3-gz-transport14`, `python3-gz-msgs11`.

---

## Step 0: Register Your Account

Before cloning your repository and submitting code, your team must be approved in the competition participant registry:

1. Navigate to the [Competitor Registration](register.md) portal (`/register/`).
2. Fill out your GitHub username and team details to generate your registration issue on [Ocean-Regatta/ocean-regatta-2026-template](https://github.com/Ocean-Regatta/ocean-regatta-2026-template).
3. The regatta committee (**@Teusner**) will review and approve your submission into `participants.json` within 24 hours.

!!! warning "Verification Required for Automated PR Grading"
    Simulation server resources and automated PR evaluation workflows run **only** for registered accounts listed in `participants.json`. If you open a Pull Request without prior registration, grading will not trigger! Additionally, evaluated runs adhere to a **60-minute cooldown** between submissions to prevent seed overfitting.

---

## 1. Create Your Team Repository

1. Navigate to the official template repository: [github.com/ocean-regatta/ocean-regatta-2026-template](https://github.com/ocean-regatta/ocean-regatta-2026-template).
2. Click the green button **"Use this template"** $\rightarrow$ **"Create a new repository"**.
3. Name your repository (e.g., `ocean-regatta-2026-team-nautilus`) and set visibility to **Public**.
4. Clone the repository to your development machine:
   ```bash
   git clone https://github.com/your-username/ocean-regatta-2026-team-nautilus.git
   cd ocean-regatta-2026-team-nautilus
   ```

---

## 2. Repository Layout

```
starter_kit/
├── student_controller.py    # ✏️ ONLY FILE EVALUATED ON SERVER
├── blueboat_driver.py       # Hardware Abstraction Layer (HAL) for sensors/actuators
├── run_docker.sh            # One-click Docker runner
├── run_local.sh             # Native Gazebo launch script
└── Dockerfile.local         # Development Docker container definition
```

!!! warning "Golden Rule of Automated Evaluation"
    During automated CI evaluation on the server, **only your `starter_kit/student_controller.py` file is extracted and tested**. The evaluator injects its own official, immutable `blueboat_driver.py` and procedural world with randomized environmental seeds.

---

## 3. Running Local Simulations

### Using Docker
On Linux (allow X11 GUI forwarding if you wish to see the 3D window):
```bash
xhost +local:root
./starter_kit/run_docker.sh
```

The script builds the local Docker image, boots Gazebo Jetty in the background with `worlds/practice_world.sdf`, and executes your `student_controller.py`.

### Using Native Gazebo
In two separate terminals:
```bash
# Terminal 1: Launch Gazebo Jetty simulation
gz sim -v 3 -r worlds/practice_world.sdf

# Terminal 2: Run your Python controller
python3 starter_kit/student_controller.py
```

---

## 4. Developing Your Autonomous Controller

Open `starter_kit/student_controller.py` in your favorite IDE (VS Code, Cursor, PyCharm).

Your controller receives a normalized sensor snapshot (`Observation`) at a constant $10 \text{ Hz}$:

```python
def step(self, obs: Observation):
    # 1. Process buoys detected in forward camera FOV
    red_buoys = [b for b in obs.buoys if b.color == "RED"]
    green_buoys = [b for b in obs.buoys if b.color == "GREEN"]

    # 2. Query portside acoustic sounder for pier distance
    if obs.ping2.is_valid:
        current_pier_distance = obs.ping2.distance

    # 3. Compute differential thrust commands
    left_thrust = 25.0
    right_thrust = 25.0

    # 4. Send motor commands (strictly clamped [-50N, +50N])
    self.driver.set_thrust(left_thrust, right_thrust)
```

Refer to the [Hardware Driver & Sensors Guide](driver_api.md) for full sensor specifications.

---

## 5. Submitting Your Code & Getting Ranked

1. Create a dedicated feature branch:
   ```bash
   git checkout -b feature/improved-wall-following
   ```
2. Commit and push your modifications:
   ```bash
   git add starter_kit/student_controller.py
   git commit -m "feat: implement PD controller for Ping2 sonar wall following"
   git push origin feature/improved-wall-following
   ```
3. Open a **Pull Request** targeting `master` on GitHub.
4. The automated GitHub Actions referee immediately boots:
   * Executes headless Gazebo evaluation under randomized currents and thruster wear.
   * Posts an evaluation summary directly as a PR comment.
   * Submits your score to the **Live Scoreboard** and awards unlocked badges!
