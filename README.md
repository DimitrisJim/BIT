# BIT

Binary Index Tree. WIP.

## Operations:

Link plots create from running `python stats`, describe why we see `O(N)` and `O(logN)` ops. 

### Initialization:

(or, `BIT.create`) O(N) Operation.

##### Getting the original layout:

##### Appending an item:

##### Updating an items original value:

##### Replacing an items original value:

##### Getting an item (prefix sum):

##### Popping an item:

##### Range Sum

### Plots:

Linear complexity (create, layout)

<p align="middle">
  <img src="stats/plots/create.png" width="400" />
  <img src="stats/plots/layout.png" width="400" /> 
</p>

Logarithmic complexity (append, update, setitem, getitem)

<p align="middle">
  <img src="stats/plots/append.png" width="300" />
  <img src="stats/plots/update.png" width="300" />
  <img src="stats/plots/setitem.png" width="300" />
  <img src="stats/plots/getitem.png" width="300" /> 
</p>


## Resources:

A couple of useful resourses for anyone looking for more:

 - [This tweakblogs entry][tweakblogs] is what I would recommend. After
   understanding the intermediate representation, the code becomes
   clear as day.
 - [This stackexchange question][seIntuition] also has a very nice
   description. It mainly talks about the 'a-ha' moment behind 
   Fenwick Trees.
 - [TopCoder article][topCoderFen], probably something most people
   have read.
 - [Wikipedia entry for Fenwick trees][wikiFenwick], always good to
   give wiki a peak.

[tweakblogs]: https://notes.tweakblogs.net/blog/9835/fenwick-trees-demystified.html
[seIntuition]: https://cs.stackexchange.com/questions/10538/bit-what-is-the-intuition-behind-a-binary-indexed-tree-and-how-was-it-thought-a
[topCoderFen]: https://www.topcoder.com/community/competitive-programming/tutorials/binary-indexed-trees/
[wikiFenwick]: https://en.wikipedia.org/wiki/Fenwick_tree
[algorithmistFenwick]: https://algorithmist.com/wiki/Fenwick_tree
