'''
let python script as linux daemon
for more use sample, see the bottom of code
'''

import os, sys, time, signal, atexit, pwd

class Daemon:
   def __init__(self, dirname, pidfile, dname="theservice", stderr='/dev/null', stdout='/dev/null'):
      self.workdir= dirname #os.path.abspath(".")
      self.pidfile=pidfile
      self.stdout=stdout
      self.stderr=stderr
      self.dname=dname

   def goDaemonMode(self):
      # First fork
      try:
         pid=os.fork()
         if pid > 0:
            sys.exit(0)
      except OSError, e:
         sys.exit("First fork failed. Info: %d (%s) \n" % (e.errno, e.strerror))
         
      # Decouple from parent environment
      os.chdir("/") #change work directory to /
      os.setsid()   #exit terminal
      os.umask(033) #set permission
      
      # Second fork
      try:
         pid=os.fork()
         if pid > 0:
            sys.exit(0)            
      except OSError, e:
         sys.exit("Second fork failed. Info: %d (%s)\n" % (e.errno, e.strerror))
      
      os.setgid(int(pwd.getpwnam("www-data")[3]))
      os.setuid(int(pwd.getpwnam("www-data")[2]))
      # flush the stdio buffers
      sys.stdout.flush()
      sys.stderr.flush()
      
      # Redirect standard file descriptors
      fstdout=open(self.stdout, "a+")
      fstderr=open(self.stderr, "a+", 0)
      fstdin=open('/dev/null', "r")
      os.close(sys.stdin.fileno())
      os.close(sys.stdout.fileno())
      os.close(sys.stderr.fileno())
      os.dup2(fstdout.fileno(), sys.stdout.fileno())
      os.dup2(fstderr.fileno(), sys.stderr.fileno())
      os.dup2(fstdin.fileno(), sys.stdin.fileno())
      
      atexit.register(self.doClean)
      open(self.pidfile, "w+").write("%s\n" % str(os.getpid()))
      
   def doClean(self):
      if os.path.exists(self.pidfile+"s"):
         os.remove(self.pidfile+"s")
      if os.path.exists(self.pidfile):
         os.remove(self.pidfile)

   def getPid(self):
      try:
         pfile=open(self.pidfile, "r")
         pid=int(pfile.read().strip())
         pfile.close()
      except IOError:
         pid=None        
      return pid     
  
   def start(self):
      pid=self.getPid()   
      if pid:
         sys.exit("csvtaskAgent is already running.\n")
         
      self.goDaemonMode()
      self.main()
      
   def startNotDaemon(self):     
      pid=self.getPid() 
      if pid:
         sys.exit("csvtaskAgent is already running.\n")

      open(self.pidfile, "w+").write("%s\n" % str(os.getpid())) 
      self.main()      
      
   def stop(self):
      pid=self.getPid()
      if not pid:
         sys.exit("csvtaskAgent is not running.\n")
      
      try:
         while 1:
            os.kill(pid, signal.SIGTERM)
            sys.stdout.write("*")
            sys.stdout.flush()
            time.sleep(1)
      except OSError, e:
         err=str(e)
         if err.find("No such process") > 0:
            if os.path.exists(self.pidfile):
               os.remove(self.pidfile)
            sys.stdout.write(" [OK]\n")


   def stop_force(self):
      pid=self.getPid()      
      if not pid:
         sys.exit(self.dname+" is not running.\n")
      
      try:        
         if os.path.exists(self.pidfile+"s"):
            self.killAllChildProcess(9)  
      except OSError, e:       
         err=str(e)
         if err.find("No such process") > 0:
            if os.path.exists(self.pidfile):
               os.remove(self.pidfile)
            sys.stdout.write(" [OK]\n")
               
   def restart(self):
      self.stop()
      self.start()
      
   def status(self):
      pid=self.getPid()
      if not pid:
         sys.stderr.write("Status: "+self.dname+" is not running!\n")
         sys.exit(1)
      else:
         sys.stderr.write("Status: "+self.dname+" is running!\n")
         sys.exit(1)
      sys.exit(0) 

   def main(self):
      pass

'''
class sampleClass(Daemon):
   def function(self):
      implementation
      ....
      ....

if __name__ == "__main__":
   daemon = sampleClass('/path/work/dir','/path/pid/file', 'app')  
   if len(sys.argv) == 2:
      if 'start' == sys.argv[1]:
         daemon.start()
      elif 'start_fg' == sys.argv[1]:
         daemon.startNotDaemon()
      elif 'stop' == sys.argv[1]:
         daemon.stop() 
      elif 'restart' == sys.argv[1]:
         daemon.restart()
      elif 'status' == sys.argv[1]:
         daemon.status()
      elif '-h' == sys.argv[1] or '--help' == sys.argv[1]:
         print "usage: %s start|stop|restart|status|start_fg" % sys.argv[0]
      else:
         print "Use -h or --help to print usage."
         sys.exit(2)
      sys.exit(0)
      
   else:
      print "usage: %s start|stop|restart|status|start_fg" % sys.argv[0]
      sys.exit(2)
'''