[GitHub Pages](https://jameskabbes.github.io/dir_ops)<br>
[PyPI](https://pypi.org/project/kabbes-dir_ops)

# dir_ops
Handy directory operations along with homemade Dir/Path classes

<br> 

# Installation
`pip install kabbes_dir_ops`

<br>

# Usage
For more in-depth documentation, read the information provided on the Pages. Or better yet, read the source code.

```python
import dir_ops as do
```

```python
do.join( 'C', 'Path', 'To', 'File' )
```

```
>>> 'C:/Path/To/File'
```

```python
do.path_to_dirs( 'C:/Path/To/File/asdf.txt' )
```

```
>>> [ 'C', 'Path', 'To', 'File', 'asdf.txt' ]
```

```python
Path_inst = do.Path( 'C:/Path/To/File/asdf.txt')
```

```python
print( Path_inst.exists() )
```

```
>>> True
```

```python
Path_inst.print_atts() #from parent_class dependency
```

```
>>>
---Path Class---
path:	C:/Path/To/File/asdf.txt
dirs:	['C:', 'Path', 'To', 'File', 'asdf.txt']
ending:	txt
size:	None
```

<br>

# Author
James Kabbes

