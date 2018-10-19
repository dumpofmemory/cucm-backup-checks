from getpass import getpass
import paramiko
from paramiko_expect import SSHClientInteraction
import time
import codecs  # converts type 'unicode'
import regex
import datetime
# import traceback
import socket


def main():

    # CREDENTIALS
    # username = 'administrator'
    # password = 'ciscopsdt'
    username = raw_input("Staff ID: ")
    password = getpass("Password: ")

    ######################################
    ### All to_text_file functionality ###
    ######################################

    def write_date():
        now = datetime.datetime.now()
        current_date = '\n\n>> CURRENT DATE: ' + now.strftime("%Y-%m-%d %H:%M:%S")
        output_file = codecs.open('out.txt', 'a', 'utf8')
        output_file.write(current_date)
        output_file.close()
        return

    def write_host(h):
        print "\n>> ATTEMPTING SSH TO %s" % host
        output_file = codecs.open('out.txt', 'a', 'utf8')
        output_file.write(h)
        output_file.close()
        return

    def write_conn_err(error):
        output_file = codecs.open('out.txt', 'a', 'utf8')
        output_file.write("Exception in connecting to the server: ")
        output_file.write(error)
        output_file.close()
        return

    def cli_output_to_text_file():
        data = interact.current_output  # program saves output of utils command to the "data" variable
        output_file = codecs.open('out.txt', 'a', 'utf8')
        output_file.write(data)
        output_file.close()
        print("\nWriting complete")
        return

    def write(any):
        output_file = codecs.open('out.txt', 'a', 'utf8')
        output_file.write(any)
        output_file.close()


    ###############################################
    ### Define and establish SSH client session ###
    ###############################################
    def set_ssh_conn():
        # Create instance of SSHClient object
        ssh = paramiko.SSHClient()
        # Automatically add untrusted hosts (make sure okay for security policy in your environment)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        return ssh

    def get_ssh(ssh, h):
        try:
            # initiate SSH connection
            ssh.connect(h, port=22, username=username, password=password)

            # print "type of ssh: "
            # print type(ssh)
            #
            # if ssh is None:
            #     print "yes, ssh is None"

            paramiko_interact = SSHClientInteraction(ssh, timeout=10, display=True)
            # print par_interact
            return paramiko_interact

        except paramiko.AuthenticationException as authentication_error:
            print "Authentication failed, please verify your credentials"
            write_conn_err(str(authentication_error))
        except paramiko.SSHException as sshException:
            print "Could not establish SSH connection: %s" % sshException
            write_conn_err(str(sshException))
        except socket.timeout as socket_timeouted:
            print "Connection timed out"
            write_conn_err(str(socket_timeouted))
        except Exception, e:
            print "Exception in connecting to the server"
            print "PYTHON SAYS:", e
            write_conn_err(str(e))


    def write_the_rest_of_cli_output(interact):
        interact.send('utils disaster_recovery status backup')  # Check the status of a Backup
        interact.expect('admin:')

        # output = interact.current_output_clean  # program saves output of show status command to the "output" variable
        cli_output_to_text_file()

        interact.send('file view install system-history.log')
        # Wait for the command to complete
        # time.sleep(2)
        interact.send('e')
        time.sleep(2)
        # overwrite = ""
        # while overwrite != 'q':
        #     overwrite = raw_input('\n[PRESS q!!!] ')
        # interact.send(overwrite)
        test = 'q'
        interact.send(test)
        time.sleep(2)
        interact.expect('admin:')
        # interact.send('show status')
        # interact.expect('admin:')
        # output = interact.current_output_clean  # program saves output of show status command to the "output" variable

        cli_output_to_text_file() # write to file


    #################################################
    ### Read host's IP address from the text file ###
    #################################################

    filename = 'server-ip-list.txt'
    f = open(filename, "r")

    o = f.read()

    ip1 = regex.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", o)
    hosts = ip1
    # print len(hosts)
    for host in hosts:
        write_date()  # write current date to the text file
        write_host(
            "\n>> ATTEMPTING SSH TO " + host + "\n")  # write the host ip to which ssh connection is established to the text file

        print "Connecting... "
        ssh_session = set_ssh_conn()
        # print "printing ssh_session below:"
        # print ssh_session
        interact = get_ssh(ssh_session, host)
        # print "print type(interact) follows below "
        # print type(interact)

        if interact is None:
            # print "yes, interact == None"
            set_ssh_conn().close()
            print("!!! TERMINATING THIS SSH CONNECTION ATTEMPT !!!")
            write("!!! TERMINATING THIS SSH CONNECTION ATTEMPT !!!")
        else:
            interact.expect(
                'admin:')  # program will wait till session is established and CUCM returns admin prompt
            interact.send(
                'utils disaster_recovery device list')  # Check the list of Backup files from remote server

            interact.expect(
                'admin:')  # program waits for utils disaster_recovery device list command to finish (this happens when CUCM returns admin prompt)
            cli_output_to_text_file()

            #############################################################
            ### utils disaster_recovery show_backupfiles {devicename} ###
            #############################################################
            # see_backup_files = ""

            # print("\nWould you like to see backup files for the device? ")
            # see_backup_files = raw_input('[y/n] ')
            # if(see_backup_files == 'y' or see_backup_files == 'Y'):
            #     command = raw_input("[TYPE THE FOLLOWING COMMAND: utils disaster_recovery show_backupfiles {devicename}] ")   # show backup files
            #     interact.send(command)
            #     interact.expect('admin:')
            #     cli_output_to_text_file()
            #
            #     write_the_rest_of_cli_output(interact)

            # else:
            write_the_rest_of_cli_output(interact)

            set_ssh_conn().close() # closing ssh connection to a host
    write("\nScript Complete")
    print "Script Complete"


if __name__ == '__main__':
    main()