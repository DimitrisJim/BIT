# BIT

Binary Index Tree. WIP.

## Operations:

Link plots create from running `python stats`, describe why we see `O(N)` and `O(logN)` ops. TODO: Add these in docs somewhere.

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
