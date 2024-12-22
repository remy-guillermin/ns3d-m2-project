import matplotlib.pyplot as plt
import numpy as np
import h5py

# Open the HDF5 file
file_path = '/home/m24075/m24075-293/Sim_data/examples/test_iso3d/ns3d_64x64x64_V3x3x3_2024-12-22_15-48-25/state_phys_t0020.003.h5'
with h5py.File(file_path, 'r') as f:
    # Extract the velocity components vx, vy, vz
    vx = f['state_phys/vx'][:]
    vy = f['state_phys/vy'][:]
    vz = f['state_phys/vz'][:]

    print(f"vx shape: {vx.shape}, vy shape: {vy.shape}, vz shape: {vz.shape}")

    # Compute the velocity magnitude
    magnitude = np.sqrt(vx**2 + vy**2 + vz**2)

    # Plot a 2D slice of the velocity magnitude at a specific slice index (e.g., z = 32)
    slice_index = 32
    plt.imshow(magnitude[:, :, slice_index], cmap='viridis')
    plt.colorbar(label='Velocity Magnitude')
    plt.title(f'Velocity Magnitude Slice at z = {slice_index}')

    output_file = 'iso_tests/velocity_slice.png'
    plt.savefig(output_file)
    print(f"Plot saved to {output_file}")
    plt.close()  # Close the plot after saving to avoid memory issues
