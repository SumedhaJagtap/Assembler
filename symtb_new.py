dataS=["dd","db","dq"]
bssS=["resd","resb","resq"]
reg32=["eax","ecx","edx","ebx","esi","edi","esp","ebp"]
reg16=["ax","bx","cx","dx"]
reg8=["ah","al","bh","bl","ch","cl","dh","dl"]
arithmetic_inst=["add","addc","sub","mul","imul","div","idiv","inc","dec"]
branch_inst=["B","BC","BR","BALR"]
data_transfer_inst=["mov","push","pop","mvi"]
logic_inst=["and","or","xor","not"]
jmp_inst=['jmp','jz','je','loop']
compare_inst=['cmp']
one_opr_inst=['mul','push','pop','inc','dec','mul','imul','div','idiv','jmp','jz','je','loop']
zero_opr_inst=['']
two_opr_inst=['mov','mvi','add','addc','sub','cmp','and','or','xor','not']
instS=arithmetic_inst+data_transfer_inst+compare_inst+jmp_inst+logic_inst+branch_inst
inst_start_val=90
inst_opcode=[]
initAddr=000000
lst_init_addr=0
lst_list=[]

list_opcodes=[]
inst_type_two_opr=['r/m8,r8','r/m16/32,r16/32','r8,r/m8','r16/32,r/m16/32','r8,i','r16,i','r32,i','m,i','al,i8','eax,i16/32']
inst_type_one_opr=['r','m','i']
#def generate_opcode(str):
# if str=='mov'
#  list_opcodes.append(tuple([89,'']))
for i in range(len(instS)):
 if instS[i] in two_opr_inst:
  for j in range(len(inst_type_two_opr)):
   inst_opcode.append(tuple([instS[i],inst_start_val,inst_type_two_opr[j]]))
   inst_start_val=inst_start_val+1
 elif instS[i] in one_opr_inst:
   for j in range(len(inst_type_one_opr)):
    inst_opcode.append(tuple([instS[i],inst_start_val,inst_type_one_opr[j]]))
    inst_start_val=inst_start_val+1 
 #generate_opcode(instS[i])
for i in range(len(inst_opcode)):
 print inst_opcode[i],"\t"


symcnt=0
symsize=0
stype=[]
lflag=0
passone=[]
symlist=[]
symname=[]
symsize=[]
symval=[]
symline=[]
lineCnt=0
symcntL=[]
litval=[]
litxval=[]
litline=[]
symDU=[]

def findOpcode(inst,opr):
 #print inst+"\t\t",opr
 itype=''
 if len(opr)>1:
  if (opr[0] in reg16 and opr[1] in reg16) or (opr[0] in reg32 and opr[1] in reg32) or (opr[0] in reg16 and strip_all(opr[1]) in symname) or (opr[0] in reg32 and strip_all(opr[1]) in symname) :
   itype='r16/32,r/m16/32'
  elif (opr[0] in reg16 and opr[1] in reg16) or (opr[0] in reg32 and opr[1] in reg32) or (opr[1] in reg16 and strip_all(opr[0]) in symname) or (opr[1] in reg32 and strip_all(opr[0]) in symname) :
   itype='r/m16/32,r16/32'
  elif opr[0] in reg32 and opr[1].strip("'") in litval:
   itype='r32,i'
  elif strip_all(opr[0]) in symname and opr[1].strip("'") in litval:
   itype='m,i'
  elif strip_all(opr[0]) in reg32 and opr[1].strip("'") in litval:
   itype='r32,i'
 elif len(opr)==1:
   if opr[0] in symname:
    itype='m'
   elif opr[0] in reg32:
    itype='r'
 #print itype,opr
 for i in range(len(inst_opcode)):
  if inst_opcode[i][0]==inst and inst_opcode[i][2]==itype:
    return tuple([inst,inst_opcode[i][1]])


