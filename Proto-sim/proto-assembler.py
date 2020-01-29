#! /usr/bin/env python3
import argparse

memory="0x3000"
labels={}

def increment_memory():
    global memory

    val=int(memory[2:],16)
    val+=4
    memory=hex(val)

def pass_one(line):
    global labels
    if(line[-1:]==":"):
        if(line[:-1] in labels):
            raise NameError("Duplicate")
        else:
            labels[line[:-1]]=memory[2:]
        return("label")
    elif(line[0]=="#"):
        return("comment")
    else:
        return(-1)

def parse(line):

    noop=False
    dir=False

    direc=pass_one(line)
    tokens=line.split()
    assembly="0x"

    #opcode parse
    if(tokens[0]=="LD"):
        if(tokens[2][0]=="R"):
            assembly+="01"
        elif(tokens[2][0:2]=="0x"):
            assembly+="00"
        elif(tokens[2][0:3]=="$0x"):
            assembly+="02"
        else:
            raise NameError("Invaid Syntax!")
    elif(tokens[0]=="ST"):
        if(tokens[2][0]=="R"):
            assembly+="13"
        elif(tokens[2][0:3]=="$0x"):
            assembly+="10"
        else:
            raise NameError("Invaid Syntax!")
    elif(tokens[0]=="STL"):
        if(tokens[2][0]=="R"):
            assembly+="14"
        elif(tokens[2][0:3]=="$0x"):
            assembly+="11"
        else:
            raise NameError("Invaid Syntax!")
    elif(tokens[0]=="STH"):
        if(tokens[2][0]=="R"):
            assembly+="15"
        elif(tokens[2][0:3]=="$0x"):
            assembly+="12"
        else:
            raise NameError("Invaid Syntax!")
    elif(tokens[0]=="CMP"):
        if(tokens[2][0]=="R"):
            assembly+="20"
        elif(tokens[2][0:2]=="0x"):
            assembly+="21"
        else:
            raise NameError("Invaid Syntax!")
    elif(tokens[0]=="BEQ"):
        assembly+="30"
        noop=True
    elif(tokens[0]=="BGT"):
        assembly+="31"
        noop=True
    elif(tokens[0]=="BLT"):
        assembly+="32"
        noop=True
    elif(tokens[0]=="BRA"):
        assembly+="33"
        noop=True
    elif(tokens[0]=="ADD"):
        if(tokens[2][0]=="R"):
            assembly+="42"
        elif(tokens[2][0:2]=="0x"):
            assembly+="40"
        else:
            raise NameError("Invaid Syntax!")
    elif(tokens[0]=="SUB"):
        if(tokens[2][0]=="R"):
            assembly+="43"
        elif(tokens[2][0:2]=="0x"):
            assembly+="41"
        else:
            raise NameError("Invaid Syntax!")
    elif(tokens[0]=="HALT"):
        assembly+="FE"
        noop=True
    elif(tokens[0]=="NOOP"):
        assembly+="FF"
        noop=True
    elif(tokens[0][-1:]==":" or tokens[0][0]=="#"):
        dir=True
        noop=True
    else:
        raise NameError("Invaid Syntax!")

    #operand translation

    #operand 1
    if(not noop):
        tp=int(tokens[1][1])
        if(tp>7):
            tp=7
        inp_reg=hex(tp)[2:]
        padding="00"
        inp_reg=padding+inp_reg
        inp_reg=inp_reg[-2:]

        assembly+=inp_reg
    else:
        if(assembly[2:4] in ["30","31","32","33"]):
            assembly+="00"
        elif(assembly[2:4] in ["FE","FF"]):
            assembly+="FF"
        else:
            pass

    #operand 2
    if(not noop):
        if(assembly[2:4]=="00"):
            assembly+=tokens[2][2:]
        elif(assembly[2:4]=="01"):
            tp=int(tokens[2][1])
            if(tp>7):
                tp=7
            inp_reg=hex(tp)[2:]
            padding="00"
            inp_reg=padding+inp_reg
            inp_reg=inp_reg[-2:]
            assembly+="00"+inp_reg
        elif(assembly[2:4]=="02"):
            assembly+=tokens[2][3:]
        elif(assembly[2:4] in ["10","11","12"]):
            assembly+=tokens[2][3:]
        elif(assembly[2:4] in ["13","14","15"]):
            tp=int(tokens[2][1])
            if(tp>7):
                tp=7
            inp_reg=hex(tp)[2:]
            padding="00"
            inp_reg=padding+inp_reg
            inp_reg=inp_reg[-2:]
            assembly+="00"+inp_reg
        elif(assembly[2:4]=="20"):
            tp=int(tokens[2][1])
            if(tp>7):
                tp=7
            inp_reg=hex(tp)[2:]
            padding="00"
            inp_reg=padding+inp_reg
            inp_reg=inp_reg[-2:]
            assembly+="00"+inp_reg
        elif(assembly[2:4]=="21"):
            assembly+=tokens[2][2:]
        elif(assembly[2:4] in ["40","41"]):
            assembly+=tokens[2][2:]
        elif(assembly[2:4] in ["42","43"]):
            tp=int(tokens[2][1])
            if(tp>7):
                tp=7
            inp_reg=hex(tp)[2:]
            padding="00"
            inp_reg=padding+inp_reg
            inp_reg=inp_reg[-2:]
            assembly+="00"+inp_reg
    else:
        if(assembly[2:4]=="FE"):
            assembly+="FEFF"
        elif(assembly[2:4]=="FF"):
            assembly+="FFFF"
        elif(assembly[2:4] in ["30","31","32","33"]):
            assembly+=labels[tokens[1]]
        else:
            pass

    if(not dir):
        return(assembly)
    else:
        return(direc)


def run(args):
    filename = args.input # these match the "dest": dest="input"
    output_filename = args.output # from dest="output"

    if(filename==None):
        run=True
        print("\n--------------Simple Custom Assebler 1.0 console------------------\n")
        while(run):
            line=input(">>>")
            if(line not in ["quit()","q()","exit","quit"]):
                try:
                    code=parse(line)
                    if(code not in ["label","comment"]):
                        print(memory[2:]+": "+code)
                        increment_memory()
                    else:
                        print(code)
                except:
                    print("Syntax error!")
            else:
                run=False
    else:
        if(output_filename==None):
            with open(filename, "r") as f:
                lc=1
                line=f.readline()[:-1]
                while(line!=""):
                    try:
                        code=parse(line)
                        if(code not in ["label","comment"]):
                            print(memory[2:]+": "+code)
                            increment_memory()
                        else:
                            print(code)
                    except:
                        print("Syntax Error at line: "+str(lc))
                        break
                    line=f.readline()[:-1]
                    lc+=1
        else:
            of=open(output_filename, "w")
            with open(filename, "r") as f:
                lc=1
                line=f.readline()[:-1]
                while(line!=""):
                    try:
                        code=parse(line)
                        if(code not in ["label","comment"]):
                            of.write(memory[2:]+": "+code+"\n")
                            increment_memory()
                        else:
                            of.write(code+"\n")
                    except:
                        print("Syntax Error at line: "+str(lc))
                        break
                    line=f.readline()[:-1]
                    lc+=1
                    if(line==""):
                        print("Done!")
            of.close()

def main():
    parser=argparse.ArgumentParser(description="Assemble Our Custom ISA.")
    parser.add_argument("-in",help="Input file" ,dest="input", type=str)
    parser.add_argument("-out",help="Output file" ,dest="output", type=str)
    parser.set_defaults(func=run)
    args=parser.parse_args()
    args.func(args)

if __name__=="__main__":
	main()
