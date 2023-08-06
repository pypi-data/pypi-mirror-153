from adarsh.follow_bot import spotify
import threading, os, time

lock = threading.Lock()
counter = 0
proxies = []
proxy_counter = 0

print("""
███████╗██████╗  ██████╗ ████████╗██╗███████╗██╗   ██╗              
██╔════╝██╔══██╗██╔═══██╗╚══██╔══╝██║██╔════╝╚██╗ ██╔╝              
███████╗██████╔╝██║   ██║   ██║   ██║█████╗   ╚████╔╝               
╚════██║██╔═══╝ ██║   ██║   ██║   ██║██╔══╝    ╚██╔╝                
███████║██║     ╚██████╔╝   ██║   ██║██║        ██║                 
╚══════╝╚═╝      ╚═════╝    ╚═╝   ╚═╝╚═╝        ╚═╝                 
                                                                    
███████╗ ██████╗ ██╗     ██╗      ██████╗ ██╗    ██╗███████╗██████╗ 
██╔════╝██╔═══██╗██║     ██║     ██╔═══██╗██║    ██║██╔════╝██╔══██╗
█████╗  ██║   ██║██║     ██║     ██║   ██║██║ █╗ ██║█████╗  ██████╔╝
██╔══╝  ██║   ██║██║     ██║     ██║   ██║██║███╗██║██╔══╝  ██╔══██╗
██║     ╚██████╔╝███████╗███████╗╚██████╔╝╚███╔███╔╝███████╗██║  ██║
╚═╝      ╚═════╝ ╚══════╝╚══════╝ ╚═════╝  ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝
                                                                    
██████╗  ██████╗  ██████╗ ███████╗████████╗███████╗██████╗          
██╔══██╗██╔═══██╗██╔═══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗         
██████╔╝██║   ██║██║   ██║███████╗   ██║   █████╗  ██████╔╝         
██╔══██╗██║   ██║██║   ██║╚════██║   ██║   ██╔══╝  ██╔══██╗         
██████╔╝╚██████╔╝╚██████╔╝███████║   ██║   ███████╗██║  ██║         
╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝         
                                                                    

\n\nCoded By Adarsh Goel  (https://github.com/adarsh-goel)  """)
spotify_profile = input("enter username on which you want to increase followers or provide link to the profile\n>> ")
threads = int(input("Enter Desired Speed (we recommend 15)\n>> "))
print(f"Running At {threads}X Speed")



def safe_print(arg):
    lock.acquire()
    print(arg)
    lock.release()

def thread_starter():
    global counter
    obj = spotify(spotify_profile)
    result, error = obj.follow()
    if result == True:
        counter += 1
        safe_print("Followed {}".format(counter))
    else:
        safe_print(f"Error {error}")

while True:
    if threading.active_count() <= threads:
        try:
            threading.Thread(target = thread_starter).start()
            proxy_counter += 1
        except:
            pass
