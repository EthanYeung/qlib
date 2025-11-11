# 简单量化交易示例 / Simple Quantitative Trading Example

## 概述 / Overview

这是一个完整的量化交易工作流程示例，适合初学者学习如何使用 Qlib 进行量化交易。

This is a complete quantitative trading workflow example, perfect for beginners to learn how to use Qlib for quantitative trading.

## 功能特性 / Features

本示例展示了量化交易的完整流程：

This example demonstrates the complete quantitative trading workflow:

1. **数据准备** / **Data Preparation**
   - 自动下载和准备中国 A 股市场数据 / Automatically download and prepare China A-share market data
   - 使用 CSI300 股票池 / Using CSI300 stock pool

2. **特征工程** / **Feature Engineering**
   - 使用 Alpha158 特征集（158个技术指标）/ Using Alpha158 feature set (158 technical indicators)
   - 包括价格、成交量、动量等多维度特征 / Including price, volume, momentum and other multi-dimensional features

3. **模型训练** / **Model Training**
   - 使用 LightGBM 机器学习模型 / Using LightGBM machine learning model
   - 自动进行特征选择和参数优化 / Automatic feature selection and parameter optimization

4. **回测** / **Backtesting**
   - 模拟真实交易环境 / Simulate real trading environment
   - 考虑交易成本和市场限制 / Consider trading costs and market constraints
   - TopkDropout 策略：持有前50只股票，每期换仓5只 / TopkDropout strategy: Hold top 50 stocks, rebalance 5 per period

5. **性能分析** / **Performance Analysis**
   - 生成详细的回测报告 / Generate detailed backtest reports
   - 计算各种性能指标 / Calculate various performance metrics
   - 与基准指数（CSI300）对比 / Compare with benchmark (CSI300)

## 安装要求 / Requirements

```bash
# 安装 Qlib / Install Qlib
pip install pyqlib

# 或从源码安装 / Or install from source
git clone https://github.com/microsoft/qlib.git
cd qlib
pip install -e .
```

## 使用方法 / Usage

### 基本运行 / Basic Run

```bash
cd examples
python simple_quant_trading.py
```

### 数据说明 / Data Information

- **数据源** / **Data Source**: 中国 A 股市场数据 / China A-share market data
- **时间范围** / **Time Range**: 2008-2020
- **股票池** / **Stock Pool**: CSI300（沪深300指数成分股）/ CSI300 constituents
- **数据存储位置** / **Data Storage**: `~/.qlib/qlib_data/cn_data`

首次运行时会自动下载数据（约500MB），请确保网络连接正常。

Data will be automatically downloaded on first run (about 500MB), please ensure stable network connection.

### 配置参数 / Configuration

示例中的关键参数：

Key parameters in the example:

```python
# 模型参数 / Model Parameters
model_config = {
    "learning_rate": 0.0421,
    "max_depth": 8,
    "num_leaves": 210,
    ...
}

# 数据集划分 / Dataset Split
"train": ("2008-01-01", "2014-12-31"),  # 7年训练数据 / 7 years training
"valid": ("2015-01-01", "2016-12-31"),  # 2年验证数据 / 2 years validation
"test": ("2017-01-01", "2020-08-01"),   # 3.5年测试数据 / 3.5 years testing

# 交易策略 / Trading Strategy
"topk": 50,      # 持有前50只股票 / Hold top 50 stocks
"n_drop": 5,     # 每期换仓5只 / Rebalance 5 per period

# 交易成本 / Trading Costs
"open_cost": 0.0005,   # 0.05% 开仓成本 / open cost
"close_cost": 0.0015,  # 0.15% 平仓成本 / close cost
```

## 输出结果 / Output

运行成功后，会生成以下结果：

After successful execution, the following results will be generated:

