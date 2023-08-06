


def check_quiet_print(quiet,home_dir,msg,end='\n'):
    out = open(home_dir+'/NERRDS.log','a+')
    out.write(msg+end)
    out.close()
    if not quiet:
        print(msg,end=end)
