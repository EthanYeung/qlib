#  Copyright (c) Microsoft Corporation.
#  Licensed under the MIT License.

"""
Test for the simple quantitative trading example
"""

import sys
import os
import pytest

# Add examples to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "examples"))


class TestSimpleQuantTrading:
    """Test simple quantitative trading example"""

    def test_import_example(self):
        """Test that the example module can be imported"""
        try:
            import simple_quant_trading
            assert hasattr(simple_quant_trading, "main")
            assert hasattr(simple_quant_trading, "prepare_data")
            assert hasattr(simple_quant_trading, "create_model_and_dataset")
            assert hasattr(simple_quant_trading, "train_model")
            assert hasattr(simple_quant_trading, "create_backtest_config")
            assert hasattr(simple_quant_trading, "run_backtest_and_analysis")
        except ImportError as e:
            pytest.fail(f"Failed to import simple_quant_trading: {e}")

    def test_create_backtest_config(self):
        """Test backtest configuration creation"""
        import simple_quant_trading
        
        config = simple_quant_trading.create_backtest_config()
        
        # Verify config structure
        assert "executor" in config
        assert "strategy" in config
        assert "backtest" in config
        
        # Verify executor config
        assert config["executor"]["class"] == "SimulatorExecutor"
        assert config["executor"]["module_path"] == "qlib.backtest.executor"
        
        # Verify strategy config
        assert config["strategy"]["class"] == "TopkDropoutStrategy"
        assert config["strategy"]["kwargs"]["topk"] == 50
        assert config["strategy"]["kwargs"]["n_drop"] == 5
        
        # Verify backtest config
        assert config["backtest"]["account"] == 100000000
        assert config["backtest"]["benchmark"] == "SH000300"
        assert config["backtest"]["start_time"] == "2017-01-01"
        assert config["backtest"]["end_time"] == "2020-08-01"

    def test_function_signatures(self):
        """Test that functions have correct signatures"""
        import simple_quant_trading
        import inspect
        
        # Check prepare_data signature
        sig = inspect.signature(simple_quant_trading.prepare_data)
        assert "provider_uri" in sig.parameters
        assert "region" in sig.parameters
        
        # Check create_model_and_dataset signature
        sig = inspect.signature(simple_quant_trading.create_model_and_dataset)
        # Should return tuple
        
        # Check train_model signature
        sig = inspect.signature(simple_quant_trading.train_model)
        assert "model" in sig.parameters
        assert "dataset" in sig.parameters
        
        # Check run_backtest_and_analysis signature
        sig = inspect.signature(simple_quant_trading.run_backtest_and_analysis)
        assert "model" in sig.parameters
        assert "dataset" in sig.parameters
        assert "backtest_config" in sig.parameters
