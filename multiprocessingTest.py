# import time

# start_time = time.time()

# def fibo(n): # 회귀적 피보나치 함수
#     if n == 0:
#         return 0
#     elif n == 1:
#         return 1
#     else:
#         return fibo(n-1) + fibo(n-2)

# num_list = [31, 32, 33, 34]
# result_list = []
# for num in num_list:
#     result_list.append(fibo(num))

# print(result_list)
# print("--- %s seconds ---" % (time.time() - start_time))

from multiprocessing import Pool
import time

start_time = time.time()


def fibo(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibo(n-1) + fibo(n-2)


def print_fibo(n):  # 피보나치 결과를 확인합니다.
    print(fibo(n))


num_list = [30, 31, 32, 33, 34]

if __name__ == '__main__':
    start_time = time.time()
    pool = Pool(processes=4)  # 4개의 프로세스를 사용합니다.
    f = pool.map(fibo, num_list)  # pool에 일을 던져줍니다.
    # result_list = []
    # for num in num_list:
    #     print(fibo(num))
    print("--- %s seconds ---" % (time.time() - start_time))
