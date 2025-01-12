#!/usr/bin/env python3

import os
import argparse
import subprocess
import datetime

def create_slurm_script(job_name, time, nodes, ntasks, filename, script):
    content = f"""#!/bin/bash -l
#SBATCH -J {job_name}
#SBATCH --time={time}
#SBATCH --time-min={time}
#SBATCH --signal=12@300
#SBATCH --nodes={nodes}
#SBATCH --ntasks-per-node={ntasks}
#SBATCH --ntasks={nodes * ntasks}
#SBATCH --output=slurm-%j.out
#SBATCH --error=slurm-%j.err

conda activate env-fluidsim-mpi
python {script}


"""
    # Write the content to the specified filename
    with open(filename, 'w') as file:
        file.write(content)

    # Make the file executable
    os.chmod(filename, 0o755)
    print(f"SLURM script '{filename}' created and made executable.")

def submit_slurm_script(filename):
    # Submit the SLURM script using sbatch
    try:
        result = subprocess.run(["sbatch", filename], capture_output=True, text=True, check=True)
        print(f"Job submitted successfully. SLURM output:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while submitting the job:\n{e.stderr}")

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description="Generate a SLURM script.")

    parser.add_argument(
        "--job-name",
        type=str,
        default="figures",
        help="Name of the SLURM job."
    )

    parser.add_argument(
        "--script",
        type=str,
        default="velocity_film.py",
        help="Python script to execute (`velocity_film.py` for example)."
    )

    # Parse the arguments
    args = parser.parse_args()

    now = datetime.datetime.now()
    date_time_str = now.strftime("%Y-%m-%d_%H-%M")

    # SLURM script filename
    filename = f"launcher_{args.job_name}_{date_time_str}.sh"

    # Call the function with parsed arguments
    create_slurm_script(
        job_name=args.job_name,
        time="01:00:00",
        nodes=1,
        ntasks=16,
        filename=filename,
        script=args.script,
    )

    # Manual confirmation before submission
    confirm = input(f"""
A launcher for the command "python {args.script}" has been created.
Should the command "sbatch {filename}" be run ? [y/N]
""").strip().lower()
    if confirm in ['yes', 'y']:
        submit_slurm_script(filename)
    else:
        print("Submission aborted by user.")

if __name__ == "__main__":
    main()
