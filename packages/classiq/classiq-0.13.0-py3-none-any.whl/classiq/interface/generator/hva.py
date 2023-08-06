from typing import Union

import pydantic
from typing_extensions import Literal

from classiq.interface.chemistry.ground_state_problem import GroundStateProblem
from classiq.interface.generator import function_params


class HVA(function_params.FunctionParams):
    """
    Hamiltonian Variational Ansatz
    """

    gs_problem: Union[
        Literal["ground_state_problem"], GroundStateProblem
    ] = pydantic.Field(description="Ground state problem object describing the system.")
    reps: pydantic.PositiveInt = pydantic.Field(
        default=1, description="Number of layers in the Ansatz"
    )
    use_naive_evolution: bool = pydantic.Field(
        default=False, description="Whether to evolve the operator naively"
    )

    _input_names = pydantic.PrivateAttr(default=[function_params.DEFAULT_INPUT_NAME])
    _output_names = pydantic.PrivateAttr(default=[function_params.DEFAULT_OUTPUT_NAME])
