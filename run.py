import argparse
import yaml
import pandas as pd
import numpy as np
import json
import logging
import time
import sys
import os


# ------------------ LOGGER ------------------
def setup_logger(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


# ------------------ CONFIG ------------------
def load_config(config_path):
    if not os.path.exists(config_path):
        raise Exception("Config file not found")

    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
    except Exception:
        raise Exception("Invalid YAML format")

    required_keys = ["seed", "window", "version"]
    for key in required_keys:
        if key not in config:
            raise Exception(f"Missing config key: {key}")

    return config


# ------------------ DATA ------------------
def load_data(input_path):
    if not os.path.exists(input_path):
        raise Exception("Input CSV file not found")

    try:
        df = pd.read_csv(input_path)
    except Exception:
        raise Exception("Invalid CSV format")

    if df.empty:
        raise Exception("CSV file is empty")

    if "close" not in df.columns:
        raise Exception("Missing 'close' column")

    return df


# ------------------ MAIN ------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)

    args = parser.parse_args()

    setup_logger(args.log_file)
    start_time = time.time()

    try:
        logging.info("Job started")

        # Load config
        config = load_config(args.config)
        seed = config["seed"]
        window = config["window"]
        version = config["version"]

        np.random.seed(seed)
        logging.info(f"Config loaded: seed={seed}, window={window}, version={version}")

        # Load data
        df = load_data(args.input)
        logging.info(f"Rows loaded: {len(df)}")

        # Rolling mean
        df["rolling_mean"] = df["close"].rolling(window=window).mean()
        logging.info("Rolling mean computed")

        # Signal (handle NaNs properly)
        df["signal"] = np.where(
            df["rolling_mean"].notna(),
            (df["close"] > df["rolling_mean"]).astype(int),
            np.nan
        )
        logging.info("Signal generated")

        # Only valid rows for metrics
        valid_signals = df["signal"].dropna()

        rows_processed = len(valid_signals)
        if rows_processed == 0:
            raise Exception("No valid rows after rolling mean computation")

        signal_rate = float(valid_signals.mean())

        latency_ms = int((time.time() - start_time) * 1000)

        metrics = {
            "version": version,
            "rows_processed": rows_processed,
            "metric": "signal_rate",
            "value": round(signal_rate, 4),
            "latency_ms": latency_ms,
            "seed": seed,
            "status": "success"
        }

        logging.info(f"Metrics: {metrics}")
        logging.info("Job completed successfully")

        with open(args.output, "w") as f:
            json.dump(metrics, f, indent=2)

        print(json.dumps(metrics, indent=2))
        sys.exit(0)

    except Exception as e:
        latency_ms = int((time.time() - start_time) * 1000)

        error_metrics = {
            "version": "v1",
            "status": "error",
            "error_message": str(e)
        }

        logging.error(f"Error: {str(e)}")

        with open(args.output, "w") as f:
            json.dump(error_metrics, f, indent=2)

        print(json.dumps(error_metrics, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
