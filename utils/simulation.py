import pandas as pd

def simulate_events(drivers_df, gp_events, race_types, standard_points, sprint_points):
    results = pd.DataFrame({"driverId": drivers_df["driverId"], **{event: 0 for event in gp_events}})
    for event_idx in range(len(gp_events)):
        is_sprint = race_types[event_idx] == "sprint"
        points = sprint_points if is_sprint else standard_points
        race_result = drivers_df.sample(weights=drivers_df["prob"], n=len(drivers_df), replace=True)
        unique_drivers = []
        for driver in race_result["driverId"]:
            if driver not in unique_drivers:
                unique_drivers.append(driver)
            if len(unique_drivers) == 10:
                break
        for pos, driver in enumerate(unique_drivers[:10]):
            results.loc[results["driverId"] == driver, gp_events[event_idx]] = points[pos]
    return results
