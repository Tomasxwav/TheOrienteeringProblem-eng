import matplotlib.pyplot as plt
import math
import random

def distancia_eu(nodo1, nodo2):
    distancia_eu = math.sqrt((x[nodo1] - x[nodo2]) ** 2 + (y[nodo1] - y[nodo2]) ** 2)
    return distancia_eu


"""LECTURA DE ARCHIVO"""
def leer_archivo():
    archivo = input(
        "Que numero de dataset desea tomar? \n1- Tsiligirides 1 \n2- Tsiligirides 2\n3- Tsiligirides 3\n4- Chao 64\n5- Chao 66\nDigite el numero: ")
    carpeta = "SET" + archivo
    if archivo == "1" or archivo == "2" or archivo == "3":
        archivo = "tsiligirides_problem_" + archivo + "_budget_"
    elif archivo == "4":
        archivo = "set_64_1_"
        carpeta = "SET64"
    elif archivo == "5":
        archivo = "set_66_1_"
        carpeta = "SET66"
    else:
        print("Digite un numero valido")
        exit()
    archivo += input("Digite el numero del archivo: ")
    file = open(f"datasets/{carpeta}/{archivo}.txt", 'r')
    numbers = []
    lines = file.read().splitlines()  # divide por lineas el archivo
    for line in lines:
        line_numbers = list(map(float, line.split()))
        numbers += line_numbers
    return numbers



def mostrar_grafico(x, y, recorrido):
    """GRAFICAR LOS PUNTOS"""
    plt.title("TSP")
    plt.xlabel("Coordenada X")
    plt.ylabel("Coordenada Y")

    for i in range(len(x)):
        plt.scatter(x[i], y[i])
        plt.text(x[i] + 0.1, y[i] + 0.1, str(i))

    """Imprimir grafico"""
    for i in range(len(recorrido) - 1):
        plt.plot([x[recorrido[i]], x[recorrido[i + 1]]], [y[recorrido[i]], y[recorrido[i + 1]]], 'r--')
    plt.plot([x[1], x[0]], [y[1], y[0]], 'r--')
    plt.show()

"""ASIGNACION DE VALORES"""

def values():
    #El primer dato del arreglo dice presupuesto de tiempo disponible por ruta y el segundo número de caminos "
    numbers = leer_archivo()
    Tmax = numbers[0]
    P = numbers[1]
    numbers = numbers[2:]  # eliminar los primeros 2 datos del arreglo con el metodo slicing ya que no los usaremos

    x,y,S = [], [], []

    for i in range(int(len(numbers) / 3)):
        x.append(numbers[0])
        y.append(numbers[1])
        S.append(numbers[2])
        numbers = numbers[3:]  # Los eliminamos del array
    return [x, y, S, Tmax]


"""HEURISTICA""""""HEURISTICA""""""HEURISTICA""""""HEURISTICA""""""HEURISTICA""""""HEURISTICA""""""HEURISTICA"""
def heuristica(S, x):
    print("\n-= HEURISITICA CONSTRUCTIVA =-")
    a = float(input("Inserte el valor de a: "))
    recorrido, T_tot, selected, dist, max_valor_node, min_valor_node = [0], 0, 0, 0, 0, 0
    constraint_feasible = True
    while constraint_feasible:
        """BUSCA EL MINIMO"""
        valor_min = 100000
        for i in range(1, len(x)-1):
            if i != selected and i != 1 and i not in recorrido:
                valor = S[i] / (distancia_eu(i, selected) + distancia_eu(i, 1))
                if valor < valor_min:
                    valor_min = valor
                    min_valor_node = i
        """BUSCA EL MAXIMO"""
        valor_max = 0
        for i in range(1, len(x)-1):
            if i != selected and i != 1 and i not in recorrido and distancia_eu(i, selected) + distancia_eu(i, 1) + T_tot < Tmax:
                valor = S[i] / (distancia_eu(i, selected) + distancia_eu(i, 1))
                if valor > valor_max:
                    valor_max = valor
                    max_valor_node = i
        """KBEST"""
        k_best = []
        k_calidad = valor_max - (valor_max - valor_min) * a
        for j in range(1, len(x)-1):
            valor_max = 0
            for i in range(len(x)):
                if i not in recorrido and i != selected and i != 1 and selected != 1 and i not in k_best:
                    valor = S[i] / (distancia_eu(i, selected) + distancia_eu(i, 1))
                    if valor > valor_max and valor > k_calidad:
                        if distancia_eu(i, selected) + distancia_eu(i, 1) + T_tot < Tmax:
                            valor_max = valor
                            max_valor_node = i
                        else:
                            constraint_feasible = False
                            break
            if max_valor_node not in k_best:
                k_best.append(max_valor_node)
            else:
                break
        max_valor_node = random.choice(k_best) #Elige un nodo random de k_best
        if max_valor_node not in recorrido:
            if T_tot + distancia_eu(selected, max_valor_node) + distancia_eu(max_valor_node, 1) < Tmax:
                T_tot += distancia_eu(max_valor_node, selected)
                selected = max_valor_node
                recorrido.append(max_valor_node)
            else:
                constraint_feasible = False
    recorrido.append(1)
    T_tot += distancia_eu(recorrido[len(recorrido) - 2], 1)
    return [recorrido, T_tot]


