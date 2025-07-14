# --------------
# import timeit
# def exec_time(func):
#     print(f'inside exec_time')
#     def wrapper(*args,**kwargs):
#         print(f'inside wrapper')
#         start_time = timeit.default_timer()
#         result = func(*args, **kwargs)
#         elapsed_time = timeit.default_timer() - start_time
#         print(f'inside wrapper, result: {result}, elapsed time: {elapsed_time}')
#         return result
#     return wrapper

# @exec_time
# def some_func(n):
#     print(f'inside some_func')
#     return sum([x for x in range(n)])

# some_func(1000000)

# --------------
# # How do you manage memory in Python? Discuss garbage collection and memory leaks
# # Memory management in Python is primarily handled through automatic garbage collection. Python uses a combination of reference counting and a cyclic garbage collector to manage memory.
# # Reference counting keeps track of the number of references to each object in memory. When an object's reference count drops to zero, it is immediately deallocated.
# # The cyclic garbage collector is responsible for detecting and collecting objects that are part of reference cycles, which reference counting alone cannot handle.
# # Memory leaks can occur if objects are referenced in a cycle, preventing their reference counts from reaching zero. To mitigate memory leaks, developers should ensure that circular references are broken when they are no longer needed, and they can use tools like `gc` module to manually trigger garbage collection or inspect objects in memory.
# # Additionally, using weak references (via the `weakref` module) can help avoid memory leaks by allowing objects to be collected even if they are still referenced by other objects, as weak references do not increase the reference count of the object.
# # give code example of garbage collection and memory leaks
# import gc
# class MyClass:
#     def __init__(self, name):
#         self.name = name
#         self.circular_ref = None

#     def __del__(self):
#         print(f"{self.name} is being deleted")
# def create_leak():
#     obj1 = MyClass("Object 1")
#     obj2 = MyClass("Object 2")
#     obj1.circular_ref = obj2
#     obj2.circular_ref = obj1  # Create a circular reference
#     return obj1, obj2

# def main():
#     obj1, obj2 = create_leak()
#     print("Objects created with circular references")
    
#     # At this point, obj1 and obj2 are still in memory due to the circular reference
#     print(f"obj1: {obj1.name}, obj2: {obj2.name}")

#     # Force garbage collection
#     gc.collect()
#     print("Garbage collection triggered")
#     # Check if objects are still in memory
#     if obj1 is not None and obj2 is not None:
#         print(f"Objects still exist: {obj1.circular_ref.name}, {obj2.circular_ref.name}")
#     else:
#         print("Objects have been collected")
# if __name__ == "__main__":
#     # gc.set_debug()  # Enable debug mode to track memory leaks
#     main()
#     gc.collect()  # Force garbage collection at the end
#     print("End of script")

# ---------
# # What are Python decorators? Give a real-world use case.
# # Python decorators are a powerful feature that allows you to modify or enhance the behavior of functions or methods without changing their code. A decorator is a function that takes another function as an argument, adds some functionality, and returns a new function.
# # Decorators are often used for logging, access control, memoization, and more. They can be applied using the `@decorator_name` syntax above the function definition.
# # A real-world use case of decorators is logging function execution time. This can be useful for performance monitoring and optimization.
# import time
# def execution_time_decorator(func):
#     def wrapper(*args, **kwargs):
#         start_time = time.time()
#         result = func(*args, **kwargs)
#         elapsed_time = time.time() - start_time
#         print(f"Function '{func.__name__}' executed in {elapsed_time:.4f} seconds")
#         return result
#     return wrapper
# @execution_time_decorator
# def example_function(n):
#     total = sum(range(n))
#     return total

# example_function(30)

# ----------
# How do you handle concurrency and parallelism in Python? Discuss threading, multiprocessing, and async.
# Concurrency and parallelism in Python can be handled using several approaches, each suited for different use cases:
# 1. **Threading**:
#    - Python's `threading` module allows you to run multiple threads (lightweight processes) within a single process. This is useful for I/O-bound tasks, such as network requests or file I/O, where threads can run concurrently while waiting for I/O operations to complete.
#    - However, due to the Global Interpreter Lock (GIL), Python threads cannot execute Python bytecode in parallel. This means that CPU-bound tasks may not benefit from threading as much as I/O-bound tasks do.

