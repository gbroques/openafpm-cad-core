#!/usr/bin/env python3
"""
Macro to test load_all function with progress callback.
Run this from FreeCAD's macro menu or console.
"""

import time
from openafpm_cad_core.get_default_parameters import get_default_parameters
from openafpm_cad_core.load import load_all

def progress_callback(stage_name, percent):
    """Progress callback that prints to FreeCAD console"""
    print(f"[{percent:3d}%] {stage_name}")

def main():
    print("Loading CAD model with progress tracking...")
    start_time = time.time()
    
    # Use T Shape parameters
    params = get_default_parameters("T Shape")
    
    # Load all documents with progress
    documents, spreadsheet = load_all(
        params['magnafpm'],
        params['furling'],
        params['user'],
        progress_callback=progress_callback
    )
    
    end_time = time.time()
    
    print(f"\nCompleted in {end_time - start_time:.1f} seconds")
    print(f"Loaded {len(documents)} documents:")
    for doc in documents:
        print(f"  - {doc.Name}")
    print(f"Spreadsheet: {spreadsheet.Name}")

if __name__ == "__main__":
    main()
