#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright (c) Microsoft Corporation.
#  Licensed under the MIT License.

"""
简单量化交易示例 / Simple Quantitative Trading Example
====================================================

这是一个完整的量化交易工作流程示例，展示了如何使用 Qlib 进行：
1. 数据准备和加载
2. 特征工程
3. 模型训练
4. 回测
5. 性能分析

This is a complete quantitative trading workflow example that demonstrates:
1. Data preparation and loading
2. Feature engineering
3. Model training
4. Backtesting
5. Performance analysis

使用方法 / Usage:
    python simple_quant_trading.py

Requirements:
    - Qlib installed with all dependencies
    - Data downloaded (will be automatically downloaded if not present)
"""

import qlib
import pandas as pd
from qlib.constant import REG_CN
from qlib.utils import init_instance_by_config, flatten_dict
from qlib.workflow import R
from qlib.workflow.record_temp import SignalRecord, PortAnaRecord, SigAnaRecord
from qlib.tests.data import GetData


def prepare_data(provider_uri="~/.qlib/qlib_data/cn_data", region=REG_CN):
    """
    准备和加载数据 / Prepare and load data
    
    Args:
        provider_uri: 数据存储路径 / Path to store data
        region: 区域配置 / Region configuration
    """
    print("=" * 80)
    print("步骤 1: 准备数据 / Step 1: Preparing Data")
    print("=" * 80)
    
    # 下载和准备数据 / Download and prepare data
    GetData().qlib_data(target_dir=provider_uri, region=region, exists_skip=True)
    
    # 初始化 Qlib / Initialize Qlib
    qlib.init(provider_uri=provider_uri, region=region)
    
    print("✓ 数据准备完成 / Data preparation completed\n")


def create_model_and_dataset():
    """
    创建模型和数据集配置 / Create model and dataset configuration
    
    Returns:
        tuple: (model, dataset) - 模型和数据集对象 / Model and dataset objects
    """
    print("=" * 80)
    print("步骤 2: 配置模型和数据集 / Step 2: Configuring Model and Dataset")
    print("=" * 80)
    
    # 定义模型配置 / Define model configuration
    # 使用 LightGBM 作为预测模型 / Using LightGBM as prediction model
    model_config = {
        "class": "LGBModel",
        "module_path": "qlib.contrib.model.gbdt",
        "kwargs": {
            "loss": "mse",
            "colsample_bytree": 0.8879,
            "learning_rate": 0.0421,
            "subsample": 0.8789,
            "lambda_l1": 205.6999,
            "lambda_l2": 580.9768,
            "max_depth": 8,
            "num_leaves": 210,
            "num_threads": 20,
        },
    }
    
    # 定义数据集配置 / Define dataset configuration
    # Alpha158 是一个包含158个特征的数据集 / Alpha158 is a dataset with 158 features
    dataset_config = {
        "class": "DatasetH",
        "module_path": "qlib.data.dataset",
        "kwargs": {
            "handler": {
                "class": "Alpha158",
                "module_path": "qlib.contrib.data.handler",
                "kwargs": {
                    "start_time": "2008-01-01",
                    "end_time": "2020-08-01",
                    "fit_start_time": "2008-01-01",
                    "fit_end_time": "2014-12-31",
                    "instruments": "csi300",
                },
            },
            "segments": {
                "train": ("2008-01-01", "2014-12-31"),
                "valid": ("2015-01-01", "2016-12-31"),
                "test": ("2017-01-01", "2020-08-01"),
            },
        },
    }
    
    # 初始化模型和数据集 / Initialize model and dataset
    model = init_instance_by_config(model_config)
    dataset = init_instance_by_config(dataset_config)
    
    print("✓ 模型类型 / Model type: LightGBM")
    print("✓ 特征集 / Feature set: Alpha158 (158 features)")
    print("✓ 训练期 / Training period: 2008-01-01 to 2014-12-31")
    print("✓ 验证期 / Validation period: 2015-01-01 to 2016-12-31")
    print("✓ 测试期 / Test period: 2017-01-01 to 2020-08-01")
    print("✓ 股票池 / Stock pool: CSI300\n")
    
    return model, dataset


def train_model(model, dataset):
    """
    训练模型 / Train the model
    
    Args:
        model: 机器学习模型 / Machine learning model
        dataset: 训练数据集 / Training dataset
    """
    print("=" * 80)
    print("步骤 3: 训练模型 / Step 3: Training Model")
    print("=" * 80)
    
    # 查看数据样本 / View data sample
    print("数据样本 / Data sample:")
    example_df = dataset.prepare("train")
    print(example_df.head())
    print(f"数据集形状 / Dataset shape: {example_df.shape}\n")
    
    # 训练模型 / Train model
    print("开始训练模型... / Starting model training...")
    model.fit(dataset)
    print("✓ 模型训练完成 / Model training completed\n")


