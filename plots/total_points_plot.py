import matplotlib.pyplot as plt

def plot_total_points(cumulative_points, gp_events, drivers_df, team_colors):
    plt.figure(figsize=(18, 8))
    team_drivers = drivers_df.groupby("constructorId")["driverId"].apply(list).to_dict()
    for idx, driver in enumerate(drivers_df["driverId"]):
        team = drivers_df.loc[idx, "constructorId"]
        driver_name = driver
        driver_points = cumulative_points.loc[idx]
        linestyle = '--' if driver_name == team_drivers[team][1] else '-'
        plt.plot(driver_points, label=driver_name, color=team_colors[team], linestyle=linestyle, marker='o', markersize=3)
    plt.title("F1 2026 Season Simulation: Total Points by Event")
    plt.xlabel("Event")
    plt.ylabel("Total Points")
    plt.xticks(range(len(gp_events)), gp_events, rotation=90)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.grid(True, color='lightgrey', alpha=0.5)
    plt.savefig('f1_simulation_points.png', dpi=300, bbox_inches='tight')
    plt.close()
