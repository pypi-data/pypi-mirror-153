"""
Definition of information related to genetics.
"""
from pkdb_data.info_nodes.units import DIMENSIONLESS
from pkdb_data.management.info_node import Choice, DType, MeasurementType


GENETICS_NODES = [
    MeasurementType(
        sid="gene-measurement",
        name="gene measurement",
        label="gene measurement",
        description="Measurement related to genotype or phenotype of gene",
        parents=["measurement"],
        dtype=DType.ABSTRACT,
    ),
    MeasurementType(
        sid="genotype",
        description="Genotype.",
        parents=["gene-measurement"],
        dtype=DType.ABSTRACT,
    ),
    MeasurementType(
        sid="gene-phenotype",
        name="gene phenotype",
        description="Gene phenotype.",
        parents=["gene-measurement"],
        dtype=DType.ABSTRACT,
    ),
    MeasurementType(
        sid="gene-variant",
        name="gene variant",
        description="Gene variant. Gene variants are larger variants such as "
        "wildtype gene or gene duplications. For genotypes see the "
        "respective genotype information.",
        parents=["gene-measurement"],
        dtype=DType.ABSTRACT,
    ),
    MeasurementType(
        sid="nat2-activity",
        name="nat2 activity",
        label="NAT2 activity",
        description="Activity score inferred from  NAT2 genotype ([*4/*4 ]-> 2 "
        ";[*5A,*5B,*5C, *6A, *7B] -> 0; [*4/x]-> 1).",
        parents=["gene-phenotype"],
        dtype=DType.CATEGORICAL,
        synonyms=[],
    ),
    Choice(
        sid="nat2-activity-0",
        name="0",
        label="0",
        description="Any of NAT2 genotype [*5A,*5B,*5C, *6A, *7B] -> 0.",
        parents=["nat2-activity"],
        synonyms=[],
    ),
    Choice(
        sid="nat2-activity-1",
        name="1",
        label="1",
        description="Any of NAT2 genotype [*4/x]-> 1. x is any of [*5A,*5B,*5C, *6A, *7B] genotypes.",
        parents=["nat2-activity"],
        synonyms=[],
    ),
    Choice(
        sid="nat2-activity-2",
        name="2",
        label="2",
        description=" NAT2 genotype *4/*4 has activity 2 ",
        parents=["nat2-activity"],
        synonyms=[],
    ),
    MeasurementType(
        sid="nat2-phenotype",
        name="nat2 phenotype",
        label="NAT2 phenotype",
        description="NAT2 gene phenotype, i.e., acetylation phenotype by N-acetyltransferase 2",
        parents=["gene-phenotype"],
        dtype=DType.CATEGORICAL,
        synonyms=[
            "N-acetyltransferase 2 phenotype",
            "N-acetyltransferase 2 genotype",
            "NAT2 genotype",
        ],
    ),
    MeasurementType(
        sid="cyp1a2-phenotype",
        name="cyp1a2 phenotype",
        label="CYP1A2 phenotype",
        description="CYP1A2 gene phenotype.",
        parents=["gene-phenotype"],
        dtype=DType.CATEGORICAL,
    ),
    MeasurementType(
        sid="cyp2c19-phenotype",
        name="cyp2c19 phenotype",
        label="CYP2C19 phenotype",
        description="CYP2C19 metabolic phenotype. Commonly measurement either by cumulative metabolic ratios in urine "
        "or by metabolic ratios in plasma and serum.",
        parents=["gene-phenotype"],
        dtype=DType.CATEGORICAL,
    ),
    MeasurementType(
        sid="cyp2d6-activity-score",
        name="cyp2d6 activity score",
        label="CYP2D6 activity score",
        description="CYP2D6 activity score. Calculated based on the allele combination"
        "and allele scores. Values are in the range [0-3].",
        parents=["gene-phenotype"],
        dtype=DType.NUMERIC,
        units=[DIMENSIONLESS],
    ),
    # FIXME: create measurement type for phenotypes estimated from genetic variants.
    MeasurementType(
        sid="cyp2d6-phenotype",
        name="cyp2d6 phenotype",
        label="CYP2D6 phenotype",
        description="CYP2D6 metabolic phenotype. Commonly measurement either by cumulative metabolic ratios in urine "
        "or by metabolic ratios in plasma and serum.",
        parents=["gene-phenotype"],
        dtype=DType.CATEGORICAL,
    ),
    Choice(
        sid="poor-metabolizer",
        name="pm",
        label="poor metabolizer (PM)",
        description="Poor metabolizer (PM).",
        parents=[
            "cyp2d6-phenotype",
            "nat2-phenotype",
            "cyp1a2-phenotype",
            "cyp2c19-phenotype",
        ],
        synonyms=["slow metabolizer", "PM", "PM/PM"],
    ),
    Choice(
        sid="intermediate-poor-metabolizer",
        name="im/pm",
        label="intermediate/poor metabolizer (IM/PM)",
        description="intermediate/poor metabolizer (IM/PM)",
        parents=[
            "cyp2d6-phenotype",
            "nat2-phenotype",
            "cyp1a2-phenotype",
            "cyp2c19-phenotype",
        ],
        synonyms=["IM/PM"],
    ),
    Choice(
        sid="intermediate-metabolizer",
        name="im",
        label="intermediate metabolizer (IM)",
        description="Intermediate metabolizer (IM)",
        parents=[
            "cyp2d6-phenotype",
            "nat2-phenotype",
            "cyp1a2-phenotype",
            "cyp2c19-phenotype",
            "cyp2c19-phenotype",
        ],
        synonyms=["IM", "IM/IM"],
    ),
    Choice(
        sid="extensive-poor-metabolizer",
        name="em/pm",
        label="extensive/poor metabolizer (EM/PM)",
        description="extensive/poor metabolizer (EM/PM)",
        parents=[
            "cyp2d6-phenotype",
            "nat2-phenotype",
            "cyp1a2-phenotype",
            "cyp2c19-phenotype",
        ],
        synonyms=["EM/PM"],
    ),
    Choice(
        sid="extensive-intermediate-metabolizer",
        name="em/im",
        label="extensive/intermediate metabolizer (EM/IM)",
        description="extensive/intermediate metabolizer (EM/IM)",
        parents=[
            "cyp2d6-phenotype",
            "nat2-phenotype",
            "cyp1a2-phenotype",
            "cyp2c19-phenotype",
        ],
        synonyms=["EM/IM"],
    ),
    Choice(
        sid="extensive-metabolizer",
        name="em",
        label="extensive metabolizer (EM)",
        description="extensive metabolizer (EM)",
        parents=[
            "cyp2d6-phenotype",
            "nat2-phenotype",
            "cyp1a2-phenotype",
            "cyp2c19-phenotype",
        ],
        synonyms=["fast metabolizer", "rapid metabolizer", "EM", "EM/EM"],
    ),
    Choice(
        sid="ultra-rapid-metabolizer",
        name="um",
        label="ultra rapid metabolizer (UM)",
        description="ultra rapid metabolizer",
        parents=[
            "cyp2d6-phenotype",
            "nat2-phenotype",
            "cyp1a2-phenotype",
            "cyp2c19-phenotype",
        ],
        synonyms=["very fast metabolizer", "UM", "UM/UM"],
    ),
    MeasurementType(
        sid="cyp2d6-variant",
        name="cyp2d6 variant",
        label="gene variant",
        description="CYP2D6 gene variants. Gene variants are larger variants such as "
        "wildtype gene or gene duplications. For genotypes see the "
        "respective genotype information.",
        parents=["gene-variant"],
        dtype=DType.CATEGORICAL,
    ),
    Choice(
        sid="wildtype-gene",
        name="wildtype gene",
        description="Wildtype gene variant.",
        parents=["cyp2d6-variant"],
    ),
    Choice(
        sid="gene-duplication",
        name="gene duplication",
        description="Gene duplication.",
        parents=["cyp2d6-variant"],
    ),
    MeasurementType(
        sid="cyp2d6 genotype",
        name="cyp2d6 genotype",
        label="CYP2D6 genotype",
        description="CYP2D6 genotype.",
        parents=["genotype"],
        dtype=DType.CATEGORICAL,
    ),
    MeasurementType(
        sid="cyp3a4-genotype",
        name="cyp3a4 genotype",
        label="CYP3A4 genotype",
        description="CYP3A4 genotype",
        parents=["genotype"],
        dtype=DType.CATEGORICAL,
    ),
    MeasurementType(
        sid="cyp3a5-genotype",
        name="cyp3a5 genotype",
        label="CYP3A5 genotype",
        description="CYP3A5 genotype.",
        parents=["genotype"],
        dtype=DType.CATEGORICAL,
    ),
    MeasurementType(
        sid="slco1b1-genotype",
        name="SLCO1B1 genotype",
        label="SLCO1B1 genotype",
        description="SLCO1B1 genotype",
        synonyms=[
            "LST1 genotype",
            "OATP1B1 genotype",
            "OATP2 genotype",
            "OATPC genotype",
            "SLC21A6 genotype",
            "LST-1 genotype",
            "OATP-C genotype",
        ],
        parents=["genotype"],
        dtype=DType.CATEGORICAL,
    ),
    MeasurementType(
        sid="mdr1-genotype",
        name="MDR1 genotype",
        label="MDR1 genotype",
        description="MDR1/P-glycoprotein (multidrug reistance 1) genotype",
        synonyms=["P-glycoprotein genotype"],
        parents=["genotype"],
        dtype=DType.CATEGORICAL,
    ),
    MeasurementType(
        sid="cyp2c9-genotype",
        name="cyp2c9 genotype",
        label="CYP2C9 genotype",
        description="CYP2C9 genotype.",
        parents=["genotype"],
        dtype=DType.CATEGORICAL,
    ),
    MeasurementType(
        sid="abcg2-genotype",
        name="ABCG2 genotype",
        label="ABCG2 genotype",
        description="ABCG2 genotype.",
        parents=["genotype"],
        dtype=DType.CATEGORICAL,
    ),
    MeasurementType(
        sid="abcb1-genotype",
        name="ABCB1 genotype",
        label="ABCB1 genotype",
        description="ABCB1 genotype.",
        parents=["genotype"],
        dtype=DType.CATEGORICAL,
    ),
    MeasurementType(
        sid="cyp1a2-genotype",
        name="CYP1A2 genotype",
        label="CYP1A2 genotype",
        description="CYP1A2 genotype.",
        parents=["genotype"],
        dtype=DType.CATEGORICAL,
    ),
]

