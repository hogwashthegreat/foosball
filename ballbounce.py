def b(yPos):
    numTables = yPos//1000
    remainder = yPos % 1000
    if numTables % 2:
        yPos = 1000-remainder
    else:
        yPos = remainder
        
    return yPos


print(b(-5))