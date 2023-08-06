import json
import os


def write_simulator_input(simulator_input: dict,
                          file_path: str = 'simulator_input.json') -> None:
    head, tail = os.path.split(file_path)
    if head:
        os.makedirs(head, exist_ok=True)
    if not tail.endswith('.json'):
        tail = f'{tail}.json'
    with open(os.path.join(head, tail), 'w') as f:
        f.write(json.dumps(simulator_input))


def read_simulator_input(file_path: str = 'simulator_input.json') -> dict:
    if not os.path.isfile(file_path) and not file_path.endswith('.json'):
        file_path = f'{file_path}.json'
    with open(file_path) as f:
        line = next(f)
    return json.loads(line)
