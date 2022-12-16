# auto_X - One stop backtesting, optimization and live trading platform

auto_X is a events-based trading platform which allows us to implement our trading strategies as independent classes where the signals and states are encoded within the object methods. 
The parameters to configure each strategy are all stored within self explanatory and easily accessible config files which allows the user to experiment with different input values themselves.    

Live deployment as of writing this document is only supported on Interactive Brokers via the IB TWS API. Other broker APIs to be supported in future versions

This repository contains:

1. [The requirements doc](requirements.txt) containing a list of external libraries and their versions which are compatible with this project.
2. [Executables](https://github.com/vthoquant/auto_X_dist/tree/main/lib/examples) within the *lib/examples* subdirectory which contain scripts to be used for backtesting, optimization and live trading.
3. [Config files](https://github.com/vthoquant/auto_X_dist/tree/main/lib/configs) within the *lib/configs* subfolder containing the collection of files which store the parameter values which drive the inputs 
and functioning within the executables for each strategy developed within this project.
4. [Strategy files](https://github.com/vthoquant/auto_X_dist/tree/main/lib/strategies) within the lib/strategies folder containing the modules where the individual strategies are implemented and loaded onto the executables.
5. [Test data](https://github.com/vthoquant/auto_X_dist/tree/main/test_data/) within the test_data folder to test out the executables. The data within this folder should ideally be moved to another location on your local system. 
This will be discussed in later sections. 
6. All remaining files have been committed in compiled form with restricted code access.

## Table of Contents

- [Setup](#setup)
	- [Set directories and variables](#set-directories-and-variables)
	- [Install Packages](#install-packages)
- [Running](#running)
	- [Backtesting](#backtesting)
	- [Optimization](#optimization)
	- [Live trading](#live-trading)
- [Data format](#data-format)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)


## Setup
You can either checkout the project or download and unzip the project into an appropriate directory. The preferred way is to fork this repository on github and clone the forked directory to a local folder (*project directory*) on your system. 
For illustration purposes let this *project directory* be `C:\Users\myUserName\auto_X_dist`. Details on how to fork a repo can be found [here](https://docs.github.com/en/get-started/quickstart/fork-a-repo). 
This can be benefitial as the user may want to commit their own changes to their own 'version' of the repo independently. 

### Set directories and variables
1. Firstly we would need to set the **PYTHONPATH** environment variable on our windows system to reference our *project directory*. 
For more details on how to set a environment varaible, refer to [this](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html) link. It would suffice to set a 'user variable' and not a 'system variable'
2. Set the **BASE_PATH** variable in the [directory_names](https://github.com/vthoquant/auto_X_dist/blob/main/lib/configs/directory_names.py) config file to an appropriate location in your local C drive. 
The *directory_names.py* file contains names to directories storing data for either one of three use-cases - (i)storage of logs, (ii)storage of price data and (iii)strategy-specific results directory. 
You can create appropriate subdirectories under the **BASE_PATH** for each of these 3 use-cases as you deem fit
3. The subfolder within the [test_data](https://github.com/vthoquant/auto_X_dist/tree/main/test_data/) folder (with all its associated data) can be moved to the directory defined under the **BARDATA_STORE_PATH** variable found in the *directory_names.py* file

### Install packages
1. Create a new python enviroment from scratch using the *conda* command on a cmd.exe prompt opened via the Aanconda Navigator. 
The current python versions supported are 3.7 and 3.8 and hence appropriate arguments need to be used while executing the conda command. Lets call this new environment *myenv*
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
6. For the IB TWS API, install the *Stable TWI API* version available on [this](https://interactivebrokers.github.io/#) link. This should install the relevent code within a *C:\TWS API* folder in your local drive. 
Within this location you'd need to navigate inside the *source/pythonclient* folder using the usual *myenv*-enabled cmd.exe window. 
Open the README.md file available here and execute all the 3 commands listed out in the end of the document to sucessfully install the ibapi package 

## Running
One can run any of the executable scripts available within the [examples](https://github.com/vthoquant/auto_X_dist/tree/main/lib/examples) folder. 
More details on setting-up the parameters to be fed into the individual executables and executing them can be found in the later subsections. 
Would like to re-iterate however that **the user has to ensure that the scripts are always executed under the *myenv* environemt only**

Once the setup described above has been carried out, one can verify that the code runs fine by navigating to the [examples](https://github.com/vthoquant/auto_X_dist/tree/main/lib/examples) folder 
and running the *backtest.py* script with its default parameters
1. please ensure that a folder with the name typed-out under the default argument for *--run_name* (which as of writing this document is *intraday-bkout-cstick*) is created within the *BASE_PATH/strategy_backtest/* folder. 
Recall that **BASE_PATH** is the variable defined within the [directory_names](https://github.com/vthoquant/auto_X_dist/blob/main/lib/configs/directory_names.py) config. 
If the folder is incorrectly created or unavailable, one would receive an ERROR on executing the code.
2. Execute the backtest using the following command from the *examples* directory
```sh
$ python backtest.py
```
Details on how to run each of the executables can be found in the following sections. <br />

**IMPORTANT! Always ensure that the scripts are executed from within the *myenv* conda environment by activating it on the cmd.exe window opened via Anaconda Navigator using the following command**
```sh
$ conda activate myenv
```

### Backtesting
The entry point for running backtesting is the [backtest.py](https://github.com/vthoquant/auto_X_dist/blob/main/lib/examples/backtest.py) script within the [examples](https://github.com/vthoquant/auto_X_dist/tree/main/lib/examples) folder. 
This backtest script has the following arguments which can be specified during its execution
- *run_name*: The name provided for the specific backtest that is to be run. This name drives the class of strategy along-with its specific parameters on which the strategy is to be executed. 
The parameters corresponding to the *run_name* is specified in the [backtest_config.py](https://github.com/vthoquant/auto_X_dist/blob/main/lib/configs/backtest_configs.py) file. 
The variable **STRATEGY_BT_CONFIG_MAP** contains the collection of params for all strategies currently in the repository. Let us take the example of the default *run_name* on which the backtest is run i.e. *intraday-bkout-cstick*. 
We would need to lookup the key *\'intraday-bkout-cstick\'* within the **STRATEGY_BT_CONFIG_MAP** dictionary variable. We then need to look-up the value corresponding to the *\'intraday-bkout-cstick\'* key. This value
is essentially another dictionary with 2 keys of its own - *strategy_name* and *params*. *strategy_name* is the name of the strategy class implementation. 
The entire list of enabled strategy classes can be found in the [strategy_mapper](https://github.com/vthoquant/auto_X_dist/blob/main/lib/configs/strategy_mapper.py) config file. The second key is *params*. 
This is simply the collection of strategy attributes which are specific to the strategy specified under *strategy_name*. 
For an existing strategy which the user requires to backtest with a different set of params, one could either edit the existing value variable corresponding to that strategy or create a new key-value pair within the **STRATEGY_BT_CONFIG_MAP** dictionary variable. 
For example, the user could create a *intraday-bkout-cstick-1* variable with a new set of strategy params and execute the backtest.py file after assigning *run_name* as *intraday-bkout-cstick-1* if they wanted to run the backtest on a new set of parameters instead
- *tickers*: the srcip on which the backtest is meant to be run. Any non-FX scrip as of now needs to have '.NS' appended at the end. The supported scrips could be either equity indices such as *NIFTY50.NS*, *BANKNIFTY.NS*, or single stocks such as *RELIANCE.NS* 
or FX such as *USDINR* or *EURINR*. *ticker_names* also support special suffixes to denote whether the underlying data is referencing a future (with suffixes such as *_M1*, *_M2* etc). 
 Multiple scrips are also supported by specifying them as a comma seperated string. For example, if I am interested to run a statistical arbitrage strategy which trades on the premium differences between the first and second month NIFTY futures, 
 I could specify the *tickers* argument as *NIFTY50_M1.NS,NIFTY50_M2.NS*. If left unspecified the default value for this argument is taken as 'NIFTY50.NS'
- *start*: the start date for the backtest to run specified in 'YYYY-MM-DD' format. The default value is '2021-05-25'
- *end*: the end date for the backtesting specified in 'YYYY-MM-DD' format. The default value is '2022-08-12'
- *interval*: the candlestick duration for the backtesst. Can be specified as '1min', '5min', '15min' or '1H', '1D' etc
- *initial_capital*: The absolute value of the underlying index/stock that has to be traded. 
Please note that this is the notional value so in the case of options or futures trading this would correspond to the notional value of the underlying stock/index and not the premium or margin 

An example execution can look like the one below
```sh
$ python backtest.py --run_name=intraday-pullback --tickers=BANKNIFTY.NS --start=2021-06-21 --end=2022-06-20 --interval=30min --initial_capital=10000000
```

The script once executed with the appropriate arguments is going to generate a tick-by-tick '-algo' file with information as to when exactly the signals were generated, position sizes etc and a '-bt' file with the performance metrics of the backtested strategy 
including hit ratios, avg returns, FDD, MAR, sharpe, annualized reutrns etc. The two files are going to be saved in the directory specified within the [direcotry_names](https://github.com/vthoquant/auto_X_dist/blob/main/lib/configs/directory_names.py) file, 
under the **STRATEGY_RUN_BASE_PATHS** variable against the key corresponding to the strategy class name.
So for example the *intraday-bkout-cstick* backtest run has been setup for a strategy having the class name **INTRADAY_BREAKOUT_CSTICK** as can be seen in the [backtest_configs](https://github.com/vthoquant/auto_X_dist/blob/main/lib/configs/backtest_configs.py) file discussed earlier. 
So we need to note the folder name against this class name as defined within the *directory_names* config and we need to ensure that that particular folder already exists else we would encounter a write error once the run is complete. 

### Optimization
The entry point for running optimization is the [optimize.py](https://github.com/vthoquant/auto_X_dist/blob/main/lib/examples/optimize.py) script within the [examples](https://github.com/vthoquant/auto_X_dist/tree/main/lib/examples) folder. 
This optimize script has the following arguments which can be specified during its execution
- *strategy_name*: The class name of the strategy on which we would like to run our optimization. 
As mentioned in the previous section, the class names of the different strategies currently in our repository can be found in the [strategy_mapper](https://github.com/vthoquant/auto_X_dist/blob/main/lib/configs/strategy_mapper.py) config file. 
The strategy class name is what drives the sample-set of parameter combinations on which the optimization is going to be run on unlike a *run_name* in the backtest. 
The idea is that there is supposed to be just a single optimization parameter-set configuration per strategy as against multiple potential parameters per strategy that one can backtest on. 
The parameter combination sample-set on which the optimization is to run on every strategy is defined within the [optimizer_configs](https://github.com/vthoquant/auto_X_dist/blob/main/lib/configs/optimizer_configs.py) file. 
Let us consider the default parameter assigned to *strategy_name* in the optimize.py script, **INTRADAY_OVERTRADE_RSI_CSTICK_REV**. 
We need to circle back to the optimizer_configs file and refer to the **STRATEGY_OPT_CONFIG_MAP** variable within which we need to find the *\'INTRADAY_OVERTRADE_RSI_CSTICK_REV\'* key. Then we refer to the variable corresponding to that key. 
We observe that the variable is turn in a dictionary with keys which correspond to the parameters for that strategy. however the values corresponding to each of those keys are not single values but rather multiple values contained within a list. 
The set of configuration combinations on which the optimization would be run is a cross product over each of the parameter lists. 
So for example if a strategy has 2 parameters *sl* and *tp* on whcih we'd like to optimize on, we could specify the optimization dictionary as something like `{'sl': [1, 2], 'tp': [2, 3, 4]}`. 
The optimization would then be run on a total of six combinations: `{'sl':1, 'tp': 2}`, `{'sl':1, 'tp': 3}`, `{'sl':1, 'tp': 4}`, `{'sl':2, 'tp': 2}`, `{'sl':2, 'tp': 3}`, `{'sl':2, 'tp': 4}`
- *run_name*: The name provided to the specific optimization run. Please note that unlike the backtest script, the *run_name* argument here doesn't hold any special significance apart from just being a name against which the output files would be stored. 
Once the optimization is run, the optimization file would be stored in the same 'strategy-specific' folder as we had discussed above in the backtesting section, having the run_name appended with the suffix '-optres'.  
- *tickers*: *\<same as the corresponding argument used for the backtest\>*
- *start*: *\<same as the corresponding argument used for the backtest\>*
- *end*: *\<same as the corresponding argument used for the backtest\>*
- *interval*: *\<same as the corresponding argument used for the backtest\>*
- *initial_capital*: *\<same as the corresponding argument used for the backtest\>*

An example execution can look like the one below
```sh
$ python optimize.py --run_name=intraday-pullback-test --strategy_name=INTRADAY_PULLBACK --tickers=BANKNIFTY.NS --start=2021-06-21 --end=2022-06-20 --interval=30min --initial_capital=10000000
```

The script once executed with the appropriate arguments is going to generate a file with '-optres' appended to the *run_name*. So in this case the optimization output would be saved into a file named *intraday_otrade_test-optres.csv*. 
The file is going to be saved in the directory specified within the [direcotry_names](https://github.com/vthoquant/auto_X_dist/blob/main/lib/configs/directory_names.py) file, 
under the **STRATEGY_RUN_BASE_PATHS** variable against the key corresponding to the strategy class name.
The '-optres' file generated as an output of optimization is similar in structure to the '-bt' file generated during the backtesting. The '-optres' csv file would contain the performance metrics of each and every one of the parameter configurations run for this particular strategy. 
It would be trivial post the generation of this csv file to sort on Sharpe or MAR or annualized returns and obtain the most optimal configuration on which to trade on.

### Live trading
As mentioned perviously , live trading as of now is only supported on Interactive Brokers. <br />
There are 2 entry points for running live trading on IB(Interactive brokers) - [run_live_ib](https://github.com/vthoquant/auto_X_dist/blob/main/lib/examples/run_live_ib.py) and [run_live_ib_multi](https://github.com/vthoquant/auto_X_dist/blob/main/lib/examples/run_live_ib_multi.py). 
For now we'll focus on the former and highlight the differences between the two towards the end. The following arguments can be specified during the execution of the [run_live_ib](https://github.com/vthoquant/auto_X_dist/blob/main/lib/examples/run_live_ib.py) script
- *run_name*: The name corresponding to the strategy configuration which is to be run on your IB account. This 'configuration' is a combination of the strategy class along-with the strategy parameters chosen by you in addition to other IB-specific settings. 
Details of the configuration specification can be found in the [ib_configs](https://github.com/vthoquant/auto_X_dist/blob/main/lib/configs/ib_configs.py) file. Let us take an example of the default *run_name* parameter, i.e. *intraday-macd-usdinr*. 
We lookup the keys of **STRATEGY_IB_CONFIG_MAP** for the *\'intraday-macd-usdinr\'* key within the ib_configs file. The value corresponding to that key is the configuration set on which the strategy is going to be run.
Given that the IB configuration set is quite extensive, we devote an entire [subsection](#ib-configs) below for its description
- *tickers*: *\<same as the corresponding argument used for the backtest\>*
- *initial_capital*: *\<same as the corresponding argument used for the backtest\>*

An example execution may look like the one below
```sh
$ python run_live_ib.py --run_name=intraday-macd-usdinr --tickers=USDINR --interval=15min --initial_capital=10000000
```
```sh
$ python run_live_ib_multi.py --main_run_name=intraday-mrev-nifty-multi-5m --tickers=NIFTY50.NS --interval=5min --initial_capital=5000000
```

The [run_live_ib_multi](https://github.com/vthoquant/auto_X_dist/blob/main/lib/examples/run_live_ib_multi.py) executable is more or less the same as the run_live_ib.py executable with the exception of one argument. 
*run_name* is replaced by *main_run_name* as the intention of this executable is actually to run multiple *\'run_name\'*s if they all depend on the same marketdata. 
The 'multi-run' configuration details can also be found by looking up the relevant key in the **STRATEGY_IB_CONFIG_MAP** variable in the ib_configs file. <br />

The script once executed is going to wait for the market open and then download all the historical data as specified within the run config. It is then going to generate signals and orders with every new candlestick that is received. 
This will go on until close of market after which each strategy would save-down 2 files into the same  strategy folder that has bene described in previous sections. The files have the same name as the *run_name* argument provided as part of this executable. 
Additionally there are 2 suffixes. The first script is suffixed with '-live-\<dateToday\>'. This is similar to the '-algo' file discussed earlier in the Backtesting section. The second file is suffixed with '-perf' and is similar to the '-bt' file discussed in earlier. 
Each day the performance metrics along-with the parameters used for that day are going to be appended and saved-down into this csv. 

#### IB configs

We start-off with the standard config defition and then move on to the 'multi-config' definition by simply highlighting the differences. Lets continue with the *intraday-macd-usdinr* example. 
The config value corresponding to this run can be found in the **INTDY_MACD_USDINR** variable. Below are the components we see
- *strategy_name*: This corresponds to the 'class name' of the strategy that is to be run. 
One can recall that the list of all available class names in the repository currently can be found in the [strategy_mapper](https://github.com/vthoquant/auto_X_dist/blob/main/lib/configs/strategy_mapper.py) file
- *params*: the strategy parameters using which the strategy class, above, is initialized. These params are ofcourse strategy-specific and would tally **exactly** with the strategy *params* used in the backtest and optimization configs
- *api_attrs*: This constitutes the set of parameters using which the **IB_API** wrapper class is initialzed. While the implementation of this wrapper class itself is infrastructural and of no consequence to the end-user, 
the parameters using which it is initialized is by itself important in terms of how the strategy would be eventually executed on TWS or IB gateway. Details of these parameters can be found below
	- *historical_data_offset*: We need to specify the amount of storage space to be kept in cache for the historical data. This is specified in terms of seconds. 
	This is necessary because one would need historical data to generate current signals for example historical prices to be used to generate an EMA. This calculation would need to be done manually by the user based on the strategy params that they plan on using. 
	For example if i require a 50-EMA on 30 min bar data that would mean I would need access to alteast 25 hours of trading data. That is a little more than 4 trading days, so we count 5. 
	However there could be trading holidays in between (atleast the weekend) so we need to add atleast 2 more days so that comes up to 7. Therefore the value of this parameter would need to be anything greater than 86000\*7. 
	Please note that there is no harm is specifying a higher offset value - it would only mean that there would be a bunch of empty rows in the cache (which would anyways be deleted later). 
	However specifying a smaller value than whats required could lead to us not having access to necessary historical data to compute our technicals. 
	- *client_id*: The TWS session acts as a sort of local server serving any number of python scripts that try to connect to it for their purpose. The *client_id* is used to differentiate between these individual python scripts. 
	This can be any natural number but point to note is that there cannot be two python scripts running at the same time with the same client_id. The TWS session would connect to and consequently serve only one of them
	- *order_config*: This drives the mechanism by which the orders are actually executed. For example a 'long' signal in your strategy can be actually executed many ways. You could either go long the futures or buy a call or sell a put or even go long the cash equity. 
	Vice-versa for a sell signal. Additionally for options one could trade using the weeklies or monthlies, ATM, OTM, ITM etc. On each of these poteential trading instruments one could fire market, 
	market limit or limit orders or maybe even leverage one of the many execution algos IB exposes to us. 
	As a result, the sub-attributes one can specify under *order_config* are as follows
		- *inst*: This could be one of 'OPT'(options), 'FUT'(futures) or 'STK'(stock/cash)
		- *dir*: only used when *inst* is set to 'OPT'. This attribute could be set to either 'BUY' (buy options) or 'SELL' (sell options)
		- *exp*: This is also used only when *inst* is set to 'OPT'. It can be set to 'weekly', 'bi-weekly' or 'monthly'
		- *strike_mode*: only used whrn *inst* is set to 'OPT'. As of now can be 'atm_minus' (close to ATM but on the OTM side) and 'atm_plus' (close to ATM but on the ITM side)
		- *order_type*: Can be 'MKT' (market), 'MTL' (marketeble limit) or 'LMT' (limit)
		- *algo_attrs*: in-case we would like to execute using one of IBs propriety execution algos. This is a dictionary where the keys and values need to tally exactly with the ones accepted by the IB APIs (such as *algoStrategy* and *algoParams*)
- *api_data_config*: Controls the format in which we receive the bar-data. It has 2 sub-attributes
	- *barSizeSetting*: the bar-data size. Can be '1 min', '5 mins', '15 mins' etc
	- *durationStr*: The number of trading days for which historical data needs to be loaded. Note that this needs to somewhat tally with the *historical_data_offset* parameter we set above. 
	This attribute is the number of trading days so would be typically lower than the value we set against *historical_data_offset*
- *event_wait_time*: The amount of time (in seconds) at which we periodically query for the arrival of a new candlestick. For most strategies this has been set to 1s although for strategies which require to be run on smaller timeframes, we could reduce this even further

The multi-run configurations invoked via the [run_live_ib_multi](https://github.com/vthoquant/auto_X_dist/blob/main/lib/examples/run_live_ib_multi.py) executable differ from the single-run configurations in only one aspect - 
the *params* attribute is replaced by the *multi_strategy_params* attribute. This new attribute is nothing but a collection of multpile individual strategy *params*. 
For the multi-run executable every other attribute such as *api_attrs*, *api_data_config* etc is exactly the same as the single-run executable.
Multi-run executables are useful when multiple strategies depend upon the same market data. If so then one can limit the number of client connections to the local TWS server to 1 instead of having seperate clients for each strategy

### Advanced Backtesting and Optimization
auto_X provides the user with various features to help carry out the backtesting assessment under certain real-life constraints. Three features are currently available:-
- **Re-scale** a short position which is currently running into losses
- Subtract **transaction costs**, such as taxes, brokerages and slippages, from the gross PnL of the trade
- Trade on **synthetic options** to get an idea of the impact of convexity and time decay on you trades

#### Re-scale shorts
For cash-market trades, the amount of margin one requires to hold a long position is typically equal to the spot price of the position. Therefore, any increase (or decrease) in the spot value of the underlying doesnt lead to any margin excess (or shortfall)
because the change in margin is exactly offset by the change in underlying value. However for short cash-market trades this becaomes a bit tricky. Firstly, the amount of margin required to be set aside for short trades is not necessarily standard. In our platform for simplicity
we assume that the margin required is exactly equal to the value of the position that is being shorted i.e. shorting trades would lead to no instantaneous cash credit. Subsequently if the value of the underlying goes up then the value of the short position goes down
by the same amount. Consequently, we would now require a higher margin to maintain the same short position (eg: we short 1 stock worth $100 and have to put aside $100 as margin. In the next instance suppose the stock goes up to $110, our portfolio would drop in value to $90.
However, we would need to put in $20 more to ensure that the prevailing margin requirement of $110 is maintained). There are two ways in which this issue could be circumvented. One is by scaling down the short position so that the amount we have shorted is exactly equal to our
current portfolio value. The second is to take up a loan to offset the margin shortfall. The *rescale_shorts* parameter that can be passed into any strategy object as a parameter (along-with other strategy-specific parameters) would control the strategy behaviour for shorts. A parameter value of True would lead to the position
size being re-adjusted whereas a parameter value of False would lead to an interest-free loan being taken to offset the shortfall

#### Transaction costs
PnL computed as part of a vanilla backtesting run is never the PnL that would actually have been realized during that period. The reason is that one typically incurrs additional costs as part of trading including but not limited to exchange charges, taxes, brokerages and slippages. 
We therefore provide a mechanism to the user to be able to add these costs into their backtesting run so that the final results are as closely representative of the actual realized PnL as possible. This feature would prove all the more useful for relatively higher frequency strategies which depend
on executing a large number of trades in a day (>5) or even scalping-style strategies where the targets and stop-losses are set very tight.

In order to enable this feature we first ensure that we configure the correct costs which are to be applied. Different costs can be applied seperately to options, futures and stock. We can also specify underlying-specific costs in each category. The values can be specified in
the [transaction_costs](https://github.com/vthoquant/auto_X_dist/blob/main/lib/configs/transaction_costs.py) config file. As mentioned earlier, the user can specify a different set of costs for options (under the **OPTIONS_COSTS_CONFIG** variable) and for futures (under the **FUTURES_COSTS_CONFIG** variable).
Under each variable one can find keys corresponding to the underlying-specific costs and also default costs in-case nothing is specifided. Against each item, one can specify **slippage_perc** (slippage as a percentage of execution price), **slippage_fixed** (slippage as a fixed cost per unit traded), **brokerage_fixed**
(fixed brokerage per trade), **brokerage_perc** (brokerage as a percentage of traded value) and **tax_perc** (tax as a percentage of traded value). For options-based trading, we can additionally specify an **options_config**, with sub-keys **ttm** (time-to-maturity) and **imp_vol** (implied vol) which would be used to 
compute an approximate ATM options price. Slippages and taxes would then be computed on this approximate price.

Once the costs are correclty documented in the config file, we would also addiitonally require to switch a toggle ON or OFF depending upon whether we require these charges to be applied in our backtesting or optimization. This is controlled via the **add_transaction_costs** parameter that is to be passed along-with other strategy parameters
into the strategy object. This parameter can take a boolean as its input

#### Synthetic Options
This feature has been added to allow the user to get an idea about the impact of convexity and time-decay that trading a non-linear instrument such as an option can have on your strategy and compare the benefits or drawbacks of trading an option vs linear instruments such as futures or cash. Here, we essentially assume that we trade in options
but given that we may not actually have access to historical options data, we compute our own synthetic options data. For indices we assume we trade in weekly options expiring on thursday while on the other hand for stocks we assume we trade in monthly options expiring on the last thursday of the month. The time to expiry is then computed on-the-fly depending
on the current backtesting time. A risk-free rate is also specified in a config, details of which are provided below. The distance from ATM that we would like to trade on can also be specified in one of those configs. The implied vol used in the price computation is basically a premium added on top of the historical vol. The historical vol is computed using the
conventional method over 30 days whereas the vol premium to be used for our backtesting would be specified in the config, details of which can be found below. Once these inputs are computed the synthetic price is then computed via the usual Black Scholes formula. 

Enabling this feature would significantly increase the runtime of the backtest. Therfore it is advisable to only turn this on when running single backtests and not optimizations over hundreds of backtests!

The setup needs to be carried out in the [synth_options_config](https://github.com/vthoquant/auto_X_dist/blob/main/lib/configs/synth_options_config.py)file. There are two variable categories that are of importance. One is a global specification and the other is the asset specification.
The global specification mapping can be found in the **OPTION_TRADE_CHOICES** variable while the asset specification mapping can be found in the **TICKER_TO_OPT_CONFIG** variable. 

Each asset specification contains certain components that need to be specified:- 
- The **imp_vol** which is an implied vol floor to be applied to the underlying. 
- The **rr** which is the risk-free rate and 
- The **strike_gap** which is the rupee-value gap between adjacent strikes that are 
openly traded in the market. 

The global specification contains another set of components that need to be specified:-
- The **short_options_or_fut** parameter. A value equal to True would mean that we would like to run our synthetic options backtest on futures or short options. The reason these two are clibbed together is the margin requirement which is almost comparable between the two
 - **is_fut** is used when the value of the above parameter is True. This is to ensure that we end up computing the correct synthetic price during backtesting. A parameter value of False would ensure that we correctly incorporate theta-decay and convexity adjustments to our
futures price
- **short_opt_lev** is the approximate leverage on capital we obtain when we trade futures or short options. This is applicable only when the **short_options_or_fut** parameter is set to True. For example a leverage of 5 would mean that a Rs 100000 margin would ensure that we could 
obtain a total notional exposure via futures or short options of Rs 500000
- The **imp_vol_mult** which is a multiplier that can be applied to the floor which is specified in the above asset specification.
- The **vol_premium** which is the volatility premium that would be added
- **max_lev_alloc** is only applicable for long options i.e. when the **short_options_or_fut** parameter is set to False. This parameter controls the fraction of our total capital that we allocate to buying options. For example a value of 0.05 would mean that we only set aside 5% of
our capital to buying options. The reason why this parameter is necessary is because a very large allocation would almost always ensure that we run a very high risk of ruin as the probability of an OTM option going to 0 at expiry is high. 
- **strike_gap_mult** is the distance away from the ATM that we would like our synthetic prices to be computed. This can take both negative (OTM) and positive (ITM) values. This integer value is multiplied by the **strike_gap** parameter to get the actual distance in rupees for a given underlying.  
on top of the 30-day historical vol. 

Once the specifications are filled-in correctly in the config file, we would then need to toggle a switch to turn ON or OFF the synthetic options feature. This parameter is called **use_synthetic_options** and is to be passed-in just as any other strategy parameter.
One can also publish various relevant metrics in the -algo file, such as the prevailing call and put strikes that was traded along-with its option type and current price so that the user can run a manual debug and ensure that the syuunthetic options usage is correct

## Data format

As of writing this, the historical candlestick data used for the purpose of backtesting and optimization is expected to be in a format which is in-line with the one seen in the [test_data](https://github.com/vthoquant/auto_X_dist/tree/main/test_data/) folder. 
Additionally they need to be placed in a subfolder which align with the subfolder set against the **LOCAL_INTRADAY_STORE_PATH** variable in the [directory_names](https://github.com/vthoquant/auto_X_dist/blob/main/lib/configs/directory_names.py) config file. 

## Maintainers
This repo is owned and maintained by **Vivin Thomas**. In case of any concerns or queries regarding this project, help with any deployment, or additional development requests please feel free to contact me on my [linkedin](https://www.linkedin.com/in/vivin-thomas-7885a2130)

## Contributing
Please feel free to add to the configs and strategy files that are available for view and edit and issue any pull requests. For any contributions to be made to the compiled infrastructure code, please contact me on my [linkedin](https://www.linkedin.com/in/vivin-thomas-7885a2130)

## License

(LICENSE) © Vivin Thomas <br />
Unauthorized distribution and access to restricted compiled code is prohibited