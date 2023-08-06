"""
Popro - Population Projection

"""

import pandas as pd

from . import engine_template, engines


def save_report(list_dict, path_report):

    df_report = pd.DataFrame(list_dict)
    df_report.to_csv(path_report, index=False)
    return df_report


class Popro:
    """Popro, a population projection engine.
    Args:
        dict_input (dict): Dictionary with the names and path of the input files required by Engine.
        engine (Engine) Default=engines.Tceduca: Engine object.
    """

    # def __init__(self, dict_input: dict, engine: Engine = engines.Tceduca):
    def __init__(
        self,
        dict_input: dict,
        engine: engine_template.Engine = engines.tceduca.Tceduca,
    ):
        self.dict_input = dict_input
        self.engine = engine(dict_input)
        self.datasets = self.engine.datasets

    def project(self, year, place, age, verbose=False):
        """Projects a single combination of place and age.

        Args:
            year (int): Year of projection.
            place (str): Projection place.
            age (int): Projection age.
            verbose (bool, optional): Show the algebraic expression of the
            calculus. Defaults to False.

        Returns:
            int: Projected population.
        """

        quantity = self.engine.project(year, place, age, verbose)
        return quantity

    def project_all(
        self, output_report_projection_path="", output_report_error_path=""
    ):

        """Projects all possible combinations of place and age.

        Args:
            output_report_projection_path (str, optional): Defaults to "".
                CSV file path of the projection report to be generated.
            output_report_error_path (str, optional): Defaults to "".
                CSV file path from the error report to be generated.
                Displays which combinations of the year and locality it was not
                possible to project and the reason.
        Returns:
            list: The projection report in list of dict.
                  Ready to be used as input in a pandas dataframe object.
        """

        dict_reports = self.engine.project_all()
        self.report_projection = dict_reports["report_projection"]
        self.report_error = dict_reports["report_error"]

        if output_report_projection_path != "":
            save_report(self.report_projection, output_report_projection_path)
        if output_report_error_path != "":
            save_report(self.report_error, output_report_error_path)
        return self.report_projection
