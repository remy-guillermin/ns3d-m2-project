import os
import argparse

def create_slurm_script(job_name, time, nodes, ntasks, filename, script, mail):
    if mail != "":
        mail_slurm = f"""
#SBATCH --mail-user={mail}
#SBATCH --mail-type=BEGIN,END,FAIL
        """
    else:
        mail_slurm = ""
        
    content = f"""
#!/bin/bash -l

#SBATCH -J {job_name}
#SBATCH --time={time}
#SBATCH --time-min={time}
#SBATCH --signal=12@300
#SBATCH --nodes={nodes}
#SBATCH --ntasks-per-node={ntasks}
#SBATCH --ntasks={nodes * ntasks}
{mail_slurm}

python {script}
"""
    # Write the content to the specified filename
    with open(filename, 'w') as file:
        file.write(content)
    
    # Make the file executable
    os.chmod(filename, 0o755)
    print(f"SLURM script '{filename}' created and made executable.")

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
        required=True, 
        help="Python script to execute (`velocity_film.py` for example)."
    )

    parser.add_argument(
        "--mail",
        type=str,
        default="",
        help="Mail to send update of the job."
    )
    
    # Parse the arguments
    args = parser.parse_args()

    # Call the function with parsed arguments
    create_slurm_script(
        job_name=args.job_name,
        time="01:00:00",
        nodes=1,
        ntasks=16,
        filename="slurm_script.sh",
        script=args.script,
        mail=args.mail
    )

if __name__ == "__main__":
    main()