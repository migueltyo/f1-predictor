def calculate_last_year_prob(drivers_df):
    drivers_df["points_prob"] = (drivers_df["points"] + 1) / (drivers_df["points"].sum() + len(drivers_df))
    return drivers_df
