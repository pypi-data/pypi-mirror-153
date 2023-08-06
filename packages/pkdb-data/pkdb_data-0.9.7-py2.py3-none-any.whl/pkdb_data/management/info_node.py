"""
Functions related to the InfoNodes
"""
from enum import Enum
from typing import Dict, List, Union

from pint import UndefinedUnitError
from pymetadata.log import get_logger
from slugify import slugify

from pkdb_data.info_nodes.units import ureg
from pkdb_data.metadata.annotation import BQB, Annotation
from pkdb_data.metadata.chebi import ChebiQuery
from pkdb_data.metadata.unichem import UnichemQuery


logger = get_logger(__name__)


class DType(str, Enum):
    """Data types."""

    ABSTRACT = "abstract"
    BOOLEAN = "boolean"
    NUMERIC = "numeric"
    CATEGORICAL = "categorical"
    NUMERIC_CATEGORICAL = ("numeric_categorical",)
    UNDEFINED = "undefined"


class NType(str, Enum):
    """Node types."""

    INFO_NODE = "info_node"  # root elements
    CHOICE = "choice"
    MEASUREMENT_TYPE = "measurement_type"
    CALCULATION_TYPE = "calculation_type"
    APPLICATION = "application"
    TISSUE = "tissue"
    METHOD = "method"
    Route = "route"
    FORM = "form"
    SUBSTANCE = "substance"
    SUBSTANCE_SET = "substance_set"


class InfoObject:
    """Object for defining information."""

    required_fields = ["sid", "name", "label", "ntype", "dtype"]

    def __init__(
        self,
        sid: str,
        name: str = None,
        label: str = None,
        description: str = None,
        ntype: str = None,
        dtype: str = None,
        annotations: List = None,
        synonyms: List[str] = None,
        xrefs: List = None,
        deprecated: bool = False,
    ):
        """

        :param sid: unique identifier
        :param name: curation identifier (used for curation!, mostly sid)
        :param label: display name
        :param ntype: node type
        :param dtype: data type
        :param description: description details.
        :param annotations:
        :param synonyms:
        :param deprecated: deprecation flag for validation
        """
        self.sid = InfoObject.url_slugify(sid)
        self.name = name if name else sid
        self.label = label if label else self.name
        self.description = description
        self.annotations = annotations
        self.synonyms = set(synonyms) if synonyms is not None else set()
        self.xrefs = xrefs
        self.ntype = ntype
        self.dtype = dtype
        self.deprecated = deprecated

        # init with empty list
        for key in ["annotations", "synonyms", "xrefs"]:
            if getattr(self, key) is None:
                setattr(self, key, list())

        self._process_annotations()
        self.validate()

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.sid} | {self.name} | {self.label}>"

    @staticmethod
    def url_slugify(key):
        """Sanitizes sid for use in url."""
        return slugify(
            key, replacements=[["*", "-times-"], ["/", "-over-"], ["+", "-plus-"]]
        )

    def validate(self) -> bool:
        """Validate info node

        :return:
        """
        self.validate_ntype()
        self.validate_dtype()

        # check that fields are simple iterables
        for key in ["annotations", "synonyms"]:
            data = getattr(self, key)
            if not isinstance(data, (list, set, tuple)):
                raise ValueError(
                    f"<{key}> must be list, " f"set or tuple for <{self.sid}>"
                )

        for field in InfoObject.required_fields:
            if not getattr(self, field):
                raise ValueError(
                    f"'Required information <{field}> missing on <{self.sid}>"
                )

        if not self.description:
            logger.warning(f"{self.__class__.__name__} <{self.sid}> misses description")

    def validate_ntype(self):
        """Validate the node type."""
        if self.ntype not in NType:
            raise ValueError(f"<{self.ntype}> is not in Ntype for sid <{self.sid}>.")

    def validate_dtype(self):
        if self.dtype not in DType:
            raise ValueError(
                f"<{self.dtype}> is not in Dtype for for sid <{self.sid}>."
            )

    def _process_annotations(self):
        """Creates annotation objects from annotation strings"""
        full_annotations = []
        for a_data in self.annotations:
            if isinstance(a_data, tuple):
                annotation = Annotation(relation=a_data[0], resource=a_data[1])
            elif isinstance(a_data, Annotation):
                annotation = a_data
            else:
                raise ValueError(
                    f"Unsupported annotation type: {type(a_data)}"
                    f" for '{self.sid}': '{a_data}'"
                )

            full_annotations.append(annotation)

        self.annotations = full_annotations

    def query_metadata(self):
        """Only call once before serialization if the complete tree exists."""

        # query annotation information from ols
        for a in self.annotations:
            # validate annotation
            a.validate()

            a.query_ols()
            if a.relation == BQB.IS:
                if a.label:
                    self.synonyms.add(a.label)
                if a.synonyms:
                    for synonym in a.synonyms:
                        if isinstance(synonym, dict):
                            self.synonyms.add(synonym["name"])
                        else:
                            self.synonyms.add(synonym)
                if a.xrefs:
                    self.xrefs.extend(a.xrefs)

        # process all the metadata
        # FIXME

    def serialize(self):
        return {
            "sid": self.sid,
            "name": self.name,
            "label": self.label,
            "ntype": self.ntype,
            "dtype": self.dtype,
            "description": self.description,
            "annotations": [a.to_dict() for a in self.annotations],
            "synonyms": sorted(list(self.synonyms)),
            "xrefs": [xref.to_dict() for xref in self.xrefs],
            "deprecated": self.deprecated,
        }


