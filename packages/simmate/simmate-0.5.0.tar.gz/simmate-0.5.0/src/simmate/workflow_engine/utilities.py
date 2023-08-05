# -*- coding: utf-8 -*-

from simmate.workflow_engine import Workflow, Parameter, ModuleStorage
from simmate.workflow_engine.common_tasks import (
    LoadInputAndRegister,
    SaveOutputTask,
)

from typing import List
from simmate.workflow_engine.supervised_staged_shell_task import S3Task
from simmate.database.base_data_types import Calculation


def s3task_to_workflow(
    name: str,
    module: str,
    project_name: str,
    s3task: S3Task,
    calculation_table: Calculation,
    register_kwargs: List[str],
    description_doc_short: str = None,
):
    """
    Builds a workflow from a S3Task and it's corresponding database table.

    Very often with Simmate's S3Tasks, the workflow for a single S3Task is
    the same. The workflow is typically made of three tasks:

    1. loading the input parameters and registering the calculation
    2. running the calculation (what this S3Task does on its own)
    3. saving the calculation results

    Task 1 and 3 always use the same functions, where we just need to tell
    it which database table we are registering/saving to.

    Because of this common recipe for workflows, we use this method to make
    the workflow for us.
    """

    s3task_obj = s3task()  # Use defaults
    load_input_and_register = LoadInputAndRegister(
        workflow_name=name,
        input_obj_name="structure",
        calculation_table=calculation_table,
    )
    save_results = SaveOutputTask(calculation_table)

    with Workflow(name) as workflow:
        structure = Parameter("structure")
        command = Parameter("command", default="vasp_std > vasp.out")
        source = Parameter("source", default=None)
        directory = Parameter("directory", default=None)
        copy_previous_directory = Parameter("copy_previous_directory", default=False)

        structure_toolkit, directory_cleaned = load_input_and_register(
            input_obj=structure,
            command=command,
            source=source,
            directory=directory,
            copy_previous_directory=copy_previous_directory,
        )
        output = s3task_obj(
            structure=structure_toolkit,
            command=command,
            directory=directory_cleaned,
        )
        calculation_id = save_results(output=output)

    workflow.storage = ModuleStorage(module)
    workflow.project_name = project_name
    workflow.calculation_table = calculation_table
    workflow.result_table = calculation_table
    workflow.register_kwargs = register_kwargs
    workflow.result_task = output
    workflow.s3task = s3task
    workflow.description_doc_short = description_doc_short

    # by default we just copy the docstring of the S3task to the workflow
    workflow.__doc__ = s3task.__doc__

    return workflow
