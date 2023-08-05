"""Example creating linear chain.

This demonstrates core SBML functionality in combination with using patterns.
`sbmlutils` allows to generate patterns of objects by combining loops in combination
with string patterns. In this example we create a kinetic model of a linear chain.
"""
from pathlib import Path
from typing import List

import libsbml

from sbmlutils.cytoscape import visualize_sbml
from sbmlutils.examples import templates
from sbmlutils.factory import *
from sbmlutils.metadata import *
from sbmlutils.resources import EXAMPLES_DIR


n_chain = 20
# -------------------------------------------------------------------------------------
_m = Model("linear_chain")
_m.compartments = [
    Compartment(sid="cell", value=1.0),
]
_m.species = [
    Species(sid="S1", initialConcentration=10.0, compartment="cell"),
]
_m.parameters = []
_m.reactions = []
for k in range(n_chain):
    _m.species.append(
        Species(sid=f"S{k + 2}", initialConcentration=0.0, compartment="cell"),
    )
    _m.parameters.append(
        Parameter(sid=f"k{k+1}", value=0.1),
    )
    _m.reactions.append(
        Reaction(
            sid=f"J{k+1}", equation=f"S{k+1} -> S{k+2}", formula=f"k{k+1} * S{k+1}"
        ),
    )
# -------------------------------------------------------------------------------------


def create(tmp: bool = False) -> FactoryResult:
    """Create model."""
    return create_model(
        models=_m,
        output_dir=EXAMPLES_DIR,
        units_consistency=False,
        tmp=tmp,
    )


if __name__ == "__main__":
    fac_result = create()
    visualize_sbml(sbml_path=fac_result.sbml_path)
