def calculate_probabilities(drivers_df, weights):
    # Normalize last year's points to get probabilities
    drivers_df["points_prob"] = (drivers_df["points"] + 1) / (drivers_df["points"].sum() + len(drivers_df))

    # Normalize experience to get probabilities
    drivers_df["experience_prob"] = drivers_df["experience"] / drivers_df["experience"].sum()

    # Normalize fastest lap times to get probabilities (lower time = higher probability)
    min_lap = min(drivers_df["fastest_lap"])
    max_lap = max(drivers_df["fastest_lap"])
    drivers_df["fastest_lap_prob"] = 1 - ((drivers_df["fastest_lap"] - min_lap) / (max_lap - min_lap))

    # Normalize form to get probabilities (lower average position = higher probability)
    min_form = min(drivers_df["form"])
    max_form = max(drivers_df["form"])
    drivers_df["form_prob"] = 1 - ((drivers_df["form"] - min_form) / (max_form - min_form))

    # Normalize reliability to get probabilities
    drivers_df["reliability_prob"] = drivers_df["reliability"] / drivers_df["reliability"].sum()

    # Combine probabilities using defined weights
    drivers_df["prob"] = (
        weights["last_year_standings"] * drivers_df["points_prob"] +
        weights["experience"] * drivers_df["experience_prob"] +
        weights["fastest_lap"] * drivers_df["fastest_lap_prob"] +
        weights["drivers_form"] * drivers_df["form_prob"] +
        weights["reliability"] * drivers_df["reliability_prob"]
    )

    return drivers_df
