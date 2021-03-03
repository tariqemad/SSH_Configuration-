import sys
import datetime
import netmiko
from netmiko import ConnectHandler


username = "**********"
password = "**********"
Time = datetime.datetime.now().strftime("%d.%b %Y %H:%M:%S")

IP_file = open("IP", 'r')
for each_line in IP_file.readlines():
    each_line = each_line.strip("\n")
    try:
        session = ConnectHandler(device_type='cisco_ios', ip=each_line, username=username, password=password)
        config = session.send_config_from_file("script")    # For send config command
        save = session.save_config()
        show = session.send_command("sh ru | section ^hostname")  # for show command
        arr = show.split()  ## if i want to splite the sentance to elimints and chose the need word
        Done = (arr[1] + " " + "---->" + " " + str(each_line) + "  " + "---->" + "  " + "Operation Done & Saved" + " " + "At" + " " + Time + "\n" + "-----------------------------" + "\n")
        output_file = open("log", "a")
        output_file.write(Done)
        session.disconnect()

    except netmiko.ssh_exception.NetMikoTimeoutException:
        ssh_timeout = (str(each_line) + " " + "---->" + " " + "SSH timeout!!!" + " " + "At" + " " + Time + "\n" + "-----------------------------" + "\n")  # Variable using it to write the ip that is timeout to file name "timeout"
        print(ssh_timeout)
        timeout_file = open("log", "a")    ### To save the IP's timeout into timeoutfile
        timeout_file.write(ssh_timeout)
        pass

    except netmiko.ssh_exception.NetMikoAuthenticationException:
        wrong_authentication = (str(each_line) + " " + "---->" + " " + "Wrong Authentication !!!" + " " + "At" + " " + Time + "\n" + "-----------------------------" + "\n")    # Variable using it to write the ip that is Wrong Authentication to file name " Wrong Authenticationt"
        print(wrong_authentication)
        output_file = open("log", "a")
        output_file.write(wrong_authentication)


    except:
        print(sys.exc_info())
        pass

#print("====== Operation Done ======== ")
sys.exit()   # To exit from Code
