# runnerase

[![pipeline status](https://gitlab.com/runner-suite/runnerase/badges/main/pipeline.svg)](https://gitlab.com/runner-suite/runnerase/-/commits/main)
[![Documentation](https://img.shields.io/badge/Documentation-latest-blue.svg)](https://theochemgoettingen.gitlab.io/RuNNer)

> An Interface between the Runner Neural Network Energy Representation (RuNNer) and the Atomic Simulation Environment (ASE).

## Key Features

- **readers and writers** for all RuNNer file formats.
- `Runner`, an **ASE calculator** class for managing the RuNNer workflow.
- `SymmetryFunction`/`SymmetryFunctionSet`, classes for generating and manipulating **atom-centered symmetry functions**.
- A `plot`ting library for generating **nice figures** from RuNNer data.
- **storage classes** for atom-centered symmetry function values, weights and scaling data of the atomic neural networks, the split between training and testing set, and the results of a RuNNer fit.
- `RunnerSinglePointCalculator`, an extension of the ASE `SinglePointCalculator` for storing the total charge of a structure.

## Installation

The package can be easily installed via pip. If they are not available, `ASE`
and `numpy` will be automatically installed as dependencies.

```sh
$ pip install runnerase
```

## Credits

This software is an extension of the [Atomic Simulation Environment](ase).

The original code was written by Alexander Knoll - @aknoll - [alexknoll@mailbox.org](alexknoll@mailbox.org).

## License

This software is distributed under the GPL v3. For details, see [LICENSE](LICENSE).

