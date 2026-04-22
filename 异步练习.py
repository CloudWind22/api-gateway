import asyncio
import time

#并发编程
async def task1():
    print("taks1 begins")
    await asyncio.sleep(1)
    print("task1 is finished")

async def task2():
    print("task2 begins")
    await asyncio.sleep(1)
    print("task2 is finisehd")

async def main():
    start = time.time()
    # await task1()
    # await asyncio.gather(task1(), task2())
    await asyncio.gather(*[task1() for _ in range(10)])
    print("2")
    print("whl")
    end = time.time()
    print(f"run about {end - start}s")

asyncio.run(main())




# #同步编程
# def task1():
#     print("task1 begins")
#     time.sleep(1)
#     print("task1 is finished")

# def task2():
#     print("task2 begins")
#     time.sleep(1)
#     print("task2 is finished")

# def main():
#     start = time.time()
#     task1()
#     task2()
#     end = time.time()
#     print(f"run about{end - start}s")

# main()