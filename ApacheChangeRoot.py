#coding : utf -8
  
import os,sys,subprocess,random,time,glob
from os import system

if sys.platform=="linux1" or sys.platform=="linux2" or sys.platform=="linux":
    system("source /etc/apache2/envvars")
cwd=os.path.dirname(os.path.abspath(__file__))
os.chdir(cwd)

class Fore:
    GREEN="\u001b[32;1m"
    BLUE="\u001b[34;1m"
    YELLOW="\u001b[33;1m"
    RED="\u001b[31;1m"
    RESET="\u001b[0m"
      
def dependencies():
    if sys.version_info[0] < 3:
        raise Exception("Must be using Python 3")
    if sys.platform!="linux1" and sys.platform!="linux2" and sys.platform!="linux":
        print(Fore.RED + "\nSorry, this script is only available for linux :(")
        sys.exit(0)
        
    system("clear")
    
    if os.getuid() != 0:
        print(Fore.RED + "\tSorry, you have to run this as root :(" + Fore.RESET)
        sys.exit(0)
       
       
    null=open(os.devnull,"w")
    package="apache2"
    retval = subprocess.call(["dpkg","-s",package],stdout=null,stderr=subprocess.STDOUT)
    null.close()
    if retval != 0:
        print(Fore.RED + "\tApache2 is not installed :( Install it before launching the script !")
        sys.exit(0)
     
def banner():
    print(Fore.GREEN + "\tWelcome to my program, allowing you to change apache2 root (LINUX ONLY) ! enjoy")
    print(Fore.RED + "\n\t\tMade by <3 by DiamondLink (bibivilleneuve11@gmail.com)")
    print(Fore.BLUE + "\n\n\t\t\t[PRESS ENTER TO CONTINUE]")
    print(Fore.GREEN + "\n\n\n\nDonate :(my monero/xmr adress) : 49KHKsubi9dWyysLYVo8oNS82iKMbtXc4axhWAi7bkPadQbF9BUN5e4FeHtgSH7gv9dBHEqZibswED7etoBreBLFTEAQWyu" + Fore.RESET)
    input("")
    
def askForSettings():
    
    global newDir,newSiteName,purgeSites,reset,siteName
    
    purgeSites=""
    while purgeSites.lower()!="y" and purgeSites.lower()!="n":
        system("clear")
        print(Fore.YELLOW + "Do you want to delete already existing available sites ? (Y/N)")
        purgeSites=input("\n>>> ")

    continuer=""
    newDir=""
    while continuer.lower()!="y":
        system("clear")
        print(Fore.GREEN + "Enter new apache2 root path :")
        newDir=input(Fore.YELLOW + "\n\n>>> ")

        if os.path.exists(newDir)==False:
            continuer=""
            while continuer.lower()!="y" and continuer.lower()!="n":
                os.system("clear")
                print(Fore.RED + "\tWarning ! The choosed path doesn't exist !\n\tDo you still want to continue ? (Y/N)")
                continuer=input(Fore.YELLOW + ">>> ")
        else:
            continuer="y"
            
    reset=""
    while reset.lower()!="y" and reset.lower()!="n":
        system("clear")
        print(Fore.YELLOW + "Do you want to reset apache configuration files ? (Y/N)")
        reset=input("\n>>> ")
        
    siteName=""
    alreadyExistingSite=""
    continuer=True
    while alreadyExistingSite.lower()!="y" and alreadyExistingSite.lower()!="n":
        system("clear")
        print(Fore.YELLOW + "Do you want to use an already existing site ? (Y/N)")
        alreadyExistingSite=input("\n>>> ")
    if alreadyExistingSite=="y":
        while continuer==True:
            system("clear")
            print(Fore.YELLOW + "Site name (press enter for default) :")
            siteName=input("\n>>> ")
            
            if siteName=="":
                siteName="/etc/apache2/sites-available/000-default.conf"
                continuer=False
            elif os.path.exists("/etc/apache2/sites-available/" + siteName + ".conf")==False:
                system("clear")
                print(Fore.RED + "\n\tThe specified site doesn't exist [PRESS ENTER]")
                input("")
            else:
                continuer=False
                siteName="/etc/apache2/sites-available/" + siteName + ".conf"
                newSiteName="/etc/apache2/sites-available/" + siteName + ".conf"
    if siteName=="/etc/apache2/sites-available/000-default.conf" or alreadyExistingSite=="n":
        system("clear")
        print(Fore.YELLOW + "Specify new site name :")
        newSiteName=input("\n>>> ")
            
    
