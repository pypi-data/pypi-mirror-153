"""Console script for popro."""
import os
import sys
from email.policy import default

import click

from popro import engines, popro


@click.command()
@click.option(
    "-i",
    "--input",
    "path_file",
    type=click.STRING,
    multiple=True,
    help="Path to a input file.",
)
@click.option(
    "-y", "--year", "year", type=click.INT, help="Year of projection."
)
@click.option(
    "-p", "--place", "place", type=click.STRING, help="Projection place."
)
@click.option("-a", "--age", "age", type=click.INT, help="Projection age.")
@click.option(
    "-o",
    "--output",
    "output_path",
    type=click.STRING,
    default="",
    help="CSV file path of the projection report to be generated.",
)
@click.option(
    "-oe",
    "--outerr",
    "output_error",
    type=click.STRING,
    default="",
    help="CSV file path from the error report to be generated."
    + "Displays which combinations of the year and locality it was not "
    + "possible to project and the reason.",
)
@click.option(
    "-v",
    "--verbose",
    default=False,
    help="Show the algebraic expression of the calculus",
)
def main(
    path_file,
    year,
    place,
    age,
    output_path="",
    output_error="",
    verbose=False,
    engine=engines.tceduca.Tceduca,
):
    """Console script for popro."""
    if path_file is None:
        click.echo("For help, type: popro --help")
        return
    dict_input = {}
    for file_input in path_file:
        list_input_info = file_input.split(",")
        if len(list_input_info) != 2:
            raise ValueError(
                f'The input file must be in the format: "input_name,file_path"\nInformed parameter: {file_input}'
            )
        dict_input[list_input_info[0]] = list_input_info[1]
    dict_input["year_census"] = int(dict_input["year_census"])

    if age is not None:
        age = int(age)

    engine_projection = popro.Popro(dict_input, engine)
    if output_path != "":
        engine_projection.project_all(output_path, output_error)
    else:
        population = engine_projection.project(year, place, age, verbose)
        click.echo(population)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
