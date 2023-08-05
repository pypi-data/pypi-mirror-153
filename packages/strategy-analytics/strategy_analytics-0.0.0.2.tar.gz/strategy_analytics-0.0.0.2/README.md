## Strategy Analytics Library

The **Strategy Analytics Library** is a python package that contains a function to compute two tables. The function is called 'strategy_stats' and it produces the following output: 

1. A drawdown table in which you will get the 10 most important drawdowns of the strategy returns you give as an input
2. A second table showing the Sharpe Ratio, the CAGR and the Maximum Drawdown


###  Install

```
$ pip install strategy_analytics
```

### Usage

Open a Python console, import the module strategy_analytics, and use the function strategy_stats together with a strategy_returns as input 😉

```
>> import strategy_analytics as sa
>>
>> sa.strategy_stats(strategy_returns)
```


### License

This project is licensed under the MIT License


### Author

[QuantInsti - Quantra Team](https://www.quantinsti.com/)
