import os
import time
from urllib.request import URLopener
import psutil
import smtplib
import schedule
from sys import *
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

def is_connected():
    try:
        urllib2 =URLopener('http://216.58.192.142',timeout =1)
        return True
    
    except urllib2.URLError as err:
        return False

def Mailsender(filename ,time):
    try:
        fromaddr="sanketlodhe9067@gmail.com"
        toaddr = "lodhesanket666@gmail.com"

        msg = MIMEMultipart()

        msg['From']= fromaddr

        msg['To']= toaddr

        body = """
        HEllo %s,
        Welcome to Flash Desktop.
        Please find atteched document which contains log of running process.
        Log file is created at  : %s

        This is auto generated mail.....
        
        """%(toaddr,time)

        subject ="""
        Flash process log generated at : %s
        """%(time)

        msg['subject']= subject
        msg.attach(MIMEText(body,'plain'))

        attachment =open(filename,"rb")

        p = MIMEBase('application ','octe-stream')

        p.set_payload((attachment).read())
        encoders.encode_base64(p)

        p.add_header('content -Dispostion',"attachment; filename=%s"%filename)

        msg.attach(p)

        s = smtplib.SMTP('smtp.gmail.com',587)

        s.starttls()

        s.login(fromaddr,"ngsafptslxynynux")

        text = msg.as_string()

        s.sendmail(fromaddr,toaddr,text)

        s.quit()

        print("Log file successfully sent thtough mail")

    except Exception as E:
        print("Unable to send mail....",E)




def processLog(log_dir = 'logfile'):
    lists = []

    if not os.path.exists(log_dir):
        try:
            os.mkdir(log_dir)
        except:
            pass
    
    separator = "-"* 80
    log_path = os.path.join(log_dir,"Flashlog%s.log"%(time.ctime()))
    f = open(log_path,"w")
    f.write(separator+"\n")
    f.write("Flash process logger:"+time.ctime()+"\n")
    f.write(separator+"\n")
    f.write("\n")

    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs =["Pid","Name","Username"])
            vms = proc.memory_info().vms/(1024*1024)
            pinfo['vms']= vms
            lists.append(pinfo)
        except (psutil.NOsuchprocess,psutil.AccessDenied,psutil.ZombieProcess):
            pass


    for element in lists:
        f.write("%s\n"%element)

        print("Log file is successfully generated at location %s",(log_path))

    connected = is_connected()

    if connected:
        startTime =time.time()
        Mailsender(log_path,time.ctime())
        endTime = time.time()

        print('Took %s seconds to send mail'%(endTime -startTime))
    else:
        print("There is no internet connections.............")

def main():
    
    #print("Application name is:",argv[0])

    #if len(argv)!=2:
      #  print("error: invalid number of arguments")
      #  exit()


    #if argv[1]=="-h" or argv[1]=="-H":
       # print("this script is used log record of running processess")
       # exit()

    #if argv[1]=="-u" or argv[1]=="-U":
      #  print("usages: application name avsolutepath of directory")
       # exit()

    try:
        schedule.every().minutes.do(processLog)
        while True:
            schedule.run_pending()
            time.sleep(1)

    except ValueError:
        print("Error : Invalid datatypes of input")

    except Exception as e:
        print("Error : Invalid input: ",e)

if __name__=="__main__":
    main()