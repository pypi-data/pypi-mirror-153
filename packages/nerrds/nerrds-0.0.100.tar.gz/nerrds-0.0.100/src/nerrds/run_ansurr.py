import os
import glob
import shutil

from ansurr import ansurr
from nerrds.functions import check_quiet_print

def run_ansurr(home_dir, job_id, pdb_id, path_to_shifts,quiet=False):

    check_quiet_print(quiet,home_dir+'/'+job_id,"running ANSURR")
    ansurr_dir = home_dir+"/"+job_id+"/ansurr/"
    os.makedirs(ansurr_dir,exist_ok=True)
    os.chdir(ansurr_dir)
    ansurr.main("-p "+home_dir+"/"+job_id+"/refined/anm_"+pdb_id+"_refined.pdb"+" -s "+path_to_shifts+" -r -q")

    ansurr_output = len(glob.glob(home_dir+"/"+job_id+"/ansurr/anm*/ANSURR_output/out/*.out"))

    # check ansurr success
    if ansurr_output > 0:
        check_quiet_print(quiet,home_dir+'/'+job_id,"ANSURR ran for "+str(ansurr_output)+" models")
    else:
        check_quiet_print(quiet,home_dir+'/'+job_id,"ERROR ANSURR failed to run for any models, quitting")
        sys.exit(0)

    to_remove = glob.glob(home_dir+"/"+job_id+"/ansurr/anm*/other_output/*")
    for t in to_remove:
        shutil.rmtree(t)

    to_remove = glob.glob(home_dir+"/"+job_id+"/ansurr/anm*/ANSURR_output/figs/*")
    for t in to_remove:
        shutil.rmtree(t)

if __name__ == "__main__":
    import sys
    home_dir = sys.argv[1]
    job_id = sys.argv[2]
    pdb_id = sys.argv[3]
    path_to_shifts = sys.argv[4]
    run_ansurr(home_dir, job_id, pdb_id, path_to_shifts)

