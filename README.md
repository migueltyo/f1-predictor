# f1-predictor
A data-driven Python project simulating the entire 2026 Formula 1 season, race by race, using historical performance, driver experience, preseason testing data, and more parameters.
# F1 2026 Season Simulation

*A Python-based simulation of the 2026 Formula 1 season, predicting race results, driver standings, and constructor championships using historical data and customizable parameters.*

---

##  Overview

This project simulates the entire 2026 F1 season, race-by-race, using:
- **Historical performance** (2025 season data)
- **Driver experience** (weighted probabilities)
- **Preseason testing results** (normalized lap times)
- **Dynamic visualizations** (plots and Excel outputs)

The simulation generates realistic race outcomes, updates championship standings, and provides visual insights into the season's progression.

---

##  Features

- **Race Simulation:** Predicts positions for each Grand Prix and sprint race.
- **Championship Tracking:** Updates driver and constructor points after every race.
- **Visualizations:** Plots driver positions and cumulative points.
- **Excel Outputs:** Detailed spreadsheets with race results and conditional formatting for podium finishes.
- **Customizable Parameters:** Adjust weights for experience, reliability, and more.

---

## 📂 Project Structure

f1-2026-simulation/
- main.py
- data/
  - constructors.py
  - drivers.py
  - events.py
- params/
  - experience.py
  - last_year_standings.py
  - preseason_fastest_lap.py
- plots/
  - championship_positions_plot.py
  - constructors_plot.py
  - total_points_plot.py
- utils/
  - helpers.py
  - simulation.py
- output/
  - f1_simulation_constructors_points.png
  - f1_simulation_points.png
  - f1_simulation_positions.png
  - f1_simulation_race_positions.xlsx