def suma(recorrido, S):
    Tot_score = 0
    for vertice in recorrido:
        Tot_score += S[vertice]
    return Tot_score

def suma_dist(path):
    tiempo = 0
    for i in range(len(path)-1):
        tiempo += distancia_eu(path[i],path[i+1])
    return tiempo


values = values()

x = values[0]
y = values[1]
Score = values[2]
Tmax = values[3]


resulado = heuristica(Score,x)
recorrido = resulado[0]
T_tot = resulado[1]
Score_tot = suma(recorrido, Score)


print(f"\nEl recorrido final sería: {recorrido}")
print(f"Con un score total de: {Score_tot} y un tiempo final de: {round(T_tot, 4)}")

mostrar_grafico(x,y,recorrido)
print("\n")



"""lOCAL SEARCH""""""lOCAL SEARCH""""""lOCAL SEARCH""""""lOCAL SEARCH""""""lOCAL SEARCH""""""lOCAL SEARCH""""""lOCAL SEARCH"""
print("-= BUSQUEDA LOCAL =-")
recorrido_vecino = list(recorrido)
Score_nuevo = int(Score_tot)
Tiempo_nuevo = int(T_tot)
vecindario = []

#va acomodarlos en mejor orden

constraint_feasible = True
while constraint_feasible:
    i_decide = True
    s = 1
    recorrido_vecino_temp = list(recorrido_vecino)
    while i_decide:
        best_position = 0
        is_better = False
        node_distance = distancia_eu(recorrido_vecino[s], recorrido_vecino[s + 1]) + distancia_eu(recorrido_vecino[s],
                                                                                                  recorrido_vecino[s - 1])
        for j in range(1, len(recorrido_vecino)):
            if s != j:
                if s != j-1:
                    node_distance2 = distancia_eu(recorrido_vecino[s], recorrido_vecino[j]) + distancia_eu(
                        recorrido_vecino[s],
                        recorrido_vecino[j - 1])
                    if node_distance2 < node_distance:
                        best_position = j
                        recorrido_vecino_temp.insert(best_position, recorrido_vecino[s])
                        for i in range(len(recorrido_vecino_temp) - 1):
                            for j in range(len(recorrido_vecino_temp) - 1):
                                if recorrido_vecino_temp[i] == recorrido_vecino_temp[j] and i != j and j != best_position:
                                    recorrido_vecino_temp.pop(j)
                                    if suma_dist(recorrido_vecino_temp) < suma_dist(recorrido_vecino):
                                        is_better = True
                                    else:
                                        recorrido_vecino_temp = list(recorrido_vecino)
                                        is_better = False

                else:
                    node_distance2 = distancia_eu(recorrido_vecino[s], recorrido_vecino[j ]) + distancia_eu(
                        recorrido_vecino[s],
                        recorrido_vecino[j - 2])

                    if node_distance2 < node_distance:
                        best_position = j
                        recorrido_vecino_temp.insert(best_position, recorrido_vecino[s])
                        if recorrido_vecino_temp[i] == recorrido_vecino_temp[j] and i != j and j != best_position:
                            recorrido_vecino_temp.pop(j)
                            if suma_dist(suma_dist(recorrido_vecino_temp)) < suma_dist(recorrido_vecino):
                                is_better = True
                            else:
                                recorrido_vecino_temp = list(recorrido_vecino)
                                is_better = False
        if is_better == True:
            recorrido_vecino = list(recorrido_vecino_temp)
        else:
            recorrido_vecino_temp = list(recorrido_vecino)

        T_vecino = suma_dist(recorrido_vecino)

        s+=1
        if s == len(recorrido_vecino)-1:
            i_decide = False

    print(f"El recorrido vecino sería: {recorrido_vecino}")
    print(f"Con un score total de: {suma(recorrido_vecino,Score)} y un tiempo final de: {round(T_vecino, 4)}\n")

    new_node = None
    menor_dist = Tmax
    for i in range(2, len(x)-1):
        if i not in recorrido_vecino:
            for j in range(len(recorrido_vecino)-1):
                if (distancia_eu(recorrido_vecino[j] , i) + distancia_eu(i, recorrido_vecino[j+1]) + T_vecino) - distancia_eu(recorrido_vecino[j],recorrido_vecino[j+1]) < Tmax:
                    if distancia_eu(recorrido_vecino[j] , i) + distancia_eu(i, recorrido_vecino[j+1]) - distancia_eu(recorrido_vecino[j], recorrido_vecino[j+1]) < menor_dist:
                        menor_dist = distancia_eu(recorrido_vecino[j] , i) + distancia_eu(i, recorrido_vecino[j+1]) - distancia_eu(recorrido_vecino[j], recorrido_vecino[j+1])
                        new_node = i
                        position_new_node = j+1

    if suma_dist(recorrido_vecino) + menor_dist < Tmax:
        recorrido_vecino.insert(position_new_node,new_node)
    else:
        constraint_feasible = False


print("-=MEJOR RECORRIDO=-")
print(f"El mejor recorrido sería: {recorrido_vecino}")
print(f"Con un score total de: {suma(recorrido_vecino,Score)} y un tiempo final de: {round(suma_dist(recorrido_vecino), 4)}")


mostrar_grafico(x,y,recorrido_vecino)

print("\n")
