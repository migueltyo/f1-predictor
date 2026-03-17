import matplotlib
matplotlib.use('Agg')
import pandas as pd
import numpy as np
from tqdm import tqdm
from params.drivers_form import get_drivers_form
from params.driver_reliability import get_driver_reliability
from params.constructor_reliability import get_constructor_reliability
from utils.data_loader import (
    load_fastest_laps, load_constructors_data, load_drivers_data,
    format_driver_name, assign_constructors_to_drivers
)
from utils.probability_calculator import calculate_probabilities
from utils.simulation_runner import run_simulations
from utils.visualisation import (
    plot_constructors_points, plot_championship_positions, plot_total_points
)
from utils.helpers import (
    adjust_probabilities_by_constructor_reliability,
    calculate_championship_positions,
    calculate_constructors_points,
    calculate_cumulative_constructors_points
)

def set_column_width(worksheet, df):
    for idx, col in enumerate(df.columns):
        max_len = max(
            df[col].apply(lambda x: len(str(x)) if pd.notna(x) else 0).max(),
            len(str(col))
        ) + 2
        worksheet.set_column(idx, idx, max_len)

def main():
    num_simulations = 100

    # Load data
    fastest_laps = load_fastest_laps()
    constructors_data = load_constructors_data()
    drivers_data = load_drivers_data()

    # Add fastest lap times to drivers_data
    drivers_data["fastest_lap"] = []
    for driver in drivers_data["driverId"]:
        driver_key = driver.replace(" ", "-").lower()
        drivers_data["fastest_lap"].append(fastest_laps.get(driver_key, 97.0))

    # Get drivers' form from the last 5 races
    drivers_form = get_drivers_form()
    drivers_data["form"] = []
    for driver in drivers_data["driverId"]:
        driver_key = driver.replace(" ", "-").lower()
        drivers_data["form"].append(drivers_form.get(driver_key, 15))

    # Get drivers' reliability
    driver_reliability = get_driver_reliability()
    drivers_data["reliability"] = []
    for driver in drivers_data["driverId"]:
        driver_key = driver.replace(" ", "-").lower()
        drivers_data["reliability"].append(driver_reliability.get(driver_key, 0.85))

    # Get constructors' reliability
    constructor_reliability = get_constructor_reliability()
    constructors_data["reliability"] = []
    for constructor in constructors_data["constructorId"]:
        constructor_key = constructor.replace(" ", "-").lower()
        constructors_data["reliability"].append(constructor_reliability.get(constructor_key, 0.85))

    # Create DataFrames
    constructors_df = pd.DataFrame(constructors_data)
    drivers_df = pd.DataFrame(drivers_data)

    # Assign constructors to drivers
    drivers_df = assign_constructors_to_drivers(drivers_df)

    # Define weights for each parameter
    weights = {
        "last_year_standings": 0.2,
        "experience": 0.1,
        "fastest_lap": 0.20,
        "drivers_form": 0.3,
        "reliability": 0.1,
        "constructor_reliability": 0.1
    }

    # Calculate probabilities
    drivers_df = calculate_probabilities(drivers_df, weights)

    # Adjust driver probabilities by constructor reliability
    drivers_df = adjust_probabilities_by_constructor_reliability(drivers_df, constructors_df)

    # Define team display names and colors
    team_display_names = {
        "mclaren": "McLaren",
        "mercedes": "Mercedes",
        "red-bull": "Red Bull",
        "ferrari": "Ferrari",
        "williams": "Williams",
        "racing-bulls": "Racing Bulls",
        "aston-martin": "Aston Martin",
        "haas": "Haas",
        "alpine": "Alpine",
        "audi": "Audi",
        "cadillac": "Cadillac"
    }

    team_colors = {
        "ferrari": (1.0, 0.0, 0.0),        # Red
        "mclaren": (1.0, 0.65, 0.0),      # Orange
        "mercedes": (0.0, 0.65, 0.65),    # Darker cyan
        "red-bull": (0.0, 0.0, 0.54),     # Dark blue
        "cadillac": (0.0, 0.0, 0.0),      # Black
        "audi": (0.5, 0.2, 0.2),          # Grey
        "racing-bulls": (0.8, 0.8, 0.0),  # Darker yellow
        "alpine": (1.0, 0.75, 0.8),       # Pink
        "haas": (0.66, 0.66, 0.66),       # Dark grey
        "williams": (0.0, 0.4, 1.0),      # Blue
        "aston-martin": (0.13, 0.54, 0.13) # Forest green
    }

    # GP names for each race and sprint
    gp_events = [
        "Australia", "China Race", "China Sprint", "Japan", "Bahrain", "Miami Race", "Miami Sprint",
        "Canada Race", "Canada Sprint", "Monaco", "Barcelona", "Austria", "Britain Race", "Britain Sprint",
        "Belgium", "Hungary", "Netherlands Race", "Netherlands Sprint", "Italy", "Spain", "Azerbaijan",
        "Singapore Race", "Singapore Sprint", "USA", "Mexico", "Brazil", "Las Vegas", "Qatar", "Abu Dhabi"
    ]

    # Determine race types
    race_types = ["sprint" if "Sprint" in event else "standard" for event in gp_events]

    # F1 points system (standard and sprint)
    standard_points = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
    sprint_points = [8, 7, 6, 5, 4, 3, 2, 1, 0, 0]

    # Run simulations
    final_positions_stats, results = run_simulations(drivers_df, constructors_df, gp_events, race_types, standard_points, sprint_points, num_simulations)

    # Calculate cumulative points
    cumulative_points = results.iloc[:, 1:].cumsum(axis=1)
    cumulative_points.insert(0, 'driverId', results['driverId'])

    # Calculate championship positions
    championship_positions = calculate_championship_positions(cumulative_points.set_index('driverId'))

    # Calculate constructors points
    constructors_points = calculate_constructors_points(drivers_df, results, constructors_df, gp_events)

    # Calculate cumulative constructors points
    cumulative_constructors_points = calculate_cumulative_constructors_points(constructors_points)

    # Create an Excel file with all results
    with pd.ExcelWriter('f1_simulation_race_positions.xlsx', engine='xlsxwriter') as writer:
        # Driver results (unchanged)
        results.to_excel(writer, sheet_name='Race Points', index=False)
        championship_points = cumulative_points.set_index('driverId')
        championship_points.to_excel(writer, sheet_name='Championship Points')

        # Constructors points - with constructorId as first column (no displayName)
        constructors_points_with_names = constructors_points.copy()
        constructors_points_with_names = constructors_points_with_names.reset_index()
        constructors_points_with_names = constructors_points_with_names.rename(columns={'index': 'constructorId'})
        constructors_points_with_names = constructors_points_with_names[['constructorId'] + gp_events]
        constructors_points_with_names.to_excel(writer, sheet_name='Constructors Points', index=False)

        # Cumulative constructors points - with constructorId as first column (no displayName)
        cumulative_constructors_points_with_names = cumulative_constructors_points.copy()
        cumulative_constructors_points_with_names = cumulative_constructors_points_with_names.reset_index()
        cumulative_constructors_points_with_names = cumulative_constructors_points_with_names.rename(
            columns={'index': 'constructorId'})
        cumulative_constructors_points_with_names = cumulative_constructors_points_with_names[
            ['constructorId'] + gp_events]
        cumulative_constructors_points_with_names.to_excel(writer, sheet_name='Cumulative Constructors Points',
                                                           index=False)

        # Final positions stats - with driverId as first column
        final_positions_stats_sorted = final_positions_stats.sort_values(by="Average Position")
        final_positions_stats_sorted = final_positions_stats_sorted.reset_index()
        final_positions_stats_sorted = final_positions_stats_sorted.rename(columns={'index': 'driverId'})
        final_positions_stats_sorted.to_excel(writer, sheet_name='Final Positions Stats', index=False)

        # Final constructor stats (unchanged)
        constructors_final_positions = pd.DataFrame(0,
                                                    index=constructors_df["constructorId"],
                                                    columns=range(1, len(constructors_df) + 1))

        for sim in tqdm(range(num_simulations), desc="Calculating constructor positions"):
            sim_results = run_simulations(drivers_df, constructors_df, gp_events, race_types, standard_points,
                                          sprint_points, 1)
            sim_constructors_points = calculate_constructors_points(drivers_df, sim_results[1], constructors_df,
                                                                    gp_events)
            final_standings = sim_constructors_points.sum(axis=1).sort_values(ascending=False)
            for position, (constructor, _) in enumerate(final_standings.items(), start=1):
                constructors_final_positions.loc[constructor, position] += 1

        constructors_final_positions["Average Position"] = (
                                                                   constructors_final_positions * constructors_final_positions.columns
                                                           ).sum(axis=1) / num_simulations
        constructors_final_positions_sorted = constructors_final_positions.sort_values(by="Average Position")
        constructors_final_positions_sorted.to_excel(writer, sheet_name='Final Constructors Stats')

    # Generate visualizations
    plot_constructors_points(constructors_df, cumulative_constructors_points, gp_events, team_display_names, team_colors)
    plot_championship_positions(drivers_df, championship_positions, gp_events, team_colors)
    plot_total_points(drivers_df, cumulative_points.set_index('driverId'), gp_events, team_colors)

if __name__ == "__main__":
    main()
