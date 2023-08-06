"""
Definition of database users and roles.
"""
DEFAULT_PASSWORD = "pkdb"

USERS_DATA = [
    {
        "username": "janekg",
        "first_name": "Jan",
        "last_name": "Grzegorzewski",
        "email": "janekg89@hotmail.de",
        "groups": ["admin"],
    },
    {
        "username": "mkoenig",
        "first_name": "Matthias",
        "last_name": "König",
        "email": "koenigmx@hu-berlin.de",
        "groups": ["admin"],
    },
    {
        "username": "dimitra",
        "first_name": "Dimitra",
        "last_name": "Eleftheriadou",
        "email": "dim.ele.paok@gmail.com",
        "groups": ["basic"],
    },
    {
        "username": "kgreen",
        "first_name": "Kathleen",
        "last_name": "Green",
        "email": "test@test.com",
        "groups": ["basic"],
    },
    {
        "username": "jbrandhorst",
        "first_name": "Janosch",
        "last_name": "Brandhorst",
        "email": "jbrandhorst1@googlemail.com",
        "groups": ["basic"],
    },
    {
        "username": "FlorBar",
        "first_name": "Florian",
        "last_name": "Bartsch",
        "email": "bartsflo@hu-berlin.de",
        "groups": ["basic"],
    },
    {
        "username": "deepa",
        "first_name": "Deepa",
        "last_name": "Maheshvare",
        "email": "deepamahm.iisc@gmail.com",
        "groups": ["basic"],
    },
    {
        "username": "yduport",
        "first_name": "Yannick",
        "last_name": "Duport",
        "email": "yannid86@zedat.fu-berlin.de",
        "groups": ["basic"],
    },
    {
        "username": "adriankl",
        "first_name": "Adrian",
        "last_name": "Koeller",
        "email": "adriankl39@googlemail.com",
        "groups": ["basic"],
    },
    {
        "username": "dannythekey",
        "first_name": "Danny",
        "last_name": "Ke",
        "email": "danny.yujia.ke@gmail.com",
        "groups": ["basic"],
    },
    {
        "username": "SaraD-hub",
        "first_name": "Sara",
        "last_name": "De Angelis",
        "email": "deangelis.sara@icould.com",
        "groups": ["basic"],
    },
    {
        "username": "balcisue",
        "first_name": "Sükrü",
        "last_name": "Balci",
        "email": "skbalci@gmail.com",
        "groups": ["basic"],
    },
    {
        "username": "paula-ogata",
        "first_name": "Paul",
        "last_name": "Ogata",
        "email": "up201900135@fe.up.pt",
        "groups": ["basic"],
    },
    {
        "username": "lepujolh",
        "first_name": "Helen",
        "last_name": "Leal",
        "email": "helenl_29@hotmail.de",
        "groups": ["basic"],
    },
    {
        "username": "stemllb",
        "first_name": "Beatrice",
        "last_name": "Stemmer Mallol",
        "email": "stemallb@hu-berlin.de",
        "groups": ["basic"],
    },
    {
        "username": "jonaspk98",
        "first_name": "Jonas",
        "last_name": "Küttner",
        "email": "jonas.kuettner98@gmail.com",
        "groups": ["basic"],
    },
    {
        "username": "reviewer",
        "first_name": "reviewer",
        "last_name": "test",
        "email": "reviewer@googlemail.com",
        "groups": ["reviewer"],
    },
]

USER_GROUPS_DATA = [
    {"name": "basic"},
    {"name": "reviewer"},
    {"name": "admin"},
]
