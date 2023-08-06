## 
## dssp.py
## 
## contains user facing functionlity
##



# NOTE - any new functions must be added to this list!
__all__ = ['predict_dssp', 'graph_dssp', 'predict_dssp_fasta', 'graph_dssp_fasta', 'predict_dssp_uniprot', 'graph_dssp_uniprot']


import os
import sys

#import protfasta to read .fasta files
import protfasta as _protfasta

# stuff for predictions
from PredictDSSP.dssp_predict import predict_dssp as _predict_dssp
from PredictDSSP import dssp_tools as _dssp_tools

# stuff for graphing
from PredictDSSP.dssp_graph import graph as _graph

# stuff for uniprot
from PredictDSSP.uniprot_predictions import fetch_sequence as _fetch_sequence
from PredictDSSP.dssp_exceptions import DsspError


def predict_dssp(sequence, raw_vals=False):
    '''
    Function to predict dssp scores

    Parameters
    ----------
    sequence : str
        The amino acid sequence as a sting

    raw_vals : bool
        Whether to return the categorization based
        on the dssp probabilities (default)
        If set to True, will return a list of lists where
        the first element in each list [0] is the probability
        that the amino acid has a helical propensity, the second
        element [1] is the propensity to form a beta strand
        / beta sheet, and the final element [2] is the
        propensity to form a coil.
    '''


    # make all uppercase
    sequence = sequence.upper()
    
    # return values
    return _predict_dssp(sequence, raw_vals=raw_vals)


