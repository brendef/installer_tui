import shlex
import subprocess

def System(Command):
    Cmds = shlex.split(Command," ")

    Output = "~output~"
    p = subprocess.Popen(
        Cmds,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    Output = p.communicate()

    try:
        Output = Output[0].decode()
    except:
        pass

    return str(Output)

def get_open_ports():
    Status = dict()
    Sl = System("sudo ufw status")[104:].split("\n")

    for S in Sl:
        S2 = S.split()
        try:
            Sport = S2[0].split("/")[0]
        except:
            Sport = ""
        try:
                Sopen = S2[1]
        except:
            Sopen= ""
       
        if not "(v6)" in S and len(Sport)>1:
            if Sopen in ["ALLOW"]:
                Open = 1
            else:
                Open = 0
            Status[Sport] = Open

    return Status

def get_ufw_status():
    return System("sudo ufw status").split()[1]

firewallStatus = get_ufw_status()
def boolean_firewall(status):
    
    if status == 'active':
        return True
    else:
        return False

print(boolean_firewall(firewallStatus))