class InfoNode(InfoObject):
    """Node."""

    def __init__(
        self,
        sid,
        description,
        parents,
        ntype=NType.INFO_NODE,
        dtype=DType.ABSTRACT,
        name=None,
        label=None,
        annotations=None,
        synonyms=None,
        xrefs=None,
        deprecated=False,
    ):
        """

        :param sid: unique identifier
        :param name: display name
        :param label: curation identifier (used for curation!)
        :param ntype: node type
        :param dtype: data type
        :param description: description details.
        :param annotations:
        :param synonyms:
        :param parents:
        """
        super().__init__(
            sid=sid,
            name=name,
            label=label,
            ntype=ntype,
            dtype=dtype,
            description=description,
            annotations=annotations,
            synonyms=synonyms,
            xrefs=xrefs,
            deprecated=deprecated,
        )
        self.parents = [self.url_slugify(p) for p in parents] if parents else list()

    @property
    def can_choice(self):
        return False

    def children(self, nodes):
        return [node for node in nodes if self.sid in node.parents]

    def parents_as_node(self, nodes_dict):
        return [nodes_dict[parent] for parent in self.parents]

    def children_sids(self, nodes):
        return [node.sid for node in nodes if self.sid in node.parents]

    def all_parents(self, nodes_dict):
        for parent in self.parents_as_node(nodes_dict):
            yield parent
            yield from parent.all_parents(nodes_dict)

    def serialize(self, all_nodes):
        into_dict = super().serialize()
        this_dict = {
            **into_dict,
            "parents": self.parents,
            "children": self.children_sids(all_nodes),
        }
        return this_dict

    def choices(self, all_nodes):
        for child in self.children(all_nodes):
            if not child.can_choice:
                yield from child.choices(all_nodes)

            if child.ntype == NType.CHOICE:
                yield child.sid


