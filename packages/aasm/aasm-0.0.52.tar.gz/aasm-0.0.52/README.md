# Agents Assembly Translator

## Table of Contents

- [About](#about)
- [Agents Assembly](#agents-assembly)
- [Getting Started](#getting-started)
- [Structure](#structure)
- [Contributing](#contributing)

## About <a name = "about"></a>
A target agnostic translator for Agents Assembly. The translator can be tested live on [Agents Assembly website](https://agents-assembly.com/translator).
It is a part of the [Agents Assembly](https://agents-assembly.com) ecosystem.
Other applications are:
- [Local Interface](https://github.com/agent-based-information-flow-simulation/local-interface) - GUI for simulation definition, management, and analysis.
- [Simulation Run Environment](https://github.com/agent-based-information-flow-simulation/simulation-run-environment) - environment for running scalable agent-based simulations.
- [Communication Server](https://github.com/agent-based-information-flow-simulation/communication-server) - cluster of servers used for XMPP communication.

## Agents Assembly <a name = "agents-assembly"></a>
Documentation of Agents Assembly can be read [here](DOCS.md).

## Getting Started <a name = "getting-started"></a>

### Prerequisites

```
Python 3.10
```

### Installation
The translator [package](https://pypi.org/project/aasm) can be installed by running:
```
pip install aasm
```
Alternatively, you can download this repository. No additional dependencies are required.

### Usage
You can run the translator as a package. To translate *agent.aasm* to SPADE, run:
```
python -m aasm.translate agent.aasm
```

For more usage information, run:
```
python -m aasm.translate --help
```

## Structure <a name = "structure"></a>

* `generating`
    * `code.py` - generated code
    * `python_code.py` - Python code base class
    * `python_graph.py` - Python graph code generation from the intermediate representation
    * `python_spade.py` - SPADE agent code generation from the intermediate representation
* `intermediate`
    * `action.py`
    * `agent.py`
    * `argument.py` - arguments used in instructions
    * `behaviour.py`
    * `block.py` - block of code representation
    * `declaration.py` - declarations used in actions
    * `graph.py`
    * `instruction.py` - instructions used in actions
    * `message.py`
* `parsing`
    * `parse.py` - parsing environment from Agents Assembly file
    * `op/` - Agents Assembly operations
    * `state.py` - state definition used for the parsing process
* `preprocessor`
    * `constants.py` - constants used in the preprocessor
    * `macro.py` - macro definitions used in the preprocessor
    * `preprocessor_item.py` - preprocessor base item
    * `preprocessor.py`
* `utils`
    * `exception.py`
    * `validation.py`
    * `iteration.py`
* `translate.py` - entrypoint

## Contributing <a name = "contributing"></a>
Please follow the [contributing guide](CONTRIBUTING.md) if you wish to contribute to the project.
