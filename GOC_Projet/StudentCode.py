# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 11:08:40 2023

@author: Jérôme
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.transpiler import Layout
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.providers.fake_provider import FakeSingaporeV2,FakeWashingtonV2,FakeCairoV2

##-------------------------------------------------------
##     Definition de la fonction fitness à minimiser
##-------------------------------------------------------
def fitness(layout):
    init_layout={qr[i]:layout[i] for i in range(len(layout))}
    init_layout=Layout(init_layout)

    pm = generate_preset_pass_manager(3,backend,initial_layout=init_layout)
    pm.layout.remove(1)
    pm.layout.remove(1)

    QC=pm.run(qc)
    return QC.depth()

##-------------------------------------------------------
##     Selection de l'instance du probleme
##-------------------------------------------------------
def instance_characteristic(backend_name,circuit_type,num_qubit):
    if backend_name == "Singapore":
        backend = FakeSingaporeV2()
    elif backend_name == "Cairo":
        backend = FakeCairoV2()
    else :
        backend = FakeWashingtonV2()
        
    l=f"{circuit_type}_indep_qiskit_{num_qubit}"
    qasmfile=f".\{l.rstrip()}.qasm"
    qc=QuantumCircuit().from_qasm_file(qasmfile)
    qr=qc.qregs[0]
    
    return backend,qc,qr

backend_list = ["Singapore","Cairo","Washington"]
circuit_list = ["ghz","dj","qaoa"]
def instance_selection(instance_num):
    if instance_num==0:
        return backend_list[0],circuit_list[0],5
    elif instance_num==1:
        return backend_list[0],circuit_list[2],8
    else:
        print("Choix d'une instance inexistance, instance par défaut revoyé")
        return backend_list[0],circuit_list[0],5


##-------------------------------------------------------
##     Pour choisir une instance: 
##     Modifier instance_num ET RIEN D'AUTRE    
##-------------------------------------------------------
instance_num=1

backend_name,circuit_type,num_qubit=instance_selection(instance_num)
backend,qc,qr=instance_characteristic(backend_name,circuit_type,num_qubit)

n=num_qubit
m=backend.num_qubits

##-------------------------------------------------------
##     A vous de jouer !  
##-------------------------------------------------------
###### Un dummy test, juste pour voir que ça marche.
fitmin=10E10
for k in range(10):
    layout=np.random.choice(m,n,False)
    fit=fitness(layout)
    if fit<fitmin:
        fitmin=fit
        layout_best=layout    
    print(layout,fit)
print(f"Best layout found is {layout_best}, with a fitness of {fitmin}")

###### A faire : un algo d'optimisation qui minimise la fonction fitness,
###### fonction qui accepte en entrée :
###### une liste de n parmi m (n<=m) entiers deux à deux distincts