class MeasurementType(InfoNode):
    def __init__(
        self,
        sid,
        description,
        parents,
        dtype,
        name=None,
        label=None,
        units=None,
        annotations=None,
        synonyms=None,
        xrefs=None,
        deprecated=False,
    ):
        super().__init__(
            sid=sid,
            name=name,
            label=label,
            ntype=NType.MEASUREMENT_TYPE,
            dtype=dtype,
            description=description,
            annotations=annotations,
            synonyms=synonyms,
            xrefs=xrefs,
            parents=parents,
            deprecated=deprecated,
        )
        self.units = units if units else list()
        self.validate_units()

    @property
    def can_choice(self):
        return self.dtype in [
            DType.CATEGORICAL,
            DType.NUMERIC_CATEGORICAL,
            DType.BOOLEAN,
        ]

    def serialize(self, all_nodes):
        into_dict = super().serialize(all_nodes)
        return {
            **into_dict,
            "measurement_type": self.measurement_type_extra(all_nodes),
        }

    def measurement_type_extra(self, all_nodes):
        measurement_type_extra = {"units": self.units}
        if self.can_choice:
            measurement_type_extra["choices"] = list(self.choices(all_nodes))
        else:
            measurement_type_extra["choices"] = []
        return measurement_type_extra

    def validate_units(self):
        """Validate that units are defined in unit registry."""
        for unit in self.units:
            try:
                ureg(unit)
            except UndefinedUnitError as err:
                logger.error(f"UndefinedUnitError for {self}: {err}")
                raise err


class Substance(InfoNode):
    """Substances"""

    def __init__(
        self,
        sid,
        name=None,
        label=None,
        parents=None,
        synonyms=None,
        description=None,
        annotations=None,
        xrefs=None,
        deprecated=False,
        dtype=DType.UNDEFINED,
        formula: str = None,
        charge: int = None,
        mass: float = None,
    ):
        super().__init__(
            sid=sid,
            name=name,
            label=label,
            description=description,
            parents=parents,
            ntype=NType.SUBSTANCE,
            dtype=dtype,
            annotations=annotations,
            synonyms=synonyms,
            xrefs=xrefs,
            deprecated=deprecated,
        )

        self.formula = formula
        self.charge = charge
        self.mass = mass

        # retrieve chebi information
        chebi = self.chebi()
        if chebi:
            chebi_dict = ChebiQuery.query(chebi)
            if self.description is None:
                self.description = chebi_dict.get("description", None)

            # chemical information
            for key in ["mass", "charge", "formula"]:
                if key in chebi_dict:
                    value = chebi_dict[key]
                    if value is None:
                        continue
                    if getattr(self, key) is not None:
                        logger.warning(
                            f"<{self.sid}> <{key}> overwritten: {getattr(self, key)} -> {value}"
                        )
                    setattr(self, key, value)

            # add inchikey to annotations
            inchikey = chebi_dict.get("inchikey", None)
            if inchikey:
                self.annotations.append(
                    Annotation(relation=BQB.IS, resource=f"inchikey/{inchikey}")
                )
                # perform unichem queries
                xrefs = UnichemQuery.query_xrefs(inchikey=inchikey)
                for xref in xrefs:
                    if xref.validate(warnings=False):
                        self.xrefs.append(xref)

        self.substance = {
            "mass": self.mass,
            "charge": self.charge,
            "formula": self.formula,
            "stype": "derived" if self.parents else "basic",
        }

    def chebi(self) -> str:
        """Read the chebi term from the annotations.
        Returns None of no chebi annotation exists.
        """
        # FIXME: this can be dangerous if additional chebi terms are added
        for annotation in self.annotations:  # type: Annotation
            # check if a chebi annotation exists (returns first)
            if (annotation.relation == BQB.IS) and (annotation.collection == "chebi"):
                return annotation.term
        return None

    def serialize(self, all_nodes):
        """To dict."""
        info_dict = super().serialize(all_nodes)
        info_dict["substance"] = self.substance
        return info_dict


class InfoNodeUndefined(InfoNode):
    def __init__(
        self,
        sid,
        name=None,
        label=None,
        parents=None,
        synonyms=None,
        description=None,
        annotations=None,
        dtype=DType.UNDEFINED,
        deprecated=False,
    ):
        super().__init__(
            sid=sid,
            name=name,
            label=label,
            description=description,
            parents=parents,
            ntype=NType.METHOD,
            dtype=dtype,
            annotations=annotations,
            synonyms=synonyms,
            deprecated=deprecated,
        )


