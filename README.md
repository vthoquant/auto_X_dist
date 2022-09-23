# auto_X - One stop backtesting, optimization and live trading platform

auto_X is a events-based trading platform project which allows us to implement our startegy as an independent class where the signals and states are encoded within the object methods. The parameters which drive each strategy are all stored within self explanatory and easily accessible config files which allows the user to experiment with different input values themselves.    

Live trading as of writing this document is only supported for interactive brokers. Other broker APIs to be supported in future versions

This repository contains:

1. [The requirements doc](requirements.txt) containing a list of external libraries and their versions which are compatible with this project.
2. [Entry point scripts](https://github.com/vthoquant/auto_X_dist/tree/main/lib/examples) within the lib/examples subdirectory which contain scripts to be used for backtesting, optimization and live trading. Going forward this collection of scripts will be refered to as *executables*
3. [Config files](https://github.com/vthoquant/auto_X_dist/tree/main/lib/configs) within the lib/configs subfolder containing a list of files which store the parameter values which drive the inputs and functioning within the executables for each strategy developed within this project.
4. [Strategy files](https://github.com/vthoquant/auto_X_dist/tree/main/lib/strategies) within the lib/strategies folder containing the modules where the individual strategies are implemented and loaded onto the executables.
5. [Test data](https://github.com/vthoquant/auto_X_dist/tree/main/test_data/) within the test_data folder to test out the executables
6. All remaining files have been committed in compiled form with restricted code access.

## Table of Contents

- [Setup](#setup)
	- [Set directories and variables] (#set-directories-and-variables)
	- [Install Packages] (#install-packages)
- [Running](#running)
	- [Backtesting](#backtesting)
	- [Optimization](#optimization)
	- [Live trading (IB)](#live-trading-(ib))
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)


## Setup
You can either checkout the project or download and unzip the project into an appropriate directory. For illustration purposes let this *project directory* be `C:\Users\myUserName\auto_X_dist`

### Set directories and variables
1. Firstly we would need to set the **PYTHONPATH** environment variable to reference our *project directory*. For more details on how to set a environment varaible, refer to [this](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html) link. It would suffice to set a 'user variable' and not a 'system variable'
2. Set the BASE_PATH variable in the [directory_names](https://github.com/vthoquant/auto_X_dist/blob/main/lib/configs/directory_names.py) config file to an appropriate location in your local C drive. The *directory_names.py* file stores names to directories performing either one of three requirements - (i)storage of logs, (ii)storage of price data and (iii)strategy-specific results directory. You can create appropriate subdirectories under the BASE_PATH for each of these 3 requirements as you deem fit
3. The subfolder within the [test_data](https://github.com/vthoquant/auto_X_dist/tree/main/test_data/) folder (with all its associated data) can be moved to the directory defined under the BARDATA_STORE_PATH variable

### Install packages
1. Create a new python enviroment from scratch using either the environments tab on the **Anaconda Navigator** application or using the *conda* command on a cmd.exe prompt openened using the Aanconda Navigator. For more details on creating a new environment using the *conda* command refer to [this](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) article. Lets call this new environment *myenv*
2. One needs to make sure that *myenv* is always activated prior to running any code within this project going forward
3. Install all the external python packages required, listed out in the *requirements.txt* file using the *pip* command. 
```sh
$ pip install -r requirements.txt
```
4. Ensure that all the external packages have been installed in the new environment. In case of any installation failures please ensure that the required version of the package is installed manually
5. The Ta-lib and ibapi packages need to be explicitly installed manually. To install the Ta-lib package via conda please use the below command on the cmd.exe window opened via the **Anaconda Navigator** application having the *myenv* environemt activated
```sh
$ conda install -c conda-forge ta-lib
```
6. For the IB TWS API, install the *Stable TWI API* version available on [this](https://interactivebrokers.github.io/#) link. This should install the relevent code within a *C:\TWS API* folder in your local drive. Within this location you'd need to navigate inside the *source/pythonclient* folder using the usual *myenv*-enabled cmd.exe window. Open the README.md file available here and execute all the 3 commands listed out in the end of the document to sucessfully install the ibapi package 

## Running

### Backtesting

### Optimization

### Live trading (IB)

## Maintainers

## Contributing

## License

(LICENSE) © Vivin Thomas
Unauthorized distribution and access to restricted compiled code is prohibited