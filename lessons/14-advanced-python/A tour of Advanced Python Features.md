# A tour of Advanced Python Features

[TOC]




## Higher Order Functions

Python treats functions as ''first class objects".  Which means:

- functions are objects
- you can store them in a variable
- you can pass them as parameters to other functions
- you can return a function from a function
- you can store them in data structures (lists, dicts, etc.)


Basically, you can treat funtions just like regular objects.


Examples:

Python functions are objects:

```python
def add(a, b):
    return a + b

isinstance(add, object) # True
```

They are simply stored in a variable

```python
# continuing from above
plus = add
plus(3, 4) # 7
plus is add # True
plus.__name__ # 'add'
```



you can pass them as parameters

```python
numbers = [1, 3, -4, 2, -1, -3, 4]
sorted(numbers) # [-4, -3, -1, 1, 2, 3, 4]

abs(-3) # 3
abs(3)  # 3

[abs(num) for num in numbers] # [1, 3, 4, 2, 1, 3, 4]

sorted([abs(num) for num in numbers]) # [1, 1, 2, 3, 3, 4, 4]

sorted(numbers, key=abs) # [1, -1, 2, 3, -3, -4, 4]

###########

final_grades = {'Billy': 60, 'Bob': 85, 'Heidi': 70, 'Martin': 78, 'Sue': 63, 'Tom': 91}

# sorts alphabetically by key
sorted(final_grades) # ['Billy', 'Bob', 'Heidi', 'Martin', 'Sue', 'Tom']

# sorts by final grade (ascending)
sorted(final_grades, key=final_grades.get) # ['Billy', 'Sue', 'Heidi', 'Martin', 'Bob', 'Tom']


```



you can return them from a function

```python
def makeadder(first):
    def add_num(second):
        return first + second
    return add_num

add3 = makeadder(3)
add7 = makeadder(7)

add3(3) # 6
add3(10) # 16

add7(3) # 10
add7(7) # 14
```

You can store them in data structures

```python
def whisper(text):
    return "(" + text.lower() + ")"

def shout(text):
    return text.upper()

def say(text):
    return text

funcs = [whisper, shout, say]

for i in range(3):
    new_message = funcs[i]('Hello There')
    print(new_message)
```



## Generators

A fuller resource: https://jeffknupp.com/blog/2013/04/07/improve-your-python-yield-and-generators-explained/



In Python, functions start executing when they are called, continue running until a `return`, an error, or the end of the function is reached.  Then the function is done.  Functions can only ever return *once*.

```python
def silly_function():
    return 'This will be seen'
	return 'This will never be seen'

silly_function() # 'This will be seen'
```



In python **Generators** are types of functions that may 'return' multiple times.  To do this, we use the **yield** keyword instead of **return**.  In essence, a generator returns a *sequence* of values, - just like iterables!



```python
def silly_generator():
    yield 'This will be seen'
    yield 'This will also be seen'

silly_generator() # <generator object silly_generator at 0x1054e6830>

# we must use the generator as an iterable.

for value in silly_generator():
    print(value)
    #  This will be seen
    #  This will also be seen
```



This is useful if you don't want to store the whole collection of returned values in memory, or you don't need to compute the whole collection of values every time.



Reducing memory consumption:

```python
def size_in_kilobytes(thing):
    from sys import getsizeof
    return getsizeof(thing) / 1000

big_list = list(range(1000000)) # 1 million digits
lazy_list = range(10000000)

size_in_kilobytes(big_list) # 9000.112, ~9 MB
size_in_kilobytes(lazy_list) # 0.048

sum(big_list) # 499999500000
sum(lazy_list) # 499999500000

```



Here, we define a generator which loops forever, yielding the numbers of the fibonnaci sequence.  We allow the person consuming the generator to decide when to stop the loop.  In this case, we just want the numbers less than 10,000.

```python
def fibonacci_generator():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b
        
# Getting a list of fibonnaci numbers < 10000
for fib in fibonacci_generator():
    if fib >= 10000:
        break
    print(fib)

```



## Generator Expressions

Just like list, set, and dictionary comprehensions, we can create a generator using our comprehension syntax.  These are called **generator expressions**.  Unlike our generator functions, they may be only iterated over once.

```python
squares = (x**2 for x in range(200))
# calling `next` on any iterable object (like a generator) manually iterates it 1 'step'
next(squares) # 0
next(squares) # 1
next(squares) # 4

# squares is a generator
repr(squares) # <generator object <genexpr> at 0x1029c9468>
sum(squares) # 2646695

# the generator is now fully consumed
next(squares) # StopIteration Error is raised

```



You can also pass generator objects directly into functions that consume them.  Just use a comprehension as you normally would but leave off the surrounding `[` or `{`:

```python
sum(x**2 for x in range(200)) # 2646700
```

