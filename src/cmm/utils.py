import subprocess
import logging

logger = logging.getLogger("cmm.utils")

def kill_process_on_port(port: int):
    """
    Kills any process currently listening on the specified port.
    Uses `lsof -ti:<port> | xargs kill -9`.
    """
    try:
        # lsof -ti:<port> returns only the PID of the process using the port.
        # xargs kill -9 sends SIGKILL to those PIDs.
        # We use shell=True to allow the pipe between lsof and xargs.
        cmd = f"lsof -ti:{port} | xargs kill -9"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            logger.info(f"Successfully cleared port {port}.")
        else:
            # lsof returns non-zero if no process is found.
            # We don't treat this as an error.
            logger.debug(f"No process found on port {port} or unable to kill it.")
    except Exception as e:
        logger.error(f"Error while trying to kill process on port {port}: {e}")
