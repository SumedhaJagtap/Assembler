from symtb_new1 import *

lst_list=[]
lst_addr=0
lst_cnt=0
lineCnt=0

def generateLstAddr(str):
 char_cnt=6
 char_cnt=char_cnt-len(str)
 str1=''
 for i in range(char_cnt):
  str1=str1+'0'
 #print str1
# print len(str)
 return '0'+str+str1

file=open("arraSum.asm","r")
for line in file:
 if line!='\n' and line.startswith(';')==False and line!='' :
  lineCnt=lineCnt+1
  lineSplit=line.split()
  if '.text' in lineSplit:
    lst_list.append(str(len(lst_list)+1)+'\t\t\t\t'+line)
    text_section_flag=1
    bss_section_flag=0
    data_section_flag=0
  if '.bss' in lineSplit:
    lst_list.append(str(len(lst_list)+1)+'\t\t\t\t'+line)
    bss_section_flag=1
    text_section_flag=0
    data_section_flag=0
  if '.data' in lineSplit:
    lst_list.append(str(len(lst_list)+1)+'\t\t\t\t'+line)
    data_section_flag=1
    text_section_flag=0
    bss_section_flag=0
  if len(lineSplit)>3:
   lineSplit[2]=(" ".join(lineSplit[2:len(lineSplit)])).strip('"')
   del lineSplit[3:len(lineSplit)]
  if data_section_flag==1: 
   if lineSplit[1] in dataS:
    symtableFormation(lineSplit,dataS.index(lineSplit[1]),'D','V',lineCnt)
    
    if lineSplit[1]=='dd' and ',' not in lineSplit[2]:
     lst_list.append(str(lst_cnt)+' '+generateAddr(str(hex(lst_addr)).strip('0x'))+' '+generateLstAddr(str(hex(int(lineSplit[2]))).strip('0x'))+'\t\t\t'+line)
     lst_addr+=symsize[symname.index(lineSplit[0])]
     lst_cnt+=1
    if lineSplit[1]=='dd' and ',' in lineSplit[2]:
     print lineSplit[2]
     sp=lineSplit[2].split(',')
     st=''
     for i in range(len(sp)):
      st+=generateLstAddr(str(hex(int(sp[i]))).strip('-0x'))
     st_array=[]
     start=0
     end=9
     if len(st)>18:
       while end<=len(st):
        st_array.append(st[start:end]+'-')
        start+=end
        end+=9
     print st_array,"st"
     lst_list.append(str(lst_cnt)+' '+generateAddr(str(hex(lst_addr)).strip('0x'))+' '+st+'\t\t\t'+line)
     lst_addr+=symsize[symname.index(lineSplit[0])]
     lst_cnt+=1
   #else:
    #print "Error : Check your code"
  if bss_section_flag==1:
   if lineSplit[1] in bssS: 
    symtableFormation(lineSplit,bssS.index(lineSplit[1]),'B','V',lineCnt)

print "lst"
for i in range(len(lst_list)):
 print lst_list[i]

