import subprocess
import logging


__version__= "$Id: kill_process_by_name.py 25 2018-01-26 19:00:40Z lbusoni $"


def killProcessByName(processName):
    proc= subprocess.Popen("pgrep -f %s" % processName,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           shell=True)

    pgrepPID= proc.pid
    pids= []
    for each in proc.stdout:
        if int(each) == pgrepPID:
            logging.debug("Skipping pgrep proc with PID %d" % (
                pgrepPID))
            continue
        logging.debug("%s with PID %s" % (processName, each))
        pids.append(int(each))

    logging.info("number of processes '%s': %d" % (processName, len(pids)))
    for each in pids:
        cmd= "kill -KILL %d" % each
        logging.debug("Executing %s" % cmd)
        exitCode= subprocess.call(cmd, shell=True)
        assert exitCode == 0, "Terminating %s with PID %d" % (
            processName, each)
