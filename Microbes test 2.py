import matplotlib.pyplot as plt
import random


# Define the chamber size
chamber_size = (200, 200)

# Define the number of microbes
num_microbes = 300

# Number of timesteps
num_timesteps = 101

# Number of timesteps to save plots
save_plot_interval = 20

# Parameters for random motion
random_motion_range = (-5, 5)

def generate_initial_positions(num_microbes, chamber_size):
    initial_positions = []
    for _ in range(num_microbes):
        mx = random.randint(1, chamber_size[0] - 2)
        my = random.randint(1, chamber_size[1] - 2)  # Avoid boundary
        initial_positions.append((mx, my))
    return initial_positions
"""
Generates the initial positions of the microbes, within the chamber. 
"""
# Initialize microbe positions
microbe_positions = generate_initial_positions(num_microbes, chamber_size)

# Function to calculate the strength of attraction
def calculate_attraction(mx, my, fx, fy):
    r = ((fx - mx) ** 2 + (fy - my) ** 2) ** 0.5

    if r > 150:
        e = 0
    elif 150 >= r > 100:
        e = 0.025
    elif 100 >= r > 50:
        e = 0.05
    else:
        e = 0.005

    return e

""" 
Calculates the strength of attraction of microbes to a food source, using microbe positions as inputs. 
"""
# Function to update microbe positions at each timestep
def update_microbe_positions(positions):
    updated_positions = []

    for mx, my in positions:
        # Random motion
        Mrx = random.randint(*random_motion_range)
        Mry = random.randint(*random_motion_range)

        # Chemotaxis motion
        fx, fy = random.randint(0, chamber_size[0]), random.randint(0, chamber_size[1])
        Mcx = calculate_attraction(mx, my, fx, fy) * (fx - mx)
        Mcy = calculate_attraction(mx, my, fx, fy) * (fy - my)

        # Fluid flow motion
        Mfy = -0.025

        # Update position using Equations 4 and 5
        new_mx = mx + Mrx + Mcx
        new_my = my + Mry + Mcy + Mfy

        # Check if the new position is within the chamber boundaries
        if 0 <= new_mx < chamber_size[0] and 0 <= new_my < chamber_size[1]:
            updated_positions.append((new_mx, new_my))
        else:
            updated_positions.append((mx, my))  # Stay at the previous position if outside boundaries

    return updated_positions

"""
Updates the position of each microbe, at each timestep, using positions as inputs
"""
# Function to save plot as PDF
def save_plot(timestep):
    plt.scatter(*zip(*microbe_positions), marker='o', s=10)  # 'o' for circle marker, s for marker size
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title(f'Microbe Movement at Timestep {timestep}')
    plt.xlim(0, chamber_size[0])
    plt.ylim(0, chamber_size[1])
    plt.savefig(f'ex2_question2_plot{timestep}.pdf')
    plt.close()

"""
Saves the plots of the updated positions, at each individual timestep to a pdf
"""

# Simulate microbe movement for each timestep
for timestep in range(num_timesteps):
    microbe_positions = update_microbe_positions(microbe_positions)

    # Save plot every 20 timesteps
    if timestep % save_plot_interval == 0:
        save_plot(timestep)