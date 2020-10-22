def aproximafechas(fecha1):
    xd=fecha1.split(":")
    xd[1]=int(xd[1])
    if(xd[1] < 15):
        xd[1]="00"
    elif((xd[1]>= 15 and xd[1] <= 30) or (xd[1] <= 45 and xd[1]> 30)):
        xd[1]="30"
    elif(xd[1]>45):
        xd[0]=str(int(xd[0])+1)
        xd[1]="00"
    xd=":".join(xd)
    return xd
    
states={"Braito":1}
print(len(states))