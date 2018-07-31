from cmd import Cmd
import os
import sys
import importlib
import subprocess

#importlib.reload(sys)
#sys.setdefaultencoding('utf-8')


#print(res)
class cmd_api():
    def setprophoto(self):
        order='php /www/wwwroot/insphp/examples/setprophoto.php'
        p = subprocess.Popen(order,shell=True,stdout=subprocess.PIPE)
        out, err = p.communicate()
        for line in out.splitlines():
            print(line)
        return out.splitlines()[-1]

    def loadphoto(self):
        order='php /www/wwwroot/insphp/examples/loadPhoto.php'
        p = subprocess.Popen(order,shell=True,stdout=subprocess.PIPE)
        out, err = p.communicate()
        for line in out.splitlines():
            print(line)
        return out.splitlines()[-1]

    def peoplelf(self):
        order='php /www/wwwroot/insphp/examples/lpeoplelf.php'
        p = subprocess.Popen(order,shell=True,stdout=subprocess.PIPE)
        out, err = p.communicate()
        for line in out.splitlines():
            print(line)
        return out.splitlines()[-1]

#order='php C:\ProgramPro\phpStudy\WWW\iam\examples\setprophoto.php'
#order='php C:\ProgramPro\phpStudy\WWW\iam\examples\peoplelf.php'