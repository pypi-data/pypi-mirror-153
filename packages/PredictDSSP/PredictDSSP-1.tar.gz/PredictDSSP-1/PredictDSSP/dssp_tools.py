
import re
from PredictDSSP.dssp_exceptions import DsspError

def valid_range(inval, minval, maxval):
    if inval < minval or inval > maxval:
        raise DsspError('Value %1.3f is outside of range [%1.3f, %1.3f]' % (inval, minval, maxval))


def write_csv(input_dict, output_file):
    """
    Function that writes the scores in an input dictionary out to a standardized CVS file format.

    Parameters
    -----------
    input_dict : dict
        Dictionary where keys are headers/identifiers and values is a list of per-residue
        disorder score

    output_file : str
        Location and filename for the output file. Assumes .csv is provided.

    Returns
    --------
    None
        No return value, but writes a .csv file to disk


    """

    # try and open the file and throw exception if anything goes wrong
    try:
        fh = open(output_file, 'w')
    except Exception:
        raise DsspError('Unable to write to file destination %s' % (output_file))

    # for each entry
    for idx in input_dict:

        # important otherwise commmas in FASTA headers render the CSV file unreadable!
        no_comma = idx.replace(',', ' ')
        fh.write('%s' % (no_comma))

        # for each score write
        for score in input_dict[idx]:
            fh.write(', %1.3f' % (score))
        fh.write('\n')



def sanitize_filename(input_filename):
    """
    Function that removes characters from a putative filename which might be problematic
    for filesystems.

    Parameters
    ------------
    input_filename : str
        Proposed filename

    Returns
    ---------
    str
        Returns a string with the nicely formatted filename

    """

    # this regular expression replace every character not equal to a
    # WORD character (i.e. alphanumeric or underscore) with a space
    s = re.sub(r'\W+', '_', input_filename)
    return s
