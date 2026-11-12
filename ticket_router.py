"""Print canonical initial team suggestions; these are not accepted assignments."""
from pathlib import Path
import pandas as pd
from support_rules import route_ticket

BASE_DIR = Path(__file__).resolve().parent


def main():
    tickets = pd.read_csv(BASE_DIR / "tickets.csv")
    print("SUGGESTED INITIAL SUPPORT ROUTING")
    print(pd.DataFrame([route_ticket(row) for _, row in tickets.iterrows()]).to_string(index=False))


if __name__ == "__main__":
    main()
