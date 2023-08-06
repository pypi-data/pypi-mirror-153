"""Manipulation of `study.json` files.

-------------------------------------------------------------------------------------
READ THIS, SERIOUSLY READ THIS
-------------------------------------------------------------------------------------

These module allows to manipulate 'study.json' files.
Use this module with extreme caution and check results before
commit of changes in the repository !!!
!!! If you screw this up you have to fix it !!!

Importantly on all operations the order in the JSON must be maintained!,
i.e. changes must be inserted at the right positions in the OrderedDicts!
All changes to the files must be minimal an should be checked with
git diff before commits !
-------------------------------------------------------------------------------------
"""
import json
import os
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, List, Optional

from pymetadata.log import get_logger

from pkdb_data.management.utils import read_json


logger = get_logger(__name__)


class JsonManipulator:
    """Class for manipulating JSON files.

    These are mainly study.json files in pkdb_data.
    To apply the manipulator to other files change the `json_name` attribute
    on the class before creating instances of the manipulator
    """

    json_name = "study.json"

    def __init__(self, json_path: Path) -> None:
        """Construct JSON manipulator for given study.

        :param json_path: JSON study path
        """
        if not json_path.exists():
            raise IOError(f"Study JSON does not exist '{json_path}'")

        self.path: Path = json_path
        self.json: OrderedDict[str, Any] = read_json(json_path)

    def __repr__(self) -> str:
        """Get representation."""
        return f"<{self.__class__}:{self.path}>"

    def __str__(self) -> str:
        """Get string."""
        return f"<{self.__class__}:{self.path}>"

    def study_sid(self) -> Optional[str]:
        """Study sid from json file."""
        if self.json is None:
            logger.error(f"Study does not have JSON content: '{self.path}'")
            return None

        sid = self.json.get("sid", None)
        if sid is None:
            logger.error(f"Study does not have sid: '{self.path}'")
        else:
            sid = str(sid)
        return sid

    @classmethod
    def from_study_dir(cls, study_path: Path) -> "JsonManipulator":
        """Create JSON Manipulator from given study directory.

        :param study_path: directory with studies.
        :return: Instance of the JSON Manipulator.
        """
        if not study_path.exists():
            raise IOError(f"Study directory does not exist '{study_path}'")
        if not study_path.is_dir():
            raise IOError(f"Study directory is not a directory '{study_path}'")

        return JsonManipulator(json_path=study_path / cls.json_name)

    def to_json(self, overwrite: bool = False) -> str:
        """Convert the content back to JSON.

        Make sure the order is preserved!

        :return:
        """
        json_str = json.dumps(self.json, indent=2, ensure_ascii=False)
        if overwrite:
            with open(self.path, "w") as f_json:
                f_json.write(json_str)
        return json_str

    @staticmethod
    def get_all_study_jsons(
        base_path: Path = Path(__file__).parent.parent / "studies",
    ) -> List[Path]:
        """Gets the study JSONs in the directory."""

        study_jsons = []

        for root, directories, files in os.walk(str(base_path)):
            for filename in files:
                # Join the two strings in order to form the full filepath.
                if filename == "study.json":
                    filepath = os.path.join(root, filename)
                    study_jsons.append(filepath)  # Add it to the list.

        return [Path(fname) for fname in sorted(study_jsons)]

    def delete_field(self, field: str) -> None:
        """Delete PKDB version field on study."""
        if field not in self.json:
            logger.warning(f"Field '{field}' does not exist, " f"cannot delete.")
        else:
            del self.json[field]
            logger.warning(f"Field '{field}' deleted.")

    def add_field_date(self, date: str):
        """Adds date field after sid."""
        if not date:
            return

        field = "date"
        if "date" in self.json:
            logger.warning(f"'{field} already in study: updated to '{date}'")
            self.json[field] = date
        else:
            # we add the date after the sid field
            sid_index = list(self.json.keys()).index("sid")

            json_new = OrderedDict()
            for k, key in enumerate(self.json.keys()):
                json_new[key] = self.json[key]
                if k == sid_index:
                    json_new[field] = date
            self.json = json_new
            logger.warning(f"Field '{field}': '{date}' added.")


def _find_studies_without_count_mapping(substance: Optional[str] = None):
    """Finds studies which miss the count mapping and are encoded by Florian.

    Allows to provide a substance folder.
    """
    base_dir = Path(__file__).parent.parent / "studies"

    studies_dir: Path
    if substance is not None:
        studies_dir = base_dir / substance
    else:
        studies_dir = base_dir

    json_paths = JsonManipulator.get_all_study_jsons(base_path=studies_dir)

    # get study dates
    for json_path in json_paths:
        # create the manipulator
        json_man = JsonManipulator(json_path)
        sid = json_man.study_sid()

        if not json_man.json:
            logger.warning(f"No JSON content in '{sid}'")
            continue

        # pprint(json_man.json)

        json: OrderedDict[str, Any] = json_man.json

        if "creator" in json and json["creator"] == "FlorBar":
            logger.debug(f"Study by Florian: {sid}")

        if "groupset" in json:
            groupset = json["groupset"]
            if "groups" in groupset:
                groups = groupset["groups"]
                for g in groups:
                    if "characteristica" in g:
                        characteristica = g["characteristica"]
                        if (
                            len(characteristica) > 0
                            and characteristica[0]["measurement_type"].startswith(
                                "col=="
                            )
                            and "count" not in characteristica[0]
                        ):
                            logger.error(json_man.path)
                            logger.error(f"Count mapping missing in {sid}:{g}")