# Pharmvar information

# (1) legacy information
# https://www.pharmvar.org/gene/CYP1A2
# sid=CYP1A2*1A
# description= rest of information + special pharmvar fields ?
# annotations = [ (BQB.IS, pubmed/Ikeya et al, 1989), Quattrochi and Tukey, 1989]
# add link to https://www.pharmvar.org/gene/CYP1A2

# (2) REST information


CYP1A2_ALLELES = []  # see https://www.pharmvar.org/gene/CYP1A2

CYP1A2_GENOTYPES = [
    "*1a/*1a",
    "*1a/*1f",
    "*1c/*1f",
    "*1f/*1f",
    "*1c*1f/*1c*1f",
    "-163C>A c/c",
    "-163C>A c/a",
    "-163C>A a/a",
    "rs2470893 G>A (zero A allele)",  # genetic variant of rs2470893 (promoter localized in the intergenic region between CYP1A1 and CYP1A2)
    "rs2470893 (one A allele)",  # genetic variant of rs2470893 (promoter localized in the intergenic region between CYP1A1 and CYP1A2)
    "rs2470893 (two A allele)",  # genetic variant of rs2470893 (promoter localized in the intergenic region between CYP1A1 and CYP1A2)
    "*1F,*1F",
    "*1B,*1F and *6",
    "*1B,*1F and *1F",
    "*1B,*1F and *1B",
    "*1B,*1F",
    "*1B,*1D,*1E,*1F and *1K",
    "*1B,*1D,*1F and *1F, C(-730)T",
    "*1B,*1D,*1F and *1F",
    "*1B,*1D,*1F and *1B,*1D,*1F",
    "*1B,*1D,*1F and *1B,*1D,*1E, *1F",
    "*1B,*1D,*1F and *1B,*1C,*1D, *1F",
    "*1B,*1D,*1F and *1B",
    "*1B,*1D,*1E,*1F and *1F",
    "*1B,*1D,*1E,*1F and *1B,*1D,*1E,*1F",
    "*1B,*1D,*1E,*1F and *1B",
    "*1B,*1C,*1D,*1F and *1B",
    "*1B,*1C,*1D,*1F and *1F",
    "*1B,*1C,*1D,*1F and *1B,*1D,*1E,*1F",
    "*1B,*1C,*1D,*1F and *1B,*1C,*1D,*1F",
    "*1B,*1B",
]
for key in CYP1A2_GENOTYPES:
    GENETICS_NODES.append(
        Choice(
            sid=f"cyp1a2-{key}",
            name=key,
            label=f"CYP1A2 {key}",
            description=f"CYP1A2 {key} genotype.",
            parents=["cyp1a2-genotype"],
        )
    )

