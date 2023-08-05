# Auto-research-note generator from Jupyter notebook

**Author :** jh.jung  


From jupyter notebook, making the research note to md file with simple syntax.  

- TOC(Table of contents)
- code
- figure
- table
- Daily note

## Installation

Using pip :

```shell
pip install nbresnote
```

## Usage

- For autorun when `git commit`, run below on your git repository :  

```shell
nbresnote install
```

For now, the `install` command will make the clone of your wiki repository of current git into `wiki/` folder.
Unfortunately, this is fixed.


- For run specific `.ipynb` files

```shell
nbresnote note1.ipynb note2.ipynb ...
```

## Documentation

### Syntax

Basically, `nbresnote` ignore all code cells. The module will read only markdown cell for making research notes.

Internelly, `nbresnote` trace the diff of git commit files, and get folder and filename of `.ipynb` in commit,  
and auto documenting the markdown and daily note for the git repository.

You can check the example folder.

Here we prepare for specific syntax `!(command)`

- TOC(Table of contents) :  
    
    Table of Contents is simple anchor of whole notebook headers
    >example)
    >`!TOC` in jupyter notebook
    ![toc](png/TOC.png)


- code
- figure
- table
- Daily note

See wiki tabs.

## future work :  

- configuration change
- directive of rst
- reference of outputs

