T = float(input())
D = float(input())

def Post_Limit():
    if 0 <= T < 1: 
        T_limit = T + 0.4
        print(f"T = {T_limit}")
    if 0 <= D < 1:
        D_limit = D + 0.4
        print(f"D = {D_limit}")
    if 1 <= T <= 2:
        T_limit = T + 0.7
        print(f"T = {T_limit}")
    if 1 <= D <= 2:
        D_limit = D + 0.7
        print(f"D = {D_limit}")
    if 2 < T <= 10:
        T_limit = T + 1
        print(f"T = {T_limit}")
    if 2 < D <= 10:
        D_limit = D + 1
        print(f"D = {D_limit}")

Post_Limit()
    