# todo: add as synonyms
# https://www.pharmvar.org/gene/CYP2D6
CYP2D6_GENOTYPES = [
    "*1/*1",  # C/C_188 # em
    "*1/*1x2",
    "*1/*2",  # em
    "*1/*2x2",
    "*1/*3",
    "*1/*4",
    "*1/*4x2",
    "*1/*5",  # em
    "*1/*6",
    "*1/*7",
    "*1/*9",
    "*1/*10",  # C/T_188 # em
    "*1/*10x2",
    "*1/*17",
    "*1/*21",
    "*1/*29",
    "*1/*36",
    "*1/*41",
    "*1/*42",
    "*1/*45 or 46",  # todo: how to encode this
    "*1x2/*1",
    "*1x2/*2",
    "*1x2/*4",
    "*1x2/*5",
    "*1x2/*10",
    "*1x2/*17",
    "*1/*35",
    "*1x2/*41",
    "*1/*1xN",  # collection of subjects with N > 1
    "*1xN/*17",  # collection of subjects with N > 1
    "*1xN/*35",  # collection of subjects with N > 1
    "*1/*2xN",  # collection of subjects with N > 1
    "*2/*1x2",
    "*2/*2",
    "*2/*2x2",
    "*2/*3",
    "*2/*4",
    "*2/*4x2",
    "*2/*5",
    "*2/*6",
    "*2/*9",
    "*2/*10",
    "*2/*14",
    "*2/*17",
    "*2/*21",
    "*2/*29",
    "*2/*36+*10x2",  # todo: Janek: Better understand what this is and if to keep it.
    "*2/*41",
    "*2x2/*1",
    "*2x2/*3",
    "*2x2/*4",
    "*2x2/*5",
    "*2x2/*17",
    "*3/*2",  # em
    "*3/*2x2",
    "*3/*3",
    "*3/*4",
    "*3/*5",  # pm
    "*4/*4",  # pm
    "*4/*5",  # pm
    "*4/*6",
    "*4/*9",
    "*4/*10",
    "*4/*17",
    "*4x2/*17",
    "*4/*36",
    "*4/*41",
    "*5/*5",
    "*5/*10",
    "*5/*14",
    "*5/*16",
    "*5/*17",
    "*5/*29",
    "*6/*6",
    "*6/*35",
    "*6/*41",
    "*7/*41",
    "*10/*10",  # T/T_188
    "*10/*10x2",
    "*10/*14",
    "*10/*17",
    "*10/*36",
    "*10/*41",
    "*10/*41x2",
    "*13+*1/*4",  # todo: Janek: Better understand what this is and if to keep it.
    "*17/*35",
    "*17/*17",
    "*17/*29",
    "*17/*41",
    "*17/*42",
    "*29/*29",
    "*29/*41",
    "*29/*45 or 46",  # todo: Janek: Better understand what this is and if to keep it.
    "*35/*35",
    "*41/*41",
    "*41/null",
    "*x/*4",
    "*other/*other",  # todo: other probably the same as x -> rename
    "*other/*17",  # todo: other probably the same as x -> rename
    "*other/*29",  # todo: other probably the same as x -> rename
    "*other/*41",  # todo: other probably the same as x -> renames
]

