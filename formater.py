import csv
import json
from typing import Dict, List


def to_csv(source: List[Dict[str, str]],
           filename: str = 'output.csv') -> None:

    with open(filename, 'w', newline='') as csvfile:
        fieldnames = source[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(source)


def to_json(source: List[Dict[str, str]],
            filename: str = 'output.json') -> None:

    with open(filename, 'w') as f:
        json.dump(source, f, indent=4)
