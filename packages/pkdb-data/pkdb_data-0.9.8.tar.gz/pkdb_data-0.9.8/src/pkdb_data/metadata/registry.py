"""
Helper tools to work with miriam metadata.

https://identifiers.org/
https://docs.identifiers.org/articles/api.html
"""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

import requests
from pymetadata.log import get_logger

from pkdb_data.metadata import CACHE_PATH, CACHE_USE
from pkdb_data.metadata.cache import (
    DataclassJSONEncoder,
    read_json_cache,
    write_json_cache,
)


logger = get_logger(__name__)


@dataclass
class Resource:
    """Resource"""

    id: int
    providerCode: str
    name: str
    urlPattern: str
    mirId: str = field(repr=False)
    description: str = field(repr=False)
    official: bool = field(repr=False)

    sampleId: str = field(repr=False)
    resourceHomeUrl: str = field(repr=False)
    institution: dict = field(repr=False)
    location: dict = field(repr=False)
    deprecated: bool = field(repr=False)
    deprecationDate: str = field(repr=False)


@dataclass
class Namespace:
    """Namespace"""

    id: int
    prefix: str
    name: str
    pattern: str
    namespaceEmbeddedInLui: bool
    description: str = field(repr=False)
    mirId: str = field(repr=False, default=None)
    resources: List = field(repr=False, default=None)
    created: str = field(repr=False, default=None)
    modified: str = field(repr=False, default=None)
    sampleId: str = field(repr=False, default=None)
    deprecated: bool = field(repr=False, default=None)
    deprecationDate: str = field(repr=False, default=None)

    def __post_init__(self):
        if self.resources is not None:
            self.resources = [Resource(**d) for d in self.resources]
        else:
            self.resources = list()


def ols_namespaces() -> Dict[str, Namespace]:
    """Ontologies available from OLS but not in identifiers.org"""
    ols_info = {
        "deprecated": False,
        "deprecationDate": None,
        "institution": {
            "description": "At EMBL-EBI, we make the "
            "world’s public biological data "
            "freely available to the "
            "scientific community via a "
            "range of services and tools, "
            "perform basic research and "
            "provide professional training "
            "in bioinformatics. \n"
            "We are part of the European "
            "Molecular Biology Laboratory "
            "(EMBL), an international, "
            "innovative and "
            "interdisciplinary research "
            "organisation funded by 26 "
            "member states and two "
            "associate member states.",
            "homeUrl": "https://www.ebi.ac.uk",
            "id": 2,
            "location": {"countryCode": "GB", "countryName": "United Kingdom"},
            "name": "European Bioinformatics Institute",
            "rorId": "https://ror.org/02catss52",
        },
        "location": {"countryCode": "GB", "countryName": "United Kingdom"},
        "official": False,
        "providerCode": "ols",
    }

    namespaces = [
        Namespace(
            id=None,
            prefix="cmo",
            pattern="^CMO:\d+$",
            name="Chemical methods ontology",
            description="Morphological and physiological measurement records "
            "generated from clinical and model organism research and health programs.",
            namespaceEmbeddedInLui=True,
        ),
        Namespace(
            id=None,
            pattern="^CHMO:\d+$",
            name="Chemical methods ontology",
            prefix="chmo",
            description="CHMO, the chemical methods ontology",
            namespaceEmbeddedInLui=True,
        ),
        Namespace(
            id=None,
            pattern="^VTO:\d+$",
            name="Vertebrate Taxonomy Ontology",
            prefix="vto",
            description="VTO Vertebrate Taxonomy Ontology",
            namespaceEmbeddedInLui=True,
        ),
        Namespace(
            id=None,
            pattern="^OPMI:\d+$",
            name="Ontology of Precision Medicine and Investigation",
            prefix="opmi",
            description="OPMI: Ontology of Precision Medicine and Investigation",
            namespaceEmbeddedInLui=True,
        ),
        Namespace(
            id=None,
            pattern="^MONDO:\d+$",
            name="MONDO",
            prefix="mondo",
            description="MONDO",
            namespaceEmbeddedInLui=True,
        ),
        Namespace(
            id=None,
            pattern="^SIO:\d+$",
            name="SIO",
            prefix="sio",
            description="Semanticscience Integrated Ontology",
            namespaceEmbeddedInLui=True,
        ),
        Namespace(
            id=None,
            pattern="^STATO:\d+$",
            name="STATO",
            prefix="stato",
            description="STATO is the statistical methods ontology. It contains concepts and properties related to "
            "statistical methods, probability distributions and other concepts related to statistical "
            "analysis, including relationships to study designs and plots.",
            namespaceEmbeddedInLui=True,
        ),
        Namespace(
            id=None,
            pattern="^ATOL:\d+$",
            name="ATOL",
            prefix="atol",
            description="Animal Trait Ontology for Livestock",
            namespaceEmbeddedInLui=True,
        ),
        Namespace(
            id=None,
            pattern="^NBO:\d+$",
            name="NBO",
            prefix="nbo",
            description="Neuro Behavior Ontology",
            namespaceEmbeddedInLui=True,
        ),
        Namespace(
            id=None,
            pattern="^SCDO:\d+$",
            name="Sickle Cell Disease Ontology",
            prefix="scdo",
            description="Sickle Cell Disease Ontology",
            namespaceEmbeddedInLui=True,
        ),
        Namespace(
            id=None,
            pattern="^FIX:\d+$",
            name="Physico-chemical methods and properties Ontology",
            prefix="fix",
            description="Physico-chemical methods and properties Ontology",
            namespaceEmbeddedInLui=True,
        ),
        Namespace(
            id=None,
            pattern="^OBA:\d+$",
            name="Ontology of Biological Attributes",
            prefix="oba",
            description="PubChem is an open chemistry database at the National Institutes of Health (NIH).",
            namespaceEmbeddedInLui=True,
        ),
        Namespace(
            id=None,
            pattern="^MMO:\d+$",
            name="Measurement method ontology",
            prefix="mmo",
            description="Measurement method ontology",
            namespaceEmbeddedInLui=True,
        ),
    ]

    for ns in namespaces:
        ns.resources.append(
            Resource(
                id=None,
                name=f"{ns.prefix} through OLS",
                description=f"{ns.prefix} through OLS",
                mirId=None,
                sampleId=None,
                resourceHomeUrl=None,
                urlPattern=f"https://www.ebi.ac.uk/ols/ontologies/chebi/terms?obo_id={ns.prefix.upper()}"
                + ":{$id}",
                **ols_info,
            )
        )

    return {ns.prefix: ns for ns in namespaces}


