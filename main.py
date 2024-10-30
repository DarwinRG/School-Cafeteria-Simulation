# Author: Darwin Guillermo

# This script simulates the operations of a school cafeteria using the SimPy library.
# It models the behavior of students arriving at the cafeteria, selecting stores, ordering food,
# paying for food, and finding seating to eat. The simulation tracks waiting times and generates
# an analysis report at the end.
#
# The main components include:
# - Student: Represents a student in the simulation.
# - Cafeteria: Represents the cafeteria with multiple stores and seating capacity.
# - select_store: Function to select a store based on a strategy.
# - student_process: Process for handling a student's actions in the cafeteria.
# - generate_arrivals: Generates student arrivals throughout the simulation.
# - run_simulation: Initializes and runs the simulation, and generates the analysis report.
#
# The simulation parameters are configured in the config module, and the analysis is handled
# by the analysis module.
#

import simpy
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from config import *
from analysis import create_detailed_analysis

class Student:
    def __init__(self, env, id, cafeteria):
        self.env = env
        self.id = id
        self.cafeteria = cafeteria

class Cafeteria:
    def __init__(self, env):
        self.env = env
        self.stores = []
        self.seating = simpy.Resource(env, SEATING_CAPACITY)
        
        # Create stores
        for i in range(STORES):
            servers = simpy.Resource(env, SERVERS_PER_STORE)
            cashiers = simpy.Resource(env, CASHIERS_PER_STORE)
            self.stores.append({
                'servers': servers,
                'cashiers': cashiers,
                'queue': 0
            })

def select_store(cafeteria):
    if STORE_SELECTION_STRATEGY == "random":
        return random.randint(0, STORES - 1)
    elif STORE_SELECTION_STRATEGY == "shortest_queue":
        return min(range(len(cafeteria.stores)), 
                  key=lambda i: cafeteria.stores[i]['queue'])
    return 0

def student_process(env, student, cafeteria, waiting_times):
    arrival_time = env.now
    
    # Select store
    store_index = select_store(cafeteria)
    store = cafeteria.stores[store_index]
    store['queue'] += 1
    
    # Order food
    with store['servers'].request() as request:
        yield request
        yield env.timeout(random.uniform(MIN_ORDER_TIME, MAX_ORDER_TIME))
    
    # Pay for food
    with store['cashiers'].request() as request:
        yield request
        yield env.timeout(random.uniform(MIN_PAYMENT_TIME, MAX_PAYMENT_TIME))
    
    store['queue'] -= 1
    
    # Find a seat and eat
    with cafeteria.seating.request() as request:
        yield request
        yield env.timeout(random.uniform(MIN_EATING_TIME, MAX_EATING_TIME))
    
    # Record waiting time
    waiting_time = env.now - arrival_time
    waiting_times.append(waiting_time)

def generate_arrivals(env, cafeteria, waiting_times):
    # Generate random number of students
    num_students = random.randint(MIN_STUDENTS, MAX_STUDENTS)
    
    # Create students throughout the day
    for i in range(num_students):
        student = Student(env, i, cafeteria)
        env.process(student_process(env, student, cafeteria, waiting_times))
        
        # Random arrival time
        yield env.timeout(random.expovariate(1.0))

def run_simulation():
    # Initialize simulation
    env = simpy.Environment()
    cafeteria = Cafeteria(env)
    waiting_times = []
    
    # Start student generation process
    env.process(generate_arrivals(env, cafeteria, waiting_times))
    
    # Run simulation
    simulation_duration = SIMULATION_END_TIME - SIMULATION_START_TIME
    env.run(until=simulation_duration)
    
    # Create analysis
    analysis_file = create_detailed_analysis(waiting_times, "cafeteria_simulation")
    print(f"\nAnalysis saved to: {analysis_file}")
    
    return waiting_times

if __name__ == "__main__":
    waiting_times = run_simulation()