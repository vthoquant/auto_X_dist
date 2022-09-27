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
	- [Set directories and variables](#set-directories-and-variables)
	- [Install Packages](#install-packages)
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
2. Set the **BASE_PATH** variable in the [directory_names](https://github.com/vthoquant/auto_X_dist/blob/main/lib/configs/directory_names.py) config file to an appropriate location in your local C drive. The *directory_names.py* file stores names to directories performing either one of three requirements - (i)storage of logs, (ii)storage of price data and (iii)strategy-specific results directory. You can create appropriate subdirectories under the **BASE_PATH** for each of these 3 requirements as you deem fit
3. The subfolder within the [test_data](https://github.com/vthoquant/auto_X_dist/tree/main/test_data/) folder (with all its associated data) can be moved to the directory defined under the **BARDATA_STORE_PATH** variable

### Install packages
1. Create a new python enviroment from scratch using the *conda* command on a cmd.exe prompt openened on the Aanconda Navigator. The current python versions supported are 3.7 and 3.8 and hence appropriate arguments need to be used while executing the conda command. Lets call this new environment *myenv*
```sh
$ conda create -n myenv python=3.8
```
For more details on creating a new environment using the *conda* command refer to [this](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) article. 
2. One needs to make sure that *myenv* is always activated prior to running any code within this project going forward. On the cmd.exe opened via the **Anaconda Navigator** this can be achieved by executing the following command
```sh
$ conda activate myenv
```
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
One can run any of the executable scripts available in the [examples](https://github.com/vthoquant/auto_X_dist/tree/main/lib/examples) folder. More details on setting-up the parameters to be fed into the individual executables and executing them can be found in the later subsections. Would like to re-iterate however that **the user has to ensure that the executables are invoked under the *myenv* environemt only**

Once the setup described above has been carried out one can verify that the code runs fine my navigating to the [examples](https://github.com/vthoquant/auto_X_dist/tree/main/lib/examples) folder and running the *backtest.py* script with its default parameters
1. please ensure that a folder with the name typed-out under the default argument for *--run_name* (which as of writing this document is *intraday-bkout-cstick*) in created in the *BASE_PATH/strategy_backtest/* folder. Recollect that **BASE_PATH** is the variable defined within the [directory_names](https://github.com/vthoquant/auto_X_dist/blob/main/lib/configs/directory_names.py) config. If the folder is incorrectly created or unavailable, one would receive an ERROR on executing the code.
2. Execute the backtest using the following command from the *examples* directory
```sh
$ python backtest.py
```

### Backtesting
The entry point for running backtesting is the [backtest.py](https://github.com/vthoquant/auto_X_dist/blob/main/lib/examples/backtest.py) script within the [examples](https://github.com/vthoquant/auto_X_dist/tree/main/lib/examples) folder. This backtest script has the following arguments which can be specified during its execution
- *run_name*: The name provided for the specific backtest that is to be run. This name drives the class of startegy along-with its specific parameters on which the strategy is to be executed. The parameters corresponding to the *run_name* provided is specified in the [backtest_config.py](https://github.com/vthoquant/auto_X_dist/blob/main/lib/configs/backtest_configs.py) file. 
The variable **STRATEGY_BT_CONFIG_MAP** contains the collection of params for all strategies currently in the repository. Let us take the example of the default *run_name* on which the backtest is run i.e. *intraday-bkout-cstick*. We would need to lookup the key *intraday-bkout-cstick* within the **STRATEGY_BT_CONFIG_MAP** dictionary variable. We then need to look-up the value corresponding to the *intraday-bkout-cstick* key. This value
is essentially another dictionary with 2 keys of its own - *strategy_name* and *params*. *strategy_name* is the name of the strategy class implementation. The entire list of enabled strategy classes can be found in the [strategy_mapper](https://github.com/vthoquant/auto_X_dist/blob/main/lib/configs/strategy_mapper.py) config file. The second key is *params*. This is simply the collection of strategy attributes which are specific to the startegy specified under *strategy_name*. 
For an existing strategy which the user requires to backtest with a different set of params, we could either edit the existing value variable corresponding to that strategy or create a new key-value pair within the **STRATEGY_BT_CONFIG_MAP** dictionary variable. For example the user could create a *intraday-bkout-cstick-1* variable with a new set of strategy params and execute the backtest.py file after assigning *run_name* as *intraday-bkout-cstick-1*
- *tickers*: the srcip on which the backtest is meant to be run. Any non-FX scrip as of now needs to have '.NS' appended at the end. The supported scrips could be either equity indices such as *NIFTY50.NS*, *BANKNIFTY.NS*, or single stocks such as *RELIANCE.NS* or FX such as *USDINR* or *EURINR*. *ticker_names* also support special suffixes to denote whether the underlying data is referening a future (with suffixes such as *_M1*, *_M2* etc). 
 Multiple scrips are also supported by specifying them as a comma seperated string. For example, if I am interested to run a statistical arbitrage strategy which trades on the premium differences between the first and second month NIFTY futures, I could specify the *tickers* argument as *NIFTY50_M1.NS,NIFTY50_M2.NS*
- *start*: the start date for the backtest to run specified in 'YYYY-MM-DD' format
- *end*: the end date for the backtesting specified in 'YYYY-MM-DD' format
- *interval*: the candlestick duration for the backtesst. Can be specified as '1min', '5min', '15min' or '1H', '1D' etc
- *initial_capital*: The absolute value of the underlying index/stock that has to be traded. Please note that this is the notional value so in the case of options trading this would correspond to the notional value of the underlying stock/index and not premium/margin 

The script once executed with the appropriate arguments is going to generate a tick-by-tick '-algo' file with information as to when exactly the signals were generated, position sizes etc and a '-bt' file with the performance metrics of the backtested strategy including hit ratios, avg returns, FDD, MAR, sharpe, annualized reutrns etc. The two files are going to be saved in the directory specified within the [direcotry_names](https://github.com/vthoquant/auto_X_dist/blob/main/lib/configs/directory_names.py) file, under the **STRATEGY_RUN_BASE_PATHS** variable against the key corresponding to the strategy class name.
So for example the *intraday-bkout-cstick* backtest run has been setup for a strategy having the class name **INTRADAY_BREAKOUT_CSTICK** as can be seen in the [backtest_configs](https://github.com/vthoquant/auto_X_dist/blob/main/lib/configs/backtest_configs.py) file discussed earlier. So we need to note the folder name against this clss name as defined within the *directory_names* config and we need to ensure that that particular folder already exists else we would encounter a write error once the run is complete. 

### Optimization

### Live trading (IB)

## Maintainers
This repo is owned and maintained by **Vivin Thomas**. In case of any concerns or queries regarding this project, help with any deployment, or additional development requests please feel free to contact me on my [linkedin](https://www.linkedin.com/in/vivin-thomas-7885a2130)

## Contributing
Please feel free to add to the configs and strategy files that are available for view and edit and issue any pull requests. For any contributions to be made to the compiled infrastructure code, please contact me on my [linkedin](https://www.linkedin.com/in/vivin-thomas-7885a2130)

## License

(LICENSE) © Vivin Thomas <br />
Unauthorized distribution and access to restricted compiled code is prohibited