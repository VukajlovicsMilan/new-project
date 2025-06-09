def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Hiba: Nullával nem lehet osztani!"
    return a / b

if __name__ == "__main__":
    print("Egyszerű számológép")
    print("Összeg: ", add(5, 3))
    print("Különbség: ", subtract(5, 3))
    print("Szorzás: ", multiply(5, 3))
    print("Osztás: ", divide(5, 3))
