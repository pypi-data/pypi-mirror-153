# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 17:15:38 2022

@author: Yates
"""
try:
    import win32com.client
except ModuleNotFoundError:
    print("Cheap fix for readthedocs")
    pass

def start():
    """
    Loads a local CST session.
    
    Since this is a Window-specific API, this functions creates an instance of
    a stand-alone client.
    
    TODO:
        In the far, far future, the need to open a Circuits & Systems or PCB
        instance may be required. I should look into that at some point. 
    """
    
    cst = win32com.client.dynamic.Dispatch("CSTStudio.Application")
    new_mws = cst.NewMWS()
    mws = cst.Active3D()
    
    return mws


def close():
    
    cst = win32com.client.dynamic.Dispatch("CSTStudio.Application")
    print("Exiting...")
    cst.quit()