#findOpcode('mov')
def symtableFormation(llist,indexat,dtype,stype,lineCnt):
 print llist,indexat,dtype,stype,lineCnt
 #print llist
 if stype=="V":
  symname.append(llist[0])
  symline.append(lineCnt)
  symcntL.append(len(symname))
  #print llist
  symDU.append('Defined') 
  if dtype=='D':
   symval.append(llist[2])
   if llist[1]=='dd' and ',' not in llist[2]:
    symsize.append(4)
   elif llist[1]=='dd' and ',' in llist[2]:
    array=llist[2].split(',')
    symsize.append(len(array)*4)
   if llist[1]=='dq' and ',' not in llist[2]:
    symsize.append(8)
   elif llist[1]=='dq' and ',' in llist[2]:
    array=llist[2].split(',')
    symsize.append(len(array)*8)
   elif llist[1]=='db':
    symsize.append(len(llist[2].strip('"')))
  elif dtype=='B':
   symval.append('-')
   symsize.append('-')
 elif stype=="L":
  if llist in symname:
   symDU[symname.index(llist)]="Defined"
  else:
   symDU.append('Defined') 
   symname.append(llist)
   symline.append(lineCnt)
   symcntL.append(len(symname))
   symval.append('-')
   symsize.append('-')
 #print stype
 #llistSplit=llist.split()
 #print llist

def strip_all(str):
 #print str
 if str.startswith('dword'):
   return "%s"%str.strip('dword[').strip(']')
 elif str.startswith('qword'): 
   return  "%s"%str.strip('qword[').strip(']')
 elif str.startswith("'") and str.endswith("'"):
   return "%s"%str.strip("'")
 else:
   return str

def search_entry(str):
 str1=strip_all(str) 
 #print str1
 if str1 in reg32:
  return 'reg32'
 elif str1 in reg16:
  return 'reg16'
 elif str1 in reg8:
  return 'reg8' 
 elif str1 in symname:
  return '#sym%d'%(symname.index(str1)+1)
 elif str1 in litval:
  return '#lit%d'%(litval.index(str1)+1)

def generateAddr(str):
 char_cnt=6
 char_cnt=char_cnt-len(str)
 str1=''
 for i in range(char_cnt):
  str1=str1+'0'
 #print str1
# print len(str)
 return str1+str


