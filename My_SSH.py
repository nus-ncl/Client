import paramiko
from forward import forward_tunnel
import sys

def port_forwarding(local_port,remote_host,remote_port,ssh_host,ssh_port,ssh_user,private_key_path):
	ssh_key = paramiko.RSAKey.from_private_key_file(private_key_path)
	transport = paramiko.Transport((ssh_host, ssh_port))
	transport.connect(username=ssh_user, pkey=ssh_key)
	try:
		forward_tunnel(local_port, remote_host, remote_port, transport)
	except KeyboardInterrupt:
		print('Port forwarding stopped.')
		sys.exit(0)

def execution_via_ssh_with_key(ssh_host,ssh_port,ssh_user,private_key_path,cmd):
	# use private key
	ssh_key = paramiko.RSAKey.from_private_key_file(private_key_path)
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(ssh_host, ssh_port, ssh_user, pkey=ssh_key)
	stdin, stdout, stderr = ssh.exec_command(cmd)
	print(stdout.read().decode('utf-8'))
	ssh.close()

def execution_via_ssh_with_password(ssh_host,ssh_port,ssh_user,private_key_path,cmd):
	# use login password
	ssh_key = paramiko.RSAKey.from_private_key_file(private_key_path)
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(ssh_host, ssh_port, ssh_user, password=ssh_key)
	stdin, stdout, stderr = ssh.exec_command(cmd)
	print(stdout.read().decode('utf-8'))
	ssh.close()

def ssh_upload(local_file_abs_path,remote_file_abs_path,remote_host,remote_port,remote_user,private_key_path):
	# upload
	ssh_key = paramiko.RSAKey.from_private_key_file(private_key_path)
	transfer = paramiko.Transport((remote_host, remote_port))
	transfer.connect(username=remote_user, pkey=ssh_key)
	sftp = paramiko.SFTPClient.from_transport(transfer)
	sftp.put(local_file_abs_path,remote_file_abs_path)
	transfer.close()

def ssh_download(local_file_abs_path,remote_file_abs_path,remote_host,remote_port,remote_user,private_key_path):
	# download
	ssh_key = paramiko.RSAKey.from_private_key_file(private_key_path)
	transfer = paramiko.Transport((remote_host, remote_port))
	transfer.connect(username=remote_user, pkey=ssh_key)
	sftp = paramiko.SFTPClient.from_transport(transfer)
	sftp.get(remote_file_abs_path,local_file_abs_path)
	transfer.close()

if __name__ == '__main__':
	pass




