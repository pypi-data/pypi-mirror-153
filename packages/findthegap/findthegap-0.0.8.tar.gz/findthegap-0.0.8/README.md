## FindTheGap


This package (also unformally known as "Gappy") provides tools for geometric data analysis, targeted at finding gaps and valleys in data distribution. It provides a (twice-differentiable) density estimator (Quartic Kernel Density Estimator) relying on pytorch for auto-differentiation, a routine to approximate critical points in the density ,and various statistics to identify and trace `gaps' and valleys in the distribution. 
 

This package can be installed through pip (https://pypi.org/project/findthegap/):

```
pip install findthegap 
```

See https://github.com/contardog/findthegap for demo and usecase notebook in the folder 'examples'.

Notebook requirements:
sklearn, matplotlib

The folder 'examples' contains a notebook showcasing how to use those tools on 2D data (available in the folder data). 



Disclaimer: this code is work in progress and might go through some changes especially for higher (>2!) dimension... 


Contributors: Gabriella Contardo (CCA at Simons Foundation), David W. Hogg(CCA/NYU/MPIA), Jason S.A. Hunt (CCA)

You can find more information about the methods in the paper "The emptiness inside: Finding gaps, valleys, and lacunae with geometric data analysis" https://arxiv.org/abs/2201.10674 




---
Dependencies:
* numpy >= 1.19.5

* torch >= 1.10.1

* scipy >= 1.5.4



Update version 0.0.5: fix path computation with gradient descent.

Update version 0.0.6: changed score_samples in quarticKDE for speed and memory.

Update version 0.0.7: Fix bug in changed score_samples

Update version 0.0.8: Make the description reappear?!

