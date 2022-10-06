'''
    This module contains all the necessary functions to perform QFT, Fourier addition and Fourier multiplication.
'''

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

def FourierAdder(reg1_qubits, reg2_qubits):
    '''
        Functionality:
            This function creates a QuantumCircuit object that performs {|reg1> + |reg2> (mod |reg2>)} in Fourier basis.
        Parameters:
            reg1_qubits (int) - Number of qubits in `reg1`.
            reg2_qubits (int) - Number of qubits in `reg2`.
        Returns:
            qc (QuantumCircuit object) - A quantum circuit with the gates needed to write the result into `reg2`.
    '''
    
    # Initializing
    reg1 = QuantumRegister(reg1_qubits, 'reg1')
    reg2 = QuantumRegister(reg2_qubits, 'reg2')
    qc = QuantumCircuit(reg1, reg2)
    qc.name = 'Fourier addition'
    
    # Applying the controlled phase shifts to create addition
    for control_q in range(reg1_qubits):
        for target_q in range(reg2_qubits):
            k = reg2_qubits - target_q
            phase = (2 * np.pi * (2 ** control_q)) / (2 ** k)
            if phase == 2 * np.pi: # Phase shifts of 2pi multiples are indistinguishable = Breaking from the inner loop
                break
            qc.cp(theta = phase, control_qubit = reg1[control_q], target_qubit = reg2[target_q])
            
    return qc

def qft(num_qubits, inverse = False):
    '''
        Functionality:
            This function creates a quantum circuit for QFT of `num_qubits`.
        Parameters:
            num_qubits (int) - The amount of qubits the QFT will be applied to.
            inverse (bool):
                False (default) - A QFT is generated.
                True - A QFT^{dagger} is generated.
        Returns:
            QFT_gate (Gate object) - The QFT as a Gate object to be appended to a quantum circuit.
        Note:
            I am aware of the fact that qiskit has a built-in QFT function (qiskit.circuit.library.QFT).
            I preferred to create a new one for the sake of completeness.
    '''
    
    # Initalizing circuit
    qc = QuantumCircuit(num_qubits)
    
    # Handling each qubit from the MSB to the LSB (little-endian)
    for i, target_q in reversed(list(enumerate(qc.qubits))):
        qc.h(target_q)
        k = i + 1  
        for j, control_q in enumerate(qc.qubits[0:i]):    
            phase = ((2 ** j) * (2 * np.pi)) / (2 ** k) 
            qc.cp(theta = phase, control_qubit  = control_q, target_qubit = target_q)

    # Performing final SWAPS
    for i in range(int(num_qubits / 2)):
        qc.swap(i, num_qubits - i - 1)
    
    # Transforming the QuantumCircuit object to a Gate object and returning it
    if inverse:
        qc = qc.inverse()
        QFT_gate = qc.to_gate(label = 'QFT_Dagger')
    else:
        QFT_gate = qc.to_gate(label = 'QFT')
        
    return QFT_gate

def EncodeInteger(i):
    '''
        Functionality:
            This function encodes a positive integer into a quantum state of a quantum register.
        Parameters:
            i (int) - The integer to encode.
        Returns: {'encoded_reg': qc, 'binary': i_bin, 'length': i_len}
            encoded_reg (QuantumCircuit object) - A quantum circuit with the value of `i` encoded as its quantum state.
            binary (str) - The bitstring representation of `i`.
            length (int) - The length of `i_bin`.
    '''
    
    # Translating `i` to binary and measuring its bitstring's length
    i_bin = bin(i)[2:]
    i_len = len(i_bin)
    
    # Initializing circuit
    qc = QuantumCircuit(i_len)
    qc.name = f'Integer encoded: {i}'
    
    # Encoding `i_bin` into the circuit (little-endian)
    for index, d in enumerate(reversed(i_bin)):
        if d == '1':
            qc.x(index)
    
    return {'encoded_reg': qc, 'binary': i_bin, 'length': i_len}

def QuantumMultiply(x, y):
    '''
        Functionality:
            This function builds a quantum circuit that computes x * y (using Fourier addition).
        Parameters:
            x (int) - First operand.
            y (int) - Second operand.
        Returns:
            qc (QuantumCircuit object) - The quantum circuit that computes x * y (not transpiled).
    '''
    
    # Encoding `x` and `y` into quantum registers and setting registers' lengths
    if x > y: # Making sure that x is the smallest integer, swapping if needed
        temp = y
        y = x
        x = temp
    x_encoded = EncodeInteger(x)
    len_x = x_encoded['length']
    y_encoded = EncodeInteger(y)
    len_y = y_encoded['length']
    len_result = len_x + len_y # That covers the maximum value case where `x` and `y` are full-ones bitstrings
    
    # Initalizing the registers and circuit
    reg_x = QuantumRegister(len_x, 'reg_x')
    reg_y = QuantumRegister(len_y, 'reg_y')
    reg_result = QuantumRegister(len_result, 'reg_result')
    classical_result = ClassicalRegister(len_result, 'classical_result')
    qc = QuantumCircuit(reg_x, reg_y, reg_result, classical_result)
    
    # Setting the `x` and `y` values to their quantum registers
    qc.append(instruction = x_encoded['encoded_reg'], qargs = reg_x)
    qc.append(instruction = y_encoded['encoded_reg'], qargs = reg_y)
    
    # Transforming reg_result to Fourier basis (for the upcoming Fourier addtion)
    qc.h(reg_result)
    qc.barrier()
    
    # `x * y` = Adding the value of `y` to `reg_result` `x` times
    c_iteration = FourierAdder(reg1_qubits = len_y, reg2_qubits = len_result).control()
    for i in range(len_x):
        times = 2 ** i
        c_iteration.name = f'If x[{i}] == 1: \nAdding y to result {times} times'
        for iteration in range(times):
            qc.append(instruction = c_iteration, qargs = [reg_x[i]] + reg_y[:] + reg_result[:])
    qc.barrier()

    # Transforming reg_result back to the computational basis
    qc.append(instruction = qft(num_qubits = len_result, inverse = True), qargs = reg_result)
    qc.barrier()
    
    # Measuring
    qc.measure(reg_result, classical_result)

    return qc
