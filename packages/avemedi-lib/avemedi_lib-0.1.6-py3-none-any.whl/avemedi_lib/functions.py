
def count(a: list) -> int:
    """
    Return count number of items in a list.

    :param a: numbers list
    """
    if len(a) == 0:
        return 0
    else:
        return 1 + count(a[1:])  # [1:] means from second item to the end


def quicksort(a: list) -> list:
    """
    Fast quick sort. Return sorted list.

    :param a: numbers list
    """

    if count(a) < 2:
        return a
    else:
        pivot = a[0]
        less = [i for i in a[1:] if i <= pivot]
        greater = [i for i in a[1:] if i > pivot]
        return quicksort(less) + [pivot] + quicksort(greater)


def average(a: list) -> list:
    """
    Return average value of numbers list.

    :param a: numbers list
    """
    n = count(a)

    if n == 1:
        return a[0]
    else:
        mid = n // 2
        return (mid * average(a[:mid]) + (n - mid) * average(a[mid:])) / n


def get_median_custom(a: list, n: int) -> float:
    """
    Calculate median value of a ordered numbers list with custom list len().

    :param a: numbers list
    :param n: length of list
    """

    if n % 2 != 0:
        return float(a[int(n/2)])

    return float((a[int((n-1)/2)] + a[int(n/2)])/2.0)


def get_median(a: list) -> float:
    """
    Return median value for ordered or unordered numbers list.

    :param a: numbers list
    """
    n = count(a)
    s = quicksort(a)

    return get_median_custom(s, n)
