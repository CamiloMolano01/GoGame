ROWS = 9
COLUMNS = 9


def goGameInit():
    # This is the table 9x9
    table = fillTable()

    print("Bienvenido, este es el tablero inicial de GO")
    printTable(table)

    i = 0
    results = [0, 0, 0]  # [0] points *, [1] points -, [2] contPass
    while True:
        results = movement(table, i, results)  # Principal function
        i += 1  # Cont of turns for change player turn

        quantity = calcRocks(table)
        print("-- Resultados parciales --")
        print("Prisioneros para (*): ", results[0])
        print("Piedras de (*): ", quantity[0])
        print("Prisioneros para (-): ", results[1])
        print("Piedras de (-): ", quantity[1])
        print("--------------------------")
        if results[2] == 2:
            print("Pasaron turno dos veces seguidas, fin de la partida")

            if results[0] + quantity[0] > results[1] + quantity[1]:
                print("El jugador negro (*) ganó la partida!")
            elif results[0] + quantity[0] < results[1] + quantity[1]:
                print("El jugador blanco (-) ganó la partida!")
            else:
                print("Hubo un empate")
            break


def movement(table, turn, results):
    global column, row
    if turn % 2 == 0:
        print("\nMueve el jugador negro (*)")
        character = "*"
    else:
        print("\nMueve el jugador blanco (-)")
        character = "-"

    isPossible = True
    isLegal = True
    while isPossible:
        isLegal = False
        while not isLegal:
            position = input("Ingrese columna y fila (en blanco pasa turno): ")

            # Count of pass
            if len(position) == 0:
                results[2] += 1
                return results
            else:
                results[2] = 0

            # Get row and column from input
            if len(position) > 2:
                row = (int(position[1]) * 10) + (int(position[2])) - 1
            else:
                row = int(position[1]) - 1
                column = ord(position[0]) - 65

            # Verify possibilities
            if ROWS > row >= 0 and COLUMNS > column >= 0:
                if table[row][column] == "[ ]":
                    # Comprobar suicidio
                    table[row][column] = "[" + character + "]"  # Piedra temporal
                    chain = reviewChain(table, row, column, character, [[row, column]])

                    # si no tiene libertades seria un suicidio teorico
                    if not reviewChainLiberties(table, chain):
                        # Pero si mata a alguna ficha puede hacer la jugada
                        if reviewSides(table, row, column, character, results):
                            isPossible = False
                        else:  # En caso contrario no
                            table[row][column] = "[ ]"
                            print("En este juego no es divertido el suicidio!")
                    else:
                        table[row][column] = "[" + character + "]"
                        # Una vez colocado revisar si puede eliminar
                        reviewSides(table, row, column, character, results)
                        isPossible = False
                else:
                    print("Lugar ocupado!")
                isLegal = True
            else:
                print("Posicion fuera de los limites")

    printTable(table)
    return results


def calcRocks(table):
    quantity = [0, 0]
    for row in range(ROWS):
        for column in range(COLUMNS):
            if table[row][column] == "[*]":
                quantity[0] += 1
            elif table[row][column] == "[-]":
                quantity[1] += 1
    return quantity


def reviewSides(table, row, column, character, results):
    # Boolean for decide if is possible a suicide play
    canKill = False

    # Select the other character to review chains
    if character == "*":
        character = "-"
    else:
        character = "*"

    if row - 1 >= 0 and table[row - 1][column] == "[" + character + "]":  # Up
        chain = reviewChain(table, row - 1, column, character, [[row - 1, column]])
        if len(chain) > 0 and not reviewChainLiberties(table, chain):
            if character == "-":
                results[0] += len(chain)
            else:
                results[1] += len(chain)
            removeChain(table, chain)
            canKill = True

    if row + 1 < ROWS and table[row + 1][column] == "[" + character + "]":  # Down
        chain = reviewChain(table, row + 1, column, character, [[row + 1, column]])
        if len(chain) > 0 and not reviewChainLiberties(table, chain):
            if character == "-":
                results[0] += len(chain)
            else:
                results[1] += len(chain)
            removeChain(table, chain)
            canKill = True

    if column - 1 >= 0 and table[row][column - 1] == "[" + character + "]":  # Left
        chain = reviewChain(table, row, column - 1, character, [[row, column - 1]])
        if len(chain) > 0 and not reviewChainLiberties(table, chain):
            if character == "-":
                results[0] += len(chain)
            else:
                results[1] += len(chain)
            removeChain(table, chain)
            canKill = True

    if column + 1 < COLUMNS and table[row][column + 1] == "[" + character + "]":  # Right
        chain = reviewChain(table, row, column + 1, character, [[row, column + 1]])
        if len(chain) > 0 and not reviewChainLiberties(table, chain):
            if character == "-":
                results[0] += len(chain)
            else:
                results[1] += len(chain)
            removeChain(table, chain)
            canKill = True

    return canKill


def reviewChain(table, row, column, character, chain):  # Depth Search
    # Up, down, left, right
    if row - 1 >= 0 and table[row - 1][column] == "[" + character + "]":  # Up
        if not existsInChain(row - 1, column, chain):
            chain.append([row - 1, column])
            reviewChain(table, row - 1, column, character, chain)

    if row + 1 < ROWS and table[row + 1][column] == "[" + character + "]":  # Down
        if not existsInChain(row + 1, column, chain):
            chain.append([row + 1, column])
            reviewChain(table, row + 1, column, character, chain)

    if column - 1 >= 0 and table[row][column - 1] == "[" + character + "]":  # Left
        if not existsInChain(row, column - 1, chain):
            chain.append([row, column - 1])
            reviewChain(table, row, column - 1, character, chain)

    if column + 1 < COLUMNS and table[row][column + 1] == "[" + character + "]":  # Right
        if not existsInChain(row, column + 1, chain):
            chain.append([row, column + 1])
            reviewChain(table, row, column + 1, character, chain)

    return chain


def existsInChain(row, column, chain):
    for position in chain:
        if position[0] == row and position[1] == column:
            return True
    return False


def reviewNearBlank(table, row, column):  # Width Search
    # Up, down, left, right
    if row - 1 >= 0 and table[row - 1][column] == "[ ]":  # Up
        return True
    elif row + 1 < ROWS and table[row + 1][column] == "[ ]":  # Down
        return True
    elif column - 1 >= 0 and table[row][column - 1] == "[ ]":  # Left
        return True
    elif column + 1 < COLUMNS and table[row][column + 1] == "[ ]":  # Right
        return True
    else:
        return False


def reviewChainLiberties(table, chain):
    # Return liberties (True, False)
    # print(chain)
    for position in chain:
        if reviewNearBlank(table, position[0], position[1]):
            return True
    return False


def removeChain(table, chain):
    print("-- Hubo ", len(chain), "eliminaciones --")
    for position in chain:
        table[position[0]][position[1]] = "[ ]"


def printTable(table):
    columns_title = " "
    for i in range(COLUMNS):
        columns_title += "      " + chr(65 + i)

    print(columns_title)
    for i in range(ROWS):
        print(i + 1, " ", table[i])


def fillTable():
    table = []
    for i in range(ROWS):
        table.append(["[ ]"] * COLUMNS)
    return table


if __name__ == '__main__':
    goGameInit()
