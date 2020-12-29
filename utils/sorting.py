
def merge(list,start, end, mid,*, key, cmp):
    """
    Realizeaza interclasarea celor doua jumatati dupa operatorul si key-ul specificat
    :param list: lista de obiecte
    :param start: inceputul secventei - int
    :param mid: mijlocul secventei - int
    :param end: sfarsitul secventei - int
    :param operator: functie reprezentand operatorul - function()
    :param key: functia care returneaza cheia dupa care se face sortarea
    """
    i = j = 0
    k = start
    left = list[start:mid]
    right = list[mid:end]

    while i < len(left) and j < len(right):
        if cmp(key(left[i]), key(right[j])):
            list[k] = left[i]
            i += 1
        else:
            list[k] = right[j]
            j += 1
        k += 1


    while i < len(left):
        list[k] = left[i]
        i += 1
        k +=1

    while j < len(right):
        list[k] = right[j]
        j += 1
        k += 1


def mergeSort(list,start, end, *, key = lambda obj: obj, reverse = False, cmp = lambda x,y: x<y):
    """
    Functia sorteaza lista list dupa criteriul key in ordinea specificata de reverse prin metoda merge sort
    :param list: lista de obiecte
    :param key: key-ul dupa care se realizeaza sortarea
    :param reverse: ordinea in care se realizeaza sortarea - default: False
    """

    if end - start <=1:
        return
    mid = (start + end) // 2
    mergeSort(list, start, mid, key=key, cmp=cmp)
    mergeSort(list, mid, end, key=key, cmp=cmp)
    merge(list, start, end, mid, key=key, cmp=cmp)

    if reverse:
        list.reverse()


def bingoSort(list, *, key=lambda obj: obj.getName(), reverse = False, cmp = lambda x,y :x>y):
    """
    Functia sorteaza lista list dupa criteriul key in ordinea specificata de reverse dupa algoritmul bingo sort
    :param list: lista de obiecte
    :param key: criteriu de sortare - function()
    :param reverse: ordine - bool
    """


    max = len(list)-1
    next = list[max]

    #we search for the current max value
    for i in range(max-1, -1, -1):
        if cmp(key(list[i]), key(next)):
            next = list[i]

    while max > 0 and key(list[max]) == key(next):
        max -=1

    while max > 0:
        current = next
        next = list[max]
        for i in range(max-1, -1, -1):
            if key(list[i]) == key(current):
                aux = list[i]
                list[i] = list[max]
                list[max] = aux
                max -=1
            elif cmp(key(list[i]), key(next)):
                next = list[i]

        while max > 0 and key(list[max]) == key(next):
            max -= 1
    if reverse:
        list.reverse()
        pass

def sort2keys(list, *, key1 = lambda x:x, key2=lambda x:x):
    """Sorteaza lista dupa cele doua criterry key1 si key2. Daca key1(x) == key1(y) se sorteaza dupa key2"""
    for i in range(0, len(list)-1):
        for j in range(i+1, len(list)):
            if key1(list[i]) > key1(list[j]) or (key1(list[i]) == key1(list[j]) and key2(list[i]) > key2(list[j])):
                aux = list[i]
                list[i]=list[j]
                list[j] = aux

