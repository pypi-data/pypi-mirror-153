import sys
import os
import subprocess
import paramiko
from scp import SCPClient
import logging

def run_cmd_on_host(host, cmdarr, encoding):
    if host and host['remote']:
        pkgout = run_remote_ssh_command(host, cmdarr[0])
        if pkgout is None:
            return None
    else:
        try:
            dev_null_device = open(os.devnull, "w")
            pkgout = subprocess.check_output(cmdarr, stderr=dev_null_device, shell=True)
            pkgout = pkgout.decode(encoding)
            dev_null_device.close()
        except subprocess.CalledProcessError:
            logging.error("Error running command [%s]" % cmdarr[0])
            return None
    return pkgout.strip()

def get_ssh_client(host):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy)
    if host.get('userpwd') is not None and len(host['userpwd']) > 0 and (host.get('privatekey') is None or len(host['privatekey'])==0):
        client.connect(host['hostname'],username=host['userlogin'],password=host['userpwd'])
    elif host.get('privatekey') is not None and len(host['privatekey']) > 0:
        if host.get('userpwd') is not None and len(host['userpwd']) > 0:
            client.connect(host['hostname'],username=host['userlogin'],key_filename=host['privatekey'],passphrase=host['userpwd'])
        else:
            client.connect(host['hostname'],username=host['userlogin'],key_filename=host['privatekey'])
    else:
        client.connect(host['hostname'],username=host['userlogin'])
    return client

def run_remote_ssh_command(host, command):
    assetid = host['assetid'] if host.get('assetid') is not None else host['hostname']
    output = ''
    try:
        client = get_ssh_client(host)
        stdin, stdout, stderr = client.exec_command(command)
        for line in stdout:
            output = output + line
        client.close()
    except paramiko.ssh_exception.AuthenticationException as e:
        logging.info("Authentication failed for asset [%s], host [%s]", assetid, host['hostname'])
        logging.info("Exception: %s", e)
        output = None
    except paramiko.ssh_exception.SSHException as e:
        logging.info("SSHException while connecting to asset [%s], host [%s]", assetid, host['hostname'])
        logging.info("Exception: %s", e)
        output = None
    except socket.error as e:
        logging.info("Socket error while connection to asset [%s], host [%s]", assetid, host['hostname'])
        logging.info("Exception: %s", e)
        output = None
    except:
        logging.info("Unknown error running remote discovery for asset [%s], host [%s]: [%s]", assetid, host['hostname'], sys.exc_info()[0])
        output = None
    finally:
        return output

def scp_put_file(host, from_path, to_path):
    _scp_file_helper(host, from_path, to_path, True)

def scp_get_file(host, from_path, to_path):
    _scp_file_helper(host, from_path, to_path, False)

# Default mode is to put the file to remote host. If you want to get file from remote host, then setput_flag to False
def _scp_file_helper(host, from_path, to_path, put_flag=True):
    assetid = host['assetid'] if host.get('assetid') is not None else host['hostname']
    ret = False
    try:
        ssh_client = get_ssh_client(host)
        scp_client = SCPClient(ssh_client.get_transport())
        if put_flag == True: # put file to remote machine
            scp_client.put(from_path, recursive=True, remote_path=to_path)
        else:
            scp_client.get(from_path, to_path)
        scp_client.close()
        ssh_client.close()
        ret = True
    except paramiko.ssh_exception.AuthenticationException as e:
        logging.info("Authentication failed for asset [%s], host [%s]", assetid, host['hostname'])
        logging.info("Exception: %s", e)
    except paramiko.ssh_exception.SSHException as e:
        logging.info("SSHException while connecting to asset [%s], host [%s]", assetid, host['hostname'])
        logging.info("Exception: %s", e)
    except socket.error as e:
        logging.info("Socket error while connection to asset [%s], host [%s]", assetid, host['hostname'])
        logging.info("Exception: %s", e)
    except:
        logging.info("Unknown error running remote discovery for asset [%s], host [%s]: [%s]", assetid, host['hostname'], sys.exc_info()[0])
    finally:
        return ret