# import threading
# def thread_func(num):
#     print(f"Thread {num} is starting")
#     # Simulate some work
#     import time
#     time.sleep(num)
#     print(f"Thread {num} is finishing")

# thread1 = threading.Thread(target=thread_func, args=(1,))
# thread2 = threading.Thread(target=thread_func, args=(2,))
# thread1.start()
# thread2.start()
# thread1.join()
# thread2.join()
# # 2. **Multiprocessing**:
# #    - The `multiprocessing` module allows you to create separate processes, each with its own Python interpreter and memory space. This is useful for CPU-bound tasks that can benefit from parallel execution, as it bypasses the GIL.
# #    - Each process can run on a separate CPU core, allowing true parallelism for CPU-bound tasks.
# import multiprocessing
# def process_func(num):
#     print(f"Process {num} is starting")
#     # Simulate some work
#     import time
#     time.sleep(num)
#     print(f"Process {num} is finishing")
# if __name__ == "__main__":
#     process1 = multiprocessing.Process(target=process_func, args=(1,))
#     process2 = multiprocessing.Process(target=process_func, args=(2,))
#     process1.start()
#     process2.start()
#     process1.join()
#     process2.join()

# # 3. **Asyncio**:
# #    - The `asyncio` module provides a framework for writing asynchronous code using coroutines. It is particularly useful for I/O-bound tasks, such as network requests, where you can use `await` to yield control while waiting for I/O operations to complete.
# import asyncio
# async def async_func(num):
#     print(f"Async task {num} is starting")
#     await asyncio.sleep(num)  # Simulate some asynchronous work
#     print(f"Async task {num} is finishing")
# async def main():
#     await asyncio.gather(async_func(1), async_func(2))
# asyncio.run(main())

# Explain the Global Interpreter Lock (GIL) and its impact on multi-threaded programs.
# The Global Interpreter Lock (GIL) is a mutex that protects access to Python objects, preventing multiple native threads from executing Python bytecodes simultaneously. This means that even in a multi-threaded program, only one thread can execute Python code at a time.
# The GIL can be a bottleneck in CPU-bound programs, as it limits the parallelism that can be achieved with threads. However, it simplifies memory management and eliminates the need for fine-grained locking in many cases.
# In I/O-bound programs, the impact of the GIL is less pronounced, as threads can release the GIL while waiting for I/O operations to complete, allowing other threads to run.
# In CPU-bound programs, using the `multiprocessing` module is often recommended to achieve true parallelism by creating separate processes that can run on multiple CPU cores, bypassing the GIL.

# How do you optimize Python code for performance?
# 1. **Use Built-in Functions and Libraries**: Python's built-in functions (like `map`, `filter`, and `sum`) are implemented in C and are generally faster than equivalent Python code. Leveraging libraries like NumPy for numerical computations can also lead to significant performance improvements.
# 2. **Profile Your Code**: Use profiling tools (like cProfile or line_profiler) to identify bottlenecks in your code. Focus your optimization efforts on the parts of the code that consume the most time.
# 3. **Avoid Global Variables**: Accessing global variables is slower than accessing local variables. If possible, pass variables as parameters to functions instead of relying on globals.
# 4. **Use Generators**: For large datasets, consider using generators instead of lists to reduce memory consumption and improve performance.
# 5. **Optimize Algorithms**: Sometimes, the best way to improve performance is to use a more efficient algorithm or data structure. Analyze the time complexity of your code and look for opportunities to optimize.

# example of map, filter, and sum
# def square(x):
#     return x * x
# numbers = [1, 2, 3, 4, 5]
# squared_numbers = list(map(square, numbers))


# write code to compare performance of list with generator
# measure_time as decorator

import time

# def measure_time(func):
#     def wrapper(n):
#         start_time = time.time()
#         result = func(n)
#         elapsed_time = time.time() - start_time
#         return result, elapsed_time
#     return wrapper
# # use measure_time as decorator

# @measure_time
# def list_comprehension(n):
#     return [x * x for x in range(n)]
# @measure_time
# def generator_expression(n):
#     return (x * x for x in range(n))

# n = 1000000
# list_result, list_time = list_comprehension(n)
# generator_result, generator_time = generator_expression(n)
# print(f"List comprehension took {list_time:.4f} seconds, result length: {len(list_result)}")
# print(f"Generator expression took {generator_time:.4f} seconds, result length: {sum(1 for _ in generator_result)}")

