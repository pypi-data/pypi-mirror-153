"""
Backend for graphing predicted disorder values in dssp.py.
"""


# code for graphing IDRs.
# Import stuff
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import metapredict as meta
from PredictDSSP.dssp_predict import predict_dssp
import alphaPredict as alpha

def graph(sequence,
          title='Predicted DSSP Scores',
          color_0='red',
          color_1='blue',
          color_2='orange',
          exclude_disorder=False,
          disorder_color = 'black',
          no_disorder_bars = False,          
          dis_threshhold = 0.3,
          DPI=150,
          output_file=None):

    """
    Function for graphing predicted dssp scores.

    Parameters
    -----------

    sequence : str 
        Input amino acid sequence (as string) to be predicted.

    title : str
        Sets the title of the generated figure. Default = "Predicted protein disorder"

    color_0 : string
        the color for 0 values, which correspond to helicity

    color_1 : string
        the color for 0 values, which correspond to beta strand/sheet

    color_2 : string
        the color for 0 values, which correspond to coil

    disorder_color : string
        the color for disordered regions

    no_disorder_bars : Bool
        If set to False, no disorder bars will be shown.

    exclude_disorder : Bool
        Whether to exlude disordered regions from predictions    

    dis_threshhold : float
        The theshhold disorder score for metapredict scores to consider something disordered

    DPI : int
        Dots-per-inch. Defines the resolution of the generated .png figure. Note that
        if an alternative filetype is pathed the matplotlib backened will automatically
        generate a file of the relevant type (e.g. .pdf, .jpg, or .eps).

    output_file : str
        If provided, the output_file variable defines the location and type of the file
        to be saved. This should be a file location and filename with a valid matplotlib
        extension (such as .png, .jpg, .pdf) and, if provided, this value is passed directly
        to the ``matplotlib.pyplot.savefig()`` function as the ``fname`` parameter. 
        Default = None.


    Returns
    -----------
    None 
        No return type, but will either generate an on-screen plot OR will save a file to disk,
        depending on if output_file is provided (or not).

    """


    # set this such that PDF-generated figures become editable
    matplotlib.rcParams['pdf.fonttype'] = 42
    matplotlib.rcParams['ps.fonttype'] = 42

    #set n_res to lenght of seq
    n_res = len(sequence)
        
    fig = plt.figure(num=title, figsize=[8, 3], dpi=DPI, edgecolor='black')
    axes = fig.add_axes([0.15, 0.15, 0.75, 0.75])        
    
    # set x label
    axes.set_xlabel("Residue")

    # set the title
    axes.set_title(title)
    
    # modify y_label if needed
    axes.set_ylabel("DSSP scores")

    # make x values for each residue with predicted score
    xValues = np.arange(1, n_res+1)

    # get the dssp scores
    dssp_scores = predict_dssp(sequence)

    # break up the scores into lists for each position number
    zero_list = []
    one_list = []
    two_list = []
    disorder_list = []

    if exclude_disorder == True:
        pLDDT_scores = alpha.predict(sequence)
        disorder_scores = meta.predict_disorder(sequence)

    for sco in range(0, len(dssp_scores)):
        cur_score = dssp_scores[sco]
        if exclude_disorder == False:
            if cur_score == 0:
                zero_list.append(1)
                one_list.append(0)
                two_list.append(0)
            elif cur_score == 1:
                zero_list.append(0)
                one_list.append(1)
                two_list.append(0)
            else:
                zero_list.append(0)
                one_list.append(0)
                two_list.append(1)
        else:
            cur_disorder_score = disorder_scores[sco]
            cur_alpha_score = pLDDT_scores[sco]
            if cur_disorder_score >= dis_threshhold and cur_alpha_score <=65:
                    zero_list.append(0)
                    one_list.append(0)
                    two_list.append(0)
                    disorder_list.append(1)

            else:
                disorder_list.append(0)
                if cur_score == 0:
                    zero_list.append(1)
                    one_list.append(0)
                    two_list.append(0)
                elif cur_score == 1:
                    zero_list.append(0)
                    one_list.append(1)
                    two_list.append(0)
                else:
                    zero_list.append(0)
                    one_list.append(0)
                    two_list.append(1)

    axes.bar(xValues + 0.00, zero_list, color=color_0)
    axes.bar(xValues + 0.00, one_list, color=color_1)
    axes.bar(xValues + 0.00, two_list, color=color_2)

    if exclude_disorder == True:
        if no_disorder_bars == False:
            axes.bar(xValues + 0.00, disorder_list, color=disorder_color)

    plt.ylim(0, 2)

    axes.set_yticks([0, 1])

    if exclude_disorder == True:
        if no_disorder_bars == False:
            axes.legend(labels=['helix', 'beta strand / sheet', 'coil', 'disordered'], loc='upper right')
        else:
            axes.legend(labels=['helix', 'beta strand / sheet', 'coil',], loc='upper right')
    else:
        axes.legend(labels=['helix', 'beta strand / sheet', 'coil'], loc='upper right')

    if output_file is None:
        plt.show()
    else:
        plt.savefig(fname=output_file, dpi=DPI)
        plt.close()

