class RiceCoding:

    def __init__(self, k, sign):
        self.k = k
        self.sign = sign

    def Encode(self, n):

        if self.sign:
            if n < 0:
                s = "1"
                n = -n
            else:
                s = "0"
        n = bin(n)[2:]

        r = n[len(n)-self.k:]
        n = n[:len(n)-self.k]
        n = int(n,2)
        r = "0" + r
        for i in range(n):
            r = "1" + r

        if self.sign:
            r = s + r

        return r
    
    def Decode(self, code):
        
        A = 0
        if self.sign:
            if code[0] == "1":
                S = "1"
            code = code[1:]
        
        while code[0] == "1":
            A += 1
            code = code[1:]
        
        code = code[1:]

        A = A + int(code, 2)

        return code
    

            
        

#Test
    
Rice_coder = RiceCoding(7, False)

kodOrd = Rice_coder.Encode(5)

print("kod ord: ",kodOrd)

value = Rice_coder.Decode(kodOrd)

print("Value: ", value)