class Method(InfoNode):
    def __init__(
        self,
        sid,
        name=None,
        label=None,
        parents=None,
        synonyms=None,
        description=None,
        annotations=None,
        dtype=DType.UNDEFINED,
        deprecated=False,
    ):
        super().__init__(
            sid=sid,
            name=name,
            label=label,
            description=description,
            parents=parents,
            ntype=NType.METHOD,
            dtype=dtype,
            annotations=annotations,
            synonyms=synonyms,
            deprecated=deprecated,
        )


class Tissue(InfoNode):
    def __init__(
        self,
        sid,
        name=None,
        label=None,
        parents=None,
        synonyms=None,
        description=None,
        annotations=None,
        dtype=DType.UNDEFINED,
        deprecated=False,
    ):
        super().__init__(
            sid=sid,
            name=name,
            label=label,
            description=description,
            parents=parents,
            ntype=NType.TISSUE,
            dtype=dtype,
            annotations=annotations,
            synonyms=synonyms,
            deprecated=deprecated,
        )


class Route(InfoNode):
    def __init__(
        self,
        sid,
        name=None,
        label=None,
        parents=None,
        synonyms=None,
        description=None,
        annotations=None,
        dtype=DType.UNDEFINED,
        deprecated=False,
    ):
        super().__init__(
            sid=sid,
            name=name,
            label=label,
            description=description,
            parents=parents,
            ntype=NType.Route,
            dtype=dtype,
            annotations=annotations,
            synonyms=synonyms,
            deprecated=deprecated,
        )


class Application(InfoNode):
    def __init__(
        self,
        sid,
        name=None,
        label=None,
        parents=None,
        synonyms=None,
        description=None,
        annotations=None,
        dtype=DType.UNDEFINED,
        deprecated=False,
    ):
        super().__init__(
            sid=sid,
            name=name,
            label=label,
            description=description,
            parents=parents,
            ntype=NType.APPLICATION,
            dtype=dtype,
            annotations=annotations,
            synonyms=synonyms,
            deprecated=deprecated,
        )


class Form(InfoNode):
    def __init__(
        self,
        sid,
        name=None,
        label=None,
        parents=None,
        synonyms=None,
        description=None,
        annotations=None,
        dtype=DType.UNDEFINED,
        deprecated=False,
    ):
        super().__init__(
            sid=sid,
            name=name,
            label=label,
            description=description,
            parents=parents,
            ntype=NType.FORM,
            dtype=dtype,
            annotations=annotations,
            synonyms=synonyms,
            deprecated=False,
        )


class CalculationType(InfoNode):
    def __init__(
        self,
        sid,
        name=None,
        label=None,
        parents=None,
        synonyms=None,
        description=None,
        annotations=None,
        dtype=DType.CATEGORICAL,
        deprecated=False,
    ):
        super().__init__(
            sid=sid,
            name=name,
            label=label,
            description=description,
            parents=parents,
            ntype=NType.CALCULATION_TYPE,
            dtype=dtype,
            annotations=annotations,
            synonyms=synonyms,
            deprecated=deprecated,
        )


class Choice(InfoNode):
    def __init__(
        self,
        sid,
        name=None,
        label=None,
        parents=None,
        synonyms=None,
        description=None,
        annotations: List = None,
        dtype=DType.UNDEFINED,
        deprecated=False,
    ):
        super().__init__(
            sid=sid,
            name=name,
            label=label,
            description=description,
            parents=parents,
            ntype=NType.CHOICE,
            dtype=dtype,
            annotations=annotations,
            synonyms=synonyms,
            deprecated=False,
        )

    def measurement_type(self, nodes):
        measurement_types = []
        for node in nodes:
            if node.ntype == NType.MEASUREMENT_TYPE:
                if self.sid in node.choices(nodes):
                    measurement_types.append(node.sid)
        return measurement_types

    def serialize(self, all_nodes):
        into_dict = super().serialize(all_nodes)
        return {
            **into_dict,
            "choice": {"measurement_types": self.measurement_type(all_nodes)},
        }
