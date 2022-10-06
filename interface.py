'''
    This module contains the functions that connects between the user to the backend functions (which are in he `building_blocks` module).
'''

from qiskit import transpile
from qiskit.visualization import plot_histogram
from qiskit.tools import job_monitor

import building_blocks

def multiplier(number_1, number_2, backend, shots = 1):
    '''
        Functionality:
            This function assembles the necessary parts to quantum compute `number_1 * number_2`.
            Progression updates are displayed to the user along th process.
        Parameters:
            number_1 (int) - The first integer to multiply.
            number_2 (int) - The second integer to multiply.
            backend (IBMQSimulator or IBMQBackend or local simulator's object) - The backend to run the circuit upon.
            shots (int) - Amount of shots desired (default = 1).
        Returns: {'product': product, 'qc': qc, 'tpqc': tpqc, 'counts': counts}
            product (int) - The product of number_1 * number_2.
            qc (QuantumCircuit object) - The quantum circuit that computes number_1 * number_2.
            tpqc (QuantumCircuit object) - The transpiled (with respect to `backend`) quantum circuit that computes number_1 * number_2.
            counts - (Counts dict object) - The results of running the circuit `shots` times.
    '''
    
    # Creating the circuit
    print('\nThe system synthesizes the appropriate quantum circuit..')
    qc = building_blocks.QuantumMultiply(x = number_1, y = number_2)
    print(f'Synthesis done.')
    
    # Transpiling the circuit
    print('\nTranspiling the circuit..')
    tpqc = transpile(qc, backend)
    print(f'Transpilation done.')
    
    # Executing the circuit on `backend`
    print('\nSending the job to the backend..')
    job = backend.run(tpqc, shots = shots)
    job_monitor(job) # Monitoring the job's progression and displaying it to the user
    results = job.result()
    print(f'Execution time: {results.time_taken: .3} seconds')
    counts = results.get_counts()
    common_result = max(counts, key = counts.get) # Taking the most common result (noisy backend = multiple results)
    product = int(common_result, 2) # Translating the result from binary to decimal
        
    return {'product': product, 'qc': qc, 'tpqc': tpqc, 'counts': counts}

def RunProgram(number_1, number_2, backend, shots = 1):
    '''
        Functionality:
            This function processes and anaylzes the product of `multiplier(number_1, number_2,) - Then it outputs the products to the user.
        Parameters:
            number_1 (int) - The first integer to multiply.
            number_2 (int) - The second integer to multiply.
            backend (IBMQSimulator or IBMQBackend or a local simulator's object) - The backend to run the circuit upon.
            shots (int) - Amount of shots desired (default = 1).
        Returns:
            None
    '''
    
    # Printing the chosen backend
    print(f'The chosen backend is {backend}')

    # `number_1 * number_2` computation
    m = multiplier(number_1 = number_1, number_2 = number_2, backend = backend, shots = shots)

    # Output
    print(f'\nnumber_1 * number_2 = {number_1} * {number_2} = {m["product"]}')
    print(f'\nThe transpiled circuit depth is: {m["tpqc"].depth()}')
    print(f'\nThe transpiled circuit\'s gate count is: {m["tpqc"].count_ops()}')
    print(f'\nThe results of running the circuit {shots} times:')
    display(plot_histogram(m['counts'], figsize = (5,3)))

    # Displaying the high-level circuit
    print("\nThe high-level circuit:")
    display(m['qc'].draw(output = 'mpl', style = {'backgroundcolor': '#EEEEEE'}, fold = -1))