def calculate_preseason_fastest_lap_prob(drivers_df):
    min_lap = min(drivers_df["fastest_lap"])
    max_lap = max(drivers_df["fastest_lap"])
    drivers_df["fastest_lap_prob"] = 1 - ((drivers_df["fastest_lap"] - min_lap) / (max_lap - min_lap))
    return drivers_df
