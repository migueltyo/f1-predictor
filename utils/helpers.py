import pandas as pd
import numpy as np

def adjust_probabilities_by_constructor_reliability(drivers_df, constructors_df):
    for idx, row in drivers_df.iterrows():
        constructor_id = row["constructorId"]
        constructor_reliability_score = constructors_df.loc[
            constructors_df["constructorId"] == constructor_id, "reliability"
        ].values[0]
        drivers_df.at[idx, "prob"] *= constructor_reliability_score
    return drivers_df

def calculate_championship_positions(cumulative_points):
    championship_positions = pd.DataFrame(
        index=cumulative_points.index,
        columns=cumulative_points.columns
    )

    for event in cumulative_points.columns:
        points = cumulative_points[event]
        ranked = points.rank(method='min', ascending=False)

        groups = ranked.groupby(ranked)
        for rank, group in groups:
            drivers = group.index.tolist()
            np.random.shuffle(drivers)
            for driver in drivers:
                championship_positions.loc[driver, event] = rank

    return championship_positions

def calculate_constructors_points(drivers_df, results, constructors_df, gp_events):
    # Create mapping of drivers to constructors
    driver_to_constructor = {}
    for _, row in drivers_df.iterrows():
        driver_to_constructor[row["driverId"]] = row["constructorId"]

    # Initialize DataFrame for constructor points
    constructors_points = pd.DataFrame(
        0,
        index=constructors_df["constructorId"],
        columns=gp_events
    )

    # For each event, calculate constructor points
    for event in gp_events:
        # Get all drivers' points for this event
        event_points = results[event]

        # For each constructor, sum points of their drivers
        for constructor in constructors_df["constructorId"]:
            constructor_drivers = [d for d, c in driver_to_constructor.items() if c == constructor]
            total_points = 0
            for driver in constructor_drivers[:2]:  # Only top 2 drivers count
                driver_points = event_points[results['driverId'] == driver]
                if not driver_points.empty:
                    total_points += driver_points.iloc[0]
            constructors_points.loc[constructor, event] = total_points

    return constructors_points

def calculate_cumulative_constructors_points(constructors_points):
    return constructors_points.cumsum(axis=1)
