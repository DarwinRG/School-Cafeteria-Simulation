# Author: Darwin Guillermo

# This file contains configuration settings for the School Cafeteria Simulation.
# It includes parameters for simulation time, cafeteria setup, student behavior,
# service times, and store selection strategy.

# Simulation Time Configuration (in seconds)
SIMULATION_START_TIME = 41400  # 11:30 AM (11*3600 + 30*60)
SIMULATION_END_TIME = 46800    # 1:00 PM (13*3600)

# Cafeteria Configuration
STORES = 2
SERVERS_PER_STORE = 2
CASHIERS_PER_STORE = 1
MEAL_CHOICES_PER_STORE = 5
SEATING_CAPACITY = 100

# Student Configuration
MIN_STUDENTS = 200
MAX_STUDENTS = 300
SKIP_LINE_PROBABILITY = 0.1

# Service Time Configuration (in seconds)
MIN_ORDER_TIME = 30    # 30 seconds
MAX_ORDER_TIME = 60   # 1 minute
MIN_PAYMENT_TIME = 20  # 20 seconds
MAX_PAYMENT_TIME = 45  # 45 seconds
MIN_EATING_TIME = 900  # 15 minutes
MAX_EATING_TIME = 1800 # 30 minutes

# Store Selection Configuration
STORE_SELECTION_STRATEGY = "shortest_queue" 
# Options: "shortest_queue", "random"
# "shortest_queue": Student selects store with shortest queue (Realistic)
# "random": Student selects store randomly
