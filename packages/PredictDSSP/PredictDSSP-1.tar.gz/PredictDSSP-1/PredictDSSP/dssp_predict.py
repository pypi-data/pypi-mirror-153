import os 
from PredictDSSP import py_predictor_v2

def predict_dssp(sequence, raw_vals=False):

    # get path to network
    PATH = os.path.dirname(os.path.realpath(__file__))
    
    # selcet the chosen network, kept as separate line of code in 
    used_predictor = 'dssp_2022_01_07_CB_thresh_0p8_hs20_nl2.pt'
    
    # set location of chosen network
    predictor_path = f'{PATH}/networks/{used_predictor}'
    
    # set predictor value using py_predictor_V2
    my_predictor = py_predictor_v2.Predictor(predictor_path, 
                                            dtype="residues")    
    # get values of prediction
    value = my_predictor.predict(sequence)
    # make empty list to hold values
    final_vals = []
    if raw_vals == False:
        # append values to the list depending on the probabilities for each value
        for i in value:
            highest_val = max(i)
            if highest_val == i[0]:
                final_vals.append(0)
            elif highest_val == i[1]:
                final_vals.append(1)
            else:
                final_vals.append(2)
        # return the final values based on the probabilities returned from the network
        return final_vals
    else:
        return value
        

