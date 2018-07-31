import subprocess
from time import sleep
from fcntl import fcntl, F_GETFL, F_SETFL
from os import O_NONBLOCK, read


# importlib.reload(sys)
# sys.setdefaultencoding('utf-8')


# print(res)
def setprophoto():
    order = 'php /www/wwwroot/insphp/examples/setprophoto.php'
    p = subprocess.Popen(order, shell=True, stdout=subprocess.PIPE)
    out, err = p.communicate()
    for line in out.splitlines():
        print(line)
    return out.splitlines()[-1]


def loadphoto():
    order = 'php /www/wwwroot/insphp/examples/loadPhoto.php'
    p = subprocess.Popen(order, shell=True, stdout=subprocess.PIPE)
    out, err = p.communicate()
    for line in out.splitlines():
        print(line)
    return out.splitlines()[-1]


def intfollow():
    order = 'php /www/wwwroot/insphp/examples/peoplefollow.php'
    p = subprocess.Popen(order, shell=True, stdout=subprocess.PIPE)
    out, err = p.communicate()
    for line in out.splitlines():
        print(line)
    return out.splitlines()[-1]


def loginphone():
    order = 'php /www/wwwroot/insphp/examples/peopleself.php'
    p = subprocess.Popen(order, shell=True, stdout=subprocess.PIPE)
    out, err = p.communicate()
    for line in out.splitlines():
        print(line)
    return out.splitlines()[-1]


def getshopfollower():
    order = ['php', '/www/wwwroot/insphp/examples/peoplelf.php']
    p = subprocess.Popen(order, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    out, err = p.communicate()
    for line in out.splitlines():
        print(line)
    return out.splitlines()[-1]


# order='php C:\ProgramPro\phpStudy\WWW\iam\examples\setprophoto.php'
# order='php C:\ProgramPro\phpStudy\WWW\iam\examples\peoplelf.php'
