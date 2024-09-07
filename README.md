# Summary

LambdaGo is a functional wrapper for the Go programming language.

It is meant to create pure functions that will be later called from a Go program. E.g.:

LambdaGo code:
```python
# Fibonacci sequence

fib::int->[int].
fib n = [0] ++ (fib2 0 1 (n-1)).

fib2::int->int->int->[int].
fib2 a b n  | n > 0 = [b] ++ (fib2 b (a+b) (n-1))
            | otherwise = <[int]> [].
```

Resulting Go code:
```Go
// Fib::int->[int]
func Fib (arg0 int) []int{
	return concat_7a637([]int{0})(Fib2(0)(1)(sub_e2fbf(arg0)(1)))
}

// Fib2::int->int->int->[int]
func Fib2 (arg0 int) func(int) func(int) []int{
	return func(arg1 int) func(int) []int{
		return func(arg2 int) []int{
			if gt_fd2cf(arg2)(0) {
				return concat_7a637([]int{arg1})(Fib2(arg1)(add_e2fbf(arg0)(arg1))(sub_e2fbf(arg2)(1)))
			}
			return type_cast_36e98([]interface{}{})
		}
	}
}
```

Calling from Go program:
```Go
fmt.Println(fib.Fib(10))

=> [0 1 1 2 3 5 8 13 21 34]
```

For more examples see [here](./examples).

# Usage

```
python3 main.py <source_path> <output_path> [--package-name <package_name>]
```

* `source_path`: path to the `.lgo` source
* `output_path`: the directory the `.go` code will be written in
* `package_name`: the name of the go package, the default is the name of the directory the sources will be written in.


# Language description

The language supports the following data types:
* integers: `int`
* floats: `float`
* strings: `str`
* functions: `(parameter_type->return_type)`
* dictionaries: `dict`
* the any type (equivalent of `interface{}`): `any`
* lists of all of the above: `[type]`
* imbricated lists: `[[type]]`, `[[[type]]]`, ...

The functions defined in LambdaGo support partial function application.

The parameters to a function can be other functions (higher order functions).

**The language enforces type safety** (e.g. The program won't compile if you pass a string to a function that expects a float).

# Built in functions

The language has a number of built in functions. Some of them are generic functions that resolve their own type according to the type of their parameters. E.g.:

```
sum1::float->float->float.
sum1 x y = add x y.

sum2::int->int->int.
sum2 x y = add x y.

is_odd::int->bool.
is_odd x = (x % 2) == 1.

f1::[int]->[int].
f1 xs = filter is_odd xs.

inc::float->float.
inc a = a + 1.0.

f2::[float]->[float].
f2 xs = map inc xs.
```

In the example above `add`, `map` and `filter` are generic functions. 

In the function `sum1`, `add` receives 2 floats and infers that the result's type must be a float.

In the funtion `sum2`, `add` receives 2 ints and infers that the result's type must be an int.

`filter` sees that the first argument is a function of the type `(int->bool)` and the second argument is of type `[int]` so it resolves its own type as `((int->bool)->[int]->[int])` (the return type is resolved as `[int]`).

`map` sees that the first argument is a function of the type `(float->float)` and the second argument is of type `[float]` so it resolves its own type as `((float->float)->[float]->[float])`.

## Arithmetic functions

All operators in LambdaGo are resolved to functions internally. (e.g. `1 + 2` is resolved to `add 1 2`).

List of arithmetic functions:
* `add`: number addition, equivalent to `+` operator
* `sub`: number subtraction, equivalent to `-` operator
* `mul`: number multiplication, equivalent to `*` operator
* `div`: number division, equivalent to `/` operator
* `mod`: modulus operation, equivalent to `%` operator

## Logical functions
* `eq`: equality, equivalent to `==` operator
* `neq`: inequality, equivalent to `!=` operator
* `gt`: greater than, equivalent to `>` operator
* `gte`: geater or equal than, equivalent to `>=` operator
* `lt`: less than, equivalent to `<` operator
* `lte`: less or equal than, equivalent to `<=` operator
* `and`: logical and, equivalent to `&&` operator
* `or`: logical or, equivalent to `||` operator

## String functions
* `starts_with`: first string starts with second string. `(str->str->bool)`
* `contains`: first string contains second string. `(str->str->bool)`
* `re_match`: second string matches regular expression given as first string `(str->str->bool)`
* `concat`: string concatenation. `(str->str->str)`

## List functions
* `concat`: list concatenation. (`[type]->[type]->[type]`)
* `len`: length of the list. (`[type]->int`)
* `append`: add one element to the list. (`[type]->type->[type]`)
* `idx`: get element at given index from the list. (`[type]->int->type`)
* `map`: apply a function to all elements of the list (`(type->ret_type)->[type]->[ret_type]`). Args:
	* the function to be applied 
	* the list the function should be applied on. 
* `filter`: only keep the elements of the list that match the given predicate (`(type->bool)->[type]->[type]`). Args:
	* a function that returns a boolean  
	* the list to be filtered. 

	
* `reduce`: reduce/fold a list of values into a single value (`[type]->(type->acc_type->acc_type)->acc_type`). Args:
	* the list to be reduced
	* a function with 2 arguments:
		* the current element of the list
		* the accumulator obtained up to that point
	* the initial value for the accumulator
## Dictionary functions
* `dict_get`: extract the value for the given key from the dictionary (`dict->str->any`) 
* `dict_get_default`: extract the value for the given key from the dictionary or return the default value if the key does not exist. (`dict->str->default_value_type->default_value_type`)
* `dict_deep_get`: perform several `dict_get_default` operations at once. The keys are separated by `"."` (e.g `"key1.key2.key3"`). (`dict->str->default_value_type->default_value_type`)
* `dict_set`: set a value in the dict (`dict->str->value_type->dict`)
* `dict_deep_set`: set a value in the dict using imbricated keys (the keys are joined by `.` in a single string as in `dict_deep_get`). If one of the intermediary keys are not found the key will be set to an empty dict. (`dict->str->value_type->dict`)
* `dict_keys`: all the keys set in the dict. Keys from deeper levels will be concatenated with `.` to the keys from the upper levels. (`dict->[str]`)

`dict_get` returns the `any` type, the value needs to be casted to the correct type before being used.

## Type casts

Type casting is used to either cast the `any` type to the correct type or to turn `int`s into `float`s and vice versa.

The `any` type can be cast to anything, including function types.

E.g.:
```
# cast float to int
f1::float->int.
f1 x = <int> x.

# cast int to float
f2::int->float.
f2 x = <float> x.

# cast any to an int
f3::any->int.
f3 x = <int> x.

# cast any to a dict
f4::any->dict.
f4 x = <dict> x.

# cast any to a function
f5::any->(int->int).
f5 x = <int->int> x.
```

You can cast an entire list of values to a different list type, as long as the list depth matches.

```
# cast a list of ints to a list of floats
f6::[int]->[float].
f6 x = <[float]> x.

# cast an imbricated list of ints to an imbricated list of floats
f7::[[[int]]]->[[[float]]].
f7 x = <[[[float]]]> x.

# cast a list of any to a list of dicts
f8::[any]->[dict].
f8 x = <[dict]> x.

# cast a list of any to a list of different depth
f9::[[any]]->[[[[int]]]].
f9 x = <[[[[int]]]]> x.
```

In `f9`, each element of the `[[any]]` list is turned into a `[[int]]`, thus resulting the `[[[[int]]]]` list.