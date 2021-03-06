# -*- coding: utf-8 -*-

#from aiida.orm.calculation.job.sum import SumCalculation
from aiida.parsers.parser import Parser
from aiida.parsers.exceptions import OutputParsingError
from aiida.orm.data.parameter import ParameterData

import json

class MultiplyParser(Parser):
    """
    This class is the implementation of the Parser class for Mul.
    """
    def parse_with_retrieved(self, retrieved):
        """
        Parses the datafolder, stores results.
        This parser for this simple code does simply store in the DB a node
        representing the file of forces in real space
        """

        successful = True
        # select the folder object
        # Check that the retrieved folder is there
        try:
            out_folder = retrieved[self._calc._get_linkname_retrieved()]
        except KeyError:
            self.logger.error("No retrieved folder found")
            return False, ()

        # check what is inside the folder
        list_of_files = out_folder.get_folder_list()
        # at least the stdout should exist
        if self._calc._OUTPUT_FILE_NAME not in list_of_files:
            successful = False
            self.logger.error("Output json not found")
            return successful,()

        try:
            with open( out_folder.get_abs_path(self._calc._OUTPUT_FILE_NAME) ) as f:
                out_dict = json.load(f)
        except ValueError:
            successful=False
            self.logger.error("Error parsing the output json")
            return successful,()

        output_data = ParameterData(dict=out_dict)
        link_name = self.get_linkname_outparams()
        new_nodes_list = [(link_name, output_data)]

        return successful,new_nodes_list


