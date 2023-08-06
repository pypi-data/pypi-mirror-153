[//]: # (1 Project's title)
# drivebox

[//]: # (2 Project description)
`Python` API to interact with the Caonabo DriveBox (CDB). The Caonabo DriveBox is a tool that combines a switch matrix module with an itnernal potentiostat/Galvanostat in order to drive electrochemical (EC) reactions through diferent EC cells. The potentiostat/galvanostat module allows for the sourcing of potentials of ±7.5V and currents of ±65mA. The switch-matrix module allows to assign signals to a total of 50 electrodes. The signals can be procided from the internal potentiostat/galvanostat itself or from and exteral source. For ease of writing from her on we will refer to the potentiostat/galvanostat module as the Source Measurement Unit (SMU).

For more information regarding the CDB hardware please visit the hardware [repository](https://github.imec.be/dna-storage/cdb).

[//]: # (3 Table of contents)
## Table of contents <a name="table-contents"></a>

1. [Installation and package dependencies](#installation)
2. [How to use the package](#use)
    + [2.1 Instantiation, initiation and general commands for the CDB](#instantiation)
    + [2.2 Working with the switch matrix module](#smx)
    + [2.3 Working with the SMU module (potentiostat/galvanostat)](#smu)
        + [Low level commands](#low_cmd)
        + [SMU applications: sweeping](#apps_sweep)
        + [SMU applications: sampling](#apps_samp)
        + [SMU applications: pulse](#apps_pulse)
3. [API reference guide](#reference)
4. [Contributors](#contributors)
5. [License](#license) 

[//]: # (4 Package dependencies)
## 1 Installation and package dependencies <a name="installation"></a>

This packager requires the previous installation of the following packages:
- [pyserial 3.5 (or newer)](https://pypi.org/project/pyserial/)

Afer installing the dependencies, the package can be installed from the Python package index (`PyPI`) repository.

In Windows:

```PowerShell
C:\> pip install --user drivebox
```

or in Linux:

```bash
$ pip install --user drivebox
```

If using the `anaconda` distribution for python you can also use the `conda` package manager for the instalation from the `dreamwere` channel. 

In Windows:

```PowerShell
C:\> conda install -c dreamwere drivebox
```

or in Linux:

```bash
$ conda install -c dreamwere drivebox
```

As an alternative, the drivebox package (inside the `src/` folder) can be download and copied into the the main folder of the project where it will be used.

[//]: # (5 How to use the package)
## 2 How to use the package <a name="use"></a>

### 2.1 Instantiation, initiation and general commands for the CDB. <a name="instantiation"></a>

First, the module must be imported:

```python
>>> from drivebox import board
```

Once imported, the cdb class inside the module must be instantatiated to gain control to an specific CDB.
Hence, the port where the CDB board is connected, as well as the ID of the board, must be specified.
For the port, the name of the port can be given such as `"COM1"` or `"AUTO"` can be used.
Sometimes, `"AUTO"` might not work due to conflict with some USB devices. 
If this happens, the port will have to be passed manually. An example instantiations can be as folows:

```python
>>> cdb = board.cdb(port="AUTO", board_id="000")
```

Once initiated, the following output will appear in the console:

>    Caonabo DriveBox (CDB) with correct ID initiated in port: COM10. 
>    Average measurement delay (For [V,I]): 170.0ms

At the end, the instance must be properly closed to avoid leaving the serial ports open. This is done by using the `close()` method:

```python
>>> cdb.close()
```

### 2.2 2.2 Working with the switch matrix module. <a name="smx"></a>

To be completed...

### 2.3 Working with the SMU module (potentiostat/galvanostat). <a name="smu"></a>

To be completed...
 
[//]: # (6 API Reference Guide)
## 3 API Reference Guide <a name="reference"></a>

To be completed...

[//]: # (7 Contributors)
## 4 Contributors <a name="contributors"></a>
- [César Javier Lockhart de la Rosa (lockhart@imec.be)](https://github.imec.be/lockhart)
- [Kherim Willems (kherim.willems@imec.be)](https://github.imec.be/willemsk)

[//]: # (8-License)
## 5 License <a name="license"></a>

Copyright (c) 2022 [César J. Lockhart de la Rosa (lockhart@imec.be)](https://github.imec.be/lockhart)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
