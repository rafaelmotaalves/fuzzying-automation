# HTML EXECUTOR
A python script to execute multiple HTML files at the [Epiphany web browser](https://github.com/GNOME/epiphany) and check if they caused any errors

## Usage
To install the needed dependencies on a Debian based linux distro execute:

```bash
    make install
``` 
* This will install the script dependencies, the Epiphany Web Browser and the WebKitGtk Driver

To use execute the all the HTMLs at a given directory execute:

```bash
    python3 executor.py /path/to/directory
```