def create_backtest_config():
    """
    创建回测配置 / Create backtest configuration
    
    Returns:
        dict: 回测配置 / Backtest configuration
    """
    print("=" * 80)
    print("步骤 4: 配置回测 / Step 4: Configuring Backtest")
    print("=" * 80)
    
    backtest_config = {
        "executor": {
            "class": "SimulatorExecutor",
            "module_path": "qlib.backtest.executor",
            "kwargs": {
                "time_per_step": "day",
                "generate_portfolio_metrics": True,
            },
        },
        "strategy": {
            "class": "TopkDropoutStrategy",
            "module_path": "qlib.contrib.strategy.signal_strategy",
            "kwargs": {
                "signal": None,  # Will be set later
                "topk": 50,
                "n_drop": 5,
            },
        },
        "backtest": {
            "start_time": "2017-01-01",
            "end_time": "2020-08-01",
            "account": 100000000,
            "benchmark": "SH000300",
            "exchange_kwargs": {
                "freq": "day",
                "limit_threshold": 0.095,
                "deal_price": "close",
                "open_cost": 0.0005,
                "close_cost": 0.0015,
                "min_cost": 5,
            },
        },
    }
    
    print("✓ 回测期间 / Backtest period: 2017-01-01 to 2020-08-01")
    print("✓ 初始资金 / Initial capital: 100,000,000")
    print("✓ 基准指数 / Benchmark: SH000300 (CSI300)")
    print("✓ 策略 / Strategy: TopkDropout (持有前50只股票，每期换仓5只)")
    print("  TopkDropout (Hold top 50 stocks, rebalance 5 stocks per period)")
    print("✓ 交易成本 / Trading costs:")
    print("  - 开仓成本 / Open cost: 0.05%")
    print("  - 平仓成本 / Close cost: 0.15%")
    print("  - 最小成本 / Min cost: 5\n")
    
    return backtest_config


def run_backtest_and_analysis(model, dataset, backtest_config):
    """
    运行回测和分析 / Run backtest and analysis
    
    Args:
        model: 训练好的模型 / Trained model
        dataset: 数据集 / Dataset
        backtest_config: 回测配置 / Backtest configuration
    """
    print("=" * 80)
    print("步骤 5: 运行回测和分析 / Step 5: Running Backtest and Analysis")
    print("=" * 80)
    
    # 设置策略信号 / Set strategy signal
    backtest_config["strategy"]["kwargs"]["signal"] = (model, dataset)
    
    # 开始实验 / Start experiment
    with R.start(experiment_name="simple_quant_trading"):
        # 保存模型 / Save model
        R.save_objects(**{"params.pkl": model})
        
        # 获取记录器 / Get recorder
        recorder = R.get_recorder()
        
        # 生成预测信号 / Generate prediction signals
        print("生成预测信号... / Generating prediction signals...")
        sr = SignalRecord(model, dataset, recorder)
        sr.generate()
        print("✓ 预测信号生成完成 / Prediction signals generated\n")
        
        # 信号分析 / Signal analysis
        print("进行信号分析... / Performing signal analysis...")
        sar = SigAnaRecord(recorder)
        sar.generate()
        print("✓ 信号分析完成 / Signal analysis completed\n")
        
        # 投资组合分析和回测 / Portfolio analysis and backtest
        print("运行回测... / Running backtest...")
        par = PortAnaRecord(recorder, backtest_config, "day")
        par.generate()
        print("✓ 回测完成 / Backtest completed\n")


def print_summary():
    """
    打印总结信息 / Print summary
    """
    print("=" * 80)
    print("完成！/ Completed!")
    print("=" * 80)
    print("""
量化交易流程已完成！/ Quantitative trading workflow completed!

您已经完成了以下步骤：
You have completed the following steps:

1. ✓ 数据准备 / Data preparation
2. ✓ 模型配置 / Model configuration  
3. ✓ 模型训练 / Model training
4. ✓ 回测配置 / Backtest configuration
5. ✓ 回测和分析 / Backtest and analysis

结果已保存在 mlruns 目录中。
Results are saved in the mlruns directory.

您可以查看：/ You can view:
- 预测信号 / Prediction signals
- 信号分析报告 / Signal analysis reports
- 投资组合表现 / Portfolio performance
- 回测结果 / Backtest results

要查看更多详细的分析图表，可以运行 examples/workflow_by_code.ipynb
For more detailed analysis charts, run examples/workflow_by_code.ipynb
""")


def main():
    """
    主函数 / Main function
    """
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     简单量化交易示例                                           ║
║                Simple Quantitative Trading Example                           ║
║                                                                              ║
║  这个示例展示了使用 Qlib 进行量化交易的完整流程                                  ║
║  This example demonstrates a complete quantitative trading workflow          ║
║  using Qlib library                                                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")
    
    try:
        # 步骤 1: 准备数据 / Step 1: Prepare data
        prepare_data()
        
        # 步骤 2: 创建模型和数据集 / Step 2: Create model and dataset
        model, dataset = create_model_and_dataset()
        
        # 步骤 3: 训练模型 / Step 3: Train model
        train_model(model, dataset)
        
        # 步骤 4: 创建回测配置 / Step 4: Create backtest configuration
        backtest_config = create_backtest_config()
        
        # 步骤 5: 运行回测和分析 / Step 5: Run backtest and analysis
        run_backtest_and_analysis(model, dataset, backtest_config)
        
        # 打印总结 / Print summary
        print_summary()
        
    except Exception as e:
        print(f"\n❌ 错误 / Error: {str(e)}")
        print("请确保已安装所有依赖项 / Please ensure all dependencies are installed")
        raise


if __name__ == "__main__":
    main()