1. **mlruns/** 目录 / **mlruns/** directory
   - 包含所有实验结果和模型 / Contains all experiment results and models
   - 可使用 MLflow UI 查看 / Can be viewed using MLflow UI

2. **控制台输出** / **Console Output**
   - 训练过程信息 / Training process information
   - 数据统计 / Data statistics
   - 回测结果摘要 / Backtest results summary

3. **性能指标** / **Performance Metrics**
   - 年化收益率 / Annualized return
   - 夏普比率 / Sharpe ratio
   - 最大回撤 / Maximum drawdown
   - 信息比率 / Information ratio
   - 超额收益 / Excess return

## 示例输出 / Example Output

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                     简单量化交易示例                                           ║
║                Simple Quantitative Trading Example                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

================================================================================
步骤 1: 准备数据 / Step 1: Preparing Data
================================================================================
✓ 数据准备完成 / Data preparation completed

================================================================================
步骤 2: 配置模型和数据集 / Step 2: Configuring Model and Dataset
================================================================================
✓ 模型类型 / Model type: LightGBM
✓ 特征集 / Feature set: Alpha158 (158 features)
✓ 训练期 / Training period: 2008-01-01 to 2014-12-31
...
```

## 查看详细结果 / View Detailed Results

### 使用 MLflow UI

```bash
# 在 examples 目录下运行 / Run in examples directory
mlflow ui

# 然后在浏览器中打开 / Then open in browser
# http://localhost:5000
```

### 使用 Jupyter Notebook

查看更详细的可视化分析，运行：

For more detailed visualization analysis, run:

```bash
jupyter notebook examples/workflow_by_code.ipynb
```

## 扩展和定制 / Extensions and Customization

### 修改股票池 / Change Stock Pool

```python
# 修改为其他市场 / Change to other markets
"instruments": "csi100",  # CSI100
"instruments": "csi500",  # CSI500
```

### 调整策略参数 / Adjust Strategy Parameters

```python
# 修改持仓数量和换仓频率 / Change position size and rebalance frequency
"topk": 30,      # 持有30只股票 / Hold 30 stocks
"n_drop": 3,     # 每期换仓3只 / Rebalance 3 per period
```

### 更换模型 / Change Model

```python
# 使用 XGBoost 代替 LightGBM / Use XGBoost instead of LightGBM
model_config = {
    "class": "XGBModel",
    "module_path": "qlib.contrib.model.xgboost",
    ...
}
```

## 常见问题 / FAQ

### Q: 首次运行下载数据失败？
A: 请检查网络连接，或手动下载数据：
```bash
python scripts/get_data.py qlib_data --target_dir ~/.qlib/qlib_data/cn_data --region cn
```

### Q: First run data download failed?
A: Please check network connection, or manually download data:
```bash
python scripts/get_data.py qlib_data --target_dir ~/.qlib/qlib_data/cn_data --region cn
```

### Q: 内存不足？
A: 建议至少 16GB 内存。可以减少股票池大小或缩短时间范围。

### Q: Out of memory?
A: Recommend at least 16GB RAM. You can reduce stock pool size or shorten time range.

### Q: 如何理解回测结果？
A: 主要关注以下指标：
- 年化收益率（Annualized Return）：年化的平均收益
- 夏普比率（Sharpe Ratio）：风险调整后的收益，越高越好
- 最大回撤（Maximum Drawdown）：最大的资产下跌幅度
- 信息比率（Information Ratio）：相对于基准的超额收益

### Q: How to understand backtest results?
A: Focus on these key metrics:
- Annualized Return: Average return per year
- Sharpe Ratio: Risk-adjusted return, higher is better
- Maximum Drawdown: Largest decline in assets
- Information Ratio: Excess return relative to benchmark

## 相关资源 / Related Resources

- [Qlib 官方文档 / Official Documentation](https://qlib.readthedocs.io/)
- [Qlib GitHub 仓库 / GitHub Repository](https://github.com/microsoft/qlib)
- [Qlib 论文 / Research Paper](https://arxiv.org/abs/2009.11189)
- [更多示例 / More Examples](https://github.com/microsoft/qlib/tree/main/examples)

## 下一步 / Next Steps

学完这个示例后，您可以：

After completing this example, you can:

1. 尝试 `workflow_by_code.ipynb` 了解更多可视化分析 / Try `workflow_by_code.ipynb` for more visualization
2. 探索 `examples/benchmarks/` 中的高级模型 / Explore advanced models in `examples/benchmarks/`
3. 学习自定义因子和模型 / Learn to customize factors and models
4. 了解高频交易和订单执行 / Learn about high-frequency trading and order execution

## 许可证 / License

Copyright (c) Microsoft Corporation. Licensed under the MIT License.
