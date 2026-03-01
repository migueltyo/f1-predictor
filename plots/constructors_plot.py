import matplotlib.pyplot as plt

def plot_constructors_points(cumulative_constructors_points, gp_events, team_display_names, team_colors):
    plt.figure(figsize=(18, 8))
    for idx, constructor in enumerate(cumulative_constructors_points["constructorId"]):
        constructor_points = cumulative_constructors_points.loc[idx, gp_events].values
        display_name = team_display_names[constructor]
        plt.plot(
            range(len(gp_events)),
            constructor_points,
            label=display_name,
            color=team_colors[constructor],
            linestyle='-',
            marker='o',
            markersize=3
        )
    plt.title("F1 2026 Season Simulation: Constructors Points by Event")
    plt.xlabel("Event")
    plt.ylabel("Total Points")
    plt.xticks(range(len(gp_events)), gp_events, rotation=90)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.grid(True, color='lightgrey', alpha=0.5)
    plt.savefig('f1_simulation_constructors_points.png', dpi=300, bbox_inches='tight')
    plt.close()
