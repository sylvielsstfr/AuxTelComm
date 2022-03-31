# README.md


## to lauch a batch

        sbatch script.sh

## to make interactive batch


        srun -p htc_interactive -n 8 --pty bash -i




## few batch commands


       squeue

       scontrol show job <jobid>
    
       scancel <jobid>


       sacct -j <jobid>
