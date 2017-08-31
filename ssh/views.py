from django.http.response import StreamingHttpResponse
from django.shortcuts import render
import paramiko


def run(komut):
	l_password = "111111"
	l_host = "localhost"
	l_user = "kandalf"
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(l_host, username=l_user, password=l_password)    
	transport = ssh.get_transport()
	session = transport.open_session()
	session.set_combine_stderr(True)
	session.get_pty()
	session.exec_command(komut)
	stdout = session.makefile('r', -1)
	stdin.write(l_password +'\n')
	stdin.flush()
	for line in iter(stdout.readline,""): 
		yield line
	ssh.close()	

def sudo(komut):
	l_password = "111111"
	l_host = "localhost"
	l_user = "kandalf"
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(l_host, username=l_user, password=l_password)    
	transport = ssh.get_transport()
	session = transport.open_session()
	session.set_combine_stderr(True)
	session.get_pty()
	session.exec_command("sudo " + komut)
	stdin = session.makefile('w', -1)
	stdout = session.makefile('r', -1)
	stdin.write(l_password +'\n')
	stdin.flush()
	for line in iter(stdout.readline,""): 
		if l_password in line or "[sudo] password for" in line:
			pass
		else:
			yield line
	ssh.close()


def test_stream(request, komut):
    stream = sudo(komut)
    response = StreamingHttpResponse(stream, status=200, content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    return response


def home(request):
    return render(request, 'index.html')
