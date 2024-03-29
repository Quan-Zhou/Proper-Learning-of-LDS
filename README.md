# Proper Learning of LDS
 
This is the source code for the paper *Proper Learning of Linear Dynamical Systems as a Non-Commutative Polynomial Optimisation Problem*:

```
@misc{https://doi.org/10.48550/arxiv.2002.01444,
  doi = {10.48550/ARXIV.2002.01444},
  url = {https://arxiv.org/abs/2002.01444},
  author = {Zhou, Quan and Marecek, Jakub},
  title = {Proper Learning of Linear Dynamical Systems as a Non-Commutative Polynomial Optimisation Problem},
  publisher = {arXiv},  
  year = {2020}, 
}
```

It inculdes the scripts, workspace and data files for each figure in the paper. In particular, it includes scripts in Python ("py"), Julia ("jl"), and MATLAB ("m").

## Dependencies

1. Mosek/9.2 https://www.mosek.com/downloads/list/9/

2. Python scripts:

- Python/3.9.6

- inputlds https://raw.githubusercontent.com/jmarecek/OnlineLDS/master/inputlds.py

- ncpol2sdpa 1.12.2 https://ncpol2sdpa.readthedocs.io/en/stable/index.html

3. Julia scripts:

- Julia/1.5.2

- NCTSSOS https://github.com/wangjie212/NCTSSOS

- TSSOS https://github.com/wangjie212/TSSOS

4. Matlab scripts:

- Matlab/R2021a
 
- Statistics and Machine Learning Toolbox https://www.mathworks.com/help/stats/

- System Identification Toolbox https://www.mathworks.com/help/ident/

- Optimization Toolbox https://www.mathworks.com/help/optim/

- Some old codes use PRETTYPLOT https://uk.mathworks.com/matlabcentral/fileexchange/27237-prettyplot to make plots in MATLAB. The plots in our draft are all made in Python.
