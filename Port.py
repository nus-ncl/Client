import socket

def is_port_used(ip, port):
	"""
	check whether the port is used by other program

	:param ip:
	:param port:
	:return: True(in use) False(idle)
	"""
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect((ip, port))
		return True
	except OSError:
		return False
	finally:
		s.close()


if __name__ == '__main__':
	port = 12345
	while (is_port_used('127.0.0.1', port)):
		port += 1
	print(port)
