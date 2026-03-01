def calculate_experience_prob(drivers_df):
    drivers_df["experience_prob"] = drivers_df["experience"] / drivers_df["experience"].sum()
    return drivers_df
