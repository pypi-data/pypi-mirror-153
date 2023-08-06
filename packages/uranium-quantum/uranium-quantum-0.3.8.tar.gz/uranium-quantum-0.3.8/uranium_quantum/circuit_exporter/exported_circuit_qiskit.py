import numpy as np
from qiskit import QuantumRegister
from qiskit.circuit import ClassicalRegister
from qiskit import QuantumCircuit

from qiskit.circuit.library.standard_gates import XGate, YGate, ZGate, HGate
from qiskit.circuit.library import RXGate, RYGate, RZGate
from qiskit.circuit.library import RXXGate, RYYGate, RZZGate
from qiskit.circuit.library import RZXGate
from qiskit.circuit.library import SXGate, SXdgGate
from qiskit.circuit.library import SGate, SdgGate, TGate, TdgGate
from qiskit.circuit.library import UGate, U1Gate
from qiskit.circuit.library import SwapGate, iSwapGate
from qiskit.circuit.library import QFT
from uranium_quantum.circuit_exporter.qiskit_custom_gates import *


cr_main = ClassicalRegister(5)
qr_main = QuantumRegister(6)
qc_main = QuantumCircuit(qr_main, cr_main)


qc_main.x(qr_main[5])

qc_main.h(qr_main[0])

qc_main.h(qr_main[1])

qc_main.h(qr_main[2])

qc_main.h(qr_main[3])

qc_main.h(qr_main[4])

qc_main.h(qr_main[5])


qc_main.append(XGate().control(num_ctrl_qubits=5, ctrl_state='11101'), [qr_main[0], qr_main[1], qr_main[2], qr_main[3], qr_main[4], qr_main[5]])

qc_main.h(qr_main[0])

qc_main.h(qr_main[1])

qc_main.h(qr_main[2])

qc_main.h(qr_main[3])

qc_main.h(qr_main[4])

qc_main.x(qr_main[0])

qc_main.x(qr_main[1])

qc_main.x(qr_main[2])

qc_main.x(qr_main[3])

qc_main.x(qr_main[4])

qc_main.append(ZGate().control(num_ctrl_qubits=4, ctrl_state='1111'), [qr_main[0], qr_main[1], qr_main[2], qr_main[3], qr_main[4]])

qc_main.x(qr_main[0])

qc_main.x(qr_main[1])

qc_main.x(qr_main[2])

qc_main.x(qr_main[3])

qc_main.x(qr_main[4])

qc_main.h(qr_main[0])

qc_main.h(qr_main[1])

qc_main.h(qr_main[2])

qc_main.h(qr_main[3])

qc_main.h(qr_main[4])


qc_main.append(XGate().control(num_ctrl_qubits=5, ctrl_state='11101'), [qr_main[0], qr_main[1], qr_main[2], qr_main[3], qr_main[4], qr_main[5]])

qc_main.h(qr_main[0])

qc_main.h(qr_main[1])

qc_main.h(qr_main[2])

qc_main.h(qr_main[3])

qc_main.h(qr_main[4])

qc_main.x(qr_main[0])

qc_main.x(qr_main[1])

qc_main.x(qr_main[2])

qc_main.x(qr_main[3])

qc_main.x(qr_main[4])

qc_main.append(ZGate().control(num_ctrl_qubits=4, ctrl_state='1111'), [qr_main[0], qr_main[1], qr_main[2], qr_main[3], qr_main[4]])

qc_main.x(qr_main[0])

qc_main.x(qr_main[1])

qc_main.x(qr_main[2])

qc_main.x(qr_main[3])

qc_main.x(qr_main[4])

qc_main.h(qr_main[0])

qc_main.h(qr_main[1])

qc_main.h(qr_main[2])

qc_main.h(qr_main[3])

qc_main.h(qr_main[4])


qc_main.append(XGate().control(num_ctrl_qubits=5, ctrl_state='11101'), [qr_main[0], qr_main[1], qr_main[2], qr_main[3], qr_main[4], qr_main[5]])

qc_main.h(qr_main[0])

qc_main.h(qr_main[1])

qc_main.h(qr_main[2])

qc_main.h(qr_main[3])

qc_main.h(qr_main[4])

qc_main.x(qr_main[0])

qc_main.x(qr_main[1])

qc_main.x(qr_main[2])

qc_main.x(qr_main[3])

qc_main.x(qr_main[4])

qc_main.append(ZGate().control(num_ctrl_qubits=4, ctrl_state='1111'), [qr_main[0], qr_main[1], qr_main[2], qr_main[3], qr_main[4]])

qc_main.x(qr_main[0])

qc_main.x(qr_main[1])

qc_main.x(qr_main[2])

qc_main.x(qr_main[3])

qc_main.x(qr_main[4])

qc_main.h(qr_main[0])

qc_main.h(qr_main[1])

qc_main.h(qr_main[2])

qc_main.h(qr_main[3])

qc_main.h(qr_main[4])


qc_main.append(XGate().control(num_ctrl_qubits=5, ctrl_state='11101'), [qr_main[0], qr_main[1], qr_main[2], qr_main[3], qr_main[4], qr_main[5]])

qc_main.h(qr_main[0])

qc_main.h(qr_main[1])

qc_main.h(qr_main[2])

qc_main.h(qr_main[3])

qc_main.h(qr_main[4])

qc_main.x(qr_main[0])

qc_main.x(qr_main[1])

qc_main.x(qr_main[2])

qc_main.x(qr_main[3])

qc_main.x(qr_main[4])

qc_main.append(ZGate().control(num_ctrl_qubits=4, ctrl_state='1111'), [qr_main[0], qr_main[1], qr_main[2], qr_main[3], qr_main[4]])

qc_main.x(qr_main[0])

qc_main.x(qr_main[1])

qc_main.x(qr_main[2])

qc_main.x(qr_main[3])

qc_main.x(qr_main[4])

qc_main.h(qr_main[0])

qc_main.h(qr_main[1])

qc_main.h(qr_main[2])

qc_main.h(qr_main[3])

qc_main.h(qr_main[4])


qc_main.measure(0, 0)

qc_main.measure(1, 1)

qc_main.measure(2, 2)

qc_main.measure(3, 3)

qc_main.measure(4, 4)

