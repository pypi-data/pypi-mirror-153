import os
import sys

from glyles.glycans.factory.factory import MonomerFactory
from glyles.grammar.parse import Glycan


def preprocess_glycans(glycan, glycan_list, glycan_file):
    """
    Preprocess the static inputs for the parsing into one single list

    Args:
        glycan (str): single glycan to parse
        glycan_list (List[str]): list of glycans to parse
        glycan_file (str): filepath of file to read glycans from

    Returns:
        list of glycans in the order they are handed to the function, i.e. glycan, glycan_list, glycan_file
    """
    glycans = []

    # fill a list with all glycans to convert
    if glycan is not None:
        glycans.append(glycan)
    if glycan_list is not None:
        glycans += glycan_list
    if glycan_file is not None:
        # check if the file is valid and read it out
        if not os.path.isfile(glycan_file):
            pass
        for line in open(glycan_file, "r").readlines():
            glycans.append(line.strip())
    return glycans


def convert(glycan=None, glycan_list=None, glycan_file=None, glycan_generator=None, output_file=None, returning=False,
            silent=True):
    """
    General user interaction interface to use this library.

    Args:
        glycan (str): Single glycan to be converted from IUPAC to SMILES
        glycan_list (List[str]): list of glycans to convert
        glycan_file (str): File to read the glycans from
        glycan_generator (generator): generator yielding iupac representation.
            Together with output_generator=True this does not create any lists
        output_file (str): File to save the converted glycans in
        returning (bool): Flag indicating to return a list of tuples
        silent (bool): Flag indicating to have no prints from this method

    Returns:
        List of type (IUPAC, SMILES) items giving the converted SMILES formulas. Only if returning=True is set.
    """

    # collect all data and return if no data were provided
    glycans = preprocess_glycans(glycan, glycan_list, glycan_file)
    if len(glycans) == 0 and glycan_generator is None:
        if not silent:
            print("List of glycans is empty", file=sys.stderr)
        return

    # determine the output format
    if output_file is not None:
        if os.path.isdir(os.path.dirname(os.path.abspath(output_file))):
            output = open(output_file, "w")
        else:
            if not silent:
                print("Path of output-file does not exist! Results will be printed on stdout.", file=sys.stderr)
            output = sys.stdout
    else:
        if returning:
            output = []
        else:
            if not silent:
                print("No output-file specified, results will be printed on stdout.")
            output = sys.stdout

    # convert the IUPAC strings into SMILES strings from the input list
    if len(glycans) != 0:
        for glycan, smiles in convert_generator(glycan_list=glycans, silent=silent):
            if returning:
                output.append((glycan, smiles))
            else:
                print(glycan, smiles, file=output, sep=",")

    # and from the input generator
    if glycan_generator is not None:
        for glycan, smiles in convert_generator(glycan_generator=glycan_generator, silent=silent):
            if returning:
                output.append((glycan, smiles))
            else:
                print(glycan, smiles, file=output, sep=",")

    if returning:
        return output
    elif output_file is not None:
        output.close()


def convert_generator(glycan=None, glycan_list=None, glycan_file=None, glycan_generator=None, silent=True):
    """
    General user interaction interface to use this library.

    Args:
        glycan (str): Single glycan to be converted from IUPAC to SMILES
        glycan_list (List[str]): list of glycans to convert
        glycan_file (str): File to read the glycans from
        glycan_generator (generator): generator yielding iupac representation.
            Together with output_generator=True this does not create any lists
        silent (bool): Flag indicating to have no output-messages from this method

    Returns:
        Generator generating pairs of type (IUPAC, SMILES) items giving the converted SMILES formulas for the IUPACs.
    """
    factory = MonomerFactory()
    glycans = preprocess_glycans(glycan, glycan_list, glycan_file)
    if len(glycans) == 0 and glycan_generator is None:
        if not silent:
            print("List of glycans is empty", file=sys.stderr)
        return

    # Convert the glycans ...
    if len(glycans) != 0:
        for glycan in glycans:
            try:
                # ... by passing them to the glycan class to parse them and return them as intended
                yield glycan, Glycan(glycan, factory).get_smiles()

            # catch any exception at glycan level to not destroy the whole pipeline because of one mis-formed glycan
            except Exception as e:
                print(f"An exception occurred with {glycan}:", e.__class__, file=sys.stderr)
                print("Error message:", e.__str__(), file=sys.stderr)
                yield glycan, ""

    # Convert the glycans ...
    if glycan_generator is not None:
        for glycan in glycan_generator:
            try:
                # ... by passing them to the glycan class to parse them and return them as intended
                yield glycan, Glycan(glycan, factory).get_smiles()

            # catch any exception at glycan level to not destroy the whole pipeline because of one mis-formed glycan
            except Exception as e:
                print(f"An exception occurred with {glycan}:", e.__class__, file=sys.stderr)
                print("Error message:", e.__str__(), file=sys.stderr)
                yield glycan, ""
