# Mark1 -- My first strategy
Author: @Yanzhong Huang  
Created: 22 Nov 2-21  
___
## requirements  
- python==3.9.7
- backtrader  
    backtrader installation command:  
  
```pip install git+https://github.com/mementum/backtrader.git@0fa63ef4a35dc53cc7320813f8b15480c8f85517#egg=backtrader```
- pandas  
- tushare  
- jupyter
- numpy
- matplotlib
___
## General strategy  
1. Rank all stocks by BM ratio. -> select stocks in index or universal?  
2. For high BM ratio: Piotroski F score
3. For Low BM ratio: G score
4. Use Neural network predict return -> identify theta
5. back test theta and holding period  

___
## Data we need
> data source: waditu.com  

### Piotroski F score

**Performance factor**  
- ROA
- CFO
- Delta ROA
- Accrual

**Leverage liquidity and source of funds**  
- Delta leverage
- Delta liquid
- EQ offer

**Operating Efficiency**
- Delta margin
- Delta Turnover

