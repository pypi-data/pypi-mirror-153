"""
Definition of available tissues
"""
from pkdb_data.management.info_node import DType, Method
from pkdb_data.metadata.annotation import BQB


METHOD_NODES = [
    Method(
        sid="assay",
        description="A qualitative or quantitative analysis performed to determine the amount of a particular "
        "constituent in a sample or the biological or pharmacological properties of a drug.",
        parents=[],
        dtype=DType.ABSTRACT,
        annotations=[
            (BQB.IS, "ncit/C60819"),
            (BQB.IS, "obi/OBI:0000070"),
            (BQB.IS, "sio/SIO:001007"),
        ],
        synonyms=[],
    ),
    Method(
        sid="nr-method",
        name="NR",
        label="Not reported (method)",
        description="Method not reported.",
        parents=["assay"],
    ),
    Method(
        sid="enzymatic-assay",
        name="enzymatic assay",
        label="enzymatic assay",
        description="A method used to measure the relative activity of a specific "
        "enzyme or its concentration in solution. Typically an enzyme "
        "substrate is added to a buffer solution containing enzyme and "
        "the rate of conversion of substrate to product is measured under "
        "controlled conditions. Many classical enzymatic assay methods "
        "involve the use of synthetic colorimetric substrates and "
        "measuring the reaction rates using a spectrophotometer.",
        annotations=[
            (BQB.IS, "scdo/SCDO:0000436"),
        ],
        parents=["assay"],
    ),
    Method(
        sid="radioenzymatic-assay",
        name="radioenzymatic assay",
        label="radioenzymatic assay",
        description="An assay in which a radioactive substrate is used to quantitate "
        "enzyme activity in a sample or in which a radioactive cofactor "
        "or substrate with an added enzyme is used to quantitate the "
        "level of another substrate in a sample.",
        annotations=[
            (BQB.IS, "mmo/MMO:0000303"),
        ],
        parents=["enzymatic-assay"],
    ),
    Method(
        sid="elisa",
        name="ELISA",
        label="enzyme-linked immunosorbent assay (ELISA)",
        description="A highly sensitive technique for detecting and measuring antigens "
        "or antibodies in a solution; the solution is run over a surface "
        "to which immobilized antibodies specific to the substance have "
        "been attached, and if the substance is present, it will bind to the "
        "antibody layer, and its presence is verified and visualized with "
        "an application of antibodies that have been tagged in some way.",
        annotations=[
            (BQB.IS, "ncit/C16553"),
        ],
        parents=["enzymatic-assay"],
    ),
    Method(
        sid="immunofluorescence",
        name="immunofluorescence",
        description="Microscopic analysis of amount, structure and/or localization of specific proteins in cells or "
        "tissues by staining with fluorescently-labeled primary or secondary antibodies.",
        parents=["assay"],
        annotations=[
            (BQB.IS, "mmo/MMO:0000662"),
        ],
        synonyms=[],
    ),
    Method(
        sid="plasma-binding-measurement",
        name="plasma binding measurement",
        description="plasma binding measurement",
        parents=["assay"],
        dtype=DType.ABSTRACT,
        annotations=[
            (BQB.IS, "ncit/C60819"),
        ],
        synonyms=[],
    ),
    Method(
        sid="competition-dialysis",
        name="competition dialysis",
        description="The separation of molecules in solution by the difference in their rates of diffusion "
        "through a semipermeable membrane. In competition dialysis an array of nucleic acid structures and "
        "sequences is dialysed against a common test ligand solution. After equilibration, "
        "the amount of ligand bound to each structure or sequence is determined by absorbance or "
        "fluorescence measurements. Since all structures and sequences are in equilibrium with the same "
        "free ligand concentration, the amount bound is directly proportional to the ligand binding affinity.",
        parents=["plasma binding measurement"],
        annotations=[
            (BQB.IS, "chmo/CHMO:0002405"),
        ],
        synonyms=["equilibrium-dialysis"],
    ),
    Method(
        sid="ultra-filtration",
        name="ultra-filtration",
        description="A separation process whereby a solution containing a solute of molecular size significantly "
        "greater than that of the solvent molecule is removed from the solvent by the application of "
        "hydraulic pressure which forces only the solvent to flow through a suitable membrane",
        parents=["plasma binding measurement"],
        annotations=[
            (BQB.IS, "chmo/CHMO:0001645"),
        ],
        synonyms=[],
    ),
    Method(
        sid="chromatography",
        description="A technique for the separation of complex mixtures that relies on the differential "
        "affinities of substances for a gas or liquid mobile medium and for a stationary "
        "adsorbing medium through which they pass. ",
        parents=["assay"],
        dtype=DType.ABSTRACT,
        annotations=[
            (BQB.IS, "ncit/C60819"),
        ],
        synonyms=[],
    ),
    Method(
        sid="emit",
        name="EMIT",
        label="Enzyme Multiplied Immunoassay Technique (EMIT)",
        description="A type of homogenous immunoassay in which sample is applied to a reagent mixture of enzyme-labeled "
        "ligand, antibody, and substrate. Substrate binding to enzyme leads to inactivation and "
        "unlabeled-ligand in the sample can be quantified by colorimetric analysis.",
        parents=["assay"],
        annotations=[
            (BQB.IS, "ncit/C111196"),
        ],
    ),
    Method(
        sid="spectrophotometry",
        name="Spectrophotometry",
        label="spectrophotometry",
        description="A laboratory test that produces a quantitative measurement of the reflection or "
        "transmission properties of a material as a function of wavelength.",
        parents=["assay"],
        annotations=[
            (BQB.IS, "ncit/C116701"),
        ],
    ),
    Method(
        sid="ria",
        name="RIA",
        label="radioimmunoassay (RIA)",
        description="Radioimmunoassay (RIA) is an immunological technique, "
        "which quantitatively determines antigen and antibody concentrations, "
        "using a radioactively labeled substance (radioligand), either directly or indirectly.",
        parents=["assay"],
        annotations=[
            (BQB.IS, "ncit/C17057"),
        ],
    ),
    Method(
        sid="cc",
        name="CC",
        label="column chromatography (CC)",
        description="Column chromatography (CC). A process used for separating mixtures by virtue of differences in absorbency. "
        "It involves stationary and mobile phases. The stationary phase was packed in a "
        "column with materials that can be of any partitioning capability, adsorption, "
        "ion exchange, or affinity. The mobile phase (either liquid or gas) "
        "is the mixture that required to be separated.",
        parents=["chromatography"],
        annotations=[
            (BQB.IS, "ncit/C18242"),
        ],
    ),
    Method(
        sid="hplc",
        name="HPLC",
        label="High-performance liquid chromatography (HPLC)",
        description="High-performance liquid chromatography (HPLC) is a column chromatography where the mobile phase is a liquid, "
        "the stationary phase consists of very small particles and "
        "the inlet pressure is relatively high.",
        parents=["cc"],
        annotations=[
            (BQB.IS, "chmo/CHMO:0001009"),
        ],
    ),
    Method(
        sid="rp-hplc",
        name="RP-HPLC",
        label="Reversed-phase high-performance liquid chromatography (RP-HPLC)",
        description="Reversed-phase high-performance liquid chromatography (RP-HPLC), reversed-phase high pressure "
        "liquid chromatography, reversed phase high-performance liquid chromatography, "
        "gradient reverse HPLC, RHPLC, reversed-phase high-pressure liquid chromatography, "
        "reverse phase high performance liquid chromatography, gradient reverse high-performance "
        "liquid chromatography, reversed-phase HPLC ",
        parents=["hplc"],
        annotations=[
            (BQB.IS, "chmo/CHMO:0001259"),
        ],
    ),
    Method(
        sid="hplc-ms-ms",
        name="HPLC MS/MS",
        label="High performance liquid chromatography-tandem mass spectrometry (HPLC MS/MS)",
        description="High performance liquid chromatography-tandem mass spectrometry (HPLC MS/MS) is an analytical "
        "technique wherein high performance liquid chromatography is coupled to tandem mass spectrometry "
        "in order to separate, identify, and quantify substances in a sample. ",
        parents=["hplc"],
        annotations=[
            (BQB.IS, "chmo/CHMO:0002876"),
            (BQB.IS, "ncit/C120691"),
        ],
    ),
    Method(
        sid="ms",
        name="MS",
        label="Mass Spectrometry (MS)",
        description="Mass Spectrometry (MS) is an analytical technique wherein ions are separated according to their ratio "
        "of charge to mass. From the mass spectrum produced, the atomic weight of the particle can be deduced.",
        parents=["assay"],
        dtype=DType.ABSTRACT,
        annotations=[
            (BQB.IS, "ncit/C17156"),
        ],
    ),
    Method(
        sid="cf-irms",
        name="CF-IRMS",
        label="Continuous-flow isotope ratio mass spectrometry (CFIRMS)",
        description="Continuous-flow isotope ratio mass spectrometry (CFIRMS). Mass spectrometry where the relative "
        "abundance of isotopes in a sample is determined. Measurements are taken immediately after sample "
        "preparation and separately to the standard gas.",
        parents=["ms"],
        annotations=[
            (BQB.IS, "chmo/CHMO:0000887"),
        ],
    ),
    Method(
        sid="lc-ms",
        name="LC/MS",
        label="Liquid chromatography mass spectrometry (LC/MS)",
        description="Liquid chromatography mass spectrometry (LC/MS) is a hyphenated technique, combining the "
        "separation molecules dissolved in a solvent, with the detection power of mass spectrometry(MS), "
        "a technique to separate gas phase ions according their m/z (mass to charge ratio) value. "
        "Used for drug screening, pharmacology studies, environmental analyses and forensics.",
        parents=["chromatography", "MS"],
        annotations=[
            (BQB.IS, "ncit/C18475"),
        ],
    ),
    Method(
        sid="lc-ms-ms",
        name="LC MS/MS",
        label="Liquid chromatography-tandem mass spectrometry (LC MS/MS)",
        description="Liquid chromatography-tandem mass spectrometry (LC MS/MS) is a method where a sample mixture is "
        "first separated by liquid chromatography before being ionised and characterised by mass-to-charge "
        "ratio and relative abundance using two mass spectrometers in series.",
        parents=["lc-ms"],
        annotations=[
            (BQB.IS, "chmo/CHMO:0000701"),
        ],
    ),
    Method(
        sid="es-ms-ms",
        name="ES+ MS/MS",
        label="Positive electrospray ionisation tandem mass spectrometry (ES+ MS/MS)",
        description="Positive electrospray ionisation tandem mass spectrometry (ES+ MS/MS) is a mass spectrometry "
        "involving multiple mass-selection steps, with some form of fragmentation "
        "occurring between each stage. Sample ionisation is achieved by forcing a solution "
        "(usually in an organic solvent) of the sample through a small heated capillary "
        "into an electric field to produce a very fine "
        "mist of positively charged droplets.",
        parents=["ms"],
        annotations=[
            (BQB.IS, "chmo/CHMO:0001109"),
        ],
    ),
    Method(
        sid="hplc-esi-ms/ms",
        name="HPLC-ESI-MS/MS",
        label="HPLC-ESI-MS/MS",
        description="High-performance liquid chromatography-electrospray ionisation tandem mass spectrometry "
        "(HPLC-ESI-MS/MS) is A method where the sample mixture is first separated by high-performance "
        "liquid chromatography before being ionised by forcing a solution (usually in an organic solvent) "
        "of it through a small heated capillary into an electric field to produce a very fine mist of "
        "charged droplets. The ions are then characterised according to mass-to-charge ratio and relative "
        "abundance by two mass spectrometers in series.",
        parents=["ms"],
        annotations=[
            (BQB.IS, "chmo/CHMO:0000578"),
        ],
    ),
    Method(
        sid="uv-spectrophotometry",
        name="UV spectrophotometry",
        description="Spectroscopy where the sample absorbs radiation from the ultraviolet region (190–400 nm) "
        "resulting in electronic transitions within the sample.",
        parents=["assay"],
        annotations=[(BQB.IS, "chmo/CHMO:0001253")],
    ),
    Method(
        sid="lc-uv",
        name="LC/UV",
        label="LC/UV",
        description="A LC-UV system is a device system that has a liquid chromatograph and an ultra-violet "
        "detector component.",
        parents=["uv-spectrophotometry"],
        annotations=[],
    ),
    Method(
        sid="gc",
        name="GC",
        label="Gas chromatography",
        description="Gas chromatography. An analytical technique in that combines the physical separation capabilities "
        "of gas chromatography (GC) with the mass analysis capabilities of mass spectrometry (MS). "
        "Molecular mixtures are initially vaporized and separated into components by GC. "
        "As these components exit the column, they are subjected to mass spectrometry for "
        "identification based on their mass-to-charge ratio and behavior in a magnetic field.",
        parents=["chromatography"],
        annotations=[(BQB.IS, "omit/0009469"), (BQB.IS, "chmo/CHMO:0000497")],
    ),
    Method(
        sid="gas-lc",
        name="G-L C",
        label="Gas-liquid chromatography (GLC)",
        description="Gas-liquid chromatography (GLC) is gas chromatography method where the stationary phase is a liquid.",
        parents=["gc"],
        annotations=[(BQB.IS, "chmo/CHMO:0001016")],
    ),
    Method(
        sid="cgc",
        name="CGC",
        label="Capillary gas chromatography",
        description="Capillary gas chromatography",
        parents=["gc"],
        annotations=[
            (BQB.IS, "fix/FIX:0000922"),
        ],
    ),
    Method(
        sid="gc-ms",
        name="GC/MS",
        label="Gas chromatography mass spectrometry (GC/MS)",
        description="Gas chromatography mass spectrometry. An analytical technique "
        "wherein gas chromatography is coupled to mass spectrometry in order "
        "to separate, identify, and quantify substances in a sample.",
        parents=["gc", "ms"],
        annotations=[
            (BQB.IS, "ncit/C111203"),
        ],
    ),
    Method(
        sid="scintillation-counting",
        name="scintillation counting",
        label="scintillation counting",
        description="It involves the incorporation of radiolabeled precursors into "
        "uniform distribution with a liquid medium capable of converting "
        "the kinetic energy of nuclear emissions into light energy. "
        "A scintillation counter is used to measure ionizing radiation.",
        parents=["assay"],
        annotations=[
            # (BQB.IS, "bao/0000405"),
            (BQB.IS, "omit/0013490"),
        ],
    ),
    Method(
        sid="fpia",
        name="FPIA",
        label="fluorescence polarization immunoassay",
        description=" ",
        parents=["assay"],
        annotations=[],
        synonyms=[],
    ),
]
