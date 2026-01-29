#!/bin/bash
trap 'kill 0' SIGINT

# Start Backend
echo "Starting Backend..."
source venv/bin/activate
cd backend
python main.py &
cd ..

# Start Frontend
echo "Starting Frontend..."
cd frontend
npm run dev -- --host &

wait