Generators can be quite useful when chained.  In this example, we'll use generators to efficently find the first fibonacci number whose digits add up to **13**:

```python
def fibonacci_generator():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b
        
# convert each fib number to string
nums_as_strings = (str(num) for num in fibonacci_generator())
# convert the string into a list of integers
digits_as_ints = ([int(digit) for digit in num] for num in nums_as_strings)
# convert back to string *only* if the digits sum to 13.
only_17s = (''.join(str(digit) for digit in num) 
            for num in digits_as_ints 
            if sum(num) == 17
           )

# Get the first one
next(only_17s)
```





## Properties

Python supports methods that act like attributes.   That is, you can use `custom_object.foo` rather than `custom_object.foo()`.  This allows you to write functions that act as attributes on the original object.  To do this, you use the `@property` decorator

This is the *pythonic* way of writing the `get_fullname` and `set_fullname` helper methods you may see in other languages. 

 For example:

```python
class Person:
       def __init__(self, first_name, last_name):
           self.first_name = first_name
           self.last_name = last_name

       @property
       def full_name(self):
           return "{0} {1}".format(self.first_name, self.last_name)

       @full_name.setter
       def full_name(self, name):
           first, last = name.split(' ')
           self.first_name = first
           self.last_name = last

# Now we can use person.fullname like its an attribute

p = Person('Bob', 'Dole')
p.first_name # 'Bob'
p.last_name # 'Dole'
p.full_name # 'Bob Dole'
p.full_name = 'Kit Harrington' # @setter function lets us do this

p.full_name # 'Kit Harrington'
p.first_name # 'Kit'
p.last_name # 'Harrington'
```



## Decorators

More reading: https://www.thecodeship.com/patterns/guide-to-python-function-decorators/

A decorator is simply a python function which takes a single function as an argument and returns a function.  They are used to alter, extend, or register functions **when they are defined**.  

The following are equivalent:

```python
def add(a, b):
    return a + b

add = decorator_function(add)
```

```python
@decorator_function
def add(a, b):
    return a + b
```



Here's a simple decorator which prints out the name of the function and its arguments each time the original function is called.

```python
def print_on_call(original_function):
    def replacement_function(*args, **kwargs):
        message = "'{}' called with args: {}  kwargs: {}".format(original_function.__name__, args, kwargs)
        print(message)
        # return the value of calling the original function
        return original_function(*args, **kwargs)
    return replacement_function

@print_on_call
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

subtract = print_on_call(subtract)


x = add(10, 20) # 'add' called with args: (10, 20)  kwargs:
print(x) # 30

y = subtract(70, 30) # 'subtract' called with args: (70, 30)  kwargs:
print(y) # 40
```

They can be much more complicated than this, but the takeaway is the same - they do something with the wrapped function as soon as its defined - usually replacing them with a new function which calls the original function, in addition to some other things (in this case, printing the function's name and arguments.).





## Context Managers

These you will use the least, simply because they are a nice tool.   We've seen context managers before, specifically when working with files.  They take the form:

```python
with context_manager() as variable_name:
    # do thing with variable_name
```

Under the hood, decorators call `__enter__` when first invoked, and `__exit__` when your block of code is completed.  They handle set up and teardown, and are most commonly used when you have some specific operations both *before* and *after* some other chunk of code.  With files:



```python
with open('some_file', 'w') as f:
    f.write('hello')
```

is the same as

```python
f = open('some_file', 'w')
f.write('hello')
f.close()
```

The context manager of `open` handles the `close` method call for you automatically.



#### Example

- a very simple context manager class which prints when it starts and ends

```python
class SillyManager():
	def __enter__(self):
		print('Context manager initiated')
	def __exit__(self, type, value, traceback):
		print('context manager over')
        
        
with SillyManager():
    print('my block of code')
  
### prints the following:
# Context manager initiated
# my block of code
# context manager over"
```

A more useful timer example:



```python
from time import time


class Timer():
    def __init__(self, message):
        self.message = message

    def __enter__(self):
        self.start = time()
        return None  # could return anything, to be used like this: with Timer("Message") as value:

    def __exit__(self, type, value, traceback):
        elapsed_time = (time() - self.start) * 1000
        print(self.message.format(elapsed_time))

        
with Timer('time for summing squares up to 100: {}ms'):
	sum(x**2 for x in range(100))
# time for summing squares up to 100: 0.10395050048828125ms
```



For simple context managers, you can use the `@contextmanager` decorator to write your context manager as a single function.



```python
from time import time
from contextlib import contextmanager

@contextmanager
def timer(message):
	start = time()
	yield
	elapsed_time = (time() - start) * 1000
	print(message.format(elapsed_time))
    
with timer('time for summing squares up to 100: {}ms'):
	sum(x**2 for x in range(100))
# time for summing squares up to 100: 0.051975250244140625ms
```

