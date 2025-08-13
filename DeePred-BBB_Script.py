#!/usr/bin/env python3

""" 
BBB Permeability prediction using a Deep Neural Network 
as published in  https://doi.org/10.3389/fnins.2022.858126

It calculates descriptors using PaDEL, and uses them to
predict BBB permeability with a trained DNN model. 

Compounds' SMILES must be in .smi file in the same folder.
Training data (data.csv), model (DeePredmodel.h5), and PaDEL
folder must be in the same folder, too. 

Edited by Dr. Freddy Bernal 
"""

import os
import sys
import pandas as pd  
import numpy as np
import subprocess
from sklearn.preprocessing import StandardScaler
from keras.models import load_model


# Create function to get predictions using trained model
def bbb(input_bbb: pd.DataFrame) -> np.ndarray:
    """Function to predict BBB permeability for a set
    set of samples with PaDEL features.

    Args:
        input_bbb (pd.DataFrame): PaDEL Features for compounds

    Returns:
        np.ndarray: BBB class (1 permeable; 0 non-permeable)
    """
    # Load training data and scale it 
    bbb_data = pd.read_csv(os.path.join(path, "data.csv"), header=None)
    scaler = StandardScaler()  
    bbb_data = scaler.fit_transform(bbb_data)  
    # Transform user data to numpy to avoid conflict with names
    bbb_user_input = scaler.transform(input_bbb.to_numpy())
    # Load model
    loaded_model = load_model(os.path.join(path, "DeePredmodel.h5")) 
    print("Model loaded")
    # Get predictions for user input
    prediction = loaded_model.predict(bbb_user_input).round()
    prediction = prediction[:,0].astype (int)
    
    return prediction
    

# Create main function to run descriptor calculation and predictions 
def run_prediction(folder: str, smi_file: str) -> None:
    """Function to calculate descriptors (using PaDEL) and to generate
    predictions of BBB permeability for a set of compounds (SMILES).

    Args:
        folder (str): Folder to search for ".smi" file (multiple structures)
        smi_file (str): Name of the ".smi" file with input structures

    Returns:
        CSV file with resulting BBB class (1 permeable; 0 non-permeable)
    """
    # Count number of molecules in input
    with open(os.path.join(folder, smi_file)) as f:
        num_molecules_in = sum(1 for line in f if line.strip())
    
    padel_output_file = os.path.join(folder, "PaDEL_features.csv")

    # Check if PaDEL features need to be calculated
    run_padel = True
    if os.path.exists(padel_output_file):
        try:
            num_molecules_out = len(pd.read_csv(padel_output_file))
            if num_molecules_in == num_molecules_out:
                print("Found existing 'PaDEL_features.csv' with matching size. Skipping PaDEL calculation.")
                run_padel = False
        except Exception:
            # If file is corrupted or empty, it will fail, so we recalculate
            pass


    if run_padel:
        # Define command for PaDEL
        padel_cmd = [
            'java', '-jar', 
            os.path.join(path, 'PaDEL-Descriptor/PaDEL-Descriptor.jar'),
            '-descriptortypes', 
            os.path.join(path, 'PaDEL-Descriptor/descriptors.xml'), 
            '-dir', folder, '-file', padel_output_file, 
            '-2d', '-fingerprints', '-removesalt', '-detectaromaticity', 
            '-standardizenitro']
        # Calculate features
        print("Calculating PaDEL features...")
        subprocess.call(padel_cmd)
        print("Features calculated")

    # Create Dataframe for calculated features
    input_bbb =pd.read_csv(padel_output_file)
    # Store name of each sample
    names = input_bbb['Name'].copy()
    # Remove names
    input_bbb = input_bbb.drop(['Name'], axis=1)
    # Run predictions
    pred = bbb(input_bbb)
    # Create Dataframe with results
    res = pd.DataFrame(names)
    res['Predicted_class'] = pred
    # Save results to csv
    res.to_csv('DeePred-BBB_predictions.csv', index=False)

    return None
    

# Run script
if __name__ == "__main__":
    # Define current directory
    if len(sys.argv) == 2:
        path = sys.argv[1]
    else:
        path = os.getcwd()
    # Verify existence of file with SMILES
    smi_files = [fname for fname in os.listdir(path) if fname.endswith(".smi")]
    if smi_files:
        # Get predictions
        run_prediction(path, smi_files[0])        
    else:
        raise FileNotFoundError("Input File NOT found")