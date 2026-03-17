from tqdm import tqdm
import pandas as pd
import numpy as np

def run_simulations(drivers_df, constructors_df, gp_events, race_types, standard_points, sprint_points, num_simulations=100):
    num_events = len(gp_events)

    # Get driver names from the DataFrame
    driver_names = drivers_df["driverId"].tolist()

    # Initialize DataFrame with positions starting from 1 to 22
    final_positions_stats = pd.DataFrame(0, index=driver_names, columns=range(1, 23))

    for _ in tqdm(range(num_simulations), desc="Running simulations"):
        results = pd.DataFrame({
            "driverId": drivers_df["driverId"],
            **{event: 0 for event in gp_events}
        })

        for event_idx in range(num_events):
            is_sprint = race_types[event_idx] == "sprint"
            points = sprint_points if is_sprint else standard_points

            race_result = drivers_df.sample(weights=drivers_df["prob"], n=len(drivers_df), replace=True)

            unique_drivers = []
            for driver in race_result["driverId"]:
                if driver not in unique_drivers:
                    unique_drivers.append(driver)
                if len(unique_drivers) == len(points):
                    break

            for pos, driver in enumerate(unique_drivers[:len(points)]):
                results.loc[results["driverId"] == driver, gp_events[event_idx]] = points[pos]

        cumulative_points = results.iloc[:, 1:].cumsum(axis=1)
        final_championship_points = cumulative_points.iloc[:, -1]

        # Get the driver names from the index
        driver_index = results["driverId"].tolist()

        # Rank the drivers by points
        ranked = pd.Series(final_championship_points.values, index=driver_index).rank(method='min', ascending=False)

        # Break ties randomly
        groups = ranked.groupby(ranked)
        final_championship_positions = pd.Series(index=driver_index, dtype=int)
        current_rank = 1
        for rank, group in groups:
            drivers = group.index.tolist()
            np.random.shuffle(drivers)
            for driver in drivers:
                final_championship_positions[driver] = current_rank
                current_rank += 1

        # Update final positions stats
        for driver, position in final_championship_positions.items():
            if driver in final_positions_stats.index and position in final_positions_stats.columns:
                final_positions_stats.loc[driver, position] += 1

    # Calculate average position
    final_positions_stats["Average Position"] = (
        (final_positions_stats * final_positions_stats.columns).sum(axis=1) / num_simulations
    )

    return final_positions_stats, results
