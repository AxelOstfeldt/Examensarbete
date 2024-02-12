k = 3

test_code ="101001"

while len(test_code) > 0:
    test_value =""
    for j in range(k):
        test_value += test_code[0]
        test_code = test_code[1:]
    print(test_value)