import numpy
import matplotlib.pyplot as plt
from sympy import Eq, symbols, sympify,Integer
from matrixgenerator import generateMatrix,getEQ
from ecuacionesJacobi import jacobi

###Esta funcion se encarga de resolver los valores obtenidos de las ecuaciones y graficarlos
###Adicionalmente se puede configurar para interpolar estos resultados
def sol(interpolater=None):
    ##Crea la matriz de coeficientes
    a=getEQ(generateMatrix(12,8, 3,3,'dx'),returnCoefs='mat',printing=None)
    #Ax=b
    b=getEQ(generateMatrix(12,8, 3,3,'dx'),returnCoefs='b',printing=None)
    #Resuelve la matriz de coeficientes
    solucion=jacobi(a,b)
    #Crea la malla discretizada
    mapa=getEQ(generateMatrix(12,8, 3,3,'dx'),returnCoefs=None,printing=None)
    ##Reemplaza los puntos faltantes
    count=0
    for y in range(len(mapa)):
        for x in range(len(mapa[y])):
            if(type(mapa[y][x])==str):
                mapa[y][x]=solucion[count]
                count+=1
    mapa = [[float(value) for value in row] for row in mapa]
    ###################################################Interpolacion##########################################################################################
    #####Saca las ecuaciones dado un punto
    #Definicion formal de los simbolos a_ij
    A=[]
    for i in range(4):
        for j in range(4):
            A.append(symbols('A{}{}'.format(j,i)))

    ##Funcion para transformar un diccionario de sympy a una lista de coeficientes
    def dictToArray(dict,symbols):
        arraycoef=numpy.zeros(len(symbols),dtype=int)
        for n in range(len(symbols)):
            for j in range(0,4):
                for i in range(0,4):
                    arraycoef[n]=dict.get(symbols[n],0)
        return arraycoef.tolist()
    ##Definicion de la funcion de spline bicubico
    def f(point):
        eq=''
        count=0
        for j in range(0,4):
            for i in range(0,4):
                eq+=f'A{i}{j} *  {point[0]}**{i} * {point[1]}**{j}'
                count+=1
                if(i<3):
                    eq+=' + '
            if(j<3):
                eq+=' + '
        splinecoef=dictToArray(sympify(eq).as_coefficients_dict(),A)
        return splinecoef
    ##Derivada en x de la funcion spline
    def dx(point):
        eq=''
        count=0
        for j in range(0,4):
            for i in range(1,4):
                eq+=f'A{i}{j} * {i} * {point[0]}**{i-1} * {point[1]}**{j}'
                if(i<3):
                    eq+=' + '
            count+=3
            if(j<3):
                eq+=' + '
        splinecoef=dictToArray(sympify(eq).as_coefficients_dict(),A)
        return splinecoef
    ##Derivada en y de la funcion spline
    def dy(point):
        eq=''
        count=0
        for j in range(1,4):
            for i in range(0,4):
                eq+=f'A{i}{j} * {j} * {point[0]}**{i} * {point[1]}**{j-1}'
                if(i<3):
                    eq+=' + '
            count+=3
            if(j<3):
                eq+=' + '
        splinecoef=dictToArray(sympify(eq).as_coefficients_dict(),A)
        return splinecoef
    ##Derivada en cruzada de la funcion spline
    def dxy(point):
        eq=''
        count=0
        for j in range(1,4):
            for i in range(1,4):
                eq+=f'A{i}{j} *{j} * {i} * {point[0]}**{i-1} * {point[1]}**{j-1}'
                count+=1
                if(i<3):
                    eq+=' + '
            if(j<3):
                eq+=' + '
        splinecoef=dictToArray(sympify(eq).as_coefficients_dict(),A)
        return splinecoef
    ##ecuaciones de imagen
    def image(point):
        eq=mapa[point[1]][point[0]]+0.00
        return eq
    ##derivada en x
    def imagex(point):
        if(point[0]>10):
            eq=(0 -  mapa[point[1]][point[0]-1])/2
        else:
            eq=(mapa[point[1]][point[0]+1] -  mapa[point[1]][point[0]-1])/2
        return eq
    ##derivada en y
    def imagey(point):
        if(point[1]>6):
            eq=(0-mapa[point[1]-1][point[0]])/2
        else:
            eq=(mapa[point[1]+1][point[0]]-mapa[point[1]-1][point[0]])/2
        return eq
    ##Derivada cruzada de imagen
    def imagexy(point):
        if(point[0]>10 or point[1]>6):
            xy=0
        else:
            xy=mapa[point[1]+1][point[0]+1]
        eq=(xy-mapa[point[1]][point[0]-1]-mapa[point[1]-1][point[0]]-mapa[point[1]][point[0]])/4
        return eq
    ############Generacion de la matriz estatica para las ecuaciones que se usaran luego
    intermatrix=[]
    defaultPoints=[[0,0],[0+1,0],[0,0+1],[0+1,0+1]]
    funciones=[f,dx,dy,dxy]
    for func in funciones:
            for point in defaultPoints:
                intermatrix.append(func(point))
    #################################################
    ###Funcion en donde dados 4 puntos te resuelve los puntos intermedios entre estos puntos
    def solvePoints(points):
        ##Funciones de imagen
        imagenes=[image,imagex,imagey,imagexy]
        imageVector=[]
        ##calculo del vector imagen usando los 4 puntos
        for img in imagenes:
            for point in points:
                imageVector.append(img(point))
        inversaSolvePoints=numpy.linalg.inv(intermatrix)
        ###coeficientes aij resueltos
        solucioncoeficientes=numpy.dot(inversaSolvePoints,imageVector)
        ###Transformados de una lista de 16 posiciones a una matriz de 4x4 para facilidad de ubicacion
        solcoefarray=numpy.array(solucioncoeficientes).reshape((len(points),len(points)))

        ##Calculo del valor de un punto usando la ecuacion de spline donde solo se debe proporcionar una coordenada [x, y]
        ##0<x<1, 0<y<1
        def solve(point):
            eq=0
            for i in range(4):
                for j in range(4):
                    eq+=solcoefarray[j][i]*((point[0])**i)*((point[1])**j)
            return eq
        ##Crea la mini-matriz de los 4 puntos originales
        solvedpoints=numpy.full((4,4),'U').tolist()
        ###Pone los 4 puntos en su lugar
        solvedpoints[0][0] = mapa[points[0][1]][points[0][0]]
        solvedpoints[0][3] = mapa[points[1][1]][points[1][0]]
        solvedpoints[3][0] = mapa[points[2][1]][points[2][0]]
        solvedpoints[3][3] = mapa[points[3][1]][points[3][0]]
        ##Calcula los puntos intermedios entre los 4 puntos con la ecuacion
        for i in range(4):
            for j in range(4):
                if(solvedpoints[i][j]=='U'):
                    solvedpoints[i][j]=solve([ j*0.25 , i*0.25 ])
        return solvedpoints
    ##Funcion para interpolar toda la grafica
    def interpolate():
        ##Doble de alto y doble de ancho
        newMatrix=numpy.zeros((16,24)).tolist()
        for i in range(4):
            for j in range(6):
                xs=j*2
                ys=i*2
                ##Calcula los puntos a interpolar
                pointers=[[xs,ys],[(xs)+1,ys],[xs,(ys)+1],[(xs)+1,(ys)+1]]
                ##Crea la Minimatriz con los 4 puntos y los puntos intermedios
                newPoints=solvePoints(pointers)
                ##Dibuja los nuevos puntos
                for x in range(4):
                    for y in range(4):
                        newMatrix[i * 4 + x][j * 4 + y] = newPoints[x][y]
        return newMatrix
    if(interpolater):
        mapa=interpolate()
    print("Hola")
    ##################Grafica la malla discretizada###########################
    plt.imshow(mapa)
    plt.colorbar(ticks=[0, numpy.max(mapa)])
    plt.grid(color='gray', linestyle='-', linewidth=0.5)
    plt.xlabel("Eje X")
    plt.ylabel("Eje Y")
    plt.show()
    return 0
sol(1)