# OPC UA Client Data Logger

Overview
This project implements an OPC UA Client that connects to a simulated OPC UA server, reads 10 dummy tags every minute, and logs them into hourly CSV files.

- Each log file = 1 hour of data
- Columns:
  - Timestamp (ISO format, local)
  - Timestamp (Epoch UTC)
  - Tag1 … Tag10

---

Setup

1. Clone the project
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate      # Windows
