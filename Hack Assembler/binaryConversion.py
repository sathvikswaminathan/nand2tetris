def decToBinary(decimal):
    decimal = int(decimal)
    return str(bin(decimal).replace("0b",""))

def getBinary(decimal):
    binaryOutput = decToBinary(decimal)
    for i in range(15-len(binaryOutput)):
        binaryOutput = "0" + binaryOutput
    return binaryOutput