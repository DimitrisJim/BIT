Notes as I go along:
--------------------

Binary operator needs to be associative (`A op B == B op A`) and commutative
(`A op (B op C) == (A op B) op C)`. 

Current list of binary operators that are known to have those properties:

#### Numeric:

According to wiki, they apply to any numeric value (Limitations due to 
floating point representation probably do apply).

 - Addition of numbers.
 - Multiplication of numbers.

#### Bitwise:



 - Bitwise and (`&`).
 - Bitwise or (`|`).
 - Bitwise xor (`^`).

#### Sets:

 - Union. 
 - Intersection. 
 - Symmetric difference.


### Inverse functions

A key issue for that appears when trying to remove elements is that of [inverse functions][invfunc]. 

For numeric:
 - addition -> subtraction
 - multiplication -> division

For bitwise operators:

 - xor -> xor (need to test this).

the rest of the bitwise operators [don't seem to have inverses][bitinverse]

todo: set ops.

[invfunc]: https://en.wikipedia.org/wiki/Inverse_function 
[bitinverse]: https://en.wikipedia.org/wiki/Bitwise_operation#Inverses_and_solving_equations
