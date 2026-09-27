# Hardware Driver & Sensor API 📡

The `blueboat_driver.py` module acts as the official Hardware Abstraction Layer (HAL). It manages Gazebo Transport communication, deserializes Protobuf packets, and applies strict physical motor clamping according to BlueBoat physical specifications.

---

## 📦 The `Observation` Dataclass

At every control cycle ($10 \text{ Hz}$), your `step(obs)` callback receives an immutable `Observation` snapshot:

```python
@dataclass
class Observation:
    imu: IMUData = field(default_factory=IMUData)
    gps: GPSData = field(default_factory=GPSData)
    ping2: Ping2Data = field(default_factory=Ping2Data)
    buoys: List[BuoyDetection] = field(default_factory=list)
    time: float = 0.0
```

---

## 👁️ 1. Forward Optical Camera (`obs.buoys`)

Simulates a front-facing computer vision perception system:

* **Field of View (FOV):** $\pm 55^\circ$ forward, maximum range $35.0 \text{ m}$.
* **No Artificial Cheating IDs:** The sensor does not provide labels like `"gate_1_port"`. Detected buoys are ordered strictly by increasing distance (`obs.buoys[0]` is the closest).
* **Natural FOV Exit:** When a gate is passed ($x_{\text{body}} < 0$), the buoys naturally exit the forward FOV behind the boat. The next gate ahead immediately becomes the closest target.

### Structure `BuoyDetection`

```python
@dataclass
class BuoyDetection:
    color: str      # "RED", "GREEN", "YELLOW_BLACK", or "UNKNOWN"
    shape: str      # "CYLINDER", "CONE", "CARDINAL", or "UNKNOWN"
    range: float    # Euclidean distance in meters (0.3m to 35.0m)
    bearing: float  # Angular bearing in radians relative to boat heading (-pi to +pi)
```

### Polar to Body-Frame Cartesian Conversion

To convert polar measurements ($r = \text{range}$, $\beta = \text{bearing}$) into the boat body frame ($x$ forward, $y$ portside / left):

$$x_{\text{body}} = r \cdot \cos(\beta)$$

$$y_{\text{body}} = r \cdot \sin(\beta)$$

```python
def polar_to_body(r: float, bearing: float) -> tuple[float, float]:
    return r * math.cos(bearing), r * math.sin(bearing)
```

---

## 🔊 2. Ping2 Portside Acoustic Sonar (`obs.ping2`)

The BlueBoat is equipped with a **Ping2** single-beam acoustic altimeter oriented strictly at $+90^\circ$ (lateral portside / left).

```python
@dataclass
class Ping2Data:
    distance: float = 999.0  # Measured distance to wall (meters, 0.5m to 30.0m)
    is_valid: bool = False   # True if measurement is fresh (<0.5s) and within range
    timestamp: float = 0.0
```

!!! tip "Wall Following Regulation"
    During the pier phase, your objective is to maintain a lateral standoff distance of $5.0 \text{ m}$ from the wall.
    A standard Proportional-Derivative (PD) controller:
    ```python
    error = obs.ping2.distance - 5.0
    d_error = (error - prev_error) / dt
    steering = (kp * error) + (kd * d_error)
    ```

---

## 🧭 3. Inertial Measurement Unit (`obs.imu`)

Provides boat attitude and rotational dynamics at $50 \text{ Hz}$:

* `obs.imu.yaw`: Compass heading in radians ($-\pi$ to $+\pi$, $0 = \text{East}$).
* `obs.imu.yaw_deg`: Compass heading in degrees ($-180^\circ$ to $+180^\circ$).
* `obs.imu.yaw_rate`: Yaw angular velocity in rad/s (crucial for derivative yaw damping).
* `obs.imu.roll`, `obs.imu.pitch`: Roll and pitch angles in radians.

---

## 📍 4. GNSS / GPS Receiver (`obs.gps`)

Provides metric local Cartesian coordinates projected at $5 \text{ Hz}$:

* `obs.gps.x`: Local X coordinate in meters ($+X$ pointing East).
* `obs.gps.y`: Local Y coordinate in meters ($+Y$ pointing North).
* `obs.gps.is_valid`: True when valid satellite lock is established.

---

## ⚡ 5. Thruster Commands (`set_thrust`)

The BlueBoat's two differential thrusters are commanded in Newtons:

```python
self.driver.set_thrust(left_thrust: float, right_thrust: float)
```

!!! warning "Strict Physical Clamping"
    * Commands are **strictly clamped between $-50.0 \text{ N}$ and $+50.0 \text{ N}$**.
    * Non-numeric values (`NaN` or `Inf`) are automatically neutralized to $0.0 \text{ N}$.
    * Standard differential thrust formulation:
      $$\text{thrust}_{\text{left}} = \text{surge} - \text{steering}$$
      $$\text{thrust}_{\text{right}} = \text{surge} + \text{steering}$$
