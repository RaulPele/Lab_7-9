
def merge(list,start, end, mid,*, key, operator):
    """
    Realizeaza interclasarea celor doua jumatati dupa operatorul si key-ul specificat
    :param list: lista de obiecte
    :param start: inceputul secventei - int
    :param mid: mijlocul secventei - int
    :param end: sfarsitul secventei - int
    :param operator: functie reprezentand operatorul - function()
    :param key: functia care returneaza cheia dupa care se face sortarea
    :return sortedList: lista rezultata in urma interclasarii
    """
    i=j=k=0
    left = list[start:mid]
    right =list[mid:end]

    while i<len(left) and j <len(right):
        if operator(key(left[i]), key(right[j])):
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


def mergeSort(list,start, end, *, key = lambda obj:obj.getName(), reverse = False):
    """
    Functia sorteaza lista list dupa criteriul key in ordinea specificata de reverse prin metoda merge sort
    :param list: lista de obiecte
    :param key: key-ul dupa care se realizeaza sortarea
    :param reverse: ordinea in care se realizeaza sortarea - default: False
    :return sortedList: lista sortata
    """
    operator = lambda x,y : x < y
    if reverse:
        operator = lambda x,y: x > y

    if end - start <= 1:
        return
    mid = (start + end) // 2
    mergeSort(list, start, mid, key=key, reverse=reverse)
    mergeSort(list, mid+1, end, key=key, reverse=reverse)
    #print(operator(key(list[1]), key(list[2])))

    merge(list, start, end, mid, key=key, operator=operator)


def bingoSort(list, *, key = lambda obj: obj.getName(), reverse = False):
    operator = lambda x, y: x > y
    if reverse:
        operator = lambda x, y: x < y

    max = len(list)-1
    next = list[max]

    #we search for the current max value
    for i in range(max-1, -1, -1):
        if operator(key(list[i]), key(next)):
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
            elif operator(key(list[i]), key(next)):
                next = list[i]

        while max > 0 and key(list[max]) == key(next):
            max -= 1