def graph_dssp(sequence,
          title='Predicted DSSP Scores',
          exclude_disorder=False,
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

    # make sure disorder threshhold okay
    _dssp_tools.valid_range(dis_threshhold, 0.0, 1.0)

    # ensure sequence is upper case
    sequence = sequence.upper()

    _graph(sequence, title=title, no_disorder_bars = no_disorder_bars,
        exclude_disorder=exclude_disorder, dis_threshhold=dis_threshhold, 
        DPI=DPI, output_file=output_file)



def predict_dssp_fasta(filepath, output_file=None, invalid_sequence_action='convert'):
    """
    Function to read in a .fasta file from a specified filepath.
    Returns a dictionary of dssp values where the key is the 
    fasta header and the values are the predicted dssp values.
    
    Parameters
    -------------

    filepath : str 
        The path to where the .fasta file is located. The filepath should end in the file name. 
        For example (on MacOS):filepath="/Users/thisUser/Desktop/folder_of_seqs/interesting_proteins.fasta"

    output_file : str
        By default, a dictionary of predicted values is returned immediately. However, you can specify 
        an output filename and path and a .csv file will be saved. This should include any file extensions.
        Default = None.

    invalid_sequence_action : str
        Tells the function how to deal with sequences that lack standard amino acids. Default is 
        convert, which as the name implies converts via standard rules. See 
        https://protfasta.readthedocs.io/en/latest/read_fasta.html for more information.


    Returns
    --------

    dict or None
        If output_file is set to None (as default) then this fiction returns a dictionary of sequence ID to
        dssp score. If output_file is set to a filename then a .csv file will instead be written and 
        no return data will be provided.

    """    
    # Test to see if the data_file exists
    test_data_file = os.path.abspath(filepath)

    if not os.path.isfile(test_data_file):
        raise FileNotFoundError('Datafile does not exist.')

    protfasta_seqs = _protfasta.read_fasta(filepath, invalid_sequence_action = invalid_sequence_action, return_list = True)

    # dict for dssp seqs
    dssp_dict={}

    # for the sequences in the protffasta_seqs list:
    for seqs in protfasta_seqs:

        # set cur_header equal to the fasta header
        cur_header = seqs[0]

        # set cur_seq equal to the sequence associated with the fasta header
        cur_seq = seqs[1]

        # make all values for curSeq uppercase so they work with predictor
        cur_seq = cur_seq.upper()

        # set cur_dssp equal to the predicted dssp values for cur_seq
        cur_dssp = _predict_dssp(cur_seq)

        # add to dict
        dssp_dict[cur_header] = cur_dssp

    # if we did not request an output file 
    if output_file is None:
        return dssp_dict

    # else write to disk 
    else:
        _dssp_tools.write_csv(dssp_dict, output_file)    


def graph_dssp_fasta(filepath,
          exclude_disorder=False,
          no_disorder_bars = False,          
          dis_threshhold = 0.3,
          DPI=150,
          output_dir=None,
          output_filetype='png', 
          invalid_sequence_action='convert',
          indexed_filenames=False):
    """
    Function to make graphs of predicted disorder from the sequences
    in a specified .fasta file. By default will save the generated
    graphs to the location output_path specified in filepath.

    **WARNING**: It is unadvisable to not include an output directory if you are reading in a .fasta 
    file with many sequences! This is because each graph must be closed individually before the next 
    will appear. Therefore, you will spend a bunch of time closing each graph.

    **NB**: You cannot specify the output file name here! By default, the file name will
    be the first 14 characters of the FASTA header followed by the filetype as specified 
    by filetype. If you wish for the files to include a unique leading number (i.e. X_rest_of_name
    where X starts at 1 and increments) then set indexed_filenames to True. This can be useful if you
    have sequences where the 1st 14 characters may be identical, which would otherwise overwrite an 
    output file.

    Parameters
    -----------

    filepath : str 
        The path to where the .fasta file is located. The filepath should end in the file name. 
        For example (on MacOS):filepath="/Users/thisUser/Desktop/folder_of_seqs/interesting_proteins.fasta"

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

    output_dir : str
        If provided, the output_dir variable defines the directory where file should besaved
        to be saved. This should be a writeable filepath. Default is None. Output files are 
        saved with filename as first 14 chars of fasta header (minus bad characters) plus the
        appropriate file extension, as defined by filetype.

    output_filetype : str
        String that defines the output filetype to be used. Must be one of pdf, png, jpg.

    invalid_sequence_action : str
        Tells the function how to deal with sequences that lack standard amino acids. Default is 
        convert, which as the name implies converts via standard rules. See 
        https://protfasta.readthedocs.io/en/latest/read_fasta.html for more information.

    indexed_filenames : bool
        Bool which, if set to true, means filenames start with an unique integer.


    Returns
    ---------

    None
        No return object, but, the graph is saved to disk or displayed locally.


    """    

    # Test to see if the data_file exists
    if not os.path.isfile(filepath):
        raise FileNotFoundError('Datafile [%s] does not exist'%(filepath))

    # Test to see if output directory exists
    if output_dir is not None:
        if not os.path.isdir(output_dir):
            raise FileNotFoundError('Proposed output directory could not be found')

    # validate dis_threshhold
    _dssp_tools.valid_range(dis_threshhold, 0,1)    

    # use protfasta to read in fasta file
    sequences =  _protfasta.read_fasta(filepath, invalid_sequence_action = invalid_sequence_action)

    # now for each sequence...
    idx_counter = 0
    for idx in sequences:
        
        # increment the index counter...
        idx_counter = idx_counter + 1

        # grab the sequence and convert to upper as well
        local_sequence = sequences[idx].upper()

        # make sure file doesn't try to save if no output dir specified
        if output_dir is not None:

            # define the full filename with filetype. NOTE - we use os.sep as an OS-independent way to define
            # filename and filepath. This may end up with the filename containing a double slash, but this is fine
            # and matplotlib deals with this appropriately. This should be a POSIX-compliant way to do cross-platform
            # file writing
            if indexed_filenames:
                filename = output_dir + os.sep + "%i_"%(idx_counter) + _dssp_tools.sanitize_filename(idx)[0:14] + ".%s"%(output_filetype)
            else:
                filename = output_dir + os.sep + _dssp_tools.sanitize_filename(idx)[0:14] + ".%s"%(output_filetype)

            # define title (including bad chars)
            title = idx[0:14]

            # plot!        
            graph_dssp(local_sequence, title=title, exclude_disorder=exclude_disorder,
            no_disorder_bars=no_disorder_bars, dis_threshhold=dis_threshhold, DPI=DPI, output_file=filename)

        # if no output_dir specified just graph the seq        
        else:
            # define title (including bad chars)
            title = idx[0:14]            
            graph_dssp(local_sequence, title=title, exclude_disorder=exclude_disorder,
            no_disorder_bars=no_disorder_bars, dis_threshhold=dis_threshhold, DPI=DPI)


def predict_dssp_uniprot(uniprot_id):
    """
    Function to return dssp scores of a single input sequence. Uses a 
    Uniprot ID to get the sequence.

    Parameters
    ------------

    uniprot_ID : str
         The uniprot ID of the sequence to predict


    Returns
    ----------
    
    dssp scores : str
        the dssp scores for the corresponding seqeunce
    
    """
    # get sequence
    sequence = _fetch_sequence(uniprot_id)

    # return scores
    return _predict_dssp(sequence)


# def graph_dssp_uniprot

def graph_dssp_uniprot(uniprot_id,
          title='Predicted DSSP Scores',
          exclude_disorder=False,
          no_disorder_bars = False,          
          dis_threshhold = 0.3,
          DPI=150,
          output_file=None):
    """
    Function for graphing predicted dssp scores.

    Parameters
    -----------

    uniprot_id : str 
        unirpot ID for corresponding sequence

    title : str
        Sets the title of the generated figure. Default = "Predicted protein disorder"

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

    # make sure disorder threshhold okay
    _dssp_tools.valid_range(dis_threshhold, 0.0, 1.0)

    # get sequence
    sequence = _fetch_sequence(uniprot_id)

    _graph(sequence, title=title, no_disorder_bars = no_disorder_bars,
        exclude_disorder=exclude_disorder, dis_threshhold=dis_threshhold, 
        DPI=DPI, output_file=output_file)

