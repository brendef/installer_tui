
import paramiko
key = paramiko.RSAKey.from_private_key_file("/home/brendan/Documents/technocorecpt.pem")
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect( hostname = "brendan.technocore.co.za", username = "admin", pkey = key )
commands = [ "cd /home/admin", "mkdir testfile" ]
for command in commands:
	print ("Executing {}".format( command ))
	stdin , stdout, stderr = c.exec_command(command)
	print (stdout.read())
	print ("Errors")
	print (stderr.read())
c.close()