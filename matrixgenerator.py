from sympy import Eq, symbols, sympify,Integer
import numpy
def generateMatrix(ancho,alto,alturaObstaculo,anchoObstaculos,dv):
    matrix=[]
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
                    line.append('U')
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
    iss=alto-alturaObstaculo
    j1=mitadAncho - (anchoObstaculos//2)
    j2=j1+anchoObstaculos
    for i in range(iss,alto):
        for j in range(j1,j2):
            matrix[i][j]=0
    if dv=='dx':
        for n in range(alto):
            matrix[n][0]=1
    else:
        for n in range(alto):
            matrix[n][0]=0

    '''
    for ses in matrix:
        print(ses)
    '''
    return matrix    
########################################################################################################################################################################
########################################################################################################################################################################
def getEQ(matrix,returnCoefs=None,printing=None):
    ##recibe un punto y calcula de donde debería tomar los valores
    ##Array de posiciones x,y
    #c= si es dx o dy

    ##Calcula la derivada de un punto
    def derivada(point):
        ##result=f'v({point[0]+1}, {point[1]}) - 8 * v({point[0]}, {point[1]}) + 3 * v({point[0]-1}, {point[1]}) + v({point[0]}, {point[1]+1}) + 3 * v({point[0]}, {point[1]-1})'
        result=f'{matrix[point[1]][point[0]+1]} - 8 * {matrix[point[1]][point[0]]} + 3 * {matrix[point[1]][point[0]-1]} + {matrix[point[1]+1][point[0]]} + 3 * {matrix[point[1]-1][point[0]]}'
        
        return result

    equations=[]
    count=1
    
    
    ##Establece las variables W1,w2,w3,...,wn
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            if(matrix[y][x]=='U'):
                matrix[y][x]=f'w{count}'
                count+=1
    w = symbols('w1:49')
    testDict=[]
    ##Calcula las ecuaciones de cada punto de la matriz
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            if(isinstance(matrix[y][x],str)):
                ##create the equation
                eq=sympify(derivada([x,y]))
                testDict.append(eq.as_coefficients_dict())
                equations.append(Eq(eq,0))
                
    ###convierte de un diccionario a una Lista comun
    def dictToArray(dict,symbols):
        arraycoef=numpy.zeros(len(symbols),dtype=int)
        for i, symbol in enumerate(symbols):
            arraycoef[i]=dict.get(symbol,0)   
        return arraycoef
    newMa=[]
    b=[]
    for n in testDict:
        b.append(-1*n.get(Integer(1),0))
        cof=dictToArray(n,w).tolist()
        newMa.append(cof)
    
    if(returnCoefs=='mat'):
        return numpy.array(newMa)
    elif (returnCoefs=='b'):
        return b
    else:
        return matrix



