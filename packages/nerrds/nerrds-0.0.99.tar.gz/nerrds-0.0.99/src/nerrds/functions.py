


def check_quiet_print(quiet,job_dir,msg,end='\n'):
    out = open(job_dir+'/NERRDS.log','a+')
    out.write(msg+end)
    out.close()
    if not quiet:
        print(msg,end=end)
