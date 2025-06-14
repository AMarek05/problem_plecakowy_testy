from sys import argv
from random import randint

def indeksy(wej):
    wej.pop(0)
    for i in range(len(wej)):
        wej[i].append(i+1)
    return wej

def alg_AD(wej, licz_elem, rozmiar):
    macierz_PD=[[0 for _ in range(rozmiar+1)] for _ in range(licz_elem+1)]
    macierz_decyzji=[[0 for _ in range(rozmiar+1)] for _ in range(licz_elem+1)]
    wybrane_przedmioty=[]
    for i in range(1,licz_elem+1):
        for j in range(1,rozmiar+1):
            if wej[i-1][0]>j:
                macierz_PD[i][j]=macierz_PD[i-1][j]
            else:
                macierz_PD[i][j]=max(macierz_PD[i-1][j],(macierz_PD[i-1][j-wej[i-1][0]]+wej[i-1][1]))
                if max(macierz_PD[i-1][j],(macierz_PD[i-1][j-wej[i-1][0]]+wej[i-1][1]))==(macierz_PD[i-1][j-wej[i-1][0]]+wej[i-1][1]):
                    macierz_decyzji[i][j]=1
    print(macierz_PD)
    print(macierz_decyzji)
    x=licz_elem
    y=rozmiar
    while x>0 and y>0:
        if macierz_decyzji[x][y]==1:
            wybrane_przedmioty.append(x)
            y=y-wej[x-1][0]
            x-=1
        else:
            x-=1
    wynik=macierz_PD[licz_elem][rozmiar]
    print("\nWartość uzyskana: \n"+str(wynik))
    print("Indeksy przedmiotów umieszczonych w plecaku(zaczynając od 1): \n"+str(wybrane_przedmioty))
    return wynik

def alg_AZ(wej,licz_elem,rozmiar):
    oryg_rozm = rozmiar
    rozmiar2=rozmiar
    indeksy=[]
    suma=0
    wej.sort(key=lambda x: x[1]/x[0],reverse=True)
    print(wej)
    for i in range(len(wej)):
        rozmiar2=rozmiar-wej[i][0]
        if rozmiar2>0:
            rozmiar=rozmiar2
            indeksy.append(wej[i][2])
            suma+=wej[i][1]
        elif rozmiar2==0:
            rozmiar=0
            indeksy.append(wej[i][2])
            suma+=wej[i][1]
            break
        else:
            continue
    if alg_AD(wej,licz_elem,oryg_rozm)==suma:
        print("Algorytm optymalny dla danego przypadku")
    else:
        print("Algorytm suboptymalny dla danego przypadku")
    print("\nWartość uzyskana: \n"+str(suma))
    print("Indeksy przedmiotów umieszczonych w plecaku(zaczynając od 1): \n"+str(indeksy))

def alg_AB(wej,licz_elem,rozmiar):
    maksymalne=0
    najlepsze_rozwiazanie=[]
    wybrane_przedmioty=[]
    for X in range(1,2**licz_elem):  # pomijamy pusty zestaw (X = 0)
        kombinacja=[int(bit) for bit in bin(X)[2:].zfill(licz_elem)]
        suma_rozmiarow=0
        suma_wartosci=0
        przedmioty=[]
        for i in range(licz_elem):
            if kombinacja[i]==1:
                suma_rozmiarow+=wej[i][0]
                suma_wartosci+=wej[i][1]
                przedmioty.append(wej[i][2])
        if suma_rozmiarow<=rozmiar and suma_wartosci>maksymalne:
            maksymalne=suma_wartosci
            najlepsze_rozwiazanie=kombinacja
            wybrane_przedmioty=przedmioty
    print("Maksymalna wartość:",maksymalne)
    print("Wybrane przedmioty (indeksy):", wybrane_przedmioty)

def gen_lista(num, poj):
    lista = [(num,poj)]
    for _ in range(num):
        rozm=randint(1, 20)
        wart=randint(1,50)
        lista.append((rozm, wart))
    return lista

def main():
    if (len(argv) == 4):
        num = int(argv[1])
        m = int(argv[3]) # który algorytm używamy
        if (int(argv[2]) == 1): # Jeżeli drugi argument pozycyjny == 1 => poprzednia wartość to pojemność, 2 => liczba przedmiotów, inna liczba to pojemność plecaka, a poprzednia to liczba przedmiotów
            rozmiar = num
            licz_elem = 1000
        elif(int(argv[2] == 2)):
            licz_elem = num
            rozmiar = 1000
        else:
            licz_elem = num
            rozmiar = argv[3]
        wej = gen_lista(rozmiar, licz_elem)
    else:
        wej=[]
        print("===WYBÓR PODAWANIA DANYCH===")
        print("Podaj w jaki sposób podasz dane wejściowe:\n1. Plik tekstowy\n2. Wpisywanie ręczne\n0. Wyjście")
        n=int(input("Liczba(0-2):"))
        print("===WYBÓR ALGORYTMU===")
        print("Podaj algorytm roziwązywania problemu plecakowego 0-1:\n1. Algorytm programowania dynamicznego\n2. Algorytm zachłanny\n3. Algorytm siłowy\n0. Wyjście")
        m=int(input("Liczba(0-3):"))
        match(n):
            case 0:
                exit(0)
            case 1:
                f=open("c.txt","r")
                for i in f:
                    wej.append(list(map(int,i.split())))
            case 2:
                print("Podaj dane tak że: pierwszy wiersz to para liczb n b (liczba przedmiotów, pojemność plecaka),\n kolejne wiersze to pary liczb r w (rozmiar przedmiotu, wartość przedmiotu).\n Spacja jest separatorem liczb w pojedynczej linii.:\n")
                i,j=map(int,input().split())
                wej.append([i,j])
                for k in range(i):
                    wej.append(list(map(int,input().split())))
            case _:
                print("Bład! Podałeś liczbę z poza zakresu 0-2.")
        licz_elem=wej[0][0]
        rozmiar=wej[0][1]
    wej=indeksy(wej)
    match(m):
            case 1:
                alg_AD(wej,licz_elem,rozmiar)
            case 2:
                alg_AZ(wej,licz_elem,rozmiar)
            case 3:
                alg_AB(wej,licz_elem,rozmiar)
            case _:
                    print("Bład! Podałeś liczbę z poza zakresu 0-2.") 

if __name__ == "__main__":
    main()
