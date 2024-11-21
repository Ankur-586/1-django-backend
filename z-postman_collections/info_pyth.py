'''
0. List Comprehensions:
   -------------------
List comprehensions provide a concise way to create lists. They are faster and more readable than traditional loops.

Example:
#List Comprehensions
squares = [x**2 for x in range(1, 11)]
print(squares)
Output:
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
Here, we are generating a list of squares for numbers from 1 to 10. Instead of using multiple lines with a loop and an append method, 
list comprehension handles everything in one line. It's especially useful when you need to perform simple transformations on lists.

1. Calculating Factorials
   ---------------------
Python's reduce() function allows you to calculate the factorial of a number in a single line.

# Calculating Factorials
from functools import reduce
factorial = reduce(lambda x, y: x * y, range(1, 6))
print(factorial)
Output:
120
This one-liner calculates the factorial of a number using reduce(), providing a concise way to perform iterative multiplications.

2. Lambda Functions for Sorting
   ----------------------------
Lambda functions are anonymous functions you can use in-line, ideal for tasks like sorting.

Example:
# Lambda Functions for Sorting
tuples_list = [(1, 'a'), (3, 'c'), (2, 'b')]
sorted_list = sorted(tuples_list, key=lambda x: x[1])
print(sorted_list)
Output:
[(1, 'a'), (2, 'b'), (3, 'c')]
Here, we are sorting a list of tuples based on the second element (in this case, the letters). 
Similarly, by using a lambda function as the key, we can also sort a dictionary based on its values.

3. Merging Two Dictionaries
   ----------------------------
Python's dictionary comprehension makes merging two dictionaries a breeze.

Example:
# Merging Two Dictionaries
dict1 = {'a': 1, 'b': 2}
dict2 = {'c': 3, 'd': 4}
merged_dict = {**dict1, **dict2}
print(merged_dict)
Output:
{'a': 1, 'b': 2, 'c': 3, 'd': 4}
This one-liner merges two dictionaries into one. It's a handy way to combine multiple dictionaries without using loops or additional functions.

4. Dictionary Comprehension
   ------------------------
Dictionary comprehensions allow for the quick creation of dictionaries from iterables.

Example:
# Dictionary Comprehension
keys = ['a', 'b', 'c']
values = [1, 2, 3]
dict_from_lists = {keys[i]: values[i] for i in range(len(keys))}
print(dict_from_lists)
Output:
{'a': 1, 'b': 2, 'c': 3}
Here, we are creating a dictionary from two lists, keys and values. Each element of keysbecomes a 
key, and the corresponding element of values becomes the associated value.

5. Finding the Maximum Value in a Dictionary
   ----------------------------------------
Python makes it easy to find the maximum value in a dictionary.

Example:
# Maximum Value in a Dictionary
max_key = max({'a': 1, 'b': 2, 'c': 3}, key=lambda k: k[1])
print(max_key)
Output:
'c'
This one-liner finds the key with the maximum value in a dictionary, which can be useful in tasks like finding the best-performing item in a dataset.

6. Checking for Substring Presence
   -------------------------------
Checking if a substring exists within a string can be done in a single, intuitive line.

Example:
# Checking for Substring Presence
contains = "Python" in "I love Python programming"
print(contains)
Output:
True
This one-liner checks if a substring exists within a string, making it useful for tasks like searching or filtering text.

7. Palindrome Check with Slicing
   ----------------------------
You can check if a string is a palindrome by reversing it with slicing.

Example:
# Palindrome Check with Slicing
is_palindrome = lambda s: s == s[::-1]
print(is_palindrome("radar"))
Output:
True
Here, this one-liner checks if a given string is a palindrome. The slicing operation s[::-1] reverses the string,
and the lambda function compares it with the original string.

8. Inverting a Dictionary
   -----------------------
Sometimes we need to invert a dictionary, swapping keys and values. Python's dictionary comprehension handles this task elegantly.

Example:
# Inverting a Dictionary
inverted_dict = {v: k for k, v in {'a': 1, 'b': 2, 'c': 3}.items()}
print(inverted_dict)
Output:
{1: 'a', 2: 'b', 3: 'c'}
Here, this one-liner inverts a dictionary by swapping keys and values, which is often required in scenarios like reverse lookups.

9. Pairing Elements with zip()
   ----------------------------
This zip() function pairs elements from multiple lists into tuples, simplifying the creation of combined datasets.

Example:
# Pairing Elements with zip()
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
name_age_pairs = list(zip(names, ages))
print(name_age_pairs)
Output:
[('Alice', 25), ('Bob', 30), ('Charlie', 35)]
This one-liner combines two lists, names and ages, into a list of tuples, where each tuple contains one element from each list.
The zip() function is invaluable when we need to merge data from different sources.

10. Finding the Intersection of Two Lists
    ------------------------------------
Calculating the intersection of two lists can be done effortlessly with set operations.

Example:
# Finding the Intersection of Two Lists
intersection = list(set([1, 2, 3]) & set([2, 3, 4]))
print(intersection)
Oytput:
[2, 3]
Here, this one-liner finds the common elements between two lists using set intersection, a useful operation in data comparison tasks.

11. Conditional Checks with any() and all()
    ---------------------------------------
any() and all() are useful for checking conditions across collections.
Example:
# Conditional Checks with any() and all()
values = [1, 2, 3, 4]
has_greater = any(x > 3 for x in values)
all_positive = all(x > 0 for x in values)
print(has_greater, all_positive)
Output:
True True
Here, the first one-liner checks if any value in the list is greater than 3, 
while the second checks if all values are positive. any() and all() provide 
an efficient way to validate conditions across collections.

12. Generating a Dictionary from Two Lists
    -------------------------------------
Creating a dictionary from two lists is simple and intuitive in Python.
Copy
# Generating a Dictionary from Two Lists
keys = ['a', 'b', 'c']
values = [1, 2, 3]
dictionary = dict(zip(keys, values))
print(dictionary)
Output:
{'a': 1, 'b': 2, 'c': 3}
This one-liner creates a dictionary by zipping two lists together, providing a quick way to map related data.

13. Transforming Lists with map()
    ----------------------------
map() applies a function to every item in an iterable, which is great for batch transformations.

Example:
# Transforming Lists with map()
strings = ["hello", "world"]
uppercase_strings = list(map(str.upper, strings))
print(uppercase_strings)
Output:
['HELLO', 'WORLD']
This one-liner converts a list of strings to uppercase using the map() function. 
Instead of using a loop to apply the transformation, map() applies the str.upper 
method to each element of the list, streamlining the process.

14. Finding the Index of an Element
    -------------------------------
Finding the index of an element in a list can be done in a single, efficient line.
Example:
# Finding the Index of an Element
index = [1, 2, 3, 4, 5].index(3)
print(index)
Output:
2

15. One-liner Nested Loop
    ---------------------
We can use list comprehension to write a nested loop in a single line.
Example:
# One liner Nested Loop
list1 = [1,2,3]
list2 = ['a', 'b']
result = [(x, y) for x in list1 for y in list2]
for x,y in result: 
    print(x, y)
Output:
1 a
1 b
2 a
2 b
3 a
3 b

16. Filtering Even Numbers
    ----------------------
Filtering data is a common task in programming, and Python allows you to do it 
efficiently with list comprehensions.
Example:
# Filtering Even Numbers
even_nums = [x for x in range(1, 21) if x % 2 == 0]
print(even_nums)
Output:
[2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

17. List of Unique Elements
Finding unique elements in a list is straightforward with Python's set operations.
Example:
# List of Unique Elements
unique_elements = list(set([1, 2, 2, 3, 4, 4, 5]))
print(unique_elements)
Output:
[1, 2, 3, 4, 5]
This one-liner removes duplicates from a list, ensuring that only unique elements 
are kept — a common requirement in data cleaning tasks.

18. Converting a List to a String
    -----------------------------
Joining a list into a single string is straightforward with Python's join() method.
Example:
# Converting a List to a String
list1 = ['Python', 'is', 'fun']
joined_string = " ".join(list1)
print(joined_string)
Output:
"Python is fun"
This one-liner joins a list of strings into a single string, which is particularly 
useful in text-processing tasks where you need to combine words or sentences.

19. Reading a File Line by Line
    ---------------------------
Reading files line by line can be done cleanly with a single line of code.
Example:
# Reading a File Line by Line
lines = [line.strip() for line in open("file.txt")]
print(lines)
Output:
['First line', 'Second line', 'Third line']
This one-liner reads all lines from a file, stripping out any extra whitespace, which is a common operation in file processing.

20. Replacing Substrings
    --------------------
Python makes it easy to replace parts of a string with the replace() method.
Example:
# Replacing Substrings
new_string = "I love Python".replace("love", "enjoy")
print(new_string)
Output:
"I enjoy Python"

21. Flattening a List of Lists
    --------------------------
When dealing with nested lists, flattening them into a single list is often required. 
Python offers a simple way to do this.
Example:
# Flattening a List of Lists
flat_list = [item for sublist in [[1, 2], [3, 4], [5, 6]] for item in sublist]
print(flat_list)
Output:
[1, 2, 3, 4, 5, 6]
'''