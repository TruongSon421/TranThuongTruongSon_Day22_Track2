"""
Run all lab steps sequentially.
Usage: python run_all.py [--step 1|2|3|4]
"""

import subprocess
import sys

STEPS = {
    1: "01_langsmith_rag_pipeline.py",
    2: "02_prompt_hub_ab_routing.py",
    3: "03_ragas_evaluation.py",
    4: "04_guardrails_validator.py",
}


def run_step(n):
    print(f"\n{'=' * 60}")
    print(f"  Running Step {n}: {STEPS[n]}")
    print(f"{'=' * 60}")
    result = subprocess.run([sys.executable, STEPS[n]])
    return result.returncode == 0


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--step", type=int, choices=[1, 2, 3, 4])
    args = parser.parse_args()

    steps = [args.step] if args.step else [1, 2, 3, 4]

    for step in steps:
        if not run_step(step):
            print(f"❌ Step {step} failed")
            sys.exit(1)

    print(f"\n✅ All steps completed successfully!")


if __name__ == "__main__":
    main()
