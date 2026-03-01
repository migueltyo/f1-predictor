import matplotlib
matplotlib.use('Agg')

import pandas as pd
from data.constructors import constructors_data, team_display_names, team_colors
from data.drivers import drivers_data, fastest_laps
from data.events import gp_events, standard_points, sprint_points
from params.experience import calculate_experience_prob
from params.preseason_fastest_lap import calculate_preseason_fastest_lap_prob
from params.last_year_standings import calculate_last_year_prob
from plots.constructors_plot import plot_constructors_points
from plots.championship_positions_plot import plot_championship_positions
from plots.total_points_plot import plot_total_points
from utils.helpers import format_driver_name
from utils.simulation import simulate_events

# Create DataFrames
constructors_df = pd.DataFrame(constructors_data)
drivers_df = pd.DataFrame(drivers_data)

# Add fastest lap times to drivers_df
for driver in drivers_df["driverId"]:
    driver_key = driver.replace(" ", "-").lower()
    drivers_df.loc[drivers_df["driverId"] == driver, "fastest_lap"] = fastest_laps.get(driver_key, 97.0)

# Format driver names
drivers_df["driverId"] = drivers_df["driverId"].apply(format_driver_name)

# Manually assign constructors to drivers
drivers_df["constructorId"] = [
    "mclaren", "mclaren", "mercedes", "mercedes", "red-bull", "red-bull",
    "ferrari", "ferrari", "williams", "williams", "racing-bulls", "racing-bulls",
    "aston-martin", "aston-martin", "haas", "haas", "audi", "audi",
    "alpine", "alpine", "cadillac", "cadillac"
]

# Define weights for each parameter
weights = {
    "last_year_standings": 0.6,
    "experience": 0.10,
    "fastest_lap": 0.30
}

# Calculate probabilities
drivers_df = calculate_last_year_prob(drivers_df)
drivers_df = calculate_experience_prob(drivers_df)
drivers_df = calculate_preseason_fastest_lap_prob(drivers_df)

# Combine probabilities
drivers_df["prob"] = (
    weights["last_year_standings"] * drivers_df["points_prob"] +
    weights["experience"] * drivers_df["experience_prob"] +
    weights["fastest_lap"] * drivers_df["fastest_lap_prob"]
)

# Determine race types
race_types = ["sprint" if "Sprint" in event else "standard" for event in gp_events]

# Simulate events
results = simulate_events(drivers_df, gp_events, race_types, standard_points, sprint_points)

# Calculate cumulative points
cumulative_points = results.iloc[:, 1:].cumsum(axis=1)

# Calculate championship positions
championship_positions = pd.DataFrame(index=results.index, columns=cumulative_points.columns)
for event in cumulative_points.columns:
    championship_positions[event] = cumulative_points[event].rank(method='dense', ascending=False)
    championship_positions = championship_positions.sort_values(by=event, kind='mergesort')
    championship_positions[event] = range(1, len(championship_positions) + 1)

# Calculate constructors points
constructors_points = pd.DataFrame(index=range(len(constructors_df)), columns=gp_events)
constructors_points["constructorId"] = constructors_df["constructorId"]
for constructor in constructors_df["constructorId"]:
    constructor_drivers = drivers_df[drivers_df["constructorId"] == constructor]["driverId"]
    for event in gp_events:
        total_points = 0
        for driver in constructor_drivers:
            total_points += results.loc[results["driverId"] == driver, event].values[0]
        constructors_points.loc[constructors_points["constructorId"] == constructor, event] = total_points

# Calculate cumulative constructors points
cumulative_constructors_points = pd.DataFrame(index=constructors_points.index, columns=gp_events)
cumulative_constructors_points["constructorId"] = constructors_points["constructorId"]
for idx, constructor in enumerate(constructors_points["constructorId"]):
    constructor_data = constructors_points.loc[constructors_points["constructorId"] == constructor, gp_events]
    cumulative_constructors_points.loc[idx, gp_events] = constructor_data.cumsum(axis=1).values.flatten()

# Add display names
constructors_df["displayName"] = constructors_df["constructorId"].map(team_display_names)
constructors_points["displayName"] = constructors_points["constructorId"].map(team_display_names)
cumulative_constructors_points["displayName"] = cumulative_constructors_points["constructorId"].map(team_display_names)

# Create Excel file
with pd.ExcelWriter('f1_simulation_race_positions.xlsx', engine='xlsxwriter') as writer:
    results.to_excel(writer, sheet_name='Race Points', index=False)
    championship_points = cumulative_points.copy()
    championship_points.insert(0, 'driverId', results['driverId'])
    championship_points.to_excel(writer, sheet_name='Championship Points', index=False)
    constructors_points.to_excel(writer, sheet_name='Constructors Points', index=False, columns=["displayName"] + gp_events)
    cumulative_constructors_points.to_excel(writer, sheet_name='Cumulative Constructors Points', index=False, columns=["displayName"] + gp_events)

# Generate plots
plot_constructors_points(cumulative_constructors_points, gp_events, team_display_names, team_colors)
plot_championship_positions(championship_positions, gp_events, drivers_df, team_colors)
plot_total_points(cumulative_points, gp_events, drivers_df, team_colors)