for key in CYP2D6_GENOTYPES:
    GENETICS_NODES.append(
        Choice(
            sid=f"cyp2d6-{key}",
            name=key,
            label=f"CYP2D6 {key}",
            description=f"CYP2D6 {key} genotype.",
            parents=["cyp2d6-genotype"],
        )
    )

CYP3A4_GENOTYPES = ["wildtype/wildtype", "other/*1B", "*1/*1", "*1/*22"]
for key in CYP3A4_GENOTYPES:
    GENETICS_NODES.append(
        Choice(
            sid=f"cyp3a4-{key}",
            name=key,
            label=f"CYP3A4 {key}",
            description=f"CYP3A4 {key} genotype.",
            parents=["cyp3a4-genotype"],
        )
    )

CYP3A5_GENOTYPES = [
    "other/*1C",
    "other/*3",
    "*3/*3",
    "*3/*1",
    "*1/*3",
    "*1/*1",
    "G/G",
    "A/G",
    "A/A",
]
for key in CYP3A5_GENOTYPES:
    GENETICS_NODES.append(
        Choice(
            sid=f"cyp3a5-{key}",
            name=key,
            label=f"CYP3A5 {key}",
            description=f"CYP3A5 {key} genotype.",
            parents=["cyp3a5-genotype"],
        )
    )

# OATP1B1 (e.g. pravastatin or simvastatin)
# rs numbers describe the SNP (single nucleotide polymorphisms)
# TODO: map on rs annotation; see https://www.ncbi.nlm.nih.gov/snp/?term=SLCO1B1%5BGene%20Name%5D


