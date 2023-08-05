"""Default dictionaries of RuNNer parameters.

Attributes
----------
RunnerOptions : TypedDict
    Type specifications for all dictionaries of RuNNer parameters. This is
    mainly used for `DEFAULT_PARAMETERS` at the moment and NOT a complete list
    of all possible parameters as given in `RUNNERCONFIG_DEFAULTS`.
    Currently commented in the code because it is not compatible with Python3.7.
DEFAULT_PARAMETERS : RunnerOptions
    A selection of those keywords in `RUNNERCONFIG_DEFAULTS` which are
        - either mandatory for RuNNer usage,
        - or very commonly used,
        - or have a default in RuNNer that is rarely seen in applications.
    This dictionary is used when initializing a RuNNer calculator object.
"""

from typing import Dict, List
from runnerase.symmetryfunctions import SymmetryFunctionSet


# Originally inherited from TypedDict, but this was removed for now to retain
# backwards compatibility with Python 3.6 and 3.7.
# class RunnerOptions(TypedDict, total=False)
#     """Type specifications for RuNNer default options."""
#
#     runner_mode: int
#     symfunction_short: SymmetryFunctionSet
#     elements: Optional[List[str]]
#     number_of_elements: int
#     bond_threshold: float
#     nn_type_short: int
#     use_short_nn: bool
#     optmode_charge: int
#     optmode_short_energy: int
#     optmode_short_force: int
#     points_in_memory: int
#     scale_symmetry_functions: bool
#     cutoff_type: int
#     # Mode 1.
#     test_fraction: float
#     # Mode 1 and 2.
#     use_short_forces: bool
#     # Mode 1 and 3.
#     remove_atom_energies: bool
#     atom_energy: Dict[str, float]
#     # Mode 2.
#     epochs: int
#     kalman_lambda_short: float
#     kalman_nue_short: float
#     mix_all_points: bool
#     nguyen_widrow_weights_short: bool
#     repeated_energy_update: bool
#     short_energy_error_threshold: float
#     short_energy_fraction: float
#     short_force_error_threshold: float
#     short_force_fraction: float
#     use_old_weights_charge: bool
#     use_old_weights_short: bool
#     write_weights_epoch: int
#     # Mode 2 and 3.
#     center_symmetry_functions: bool
#     precondition_weights: bool
#     global_activation_short: List[str]
#     global_hidden_layers_short: int
#     global_nodes_short: List[int]
#     # Mode 3.
#     calculate_forces: bool
#     calculate_stress: bool


DEFAULT_PARAMETERS: Dict[str, object] = {
    # General for all modes.
    'runner_mode': 1,                     # Default is starting a new fit.
    # All modes.
    'symfunction_short': SymmetryFunctionSet(),  # Auto-set if net provided.
    'elements': None,                     # Auto-set by `set_atoms()`.
    'number_of_elements': 0,              # Auto-set by `set_atoms()`.
    'bond_threshold': 0.5,                # Default OK but system-dependent.
    'nn_type_short': 1,                   # Most people use atomic NNs.
    # 'nnp_gen': 2,                        # 2Gs remain the most common usage.
    'use_short_nn': True,                 # Short-range fitting is the default.
    'optmode_charge': 1,                  # Default OK but option is relevant.
    'optmode_short_energy': 1,            # Default OK but option is relevant.
    'optmode_short_force': 1,             # Default OK but option is relevant.
    'points_in_memory': 1000,             # Default value is legacy.
    'scale_symmetry_functions': True,     # Scaling is used by almost everyone.
    'cutoff_type': 1,                     # Default OK, but important.
    # Mode 1.
    'test_fraction': 0.1,                 # Default too small, more common.
    # Mode 1 and 2.
    'use_short_forces': True,             # Force fitting is standard.
    # Mode 2.
    'epochs': 30,                         # Default is 0, 30 is common.
    'kalman_lambda_short': 0.98000,       # No Default, this is sensible value.
    'kalman_nue_short': 0.99870,          # No Default, this is sensible value.
    'mix_all_points': True,               # Standard option.
    'nguyen_widrow_weights_short': True,  # Typically improves the fit.
    'repeated_energy_update': True,       # Default is False, but usage common.
    'short_energy_error_threshold': 0.1,  # Use only energies > 0.1*RMSE.
    'short_energy_fraction': 1.0,         # All energies are used.
    'short_force_error_threshold': 1.0,   # All forces are used.
    'short_force_fraction': 0.1,          # 10% of the forces are used.
    'use_old_weights_charge': False,      # Relevant for calculation restart.
    'use_old_weights_short': False,       # Relevant for calculation restart.
    'write_weights_epoch': 5,             # Default is 1, very verbose.
    # Mode 2 and 3.
    'center_symmetry_functions': True,    # This is standard procedure.
    'precondition_weights': True,         # This is standard procedure.
    'global_activation_short': [['t', 't', 'l']],  # tanh / linear activ. func.
    'global_hidden_layers_short': 2,      # 2 hidden layers
    'global_nodes_short': [[15, 15]],       # 15 nodes per hidden layer.
}


RUNNERDATA_KEYWORDS: List[str] = ['begin', 'comment', 'lattice', 'atom',
                                  'charge', 'energy', 'end']