def purge_sites(dir1="/etc/apache2/sites-available",dir2="/etc/apache2/sites-enabled"):
    os.chdir(dir1)
    for i in range(2):
        files = glob.glob("*")
        for el in files:
            if el!="000-default.conf":
                os.remove(el)
        os.chdir(dir2) 
        
def manageApacheSites(sitesToEnable,sitesToDisable="all",verbose=False):
    
    if not isinstance(sitesToEnable,list):
        raise TypeError("siteToEnable must be a list")
    if not isinstance(sitesToDisable,list) and sitesToDisable!="all":
        raise TypeError("siteToDisable must be a list")
    
    system("clear")
    
    os.chdir("/etc/apache2/sites-available")
    null=open(os.devnull,"w")
    
    print(Fore.GREEN)
    
    if sitesToDisable=="all":
        if verbose==True:
            print("\nDisabling all enabled sites...")
        output=subprocess.call("a2dissite *",shell=True,stdout=null,stderr=null)    
    else:
        for el in sitesToDisable:
            if verbose==True:
                print("Site " + el + " disabled")
            output=subprocess.call("a2dissite " + el,shell=True,stdout=null,stderr=null) 
            time.sleep(0.2)
            
    time.sleep(1)
                
    for el in sitesToEnable:
        if verbose==True:
            print("Site " + el + " enabled")
        output=subprocess.call("a2ensite " + el,shell=True,stdout=null,stderr=null)
            
    time.sleep(1)
    
    if verbose==True:
        print("Restarting apache2 server...")
    output=subprocess.call("systemctl restart apache2",shell=True,stdout=null,stderr=null)
    time.sleep(0.2)
    
    if verbose==True:
        print("\nDone ! apache2 root has been successfully changed !\n" + Fore.RESET)
    
    null.close()

class newRoot:
    def __init__(self,newDirectory,site="default_site.conf",apachepath="apache2.conf"):

        os.chdir(cwd)
        #GETTING NEW CONFIG FILE FOR SITE
        with open(site,"r") as default:
            self.siteConfigFile=""
            for count,line in enumerate(default):
                if "DocumentRoot" in line:
                    self.siteConfigFile+="\n\tDocumentRoot " + newDirectory
                else:
                    self.siteConfigFile+=line
                    
        #GETTING APACHE ADDS TO CONF
        with open("defaultconf.conf","r") as deconf:
            self.apacheAdds=""
            for count,line in enumerate(deconf):
                if "NEWDIR" in line:
                    self.apacheAdds+=line.replace("NEWDIR",newDirectory)
                else:
                    self.apacheAdds+="\n" + line
        
        #GETTING APACHE CONF
        with open(apachepath,"r") as conf:
            self.newApacheConf=""
            first=True
            for count,line in enumerate(conf):
                if "</Directory>" in line:
                    if first==True:
                        self.newApacheConf+="\n" + line + "\n"
                        self.newApacheConf+=self.apacheAdds
                        first=False
                    else:
                        self.newApacheConf+="\n" + line
                else:
                    self.newApacheConf+=line
                    
    def setSiteFile(self,name,dir="/etc/apache2/sites-available/"):
        with open(dir + name + ".conf","w") as File:
            File.write(self.siteConfigFile)
    
    def setApacheConf(self,dir="/etc/apache2"):
        os.chdir(dir)
        os.remove("apache2.conf")
        
        with open("apache2.conf","w") as apache2conf:
            apache2conf.write(self.newApacheConf)
            
    def setNewApacheRoot(self,siteName):
        self.setSiteFile(siteName)
        self.setApacheConf()

if __name__=="__main__":
    dependencies()
    banner()
    askForSettings()
    
    if purgeSites=="y":
        purge_sites()
        
    if reset=="y":
        apacheConfPath="apache2.conf"
    else:
        apacheconfPath="/etc/apache2/apache2.conf"
        
    if siteName=="":
        customRoot=newRoot(newDir,apachepath=apacheConfPath)
    else:
        customRoot=newRoot(newDir,site=siteName,apachepath=apacheConfPath)
    
    customRoot.setSiteFile(newSiteName)
    customRoot.setApacheConf()
    
    newSiteName = newSiteName.split(None)
    manageApacheSites(sitesToEnable=newSiteName,verbose=True)
    
    print(Fore.RESET)
    

