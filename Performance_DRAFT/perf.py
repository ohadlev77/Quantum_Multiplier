'''
    TODO COMPLETE
'''

import sys
sys.path.append('..')
import building_blocks

import time
from qiskit import transpile

class ExpPerf():
    '''
        TODO COMPLETE
    '''
    
    def __init__(self, qc, backend):
        self.qc = qc
        self.backend = backend
    
    def get_runtime(self):
        return self.runtime
    
    def transpile(self, optimization_level = 1):
        '''
            TODO COMPLETE
        '''
        
        start = time.perf_counter()
        tpqc = transpile(circuits = self.qc, backend = self.backend, optimization_level = optimization_level)
        end = time.perf_counter()
        tp_time = round(end - start, 2)
        
        self.tpqc = tpqc
        self.tp_time = tp_time
    
    def run(self, timeout = 40):
        '''
            TODO COMPLETE
        '''
        
        job = self.backend.run(self.tpqc)
        try:
            job.wait_for_final_state(timeout = timeout)
            results = job.result()
            runtime = round(results.time_taken, 2)
        except:
            results = None
            runtime = -1
        
        self.results = results
        self.runtime = runtime


max_values = [1, 3, 7, 15, 31, 63, 127, 255, 511, 1023, 2047, 8191, 16383 ,32767]
        
def create_circuits(max_int, backend, timeout = 40):
    '''
        TODO COMPLETE
    '''
    
    # COMPLETE
    num_qubits = backend.configuration().n_qubits
    min_qubits_needed = qubits_cost(number_1 = 1, number_2 = max_int)
    
    #COMPLETE
    if min_qubits_needed > num_qubits:
        print(f'At least {min_qubits_needed} qubits are needed. {backend} has only {num_qubits} qubits available.')
        return False
    
    circuits = {}
    for i,x in enumerate(max_values):
        if qubits_cost(number_1 = x, number_2 = 1) > num_qubits:
            break
        circuits[f'{x}'] = {}
        for j in range(i, len(max_values)):
            y = max_values[j]
            if qubits_cost(number_1 = x, number_2 = y) > num_qubits:
                break
            qc = building_blocks.QuantumMultiply(x = x, y = y)
            perf_obj = ExpPerf(qc = qc, backend = backend)
            perf_obj.transpile()
            circuits[f'{x}'][f'{y}'] = perf_obj
            print(f'Inserted for {x} and {y}')
    
    return circuits        
        
def perf_assess(max_int, backend, timeout = 40):
    '''
        TODO COMPLETE
    '''
    
    # COMPLETE
    num_qubits = backend.configuration().n_qubits
    min_qubits_needed = qubits_cost(number_1 = 1, number_2 = max_int)
    
    #COMPLETE
    if min_qubits_needed > num_qubits:
        print(f'At least {min_qubits_needed} qubits are needed. {backend} has only {num_qubits} qubits available.')
        return False
    
    data = {}
    for x in range(max_int + 1):
        data[f'{x}'] = {}
        for y in range(x, max_int + 1):
            qc = building_blocks.QuantumMultiply(x = x, y = y)
            perf_obj = ExpPerf(qc = qc, backend = backend)
            perf_obj.transpile()
            perf_obj.run()
            data[f'{x}'][f'{y}'] = perf_obj.get_runtime()
            print(f'Inserted for {x} and {y}')
    
    return data
            

def qubits_cost(number_1, number_2):
    '''
        TODO COMPLETE
    '''
    
    n1_len = len(bin(number_1)[2:])
    n2_len = len(bin(number_2)[2:])
    num_qubits = (n1_len + n2_len) * 2 
        
    return num_qubits