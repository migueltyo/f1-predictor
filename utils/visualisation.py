import matplotlib.pyplot as plt
import pandas as pd

def plot_constructors_points(constructors_df, cumulative_constructors_points, gp_events, team_display_names, team_colors):
    plt.figure(figsize=(15, 8))

    # Plot each constructor's points progression
    for constructor in constructors_df["constructorId"]:
        if constructor in cumulative_constructors_points.index:
            points = [cumulative_constructors_points.loc[constructor, event] for event in gp_events]
            display_name = team_display_names.get(constructor, constructor)
            color = team_colors.get(constructor.lower(), (0.5, 0.5, 0.5))
            plt.plot(gp_events, points, marker='o', label=display_name, color=color)

    plt.title('F1 2026 Season Simulation: Constructors Points by Event')
    plt.xlabel('Event')
    plt.ylabel('Total Points')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('constructors_points.png')
    plt.close()

def plot_championship_positions(drivers_df, championship_positions, gp_events, team_colors):
    plt.figure(figsize=(15, 8))

    # Plot each driver's positions
    for idx, driver in enumerate(drivers_df["driverId"]):
        if driver in championship_positions.index:
            positions = championship_positions.loc[driver].values
            constructor = drivers_df.loc[idx, "constructorId"]
            color = team_colors.get(constructor.lower(), (0.5, 0.5, 0.5))
            driver_name = driver.replace('-', ' ').title()
            plt.plot(gp_events, positions, marker='o', label=driver_name, color=color)

    plt.title('F1 2026 Season Simulation: Driver Championship Positions')
    plt.xlabel('Event')
    plt.ylabel('Championship Position')
    plt.xticks(rotation=45)
    plt.gca().invert_yaxis()  # Lower positions are better
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('championship_positions.png')
    plt.close()

def plot_total_points(drivers_df, cumulative_points, gp_events, team_colors):
    plt.figure(figsize=(15, 8))

    # Plot each driver's points progression
    for idx, driver in enumerate(drivers_df["driverId"]):
        if driver in cumulative_points.index:
            points = cumulative_points.loc[driver].values
            constructor = drivers_df.loc[idx, "constructorId"]
            color = team_colors.get(constructor.lower(), (0.5, 0.5, 0.5))
            driver_name = driver.replace('-', ' ').title()
            plt.plot(gp_events, points, marker='o', label=driver_name, color=color)

    plt.title('F1 2026 Season Simulation: Driver Points Progression')
    plt.xlabel('Event')
    plt.ylabel('Total Points')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('driver_points.png')
    plt.close()