def misc_namespaces() -> List[Namespace]:
    namespaces = []
    return {ns.prefix: ns for ns in namespaces}


class Registry:
    """Managing the available annotation information.

    Registry of meta information.
    """

    URL = "https://registry.api.identifiers.org/resolutionApi/getResolverDataset"
    CUSTOM_NAMESPACES = {
        **ols_namespaces(),
        **misc_namespaces(),
    }

    def __init__(self, cache_path: Path = CACHE_PATH, cache: bool = CACHE_USE):
        """

        :param cache: retrieve the latest MIRIAM definition
        """
        self.registry_path = cache_path / "identifiers.json"
        self.ns_dict = (
            self.update() if not cache else Registry.load_registry(self.registry_path)
        )  # type: Dict[str, Namespace]

    def update(self) -> Dict[str, Namespace]:
        Registry.update_registry(registry_path=self.registry_path)
        return Registry.load_registry(registry_path=self.registry_path)

    @staticmethod
    def update_registry(
        custom_namespaces: Dict[str, Namespace] = CUSTOM_NAMESPACES,
        registry_path: Path = None,
    ) -> Dict[str, Namespace]:
        """Update registry from identifiers.org webservice."""
        logger.warning(f"Update registry: {Registry.URL}")
        response = requests.get(Registry.URL)
        namespaces = response.json()["payload"]["namespaces"]

        ns_dict = {}
        for k, data in enumerate(namespaces):
            ns = Namespace(**data)
            # for resource in ns.resources:
            #    print(resource)

            ns_dict[ns.prefix] = ns

        if custom_namespaces is not None:
            logger.warning(
                f"Adding custom namespaces: {sorted(custom_namespaces.keys())}"
            )
            for key, ns in custom_namespaces.items():
                if key in ns_dict:
                    logger.error(
                        f"Namespace with key '{key}' exists in MIRIAM. Overwrite namespace!"
                    )
                ns_dict[key] = ns

        if registry_path is not None:
            write_json_cache(
                data=ns_dict,
                cache_path=registry_path,
                json_encoder=DataclassJSONEncoder,
            )

        return ns_dict

    @staticmethod
    def load_registry(registry_path: Path) -> Dict[str, Namespace]:
        """Loads namespaces with resources from path."""
        if not registry_path.exists():
            Registry.update_registry(registry_path=registry_path)

        d = read_json_cache(cache_path=registry_path)

        return {k: Namespace(**v) for k, v in d.items()}


if __name__ == "__main__":
    registry = Registry(cache=False)
