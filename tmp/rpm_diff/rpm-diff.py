#Script written by karthik.radha.krishnan@oracle.com
import paramiko
import time
import re

ip1 = raw_input("Please enter IP/HOSTNAME of SERVER 1:")
name1 = raw_input("Please enter UserName:")
password1 = raw_input("Please enter Password:")
ip2 = raw_input("Please enter IP/HOSTNAME of SERVER 2:")
name2 = raw_input("Please enter UserName:")
password2 = raw_input("Please enter Password:")
ssh_client1 = paramiko.SSHClient()
ssh_client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client1.connect(hostname=ip1,username=name1,password=password1)
ssh_client2 = paramiko.SSHClient()
ssh_client2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client2.connect(hostname=ip2,username=name2,password=password2)
stdin1,stdout1,stderr1=ssh_client1.exec_command("rpm -qa --qf '%{NAME}.%{ARCH}\n' | sort | cat")
data = stdout1.channel.recv(1024)
out= str(data)
while data:
    data = stdout1.channel.recv(1024)
    out = out + str(data)
stdin2,stdout2,stderr2=ssh_client2.exec_command("rpm -qa --qf '%{NAME}.%{ARCH}\n' | sort | cat")
data2 = stdout2.channel.recv(1024)
out2= str(data2)
while data2:
    data2 = stdout2.channel.recv(1024)
    out2 = out2 + str(data2)
stdin3,stdout3,stderr3=ssh_client1.exec_command("rpm -qa | sort | cat")
data = stdout3.channel.recv(1024)
out3= str(data)
while data:
    data = stdout3.channel.recv(1024)
    out3 = out3 + str(data)
stdin4,stdout4,stderr4=ssh_client2.exec_command("rpm -qa | sort | cat")
data2 = stdout4.channel.recv(1024)
out4= str(data2)
while data2:
    data2 = stdout4.channel.recv(1024)
    out4 = out4 + str(data2)



def printrpmuni(ou1,ou2):
    flag=0
    newp1=""
    newp2=""
    print("\n")
    print("==================================================================================================================")
    print("UNIQUE RPMS LIST OF BOTH SERVERS")
    print("\n")
    print("==================================================================================================================")
    print(" "*8 + '{0:60}  {1}'.format("RPM UNIQUE IN SERVER1", "RPM UNIQUE IN SERVER2"))
    print("\n")

    for word in ou1.split():
        flag=0
        for word2 in ou2.split():
                if word == word2 and flag==0:
                        flag=1
                        break
                else:
                        continue
        if flag == 0 :
                newp1= newp1+ word + "\n"
    for word in ou2.split():
        flag=0
        for word2 in ou1.split():
                if word == word2 and flag==0:
                        flag=1
                        break
                else:
                        continue
        if flag == 0 :
                newp2 = newp2 + word + "\n"
    newp11=newp1.split()
    newp22=newp2.split()
    if len(newp11)>len(newp22):
        for i in range(len(newp22)):
            print('{0:70}  {1}'.format(newp11[i],newp22[i]))
        for j in range (len(newp22), len(newp11)):
            print(newp11[j])
    else:
        for i in range(len(newp11)):
            print('{0:70}  {1}'.format(newp11[i],newp22[i]))
        for j in range (len(newp11), len(newp22)):
            print(newp22[j])

printrpmuni(out,out2)

newword= ""
for word in out2.split():
        flag=0
        for word2 in out.split():
                if word == word2 and flag==0:
                        flag=1
                        break
                else:
                        continue
        if flag == 1 :
                newword = newword + word.split('.')[0]+"\n"

new1=""
new2=""
for word in newword.split():
    count1=0
    count2=0
    for word2 in out3.split():
        if re.split('-[0-9]',word2)[0] == word:
            count1=count1+1
            new1 = new1 + word2 + "\n"
        else:
            continue
    for word3 in out4.split():
        if re.split('-[0-9]',word3)[0] == word:
            count2=count2+1
            new2 = new2 + word3 + "\n"
        else:
            continue
    if count1 > count2:
        count1=count1-count2
        for i in range (count1):
            new2 = new2 + "DUPRPMS" + "\n"
    else:
        count2=count2-count1
        for i in range (count2):
            new1 = new1 + "DUPRPMS" + "\n"
new11=new1.split()
new22=new2.split()
print("=========================================================================================================================")
print("\n")
print("Below is the comparison of versions of the installed RPMs")
print("\n")
print("=========================================================================================================================")
print(" "*8 + '{0:85}  {1}'.format("RPM VERSION IN SERVER1", "RPM VERSION IN SERVER2"))

for j in range (len(new11)):
        new111=re.split('\.',new11[j].replace("-","."))
        new222=re.split('\.',new22[j].replace("-","."))
        flag=0
        for i, k in zip(range(len(new111)), range(len(new222))):
                if new111[i].isdigit()==True and new222[k].isdigit()==True and flag==0:
                        if int(new111[i]) > int(new222[k]):
                                print ('{0:55} {1:25} {2} '.format(new11[j], " is greater than >>>> " ,new22[j]))
                                flag=1
                        elif int(new111[i]) < int(new222[k]):
                                print ('{0:55} {1:25} {2} '.format(new11[j], " is lesser than <<<< " ,new22[j]))
                                flag=1
                        else:
                                continue

                elif new111[i]=="DUPRPMS":
                        print ('{0:55} {1:25} {2} '.format("DUPLIACTE RPM IN SERVER2", "DUPLICATE RPM" ,new22[j]))
                        flag=1
                elif new222[i]=="DUPRPMS":
                        print ('{0:55} {1:25} {2} '.format(new11[j], "DUPLICATE RPM" ,"DUPLIACTE RPM IN SERVER2"))
                        flag=1
                elif new111[i].isdigit()== False or new222[k].isdigit()==False:
                        continue

        if flag == 0 :
                print ('{0:55} {1:25} {2} '.format(new11[j], " is same as === " ,new22[j]))
print("=========================================================================================================================")



ssh_client1.close
ssh_client2.close

