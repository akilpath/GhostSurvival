def main():
    t = int(input())
    for case in range(1,t+1):
        nb = input()
        nb = nb.split()
        n = nb[0]
        b = nb[1]
        prices = str(input()).split()
        prices = [int(num) for num in prices]
        prices.sort()
        
        
        
        print(f"Case #{case}: {output(n,b,prices)}")
        

def output(n,b,prices):
    b = int(b)
    y = 0
    for i in range(int(n)):
        print(i)
        print(y)
        if b - int(prices[i]) < 0:
            return y
        else: 
            b -= int(prices[i])
            y += 1
    return y

main()