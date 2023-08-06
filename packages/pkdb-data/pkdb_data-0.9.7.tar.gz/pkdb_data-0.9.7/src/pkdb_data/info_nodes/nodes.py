"""
Definition of information tree.

Here all the possible info_nodes are defined.
"""
import pandas as pd
from pymetadata.log import get_logger

from pkdb_data.info_nodes.anthropometry import ANTHROPOMETRY_NODES
from pkdb_data.info_nodes.calculation_type import CALCULATION_NODES
from pkdb_data.info_nodes.demographics import DEMOGRAPHICS_NODES
from pkdb_data.info_nodes.disease import DISEASE_NODES
from pkdb_data.info_nodes.dosing import (
    ADMINISTRATION_FORM_NODES,
    ADMINISTRATION_ROUTE_NODES,
    APPLICATION_NODES,
    DOSING_NODES,
)
from pkdb_data.info_nodes.ethnicity import ETHNICITY_NODES
from pkdb_data.info_nodes.genetics import GENETICS_NODES
from pkdb_data.info_nodes.lifestyle import LIFESTYLE_NODES
from pkdb_data.info_nodes.measurement import MEASUREMENT_NODES
from pkdb_data.info_nodes.medical_procedure import MEDICAL_PROCEDURE_NODES
from pkdb_data.info_nodes.method import METHOD_NODES
from pkdb_data.info_nodes.specie import SPECIE_NODES
from pkdb_data.info_nodes.substance import SUBSTANCE_NODES
from pkdb_data.info_nodes.tissue import TISSUE_NODES
from pkdb_data.management.info_node import Choice, DType, InfoNode, NType


logger = get_logger(__name__)


def _is_duplicate(nodes_df, on):
    """Check for duplicate definitions."""
    _duplicates = nodes_df[nodes_df[on].duplicated(keep="first")]
    _duplicates_no_undefined = _duplicates[_duplicates.ntype != NType.CHOICE]
    if not _duplicates_no_undefined.empty:
        ntype = _duplicates_no_undefined.ntype
        raise Exception(
            f"For Dtype <{ntype.unique()}> the {on}s are not unique. Detail: <{list(getattr(_duplicates_no_undefined, on))}> "
        )


def collect_nodes():
    """Collect and create all nodes.

    :return: [InfoNode]
    """
    # -----------------------------------------------------------------------------
    # Graph definition
    # -----------------------------------------------------------------------------
    ROOT = "root"
    INTERVENTION = "intervention"  # only used on intervention
    MEASUREMENT = "measurement"  # only used on output/time course

    NODES = [
        InfoNode(ROOT, ROOT, parents=None),
        InfoNode(INTERVENTION, "intervention", parents=[], dtype=DType.ABSTRACT),
        InfoNode(MEASUREMENT, "measurement", parents=[], dtype=DType.ABSTRACT),
    ]

    # add nodes to nodes list
    for nodes in [
        MEASUREMENT_NODES,
        ANTHROPOMETRY_NODES,
        DEMOGRAPHICS_NODES,
        LIFESTYLE_NODES,
        DISEASE_NODES,
        SPECIE_NODES,
        ETHNICITY_NODES,
        GENETICS_NODES,
        MEDICAL_PROCEDURE_NODES,
        DOSING_NODES,
        ADMINISTRATION_ROUTE_NODES,
        APPLICATION_NODES,
        ADMINISTRATION_FORM_NODES,
        TISSUE_NODES,
        METHOD_NODES,
        SUBSTANCE_NODES,
        CALCULATION_NODES,
    ]:
        nodes_df = pd.DataFrame([node.serialize(nodes) for node in nodes])
        _is_duplicate(nodes_df, "name")

        NODES.extend(nodes)

    # ----------------------
    # Query metadata
    # ----------------------
    for node in NODES:
        node.query_metadata()

    # -------------------------------------
    # Boolean nodes
    # -------------------------------------
    BOOLEAN_NODES = []
    for info_node in NODES:
        sid = info_node.sid
        # YES/NO info_nodes
        if info_node.dtype == DType.BOOLEAN:
            BOOLEAN_NODES.extend(
                [
                    Choice(
                        sid=f"{sid}-YES",
                        description=f"Yes {info_node.name}.",
                        parents=[sid],
                        name="Y",
                        label=f"{sid}",
                    ),
                    Choice(
                        f"{sid}-NO",
                        description=f"No {info_node.name}.",
                        parents=[sid],
                        name="N",
                        label=f"No {sid}",
                    ),
                ]
            )
        # NR info_nodes
        if info_node.dtype in [
            DType.BOOLEAN,
            DType.CATEGORICAL,
            DType.NUMERIC_CATEGORICAL,
        ]:
            BOOLEAN_NODES.append(
                Choice(
                    sid=f"{sid}-Not-Reported",
                    name="NR",
                    label=f"Not reported {info_node.name}",
                    description=f"Not Reported {info_node.name}.",
                    parents=[sid],
                )
            )

    NODES.extend(BOOLEAN_NODES)

    # -------------------------------------
    # Substance set nodes
    # -------------------------------------
    substance_all_nodes = [
        "medication-duration",
        "medication-amount",
        "medication",
        "dosing",
        "qualitative-dosing",
        "abstinence",
        "consumption",
        "metabolic-ratio",
        "metabolic-phenotype",
        "auc_inf",
        "auc_end",
        "auc_relative",
        "auc_per_dose",
        "aumc_inf",
        "amount",
        "cumulative-amount",
        "concentration",
        "concentration_unbound",
        "clearance",
        "clearance_unbound",
        "clearance_partial",
        "clearance_intrinsic",
        "clearance_renal",
        "clearance_intrinsic_unbound",
        "clearance_renal_unbound",
        "vd",
        "vd_unbound",
        "thalf",
        "tmax",
        "oro-cecal-transit-time",
        "mrt",
        "cmax",
        "kel",
        "kabs",
        "thalf_absorption",
        "fraction_absorbed",
        "plasma_binding",
        "fraction_unbound",
        "recovery",
        "egp",
        "ra",
        "rd",
        "secretion-rate",
    ]

    SUBSTANCE_SET_NODES = []
    for substance_node in substance_all_nodes:
        SUBSTANCE_SET_NODES.append(
            InfoNode(
                sid=f"{substance_node}-substances-all",
                description=f"{substance_node} substances all",
                parents=[f"{substance_node}"],
                name="substances all",
            )
        )

    NODES.extend(SUBSTANCE_SET_NODES)

    # check that all parents exist as nodes and are defined in order
    sids = {n.sid: k for k, n in enumerate(NODES)}
    for k, n in enumerate(NODES):
        for parent in n.parents:
            if parent not in sids:
                logger.error(
                    f"parent node with sid '{parent}' in node '{n.sid}' does not exist"
                )
            elif sids[parent] > k:
                logger.error(
                    f"parent node <'{parent}'> defined after child node <'{n.sid}'>, "
                    f"change order."
                )

    nodes_df = pd.DataFrame([node.serialize(nodes) for node in NODES])
    _is_duplicate(nodes_df, "sid")

    return NODES
