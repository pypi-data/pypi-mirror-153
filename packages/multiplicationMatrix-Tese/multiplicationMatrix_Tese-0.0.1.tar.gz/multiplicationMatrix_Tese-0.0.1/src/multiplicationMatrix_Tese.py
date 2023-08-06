from __future__ import print_function
import sys
import numpy as np
import scipy.io
from scipy.sparse import csr_matrix
import os, psutil
import openpyxl
import datetime
import cupyx as cpx
import cupy as cp
import random

def multiply_Matrix_GPU(mat_sparse_dose, arrayVetores, NV):

    #resultadosExcel = openpyxl.load_workbook("temposVariosVetores.xlsx")
    #SparseGPU_Page = resultadosExcel['Sparse_GPU']

    global_start_time = datetime.datetime.now()

    mat_dose_gpu = cpx.scipy.sparse.csc_matrix(mat_sparse_dose)

    #for matrix sparse calculation on the gpu
    for i in range(len(arrayVetores)):
        vector_host = np.float64(arrayVetores[i])
        vector_gpu = cp.asarray(vector_host)    
        resultado = mat_dose_gpu.dot(vector_gpu)

    global_end_time = datetime.datetime.now()
    global_time_diff = (global_end_time - global_start_time)
    global_execution_time = global_time_diff.total_seconds()
    print("{} VETORES NO GPU".format(NV))
    print("Global execution time {}s".format(global_execution_time))

    #SparseGPU_Page.append([NV, global_execution_time])
    #resultadosExcel.save("temposVariosVetores.xlsx")

def multiply_Matrix_CPU(mat_sparse_dose, arrayVetores, NV):

    #resultadosExcel = openpyxl.load_workbook("temposVariosVetores.xlsx")
    #SparseCPU_Page = resultadosExcel['Sparse_CPU']

    global_start_time = datetime.datetime.now()

    #for matrix sparse calculation on the cpu
    for l in range(len(arrayVetores)):
        globals()['resultado%s' % l] = mat_sparse_dose.dot(csr_matrix(arrayVetores[l]))

    global_end_time = datetime.datetime.now()
    global_time_diff = (global_end_time - global_start_time)
    global_execution_time = global_time_diff.total_seconds()
    print("{} VETORES NO CPU".format(NV))
    print("Global execution time {}s".format(global_execution_time))

    #SparseCPU_Page.append([NV, global_execution_time])
    #resultadosExcel.save("temposVariosVetores.xlsx")

def read_mat(path):
    file = scipy.io.loadmat(path)
    return file