def _fix_1():
    """This fix removes the pkdb_version field and
    adds the date information on the studies.
    :return:
    """
    from pprint import pprint

    base_dir = Path(__file__).parent.parent / "studies"

    # test study
    # json_path = studies_dir / 'Abernethy1985' / "study.json"
    # json_paths = [json_path]

    # all caffeine studies
    # studies_dir = base_dir / 'caffeine'
    studies_dir = base_dir
    json_paths = JsonManipulator.get_all_study_jsons(base_path=studies_dir)

    # get study dates
    study_infos = read_json(base_dir / "study_identifiers.json")
    pprint(study_infos)

    for json_path in json_paths:
        # create the manipulator
        json_man = JsonManipulator(json_path)
        logger.warning(json_man)
        sid = json_man.study_sid()

        if sid in study_infos:
            (_, date) = study_infos[sid]
        else:
            if sid.startswith("PKDB"):
                logger.error(f"'^PKDB\d+$' studies require date information: {sid}")
                raise IOError
            date = None

        # apply manipulations
        json_man.delete_field("pkdb_version")
        json_man.add_field_date(date=date)
        # pprint(json_man.json)

        # store file
        json_str = json_man.to_json(overwrite=True)
        # print(json_str)


def _fix_2(substance=None):
    """This fix
    - removes groupby fields from individuals and groups
    - renames "figure" to "image" in outputs and timecourses

    - adds output_type: timecourse to timecourse
    - adds output_type: output to output
    - renames groupby on timecourse to label, or adds label if not existing
    - moves timecourses to outputs
    - removes timecourses
    adds the date information on the studies.
    :return:
    """
    if substance is None:
        logger.error("No substance provided")
        return

    base_dir = Path(__file__).parent.parent / "studies" / substance
    studies_dir = base_dir
    json_paths = JsonManipulator.get_all_study_jsons(base_path=studies_dir)

    for json_path in json_paths:
        # create the manipulator
        json_man = JsonManipulator(json_path)
        logger.warning(json_man)
        sid = json_man.study_sid()
        logger.info(f"study: {sid} | {json_man.path}")
        if sid is None:
            logger.error(
                f"Do not apply script if information is missing: {sid} | {json_man.path}"
            )
            continue

        # apply manipulations
        json_data = json_man.json
        # [1] removes groupby fields from individuals and groups
        groupset = json_data.get("groupset", None)
        if groupset:
            groups = groupset.get("groups", None)
            if groups:
                for group in groups:
                    if "groupby" in group:
                        logger.warning("delete 'groupby' on group")
                        del group["groupby"]

        individualset = json_data.get("individualset", None)
        if individualset:
            individuals = groupset.get("individuals", None)
            if individuals:
                for individual in individuals:
                    if "groupby" in individual:
                        logger.warning("delete 'groupby' on individual")
                        del individual["groupby"]

        # [2] renames "figure" to "image" in outputs and timecourses
        outputset = json_data.get("outputset", None)
        if outputset:
            for key in ["outputs", "timecourses"]:
                items = outputset.get(key, None)
                if items:
                    for item in items:
                        if "figure" in item:
                            logger.warning(f"renaming 'figure' -> 'image' on {key}")
                            item["image"] = item["figure"]

                            del item["figure"]

                        # [3]
                        # - adds output_type: timecourse to timecourse
                        # - adds output_type: output to output
                        if "output_type" not in item:
                            output_type = key[:-1]
                            logger.warning(f"Adding 'output_type' = '{output_type}'")
                            item["output_type"] = output_type

                        # [4] add label to timecourse
                        if key == "timecourses" and "label" not in item:
                            if "groupby" in item:
                                logger.warning(
                                    "renaming 'groupby' -> 'label' on timecourse"
                                )
                                item["label"] = item["groupby"]
                                del item["groupby"]
                            else:
                                logger.warning("adding 'label' on timecourse")
                                item["label"] = "col==label"

            # - move timecourse to outputs
            # - remove timecourses

            timecourses = outputset.get("timecourses", None)
            if timecourses is not None:
                outputs = outputset.get("outputs", None)
                if timecourses and outputs is None:
                    outputs = []
                for timecourse in timecourses:
                    outputs.append(timecourse)
                outputset["outputs"] = outputs
                logger.warning("move timecourses to outputs")
                del outputset["timecourses"]

        # store file
        json_str = json_man.to_json(overwrite=True)
        # print(json_str)


if __name__ == "__main__":
    # TODO: log to file

    _find_studies_without_count_mapping()
    # _find_studies_without_count_mapping("caffeine")
    # _fix_2("midazolam")
