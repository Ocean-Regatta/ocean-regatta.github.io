# Ocean Regatta — Official Portal & Multi-Edition Scoreboard 🌐🏆

Official documentation website and static live scoreboard for **Ocean Regatta**, hosted on GitHub Pages: [https://ocean-regatta.github.io](https://ocean-regatta.github.io).

---

## 🏛️ Repository Structure

```text
.
├── .github/
│   └── workflows/
│       └── deploy_docs.yml        # Automated MkDocs build & deployment to GitHub Pages
├── docs/                          # Static documentation & scoreboard pages
│   ├── index.md                   # Home page & challenge edition roadmap
│   ├── quickstart.md              # Competitor setup & Docker workflow
│   ├── driver_api.md              # Hardware Abstraction Layer & sensor specs
│   ├── replay.md                  # 3D playback & Gazebo replay instructions
│   ├── maintenance_deploy.md      # Organizer deployment & administration guide
│   ├── editions/
│   │   └── 2026.md                # 2026 official technical rules & mathematical formulas
│   ├── scoreboards/
│   │   └── 2026.md                # 2026 dynamic static scoreboard & badge gallery
│   ├── data/
│   │   ├── leaderboard.json       # Live JSON metrics feed (active edition)
│   │   └── leaderboard_2026.json  # 2026 edition metrics feed
│   ├── javascripts/
│   │   └── mathjax.js             # MathJax LaTeX rendering configuration
│   └── stylesheets/
│       └── extra.css              # Custom ocean theme & scoreboard table styles
├── scripts/
│   └── update_leaderboard.py      # Automated leaderboard & badge evaluation engine
├── mkdocs.yml                     # MkDocs configuration (Material for MkDocs)
├── requirements-docs.txt          # Python documentation dependencies
└── README.md                      # Repository overview
```

---

## 🌟 Key Features

### 1. 100% Static & Serverless Architecture
* The entire documentation and leaderboard operate statically via **GitHub Pages**.
* Zero external web servers or databases required.
* Results are updated in CI/CD by appending or updating `docs/data/leaderboard.json`, automatically rebuilding the static site.

### 2. Multi-Edition Hierarchy
* The portal supports archiving historical editions while featuring the active edition.
* Main navigation tab **Live Scoreboard** opens the active edition (`scoreboards/2026.md`).
* Previous editions can be preserved alongside future editions without restructuring the portal.

### 3. Dynamic Telemetry Badges & Trophy Gallery
* Distinction badges and trophies are verified automatically from run telemetry (simulation time, precision distance, thruster energy, drift tolerance, and collision detection).
* Dynamic badges include exclusive trophies (👑 **Quay Sovereign**, ⚡ **Speed Demon**, 🎯 **Sniper**, 🔋 **Watt Miser**, 🦇 **Sonar Whisperer**, 🔱 **Poseidon's Chosen**) and lore achievements (🐙 **Kraken's Grip**, 🧜‍♀️ **Siren's Call**, 🦀 **Crab Walk**, 🍩 **Donut King**, 🩹 **Tis But a Scratch**, ☕ **Espresso Powered**, and more).

---

## 🚀 Local Development

To run and preview the portal locally:

```bash
# 1. Install dependencies
pip install -r requirements-docs.txt

# 2. Start local live-reloading server
mkdocs serve
```

Open `http://127.0.0.1:8000/` in your browser.

To verify the build strictly:

```bash
python -m mkdocs build --strict
```

---

## 📄 License

Released under the [MIT License](LICENSE).