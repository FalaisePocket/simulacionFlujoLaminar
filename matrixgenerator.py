

def generateMatrix(ancho,alto,alturaObstaculo,anchoObstaculos):
    matrix=[]
    var=1
    for y in range(alto):
        line=[]

        if(y==0 or y==alto-1):
            for x in range(ancho):
                line.append(0)
        else:
            for x in range(ancho):
                if(x==0 or x==(ancho-1)):
                    line.append(0)
                else:
                    line.append("U")
                    
        matrix.append(line)

    ##Columnas
    mitadAncho = round(ancho/2)-1

    jsince= mitadAncho - (anchoObstaculos//2)
    
    
        

    ##variables columna arriba
    i=0
    for i in range(alturaObstaculo):
        for j in range( jsince,jsince+anchoObstaculos):
            matrix [i][j]=0 


    ##variables columna abajo
    isince=(alto-alturaObstaculo)
    
    for k in range(isince,alto):
        for l in range(jsince,jsince+anchoObstaculos):
            matrix [k][l]=0

    ###
    for i in range (alto):
        matrix[i][0]=1

    ####imprime la wea
    
    '''
    for ses in matrix:
        print(ses)
    '''
    return matrix    


def ecugenerator():
    matrix=generateMatrix(11,7, 3,3)
    var=1
    for i in range(7):
        for j in range(11):
            if(matrix[i][j]=="U"):
                matrix[i][j]=matrix[i][j]+str(var)
                var=var+1
    print(matrix)
    '''
    for y in range(7):
        for x in range(11):
            if(matrix[y][x]=="U"):
                matrix=matrix[y][x+1]
    '''

ecugenerator()


