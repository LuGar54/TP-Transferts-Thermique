import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
from matplotlib.colors import Normalize


def animate_thermal_system(data_array, skip_step=10, interval=20):
    """
    Animates the thermal profile.
    
    Args:
        data_array: Shape (X, 13)
        skip_step:  Renders only every Nth frame (e.g., 10 skips 9 frames).
        interval:   Delay between frames in milliseconds (lower = faster playback).
    """
    
    # --- 1. Setup Figure ---
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Geometry Constants
    n_cells = 6
    cell_width = 2.0
    cell_height = 2.0
    wall_thickness = 0.5
    gap = 0.2 
    
    total_structure_width = n_cells * (cell_width + gap) + gap
    total_structure_height = cell_height + 2 * wall_thickness
    
    ax.set_xlim(-2, total_structure_width + 2)
    ax.set_ylim(-2, total_structure_height + 2)

    # --- 2. Color Scaling ---
    vmin = np.min(data_array)
    vmax = np.max(data_array)
    norm = Normalize(vmin=vmin, vmax=vmax)
    cmap = plt.cm.coolwarm 

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, orientation='horizontal', fraction=0.05, pad=0.05)
    cbar.set_label('Temperature (°C)')

    # --- 3. Create Patches (Geometry) ---
    patches_dict = {}

    # A. Ground (Index 12)
    ground_rect = patches.Rectangle(
        (-2, -2), total_structure_width + 4, total_structure_height + 4,
        linewidth=0, facecolor=cmap(norm(data_array[0, 12]))
    )
    ax.add_patch(ground_rect)
    patches_dict['ground'] = ground_rect
    ax.text(0, -1.5, "Ground (Ext)", fontsize=10, color='black', fontweight='bold')

    # B. Cells and Walls
    start_x = gap
    y_wall_bottom = 0
    y_air = wall_thickness
    y_wall_top = wall_thickness + cell_height

    for i in range(n_cells):
        x_pos = start_x + i * (cell_width + gap)
        current_wall_patches = []

        # Bottom Wall
        rect_wall_bot = patches.Rectangle(
            (x_pos, y_wall_bottom), cell_width, wall_thickness,
            edgecolor='black', facecolor=cmap(norm(data_array[0, i+6]))
        )
        ax.add_patch(rect_wall_bot)
        current_wall_patches.append(rect_wall_bot)
        
        # Top Wall
        rect_wall_top = patches.Rectangle(
            (x_pos, y_wall_top), cell_width, wall_thickness,
            edgecolor='black', facecolor=cmap(norm(data_array[0, i+6]))
        )
        ax.add_patch(rect_wall_top)
        current_wall_patches.append(rect_wall_top)

        # Left End Wall (Cell 0)
        if i == 0:
            rect_wall_left = patches.Rectangle(
                (x_pos - wall_thickness, y_wall_bottom), wall_thickness, total_structure_height,
                edgecolor='black', facecolor=cmap(norm(data_array[0, i+6]))
            )
            ax.add_patch(rect_wall_left)
            current_wall_patches.append(rect_wall_left)

        # Right End Wall (Cell 5)
        if i == n_cells - 1:
            rect_wall_right = patches.Rectangle(
                (x_pos + cell_width, y_wall_bottom), wall_thickness, total_structure_height,
                edgecolor='black', facecolor=cmap(norm(data_array[0, i+6]))
            )
            ax.add_patch(rect_wall_right)
            current_wall_patches.append(rect_wall_right)

        patches_dict[f'wall_{i}'] = current_wall_patches

        # Air Cell
        rect_air = patches.Rectangle(
            (x_pos, y_air), cell_width, cell_height,
            edgecolor='black', linestyle='--', linewidth=0.5,
            facecolor=cmap(norm(data_array[0, i]))
        )
        ax.add_patch(rect_air)
        patches_dict[f'air_{i}'] = rect_air
        
        ax.text(x_pos + cell_width/2, y_air + cell_height/2, f"P{i+1}", 
                ha='center', va='center', fontsize=9, color='white', fontweight='bold')

    # --- 4. Animation Update ---
    def update(frame_idx):
        # 'frame_idx' will now jump: 0, 10, 20...
        current_temps = data_array[frame_idx]
        
        # Update Ground
        patches_dict['ground'].set_facecolor(cmap(norm(current_temps[12])))
        
        # Update Cells and Walls
        for i in range(n_cells):
            patches_dict[f'air_{i}'].set_facecolor(cmap(norm(current_temps[i])))
            
            color_wall = cmap(norm(current_temps[i+6]))
            for wall_part in patches_dict[f'wall_{i}']:
                wall_part.set_facecolor(color_wall)
        
        ax.set_title(f"Thermal Simulation: Step {frame_idx}")
        return []

    # KEY CHANGE: 'frames' uses a stepped range
    total_frames = len(data_array)
    anim = animation.FuncAnimation(
        fig, update, 
        frames=range(0, total_frames, skip_step), # Pass indices with stride
        interval=interval, 
        blit=False
    )
    
    plt.show()