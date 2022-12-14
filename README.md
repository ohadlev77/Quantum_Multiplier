# Quantum Multiplier

This small-scale Qiskit-based program builds and runs quantum circuits for integers multiplication.
The implementation is based on Fourier basis addition.

# Instructions

1. Copy the repository to your local machine (`git clone https://github.com/ohadlev77/Quantum_Multiplier.git`).
2. Set the downloaded directory as the chosen directory (`cd Quantum_Multiplier`).
3. Open Jupyter Notebook (`notebook` or `py -m notebook`) - The chosen directory will be opened on the Jupyter Notebook platform.
2. Run `main.ipynb` - The rest of the instructions appears within that file.

# Functionality

The program synthesizes a specific quantum circuit appropriate for the integers (`number_1`, `number_2`) multiplication chosen, and runs it on a simulator (the default backend is `ibmq_qasm_simulator`, consisted of 32 qubits).
it is possible to enter integers with different bitstring lengths.
The size of the integers is limited by the specification of the backend that we run the circuit upon - The circuit is consisting of $2(n + m)$ qubits, while $n$ and $m$ are the lengths of the integers' bitstrings. See the *Performance* section for more details.
NOTE: Due to the nature of the Fourier multiplication algorithm it's practically impossible to achieve valuable results from NISQ hardware.

# Performance

2 factors have been taken into account - The transpilation time and the running time of any circuit on `ibmq_qasm_simulator`.
Of course that the transpilation time varies between different computers since the transpilation process takes place locally, but I think this data is still useful and might provide some global reference. 
90 seconds was fixed as the timeout bound for running 1 circuit, 1 shot (since the simulator is noiseless 1 shot is enough) - Failed attempts that reached the timeout bound are marked with `Nan` running time.
Since what affects the circuit depth and the gates count (and therefore the overall performance and the execution time) is the number of qubits that are needed to represent the integers - In the following data samplings we chose the all-ones bitstrings integers to be shown (1, 3, 7, 15, and so on..).
In addition, due to the structure of the algorithm, it's much less complex to set the smaller integer as `number_1` and the larger integer as `number_2` compared to the opposite case. Even if the data is set the other way around, the program fix that (classically - that's a little 'cheat' but if `number_1 <= number_2` in the first place it can be ignored).

### The execution and transpilation time data:
<div align = "center">
    <img src = "perf/combined_tables.png" />
</div>