SLCO1B1_GENOTYPES = [
    # FIXME: https://www.ncbi.nlm.nih.gov/snp/
    # star syntax
    "*1/*1",
    "*1/*16",
    "*1b/*16",
    "*1a/*1a",
    "*1a/*1b",
    "*1b/*1b",
    "*1a/*5",
    "*1a/*15",
    "*1b/*15",
    "*1b/*5",
    "*15/*15",
    # single nucleotide polymorphisms
    # rs4149056 = c.521T>C
    # rs2306283 = c.388A>G
    # c.571T>C
    # c.597C>T
    # g.11187G>A
    "c.521 T/T",  # (1*/1*), c.521T/c.521T synonym 521TT genotype, FIXME: not sure that *1 is *1
    "c.521 T/C",  # (1*/rs4149056) 521 T>C, rs4149056 (haplotypes with variant alleles: *5, *15, *17, *40, *46, *47)
    "c.521 C/C",  # (rs4149056/rs4149056); c.521T>C/c.521T>C
    "c.521 C/T",  # (rs4149056/1*)
    # "c.521 T/T-CGC/CGC",
    # "c.521 T/T-TTT/TTT",
    # "c.521 T/C-TTT/TTT",
    # "c.521 T/C-CGC/CGC",
    "c.388 A/A",
    "c.388 A/G",
    "c.388 G/G",
    "c.571 T/T",  # FIXME: map to rs code
    "c.571 C/T",
    "c.571 C/C",
    "c.597 C/C",  # FIXME: map to rs code
    "c.597 C/T",
    "c.597 T/T",
    "g.11187 G/G",  # FIXME: map to rs code, # -11187G>A
    "g.11187 A/G",
    "g.11187 G/A",
    # alleles
    "no *15b",  # non-carriers of *15B: (c.388A/c388A) & (c.521T/c521T)
    "no *17",  # non-carriers of *17: (c.388A/c388A) & (c.521T/c521T) & (g.11187G/g.11187G)
    "*x/*15b",  # heterozygous carriers of *15B (c.388A/c388A>G) & (c.521T/c521T>C)
    "*x/*17",  # heterozygous carriers of *17 (c.388A/c388A>G) & (c.521T/c521T>C) & (g.11187G/g.11187G>A)
]
for key in SLCO1B1_GENOTYPES:
    GENETICS_NODES.append(
        Choice(
            sid=f"slco1b1-{key}",
            name=key,
            label=f"SLCO1B1 {key}",
            description=f"SLCO1B1 {key} genotype.",
            parents=["slco1b1-genotype"],
            synonyms=[
                f"LST1 {key} genotype",
                f"OATP1B1 {key} genotype",
                f"OATP2 {key} genotype",
                f"OATPC {key} genotype",
                f"SLC21A6 {key} genotype",
                f"LST-1 {key} genotype",
                f"OATP-C {key} genotype",
            ],
        ),
    )

CYP2C9_GENOTYPES = ["C/A", "A/A"]
for key in CYP2C9_GENOTYPES:
    GENETICS_NODES.append(
        Choice(
            sid=f"cyp2c9-{key}",
            name=key,
            label=f"CYP2C9 {key}",
            description=f"CYP2C9 {key} genotype.",
            parents=["cyp2c9-genotype"],
        )
    )

ABCG2_GENOTYPES = [
    "c.34 A/G",
    "c.34 G/G",
    "c.421 C/C",
    "c.421 C/A",
    "c.421 A/A",
]
for key in ABCG2_GENOTYPES:
    GENETICS_NODES.append(
        Choice(
            sid=f"abcg2-{key}",
            name=key,
            label=f"ABCG2 {key}",
            description=f"ABCG2 {key} genotype.",
            parents=["abcg2-genotype"],
        )
    )

MDR1_GENOTYPES = [
    "3435CC",
    "3435CT",
    "3435TT",
]
for key in MDR1_GENOTYPES:
    GENETICS_NODES.append(
        Choice(
            sid=f"mdr1-{key}",
            name=key,
            label=f"MDR1 {key}",
            description=f"MDR1 {key} genotype.",
            parents=["mdr1-genotype"],
        )
    )

ABCB1_GENOTYPES = [
    "G2677T/A A/T",
    "G2677T/A T/T",
    "G2677T/A G/A",
    "G2677T/A G/T",
    "G2677T/A G/G",
    "C3435T C/C",
    "C3435T T/C",
    "C3435T T/T",
    "TTT",
    "CGC",
    "Non-TTT",
]
for key in ABCB1_GENOTYPES:
    GENETICS_NODES.append(
        Choice(
            sid=f"ABCB1{key}",
            name=key,
            label=f"ABCB1 {key}",
            description=f"ABCB1 {key} genotype.",
            parents=["abcb1-genotype"],
        )
    )
