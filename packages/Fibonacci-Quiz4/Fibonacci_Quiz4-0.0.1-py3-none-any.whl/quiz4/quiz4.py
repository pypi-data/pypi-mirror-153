def fibonacci(n):
    sequencelist = [0]
    num1 = 0
    num2 = 1
    count = 0
    while count < 100:
        num3 = num1 + num2
        sequencelist.append(num3)
        num1 = num2
        num2 = num3
        count += 1
    return sequencelist[n-1]