def compute_address(str):
 if len(str)==1:
  if str[0] in reg32:
   #initAddr=initAddr+2
   #return initAddr
   return 2
  elif strip_all(str[0]) in symname :
   #initAddr=initAddr+4
   #return initAddr
   return 4
  elif str[0].strip("'") in litval:
   #initAddr=initAddr+4
   #return initAddr
   return 4
 else:
  #if strip_all(str[1]) in symname:
   #print str[0],str[1]
  if str[0] in reg32 and str[1] in reg32:
   #initAddr=initAddr+4
   #return initAddr
   return 4
  elif strip_all(str[0]) in symname or strip_all(str[1]) in symname or str[0].strip("'") in litval or str[1].strip("'") in litval:
   #initAddr=initAddr+6 
   #return initAddr
   return 6
 
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
   lineSplit[2]=" ".join(lineSplit[2:len(lineSplit)])   #joining 'string in data section'
  if data_section_flag==1: 
   if lineSplit[1] in dataS:
    symtableFormation(lineSplit,dataS.index(lineSplit[1]),'D','V',lineCnt)
   #else:
    #print "Error : Check your code"
  if bss_section_flag==1:
   if lineSplit[1] in bssS: 
    symtableFormation(lineSplit,bssS.index(lineSplit[1]),'B','V',lineCnt)
   #else:
    #print "Error : Check your code"
  if lineSplit[0].endswith(':') and text_section_flag==1: 
   #print lineSplit[0].strip(':')
   symtableFormation(lineSplit[0].strip(':'),0,'-','L',lineCnt)
  
  #if len(lineSplit)>2 and lineSplit[2] not in symname:
  # litval.append(lineSplit[2])
  # litline.append(lineCnt)
  if lineSplit[0] in jmp_inst and lineSplit[1] not in symname:
   symname.append(lineSplit[1])
   symval.append('-')
   symDU.append('Undefined')
   symsize.append('-')
   symline.append(lineCnt)
  if lineSplit[0] in instS and text_section_flag==1:
   instSplit=lineSplit[1].split(',')
   #print lineSplit,instSplit
   
   if instSplit[len(instSplit)-1].startswith("'") and instSplit[len(instSplit)-1].endswith("'"):
    litval.append(instSplit[len(instSplit)-1].strip("'"))
    litline.append(lineCnt)
    litxval.append(hex(ord(instSplit[len(instSplit)-1].strip("'"))))
   elif instSplit[len(instSplit)-1].strip('-').isdigit():
    litval.append(instSplit[len(instSplit)-1]) 
    litline.append(lineCnt)
    #print instSplit,"sfbjagdk"
    hexval=instSplit[len(instSplit)-1].strip('-')
    if int(hexval,16):
     litxval.append(hexval)
    elif hexval=='0':
     litxval.append(hexval)
   if len(instSplit)>1:
    initAddr=initAddr+compute_address(instSplit)
    passone_attr=str(lineCnt)+"\t"+generateAddr(str(initAddr))+"\t"+str(findOpcode(lineSplit[0],instSplit))+"\t\t"+str(tuple([strip_all(instSplit[0]),"%s"%search_entry(instSplit[0].strip("'"))]))+"\t,\t"+str(tuple([strip_all(instSplit[1]),search_entry(instSplit[1].strip("'"))]))
   else:
    initAddr=initAddr+compute_address(instSplit)
    passone_attr=str(lineCnt)+"\t"+generateAddr(str(initAddr))+"\t"+str(findOpcode(lineSplit[0],instSplit))+"\t\t"+str(tuple([strip_all(instSplit[0]),"%s"%search_entry(instSplit[0].strip("'"))]))
   passone.append(passone_attr)
     
#	print instSplit
#print "symlist",len(symname)
#print "symval",symval
#print "symsize",symsize
#print "symline",symline
#print "\n\n"



print "Symbol Table"
print "Symbol\tSize\tLine\tD/UD\tValue"
for i in range(len(symname)):
 print "%s"%symname[i],"\t%s"%symsize[i],"\t%s"%symline[i],"\t%s"%symDU[i],"\t%s"%symval[i]
print "\n\n"
print "Literal table"
print "Number\tValue\tLineNo\tHexValue"
for i in range(len(litval)):
 print i+1,"\t",litval[i],"\t",litline[i],"\t",litxval[i]
#print litval.index('0'),"litval"



print "\n\nIntermediate code"
print "lineCnt\tAddress\tInstruction\t\t   operand1\t\t\toperand2"
for i in range(len(passone)):
 print passone[i]

print"\n\nLst File"
for i in range(len(lst_list)):
 print lst_list[i]
fp1=open("output.txt","w")
fp1.write("Symbol Table\n")

fp1.write("Symbol\tSize\tLine\tD/UD\tValue\n")
for i in range(len(litval)):
 fp1.write("%s"%symname[i]+"\t%s"%symsize[i]+"\t%s"%symline[i]+"\t%s"%symDU[i]+"\t%s"%symval[i]+"\n")


fp1.write("\n\nLiteral table\n")
fp1.write("Number\tValue\tLineNo\tHexValue\n")
for i in range(len(litval)):
 fp1.write(str(i+1)+"\t"+str(litval[i])+"\t"+str(litline[i])+"\t"+str(litxval[i])+"\n")

fp1.write("\n\nIntermediate code\n")
fp1.write("lineCnt\tAddress\tInstruction\t\t   operand1\t\t\toperand2\n")
for i in range(len(passone)):
 fp1.write(passone[i]+"\n")


