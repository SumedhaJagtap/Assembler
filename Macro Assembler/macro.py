mnt=[]
mdt=[]
mnt_name=[]
mdefflag=0
sectionFlag=0
dataFlag=0
bssFlag=0
mnt_cnt=0
mdt_cnt=0
expand_flag=0
fp=open("macro_input.asm","r")
line=fp.readline()
while line!="":
  lineSplit=line.split()
  
  if lineSplit[0]=='%macro':
    mdt.append(str(mdt_cnt)+"\t"+" ".join(lineSplit[1:len(lineSplit)]))
    mnt.append(str(mnt_cnt)+"\t"+lineSplit[1]+"\t"+str(mdt_cnt))
    mnt_name.append(lineSplit[1])
    mnt_cnt+=1
    mdt_cnt+=1
    line=fp.readline()
    
    while('%endmacro' not in line):
     mdt.append(str(mdt_cnt)+'\t'+line)
     mdt_cnt+=1
     line=fp.readline()
    mdt.append(str(mdt_cnt)+line)
  else:
   #print line
   for i in range(len(mdt)):
    mdt_split=mdt[i].split()
    #print mdt_split,"main"
    i+=1
    if len(mdt_split)>1:
     if lineSplit[0]==mdt_split[1]:
      expand_flag=0
      while('endmacro' not in mdt[i]):  
       parm=lineSplit[1].split(',')
       if '%' in mdt[i].split()[len(mdt[i].split())-1]:
        if expand_flag==0: 
 	 print '..@'+mdt[i][:-3]+str(parm[int(mdt[i].split()[len(mdt[i].split())-1].split(',')[1].strip('%'))-1])
         expand_flag=1
        else:
         print mdt[i][:-3]+str(parm[int(mdt[i].split()[len(mdt[i].split())-1].split(',')[1].strip('%'))-1])
        #print (mdt[i].split()[len(mdt[i].split())-1])
        #print (mdt[i].split()[len(mdt[i].split())-1].split(',')[1])
        #print line[:-2]
	#print parm[int(mdt[i].split()[len(mdt[i].split())-1].split(',')[1].strip('%'))-1] #,parm
       #if '%' in mdt_split[len(mdt_split)-1]:
       # print mdt_split
        # ==print mdt[i].index('%'),mdt[i]
       i+=1
     
   print line
   #for i in range(len(mnt)):
    #mnt_split=mnt[i].split()
    #print mnt_split,lineSplit[0]
   # for i in mnt_name:
    # if lineSplit[0]== i:
    #  print i
    #  for j in range(len(mdt)):
     #   mdt_split=mdt.split()
   # for i in range(len(mnt)):
    # mnt_split=mnt[i].split()
   #  print mnt_split[2]
   #  print mdt[int(mnt_split[2])],mdt[int(mnt[i+1].split()[2])]
     #for j in range(int(mnt_split[2]),int(mnt[i+1].split()[2])):
      # print mdt[j]
     #for i in range(len(mdt)):
      #if mnt_split[1] in mdt[i]:
       #print mdt[i],"mdt enty"  
  line=fp.readline()
 

'''  
   mnt_entry=(" ".join(lineSplit[1:len(lineSplit)]))
   line=fp.readline()
   mnt.append(str(mnt_cnt)+' '+mnt_entry+'mdt_entry')
   mnt_cnt+=1
   while('%endmacro' not in line):
    mdt.append(line)
    line=fp.readline()
  line=fp.readline() 
'''

print "MDT\nindex\tValue"
for i in mdt:
 print i

print "\n\n\tMNT\nindex\tname\tmdt_index"
for i in mnt:
 print i
'''
fp=open("macro_input.asm","r")
for line in fp:
 lineSplit=line.split()
 if lineSplit[0] in mnt:
  macro_expansion(line)
 else:
  print line
'''
