# -*- coding: utf-8 -*-

from simmate.workflow_engine.workflow import (
    Workflow,
    Parameter,
    ModuleStorage,
)
from simmate.workflow_engine.common_tasks import LoadInputAndRegister, SaveOutputTask
from simmate.calculators.vasp.tasks.dynamics import MITDynamics
from simmate.calculators.vasp.database.dynamics import MITDynamicsRun

WORKFLOW_NAME = "dynamics/mit"

s3task_obj = MITDynamics()
load_input_and_register = LoadInputAndRegister(MITDynamicsRun)
load_input_and_register = LoadInputAndRegister(
    workflow_name=WORKFLOW_NAME,
    input_obj_name="structure",
    calculation_table=MITDynamicsRun,
)
save_results = SaveOutputTask(MITDynamicsRun)

with Workflow(WORKFLOW_NAME) as workflow:
    structure = Parameter("structure")
    command = Parameter("command", default="vasp_std > vasp.out")
    source = Parameter("source", default=None)
    directory = Parameter("directory", default=None)
    copy_previous_directory = Parameter("copy_previous_directory", default=False)

    # extra parameters unique to molecular dynamics runs
    temperature_start = Parameter("temperature_start", default=300)
    temperature_end = Parameter("temperature_end", default=1200)
    time_step = Parameter("time_step", default=2)
    nsteps = Parameter("nsteps", default=10000)

    structure_toolkit, directory_cleaned = load_input_and_register(
        input_obj=structure,
        source=source,
        directory=directory,
        command=command,
        copy_previous_directory=copy_previous_directory,
        temperature_start=temperature_start,
        temperature_end=temperature_end,
        time_step=time_step,
        nsteps=nsteps,
    )
    output = s3task_obj(
        structure=structure_toolkit,
        command=command,
        directory=directory_cleaned,
        temperature_start=temperature_start,
        temperature_end=temperature_end,
        time_step=time_step,
        nsteps=nsteps,
    )
    calculation_id = save_results(output=output)

workflow.storage = ModuleStorage(__name__)
workflow.project_name = "Simmate-Dynamics"
workflow.calculation_table = MITDynamicsRun
workflow.result_table = MITDynamicsRun
workflow.register_kwargs = (["prefect_flow_run_id", "structure", "source"],)
workflow.result_task = output
workflow.s3task = MITDynamics

# by default we just copy the docstring of the S3task to the workflow
workflow.__doc__ = MITDynamics.__doc__
workflow.description_doc_short = "uses MIT Project settings"
