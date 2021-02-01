from tkinter import *
import pickle

def open_file(file_name):
    with open(file_name, 'rb') as f:
        return pickle.load(f)


open_file('PRTF_final.pickle')
open_file('PRTS_final.pickle')
open_file('ADJ_full_final.pickle')
open_file('ADJ_short_final.pickle')
open_file('Adj_cmp_final.pickle')
open_file('Adj_sup_final.pickle')

