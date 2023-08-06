import time
import paramiko


def ssh_connect(hostname: str, username: str, password: str) -> paramiko.SSHClient:
    """return connected ssh

    Args:
        hostname (str): address of host
        username (str): username to login
        password (str): password to login

    Returns:
        ssh (paramiko.SSHClient): connected ssh client
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, port=22, username=username, password=password)
    return ssh


def command(ssh: paramiko.SSHClient, query: str, timeout = None):
    """execute shell command

    Args:
        ssh (paramiko.SSHClient): paramiko ssh client
        query (str): shell command

    Returns:
        tuple[str, str]: stdout, stderr
    """
    
    stdin, stdout, stderr = ssh.exec_command(query, timeout=timeout)
    
    if timeout:
        start_time = time.time()
    
    # Wait for the command to terminate  
    while not stdout.channel.exit_status_ready():
        time.sleep(1)
        if timeout:
            latest_time = time.time()

            if latest_time - start_time > timeout:
                stdout_text = stdout.read().decode('utf-8').strip()
                err_text = stderr.read().decode('utf-8').strip()
                return stdout_text, err_text
    
    stdout_text = stdout.read().decode('utf-8').strip()
    err_text = stderr.read().decode('utf-8').strip()
    return stdout_text, err_text


def execute_sql_query(ssh: paramiko.SSHClient, user_id: str, user_pw: str, db_name: str, query: str):
    """execute sql query

    Args:
        ssh (paramiko.SSHClient): paramiko ssh client.
        user_id (str): ID to log in.
        user_pw (str): Password to log in.
        db_name (str): Name of the database to be connected to.
        query (str): query statement to execute.

    Returns:
        tuple[str, str]: stdout, stderr
    """    
    query = query.replace('\'','\"')
    fquery = f"""mysql -u{user_id} -p{user_pw} {db_name} -e '{query}'"""
    return command(ssh, fquery)
