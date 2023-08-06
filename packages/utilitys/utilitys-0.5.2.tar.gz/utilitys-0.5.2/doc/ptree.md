# Parameter Tree-based Controller
A utility that automatically turns function arguments into parameters, similar to the `interact` capabilities of `ipywidgets`. Unlike the latter, though, this works natively within Qt and doesn't need a notebook / js integration to render. Also, it's much faster and gives a bit more granularity over parameter access.

A decorator, `interact()`, takes all function parameters with default arguments and creates pyqtgraph Parameters out of them, inferring type either (a) by the default type or (b) by the function documentation. These can be seen in the example code found [here](../examples/parameditor.py).

More complex usage is showcased by the [imgcropper](https://gitlab.com/ntjess/imgcropper) project.