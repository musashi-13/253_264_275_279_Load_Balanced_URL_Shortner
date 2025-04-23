#!/bin/bash

# Make sure logs directory exists
mkdir -p logs

# Set Redis host
export REDIS_HOST=localhost

# Start first instance on port 5000
echo "Starting Flask instance 1 on port 5000..."
python3 app.py --port=5000 > logs/flask-5000.log 2>&1 &
echo "PID: $!"

# Start second instance on port 5001
echo "Starting Flask instance 2 on port 5001..."
python3 app.py --port=5001 > logs/flask-5001.log 2>&1 &
echo "PID: $!"

# Start third instance on port 5002
echo "Starting Flask instance 3 on port 5002..."
python3 app.py --port=5002 > logs/flask-5002.log 2>&1 &
echo "PID: $!"

echo "All Flask instances are running in the background."
echo "You can access them at:"
echo "  http://localhost:5000"
echo "  http://localhost:5001"
echo "  http://localhost:5002"
echo "To stop them, use 'pkill -f \"python3 app.py\"'" 