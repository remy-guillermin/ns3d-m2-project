
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import glob
import ffmpeg
import progressBar
import h5py
from fluidsim import load_sim_for_plot

file_name = 'ns3d_128x128x32_V3x3x0.75_2025-01-10_18-15-53.path'

with open(file_name, 'r') as file:
    simul_path = file.read().strip()

simul_name = os.path.basename(simul_path.rstrip('/'))

# Output directory for frames
frames_dir = 'frames/' + simul_name
os.makedirs(frames_dir, exist_ok=True)

print("Cleaning frames folder")
# Clear frames directory before adding new frames
for file in os.listdir(frames_dir):
	file_path = os.path.join(frames_dir, file)
	if os.path.isfile(file_path):
		os.remove(file_path)
output_dir = 'output/' + simul_name
os.makedirs(output_dir, exist_ok=True)

print("Fetching simulation data")
sim = load_sim_for_plot(simul_path, hide_stdout=True)
print(sim.output.phys_fields)

state_phys_pattern = 'state_phys*.h5'
state_phys_list = sorted(glob.glob(os.path.join(simul_path, state_phys_pattern))) 
print(f'{len(state_phys_list)} files found')

# Open the HDF5 file
print("Processing velocity files and saving frames")
progressBar.printProgressBar(0, len(state_phys_list), prefix = 'Progress:', suffix = 'Complete', length = 50)

vmin, vmax = -1, 1

for idx, file_path in enumerate(state_phys_list):
    with h5py.File(file_path, 'r') as f:
        # Extract the velocity components vx, vy, vz
        vx = f['state_phys/vx'][:]
        vy = f['state_phys/vy'][:]
        vz = f['state_phys/vz'][:]

        # Compute the velocity magnitude
        magnitude = np.sqrt(vx**2 + vy**2 + vz**2)

        # Plot a 2D slice of the velocity magnitude at a specific slice index (e.g., the middle layer)
        slice_index = int(vz.shape[0]/2)
        plt.imshow(magnitude[slice_index, :, :], cmap='viridis', vmin=vmin, vmax=vmax)
        plt.colorbar(label='Velocity Magnitude')
        plt.title(f'Velocity Magnitude Z-Slice')
        plt.tight_layout()

        frame_path = os.path.join(frames_dir, f'frame_mag_{idx:04d}.png')
        plt.savefig(frame_path, bbox_inches='tight')
        plt.close()

        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        # Plot vx
        axes[0].imshow(vx[slice_index, :, :], cmap='viridis', vmin=vmin, vmax=vmax)
        axes[0].set_title(r'$v_x$')
        fig.colorbar(axes[0].imshow(vx[slice_index, :, :], cmap='viridis', vmin=vmin, vmax=vmax), ax=axes[0])

        # Plot vy
        axes[1].imshow(vy[slice_index, :, :], cmap='viridis', vmin=vmin, vmax=vmax)
        axes[1].set_title(r'$v_y$')
        fig.colorbar(axes[1].imshow(vy[slice_index, :, :], cmap='viridis', vmin=vmin, vmax=vmax), ax=axes[1])

        # Plot vz
        axes[2].imshow(vz[slice_index, :, :], cmap='viridis', vmin=vmin, vmax=vmax)
        axes[2].set_title(r'$v_z$')
        fig.colorbar(axes[2].imshow(vz[slice_index, :, :], cmap='viridis', vmin=vmin, vmax=vmax), ax=axes[2])

        plt.tight_layout()
        frame_path = os.path.join(frames_dir, f'frame_vel_{idx:04d}.png')
        plt.savefig(frame_path, bbox_inches='tight')
        plt.close()

        progressBar.printProgressBar(idx+1, len(state_phys_list), prefix = 'Progress:', suffix = 'Complete', length = 50) 

# Combine frames into a video using ffmpeg
print("Combining velocity frames into a video")
video_path = f'{output_dir}/magnitude.mp4'
(
    ffmpeg
    .input(f'{frames_dir}/frame_mag_%04d.png', framerate=10)  # 10 fps
    .output(video_path, pix_fmt='yuv420p', vf='scale=1588:390')
    .run(overwrite_output=True, quiet=True)
)
print(f"Video saved at {video_path}")

video_path = f'{output_dir}/velocity.mp4'
(
    ffmpeg
    .input(f'{frames_dir}/frame_vel_%04d.png', framerate=10)  # 10 fps
    .output(video_path, pix_fmt='yuv420p', vf='scale=1588:390')
    .run(overwrite_output=True, quiet=True)
)

print(f"Video saved at {video_path}")

print("Cleaning frames folder")
# Clear frames directory before adding new frames
for file in os.listdir(frames_dir):
	file_path = os.path.join(frames_dir, file)
	if os.path.isfile(file_path):
		os.remove(file_path)
