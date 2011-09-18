datagrid = [[4,'V','H','Y',4,6,'P','W',9,'Q'],['T',5,9,3,'C',8,9,'R','H','H'],[7,'J',8,'F',2,'F','J',1,'Y',0],[8,'Y','C',2,'D',7,'P','V','J',8],['N','F','C',5,0,'P','V','J',8],['N','F','C',5,0,'P','D','X',8,5]]
yaxis = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,'I':8,'J':9}

def parseChallengeString(rawInput):
    import re
    return [re.findall('[A-Z]',rawInput),re.findall('[\d]',rawInput)]

if __name__ == "__main__":
        param = "[A4][B2][C3]"
        parsedArrays = parseChallengeString(param)
        print [datagrid[int(parsedArrays[1][i])-1][yaxis[parsedArrays[0][i]]] for i in range(len(parsedArrays[0]))]
