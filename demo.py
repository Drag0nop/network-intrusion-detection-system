def closest_number(n, m):
    # First closest multiple
    q = n // m
    a = q * m
    b = (q + 1) * m

    diff1 = abs(n - a)
    diff2 = abs(n - b)

    if diff1 < diff2:
        return a
    elif diff2 < diff1:
        return b
    else:
        # If tie, choose the one with maximum absolute value
        return a if abs(a) > abs(b) else b
# Example usage
n = 13
m = 4
result = closest_number(n, m)
print(f"The closest number to {n} that is a multiple of {m} is {result}.")

# function to convert decimal to binary
def decToBinary(n):
    binArr = []

    while n > 0:
        bit = n % 2
        binArr.append(str(bit))
        n //= 2

    # reverse the string
    binArr.reverse()
    return "".join(binArr)

if __name__ == "__main__":
    n = 12
    print(decToBinary(n))