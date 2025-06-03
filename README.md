# Ray Distributed Matrix Calculation System

This project demonstrates a distributed matrix calculation system using Ray framework, where matrix operations are distributed across multiple services.

## System Architecture

- **client_a.py**: Main client program that:
  - Initializes Ray cluster
  - Deploys B and C services
  - Generates initial matrix
  - Coordinates the distributed calculation
  - Collects final result

- **serve_b.py**: B Service that:
  - Performs matrix multiplication with its fixed matrix
  - Forwards result to C Service

- **serve_c.py**: C Service that:
  - Performs final matrix multiplication
  - Returns the result to client

## Requirements

- Python 3.7+
- Ray 2.0+
- NumPy

## Installation

1. Install Python dependencies:
```bash
pip install ray numpy
```

2. Clone this repository (if applicable)

## Running the System

1. Start the system by running:
```bash
python3 client_a.py
```

2. Expected output flow:
- Ray cluster initialization
- Services deployment
- Matrix calculation process
- Final result display

## Expected Output

You should see logs showing:
1. Ray cluster initialization
2. Services deployment
3. Matrix operations at each step
4. Final calculated matrix result

## Notes

- The system uses Ray's default ports (10001 for client, 8265 for dashboard)
- Dashboard is available at: http://127.0.0.1:8265
- For production use, modify the Ray initialization to connect to a proper cluster instead of local mode
