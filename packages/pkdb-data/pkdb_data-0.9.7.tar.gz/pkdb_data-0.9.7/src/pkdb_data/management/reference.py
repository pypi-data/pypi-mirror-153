"""
Handling reference information.

Creates reference.json from given pubmed id.
"""
import json
import os
import xml.etree.ElementTree as ET

import requests
from Bio import Entrez
from pymetadata.log import get_logger

from pkdb_data.management.utils import recursive_iter, set_keys


logger = get_logger(__name__)

# FIXME: get proper email
ENTREZ_EMAIL = "janekg89@hotmail.de"


def run(args):
    ref_dict = {"reference_path": args.reference, "pmid": args.pmid}
    logger.info(ref_dict)
    save_json(add_doi(create_json(xml_to_data(load_from_biopython(ref_dict)))))


def is_numeric(value):
    try:
        is_digit = str.isdigit(value)

    except TypeError:
        is_digit = isinstance(value, int)
    return is_digit


def load_from_biopython(d):
    """Retrieves pubmed information.

    :param d:
    :return:
    """
    Entrez.email = ENTREZ_EMAIL

    if is_numeric(d["pmid"]):
        handle = Entrez.efetch(db="pubmed", id=d["pmid"], retmode="xml")
        all_info = handle.read()
        handle.close()

    else:
        logger.warning(
            "Empty `reference.json` was created. Fill out required fields ['title', 'date']. "
        )
        all_info = (
            "<all>"
            "<PMID> 12345 </PMID>"
            "<DateCompleted>"
            "<Year>1000</Year>"
            "<Month>10</Month>"
            "<Day>10</Day>"
            "</DateCompleted>"
            "<Article>"
            "<Journal>"
            "<Title>Add your title</Title>"
            "</Journal>"
            "<ArticleTitle>Add your title</ArticleTitle>"
            "<AuthorList>"
            "<Author>"
            "<LastName>Mustermann</LastName>"
            "<ForeName>Max</ForeName>"
            "<Initials>MM</Initials>"
            "</Author>"
            "</AuthorList>"
            "</Article>"
            "</all>"
        )

    return {**d, "xml": all_info}


def xml_to_data(d):
    return {**d, "data": ET.fromstring(d["xml"])}


def create_json(d):
    """Creates reference.json"""
    json_dict = {}
    json_dict["name"] = d["reference_path"].name
    print(d["reference_path"].name)
    if is_numeric(d["pmid"]):
        json_dict["pmid"] = d["pmid"]
    json_dict["sid"] = d["pmid"]

    for date in d["data"].iter("DateCompleted"):
        year = date.find("Year").text
        month = date.find("Month").text
        day = date.find("Day").text
        json_dict["date"] = f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}"
        continue
    for journal in d["data"].iter("Title"):
        json_dict["journal"] = journal.text
        continue
    for title in d["data"].iter("ArticleTitle"):
        json_dict["title"] = title.text
        continue
    for abstract in d["data"].iter("AbstractText"):
        json_dict["abstract"] = abstract.text
        continue

    authors = []
    for author in d["data"].iter("Author"):
        author_dict = {}
        for key, value in {"first_name": "ForeName", "last_name": "LastName"}.items():
            try:
                author_dict[key] = author.find(value).text
            except AttributeError:
                msg = f"No Info on author <{key}>. Consider adding the {key} manually to <reference.json>."
                logger.warning(msg)
        authors.append(author_dict)

    json_dict["authors"] = authors

    for keys, item in recursive_iter(json_dict):
        if item == "":
            set_keys(json_dict, None, *keys)

    return {"json": json_dict, "reference_path": d["reference_path"]}


def add_doi(d):
    """Try to get DOI.

    :param d:
    :return:
    """
    json_dict = d["json"]

    if json_dict.get("pmid"):

        response = requests.get(
            f'https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?tool=my_tool&email=my_email@example.com&ids={json_dict["pmid"]}'
        )

        pmcids = ET.fromstring(response.content)
        for records in pmcids.iter("record"):
            json_dict["doi"] = records.get("doi", None)

    return {"json": json_dict, "reference_path": d["reference_path"]}


def save_json(d):
    json_file = os.path.join(d["reference_path"], "reference.json")
    directory = os.path.dirname(json_file)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(json_file, "w") as fp:
        json.dump(d["json"], fp, indent=4)
