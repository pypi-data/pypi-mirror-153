"""
Substance information.
"""
from pkdb_data.management.info_node import Substance
from pkdb_data.metadata.annotation import BQB


SUBSTANCE_NODES = [
    Substance(
        sid="placebo",
        description="An inactive substance, treatment or procedure that is intended "
        "to provide baseline measurements for the experimental protocol of "
        "a clinical trial. A placebo is a substance or treatment which "
        "is designed to have no therapeutic value. Common placebos "
        "include inert tablets (like sugar pills), inert injections "
        "(like saline), sham surgery, and other procedures.",
        annotations=[
            (BQB.IS, "ncit/C753"),
            (BQB.IS, "efo/0001674"),
        ],
    ),
    Substance(
        sid="nr-substance",
        label="Not reported (substance)",
        name="NR",
        description="Substance was not reported.",
        annotations=[],
    ),
    Substance(
        sid="beta-blocker",
        description="Beta-blocker are a class of medications that are predominantly "
        "used to manage abnormal heart rhythms, and to protect the heart "
        "from a second heart attack (myocardial infarction) after a first "
        "heart attack (secondary prevention).",
        annotations=[],
    ),
    Substance(
        sid="atazanavir",
        description="An aza-dipeptide analogue with a bis-aryl substituent on the "
        "(hydroxethyl)hydrazine moiety with activity against both wild "
        "type and mutant forms of HIV protease. Atazanavir does not "
        "elevate serum lipids, a common problem with other protease "
        "inhibitors.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:37924"),
            (BQB.IS, "ncit/C66872"),
        ],
        synonyms=["Atazanavir"],
    ),
    Substance(
        sid="buspirone",
        description="Buspirone, sold under the brand name Buspar among others, is a "
        "medication primarily used to treat anxiety disorders, "
        "particularly generalized anxiety disorder. An anxiolytic agent "
        "chemically and pharmacologically unrelated to benzodiazepines, "
        "barbiturates, or other sedative/hypnotic drugs.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:3223"),
            (BQB.IS, "ncit/C62013"),
        ],
        synonyms=["Buspirone"],
    ),
    Substance(
        sid="ezetimibe",
        description="An azetidinone derivative and a cholesterol absorption inhibitor "
        "with lipid-lowering activity. Ezetimibe appears to interact "
        "physically with cholesterol transporters at the brush border of "
        "the small intestine and inhibits the intestinal absorption of "
        "cholesterol and related phytosterols. As a result, ezetimibe "
        "causes a decrease in the level of blood cholesterol or an "
        "increase in the clearance of cholesterol from the bloodstream.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:49040"),
            (BQB.IS, "ncit/C47529"),
        ],
        synonyms=["Ezetimibe"],
    ),
    Substance(
        sid="dapagliflozin",
        description="Dapagliflozin. A selective sodium-glucose co-transporter subtype "
        "2 (SGLT2) inhibitor with antihyperglycemic activity. "
        "Dapagliflozin selectively and potently inhibits SGLT2 compared "
        "to SGLT1, which is the cotransporter of glucose in the gut.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:85078"),
            (BQB.IS, "ncit/C78126"),
        ],
        synonyms=["Dapagliflozin"],
    ),
    Substance(
        sid="dapagliflozin-3-o-glucuronide",
        name="dapagliflozin 3-o-glucuronide",
        description="Dapagliflozin 3-O-glucuronide. A metabolite of Dapagliflozin.",
        mass=585,
        formula="C27H33ClO12",
        annotations=[
            (BQB.IS, "pubchem.substance/91617971"),
            (BQB.IS, "inchikey/ZYZULHSUKTZGTR-PTNNFGGUSA-N"),
        ],
        synonyms=["Dapagliflozin M-15 metabolite"],
    ),
    Substance(
        sid="dapagliflozin-2-o-glucuronide",
        name="dapagliflozin 2-o-glucuronide",
        description="Dapagliflozin 2-O-glucuronide. A metabolite of Dapagliflozin.",
    ),
    Substance(
        sid="raltegravir",
        description="Raltegravir. A small molecule with activity against human "
        "immunodeficiency virus (HIV). Raltegravir is an integrase "
        "inhibitor that blocks the integration of the viral genome into "
        "the host DNA, a critical step in the pathogenesis of HIV.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:82960"),
            (BQB.IS, "ncit/C72837"),
        ],
        synonyms=["Raltegravir"],
    ),
    Substance(
        sid="coffee",
        description="Coffee is a brewed drink prepared from roasted coffee beans, "
        "the seeds of berries from certain Coffea species.",
        annotations=[(BQB.IS, "omit/0004379")],
    ),
    Substance(
        sid="tea",
        description="Tea is an aromatic beverage commonly prepared by pouring hot or "
        "boiling water over cured or fresh leaves of the Camellia "
        "sinensis, an evergreen shrub (bush) native to East Asia.",
        annotations=[
            (BQB.IS, "omit/0014519"),
        ],
    ),
    Substance(
        sid="green tea",
        description="Tea derived from the dried leaves of the plant Camellia sinensis "
        "with potential antioxidant, chemopreventive, and lipid-lowering "
        "activities. Green tea contains polyphenols that are believed to "
        "be responsible for its chemopreventive effect. The polyphenol "
        "fraction contains mainly Epigallocatechin-3-gallate (EGCG) and "
        "other catechins, such as epicatechin (EC), gallocatechin gallate "
        "(GCG), epigallocatechin (EGC), and epicatechin gallate (ECG).",
        annotations=[
            (BQB.IS, "ncit/C67048"),
        ],
    ),
    Substance(
        sid="kola-nuts",
        name="kola nuts",
        description="Seeds used for infusions or hot drinks of the plant classified "
        "under the species Cola",
    ),
    Substance(
        sid="nicotine",
        description="A plant alkaloid, found in the tobacco plant, and addictive "
        "central nervous system (CNS) stimulant that causes either "
        "ganglionic stimulation in low doses or ganglionic blockage in "
        "high doses. Nicotine acts as an agonist at the nicotinic "
        "cholinergic receptors in the autonomic ganglia, at neuromuscular "
        "junctions, and in the adrenal medulla and the brain.",
        annotations=[
            (BQB.IS, "ncit/C691"),
            (BQB.IS, "chebi/CHEBI:18723"),
        ],
    ),
    Substance(
        sid="cocoa",
        description="The powdered form of cocoa bean solids remaining after cocoa "
        "butter, the fat component, is extracted from chocolate liquor, "
        "roasted cocoa beans that have been ground into a liquid state.",
    ),
    Substance(
        sid="coke",
        description="Coca-Cola, or Coke, is a carbonated soft drink manufactured by "
        "The Coca-Cola Company.",
        synonyms=["coca cola", "Coca-Cola"],
    ),
    Substance(
        sid="chocolate",
        description="NChocolate is a preparation of roasted and ground cacao seeds "
        "that is made in the form of a liquid, paste, or in a block, "
        "which may also be used as a flavoring ingredient in other foods.",
        annotations=[(BQB.IS, "ncit/C68655")],
    ),
    Substance(
        sid="curcuminoids",
        description="A curcuminoid is a linear diarylheptanoid, with molecules such "
        "as curcumin or derivatives of curcumin with different chemical "
        "groups that have been formed to increase solubility of curcumins "
        "and make them suitable for drug formulation. These compounds are "
        "natural phenols and produce a pronounced yellow color.",
        annotations=[
            (BQB.IS, "ncit/C125480"),
        ],
    ),
    Substance(
        sid="grapefruit",
        name="grapefruit",
        description="The sour to semi-sweet fruit of Citrus x paradisi. Grapefruit "
        "can have interactions with drugs, often increasing the effective "
        "potency of compounds. See also 'grapefruit juice'.",
        annotations=[
            (BQB.IS, "ncit/C71974"),
        ],
    ),
    Substance(
        sid="grapefruit-juice",
        name="grapefruit juice",
        description="Grapefruit juice is the juice from grapefruits. It is rich in "
        "vitamin C and ranges from sweet-tart to very sour. Grapefruit "
        "juice is important in medicine because of its interactions "
        "with many common drugs including caffeine and medications.",
        annotations=[
            (BQB.IS, "ncit/C71961"),
        ],
    ),
    Substance(
        sid="watercress",
        description="Watercress or yellowcress is a species of aquatic flowering plant "
        "in the cabbage family Brassicaceae. Its botanical name is "
        "Nasturtium officinale.",
        annotations=[(BQB.IS, "ncit/C75666")],
        synonyms=["Nasturtium officinale"],
    ),
    Substance(
        sid="cabbage",
        description="Cabbage (comprising several cultivars of Brassica oleracea) is a "
        "leafy green, red (purple), or white (pale green) biennial plant "
        "grown as an annual vegetable crop for its dense-leaved heads.",
        annotations=[
            (BQB.IS, "ncit/C71999"),
        ],
    ),
    Substance(
        sid="brussel-sprouts",
        name="brussel sprouts",
        description="The Brussels sprout is a member of the Gemmifera Group of "
        "cabbages (Brassica oleracea), "
        "grown for its edible buds.",
        annotations=[
            (BQB.IS, "taxonomy/657506"),
        ],
        parents=["cabbage"],
    ),
    Substance(
        sid="pomegranate juice",
        name="pomegranate-juice",
        description="A natural juice isolated from the fruit of the plant Punica "
        "granatum with antioxidant, potential antineoplastic, and "
        "chemopreventive activities.",
        annotations=[
            (BQB.IS, "ncit/C26665"),
            (BQB.IS_VERSION_OF, "ncit/C73929"),
        ],
    ),
    Substance(
        sid="methacetin",
        description="A member of the class of acetamides that is paracetamol in which "
        "the hydrogen of phenolic "
        "hydroxy group has been replaced by a methyl group.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:139354"),
        ],
    ),
    Substance(
        sid="13cmet",
        name="13C-methacetin",
        description="A (13)C-modified compound that is methacetin which has (13)C as "
        "the predominant isotope of the methoxy carbon. In normal "
        "subjects, methacetin is rapidly metabolised in the liver, being "
        "dealkylated by hepatic CYP1A2 to give paracetamol (acetaminophen),"
        " the methyl of the methoxy group is eliminated as CO2.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:139355"),
        ],
    ),
    Substance(
        sid="co2",
        name="carbon dioxide",
        description="A colorless, odorless, incombustible gas resulting from the oxidation of carbon."
        "A one-carbon compound with formula CO2 in which the carbon is attached to each oxygen atom "
        "by a double bond. A colourless, odourless gas under normal conditions, it is produced during "
        "respiration by all animals, fungi and microorganisms that depend directly or indirectly on "
        "living or decaying plants for food.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:16526"),
            (BQB.IS, "ncit/C65288"),
        ],
    ),
    Substance(
        sid="13cco2",
        name="13C-co2",
        label="13C-carbon dioxide",
        description="13C carbon dioxide is a (13)C-modified compound that is carbon dioxide in which the carbon "
        "is present as its (13)C isotope. It has a role as a diagnostic agent.",
        annotations=[(BQB.IS, "chebi/CHEBI:139538")],
        synonyms=["13C-hydrogencarbonate"],
    ),
    Substance(
        sid="14cco2",
        name="14C-co2",
        label="14C carbon dioxide",
        description="14C carbon dioxide is a (14)C-modified compound that is carbon dioxide in which the carbon "
        "is present as its (14)C isotope. It has a role as a diagnostic agent.",
        synonyms=["14C-hydrogencarbonate"],
    ),
    # cholesterol and triglycerides
    # --------------------------------
    Substance(
        sid="triglyceride",
        description="Fats composed of three fatty acid chains linked to a "
        "glycerol molecule.",
        synonyms=["triglycerides"],
        annotations=[
            (BQB.IS, "ncit/C906"),
            (BQB.IS, "omit/0015118"),
            (BQB.IS, "chebi/CHEBI:17855"),
        ],
    ),
    Substance(
        sid="cholesterol",
        description="Total cholesterol",
        synonyms=["Total cholesterol"],
        annotations=[
            (BQB.IS, "chebi/CHEBI:16113"),
            (BQB.IS, "ncit/C369"),
        ],
    ),
    Substance(
        sid="c-reactive-protein",
        name="CRP",
        description="c-reactive-protein",
        synonyms=["CRP"],
        annotations=[],
    ),
    Substance(
        sid="apolipoprotein A-I",
        name="apoA-I",
        synonyms=["APOA1"],
        description="Apolipoprotein A-I (267 aa, ~31 kDa) is encoded by the human APOA1 gene."
        "This protein is involved in the transport and metabolism of cholesterol. "
        "Participates in the reverse transport of cholesterol from tissues to the liver for "
        "excretion by promoting cholesterol efflux from tissues and by acting as a cofactor for "
        "the lecithin cholesterol acyltransferase (LCAT). As part of the SPAP complex, "
        "activates spermatozoa motility.",
        annotations=[
            (BQB.IS, "ncit/C116419"),
            (BQB.IS, "uniprot/P02647"),
        ],
    ),
    Substance(
        sid="apolipoprotein A-II",
        name="apoA-II",
        synonyms=["APOA2"],
        description="May stabilize HDL (high density lipoprotein) structure by its association"
        "with lipids, and affect the HDL metabolism.",
        annotations=[
            (BQB.IS, "uniprot/P02652"),
        ],
    ),
    Substance(
        sid="apolipoprotein B-100",
        name="apoB-100",
        description="Apolipoprotein B is a major protein constituent of chylomicrons "
        "(apo B-48), LDL (apo B-100) and VLDL (apo B-100). Apo B-100 functions as a"
        "recognition signal for the cellular binding and internalization of LDL particles by "
        "the apoB/E receptor.",
        annotations=[
            (BQB.IS, "ncit/C106032"),
            (BQB.IS, "uniprot/P04114"),
        ],
    ),
    Substance(
        sid="apolipoprotein B100+B48",
        name="apoB100+48",
        synonyms=["APOB", "apoB", "apo-B"],
        description="Apolipoprotein B100 and B48 come from the same gene, while B48"
        "is truncated; some immunological assays may quantify the sum (FlorBar)",
        annotations=[],
    ),
    Substance(
        sid="apolipoprotein E",
        name="apoE",
        synonyms=["APOE"],
        description="Apolipoprotein E (317 aa, ~36 kDa) is encoded by the human APOE gene. "
        "This protein is involved in lipid metabolism and transport.",
        annotations=[
            (BQB.IS, "ncit/C84470"),
            (BQB.IS, "uniprot/Q8TCZ8"),
        ],
    ),
    Substance(
        sid="lipoprotein A-I",
        name="Lp-A-I",
        synonyms=["LPA1"],
    ),
    Substance(
        sid="lipoprotein A-I:A-II",
        name="Lp-A-I:A-II",
        synonyms=["LPA1:A2"],
    ),
    Substance(
        sid="idrocilamide",
        name="idrocilamide",
        description="This compound belongs to the class of organic compounds known as "
        "cinnamic acid amides. These are amides of cinnamic acids. "
        "Cinnamic acid is an aromatic compound containing a benzene and "
        "a carboxylic acid group forming 3-phenylprop-2-enoic acid.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:134842"),
            (BQB.IS, "inchikey/OSCTXCOERRNGLW-VOTSOKGWSA-N"),
        ],
    ),
    Substance(
        sid="ldlc",
        name="ldl-c",
        label="LDL cholesterol",
        description="low density lipoprotein cholesterol. Cholesterol esters "
        "and free cholesterol which are contained in or bound to "
        "low-density lipoproteins (LDL).",
        synonyms=["LDL-Cholesterin", "LDL cholesterol"],
        annotations=[
            (BQB.IS, "efo/0004195"),
            (BQB.IS, "chebi/CHEBI:47774"),
        ],
    ),
    Substance(
        sid="ldl",
        name="ldl",
        description="A class of lipoproteins of small size (18-25 nm) and low density (1.019-1.063 g/ml) particles with a core composed mainly of cholesterol esters and smaller amounts of triglycerides. The surface monolayer consists mostly of phospholipids, a single copy of apolipoprotein B-100, and free cholesterol molecules. The main function of LDL is to transport cholesterol and cholesterol esters from the liver. Excessive levels are associated with cardiovascular disease.",
        annotations=[
            (BQB.IS, "omit/0009160"),
            (BQB.IS, "chebi/CHEBI:39026"),
        ],
    ),
    Substance(
        sid="ldl1",
        name="ldl1",
        description="ldl subfraction based on density measurements"
        "density interval: LDL-1, 1.020-1.024 g/mL",
        parents=["ldl"],
    ),
    Substance(
        sid="ldl2",
        name="ldl2",
        description="ldl subfraction based on density measurements"
        "density interval: LDL-2, 1.025±1.029 g/mL",
        parents=["ldl"],
    ),
    Substance(
        sid="ldl3",
        name="ldl3",
        description="ldl subfraction based on density measurements"
        "density interval: LDL-3, 1.030±1.034 g/mL",
        parents=["ldl"],
    ),
    Substance(
        sid="ldl4",
        name="ldl4",
        description="ldl subfraction based on density measurements"
        "density interval: LDL-4, 1.035±1.040 g/mL",
        parents=["ldl"],
    ),
    Substance(
        sid="ldl5",
        name="ldl5",
        description="ldl subfraction based on density measurements"
        "density interval: LDL-5, 1.041±1.047 g/mL",
        parents=["ldl"],
    ),
    Substance(
        sid="ldl6",
        name="ldl6",
        description="ldl subfraction based on density measurements"
        "density interval: LDL-6, 1.048±1.057 g/mL",
        parents=["ldl"],
    ),
    Substance(
        sid="ldl7",
        name="ldl7",
        description="ldl subfraction based on density measurements"
        "density interval: LDL-7, 1.058±1.066 g/mL",
        parents=["ldl"],
    ),
    Substance(
        sid="large-buoyant-ldl",
        name="large-buoyant-ldl",
        description="ldl1 and ldl2" "density interval: 1.020±1.029 g/mL",
        parents=["ldl1", "ldl2"],
    ),
    Substance(
        sid="intermediate-buoyant-ldl",
        name="intermediate-buoyant-ldl",
        description="ldl3 and ldl4" "density interval: 1.030±1.040 g/mL",
        parents=["ldl3", "ldl4"],
    ),
    Substance(
        sid="small-buoyant-ldl",
        name="small-buoyant-ldl",
        description="ldl5, ldl6 and ldl7" "density interval: 1.041±1.066 g/mL",
        parents=["ldl5", "ldl6", "ldl7"],
    ),
    Substance(
        sid="hdlc",
        name="hdl-c",
        label="HDL cholesterol",
        description="high density lipoprotein cholesterol. Cholesterol esters "
        "and free cholesterol which are contained in or bound to "
        "high-density lipoproteins (HDL).",
        synonyms=["HDL-Cholesterin", "HDL cholesterol"],
        annotations=[
            (BQB.IS, "omit/0009159"),
            (BQB.IS, "chebi/CHEBI:47775"),
        ],
    ),
    Substance(
        sid="non-hdlc",
        name="non-hdl-c",
        label="non-HDL cholesterol",
        description="determining the amount of lipoprotein and cholesterol which"
        "is not hdl-c",
        parents=["hdlc"],
    ),
    Substance(
        sid="hdl",
        name="hdl",
        description="A class of lipoproteins of small size (4-13 nm) and dense (greater than 1.063 g/ml) particles. They are synthesized in the liver without a lipid core, accumulate cholesterol esters from peripheral tissues and transport them to the liver for re-utilization or elimination from the body (the reverse cholesterol transport).",
        annotations=[
            (BQB.IS, "chebi/CHEBI:39025"),
            (BQB.IS, "omit/0009158"),
        ],
    ),
    Substance(
        sid="hdl2-c",
        name="hdl2-c",
        description="class of HDL-cholesterol; subfraction of HDL-cholesterol based on density into the large buoyant HDL2-c",
        parents=["hdlc"],
        annotations=[],
    ),
    Substance(
        sid="hdl3-c",
        name="hdl3-c",
        description="class of HDL-cholesterol; subfraction of HDL-cholesterol based on density into the small dense HDL3-c",
        parents=["hdlc"],
        annotations=[],
    ),
    Substance(
        sid="vldlc",
        name="vldl-c",
        label="VLDL cholesterol",
        description="VLDL - very low density lipoprotein cholesterol. "
        "Cholesterol esters and free cholesterol which are "
        "contained in or bound to very low density lipoproteins "
        "(VLDL).",
        synonyms=["VLDL cholesterol"],
        annotations=[
            (BQB.IS, "omit/0016033"),
            (BQB.IS, "chebi/CHEBI:47773"),
        ],
    ),
    Substance(
        sid="vldl",
        name="vldl",
        description="VLDL - very low density lipoproteins (consisting of cholesterol and lipoproteins).",
        synonyms=["VLDL"],
        annotations=[
            (BQB.HAS_PART, "omit/0009162"),
            (BQB.HAS_PART, "omit/0016033"),
        ],
    ),
    Substance(
        sid="vldlc/triglyeride",
        name="vldl-c/triglyceride",
        description="ratio of VLDL-cholesterol and triglycerides",
        parents=["vldlc", "triglyceride"],
    ),
    Substance(
        sid="ldl/hdl-c",
        name="ldl/hdl-c",
        description="ratio of LDL-cholesterol and HDL-cholesterol",
        parents=["ldlc", "hdlc"],
    ),
    Substance(
        sid="total/hdl-c",
        name="total/hdl-c",
        description="ratio of total cholesterol and HDL-cholesterol",
        parents=["cholesterol", "hdlc"],
    ),
    Substance(
        sid="ldl-esterified/free-cholesterol",
        name="ldl-esterified/free-cholesterol",
        description="ratio of esterified LDL-cholesterol and free-cholesterol",
        parents=["ldlc", "cholesterol"],
    ),
    Substance(
        sid="ldl-triglyeride",
        name="ldl triglyceride",
        description="fraction of triglycerides in the LDL particle",
        parents=["ldl", "triglyceride"],
    ),
    Substance(
        sid="vldl-triglyeride",
        name="vldl triglyceride",
        description="fraction of triglycerides in the VLDL particle",
        parents=["vldl", "triglyceride"],
    ),
    Substance(
        sid="hdl-triglyeride",
        name="hdl triglyceride",
        description="fraction of triglycerides in the HDL particle",
        parents=["hdl", "triglyceride"],
    ),
    Substance(
        sid="vldl-apoB100+48",
        name="vldl-apoB100+48",
        description="fraction of apoB100+48 in the VLDL particle",
        parents=["VLDL", "apolipoprotein B100+B48"],
    ),
    Substance(
        sid="ldl-apoB100+48",
        name="ldl-apoB100+48",
        description="fraction of apoB100+48 in the LDL particle",
        parents=["LDL", "apolipoprotein B100+B48"],
    ),
    Substance(
        sid="phospholipids",
        description="A lipid containing phosphoric acid as a mono- or di-ester. "
        "The term encompasses phosphatidic acids and phosphoglycerides.",
        synonyms=[],
        annotations=[
            (BQB.IS, "chebi/CHEBI:16247"),
        ],
    ),
    # ------------------
    Substance(
        sid="haemoglobin",
        description="A protein composed of four globin chains and heme that gives red blood cells their "
        "characteristic color; its function is primarily to transport oxygen.",
        annotations=[
            (BQB.IS, "fma/FMA:62293"),
        ],
        synonyms=["human haemoglobin", "hemoglobin"],
    ),
    Substance(
        sid="fructosamine",
        description="Fructosamine, the compound that results from glycation reactions between a sugar and a primary "
        "amine, followed by isomerization via the Amadori rearrangement.",
        annotations=[(BQB.IS, "chebi/CHEBI:24103")],
    ),
    Substance(
        sid="hba1c",
        label="glycosylated hemoglobin (HbA1c)",
        description="Glycated hemoglobin (HbA1c) is a form of hemoglobin (Hb) that is chemically linked to a sugar. "
        "The formation of the sugar-Hb linkage indicates the presence of excessive sugar in the "
        "bloodstream, often indicative of diabetes.",
        synonyms=[
            "glycosylated hemoglobin",
            "glycated hemoglobin",
            "HbA1c",
            "hemoglobin A1c",
            "A1c",
        ],
    ),
    Substance(
        sid="creatinine",
        description="Creatinine. The breakdown product of creatine, a constituent of muscle tissue, that "
        "is excreted by the kidney and whose serum level is used to evaluate kidney function.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:16737"),
            (BQB.IS, "ncit/C399"),
        ],
    ),
    Substance(
        sid="creatine-kinase",
        name="creatine kinase",
        description="An enzyme complex that can reversibly convert ATP and creatine to phosphocreatine and ADP. Cytosolic creatine kinases are comprised of homodimers or heterodimers of creatine kinase B-type protein and creatine kinase M-type protein. Mitochondrial creatine kinases are octomers comprised of either four homodimers of creatine kinase U-type, mitochondrial protein or four creatine kinase S-type, mitochondrial protein homodimers.",
        annotations=[
            (BQB.IS, "ncit/C113245"),
        ],
    ),
    Substance(
        sid="urea",
        description="A nitrogenous compound containing a carbonyl group attached to two amine groups with osmotic "
        "diuretic activity. In vivo, urea is formed in the liver via the urea cycle from ammonia and is "
        "the final end product of protein metabolism.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:16199"),
            (BQB.IS, "ncit/C29531"),
        ],
    ),
    Substance(
        sid="uric-acid",
        name="uric acid",
        description="A white tasteless odorless crystalline product of protein metabolism, found in the blood and "
        "urine, as well as trace amounts found in the various organs of the body. It can build up and "
        "form stones or crystals in various disease states.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:27226"),
            (BQB.IS, "ncit/C62652"),
        ],
    ),
    Substance(
        sid="h2o",
        name="h2o",
        label="water",
        description="H2O. An oxygen hydride consisting of an oxygen atom that is covalently bonded to two hydrogen atoms.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:15377"),
        ],
        synonyms=["water"],
    ),
    Substance(
        sid="sodium",
        description="Sodium. An element with atomic symbol Na, atomic number 11, and atomic weight 23.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:26708"),
            (BQB.IS, "ncit/C830"),
        ],
        synonyms=["Na"],
    ),
    Substance(
        sid="calcium",
        description="Calcium. An element with atomic symbol Ca, atomic number 20, and atomic weight 40.08.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:22984"),
            (BQB.IS, "ncit/C331"),
        ],
        synonyms=["Ca", "Ca2"],
    ),
    Substance(
        sid="potassium",
        description="Potassium. An element with atomic symbol K, atomic number 19, and atomic weight 39.10.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:26216"),
            (BQB.IS, "ncit/C765"),
        ],
        synonyms=["K"],
    ),
    Substance(
        sid="chloride",
        description="Chloride. A halide anion formed when chlorine picks up an electron to form an an anion.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:17996"),
        ],
        synonyms=["Cl"],
    ),
    Substance(
        sid="phosphate",
        description="Phosphate (3-). A phosphate ion that is the conjugate base of hydrogenphosphate.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:18367"),
        ],
    ),
    Substance(
        sid="albumin",
        description="Albumin. A family of globular proteins found in many plant and animal tissues that tend to bind "
        "a wide variety of ligands. Albumin is the main protein in blood plasma. Low serum levels occur "
        "in conditions associated with malnutrition, inflammation and liver and kidney diseases.",
        annotations=[
            (BQB.IS, "ncit/C214"),
            (BQB.IS, "uniprot/P02768"),
        ],
        mass="66437",  # (Sigma-Aldrich); 69,367 (uniprot)
    ),
    Substance(
        sid="bilirubin",
        description="Bilirubin. A dark orange, yellow pigment that is the product of the breakdown of iron in the "
        "blood; it is conjugated in the liver and excreted in the bile.",
        annotations=[
            (BQB.IS, "ncit/C305"),
            (BQB.IS, "chebi/CHEBI:16990"),
            (BQB.IS, "inchikey/BPYKTIZUTYGOLE-IFADSCNNSA-N"),
        ],
    ),
    Substance(
        sid="alp",
        label="Alkaline phosphatase (ALP)",
        description="Serum Alkaline phosphatase.",
        synonyms=["Afos", "Alkaline phosphatase"],
    ),
    Substance(
        sid="got",
        label="Glutamic oxaloacetic transaminase (GOT, SGOT)",
        description="Glutamic oxaloacetic transaminase (GOT, SGOT). "
        "Activity measured as a test of liver function, "
        "46/47-kDa homodimeric human Aspartate Aminotransferases "
        "(Class-I Pyridoxal-Phosphate-Dependent Aminotransferase Family) "
        "are pyridoxal phosphate-dependent enzymes involved in amino acid "
        "metabolism and in the urea and tricarboxylic acid cycles.",
        synonyms=["SGOT", "GOT"],
        annotations=[
            (BQB.IS, "ncit/C25202"),
        ],
        deprecated=True,
        # FIXME: duplicate entry ast & got, remove got and merge with AST
    ),
    Substance(
        sid="ast",
        label="Aspartate aminotransferase (AST)",
        description="Aspartate aminotransferase, also known as "
        "AspAT/ASAT/AAT or (serum) "
        "glutamic oxaloacetic transaminase (GOT, SGOT).",
        synonyms=["AST"],
        annotations=[
            (BQB.IS, "ncit/C64467"),
        ],
    ),
    Substance(
        sid="ggt",
        name="ggt",
        label="Gamma glutamate transaminase (GGT)",
        description="Gamma glutamate transaminase.",
        synonyms=["GGT", "g-Gt"],
        annotations=[
            (BQB.IS, "ncit/C64467"),
        ],
    ),
    Substance(
        sid="alt",
        name="alt",
        label="Alanine aminotransferase (ALT)",
        description="Alanine aminotransferase, formerly called serum "
        "glutamate-pyruvate transaminase (SGPT) or "
        "serum glutamic-pyruvic transaminase (SGPT). "
        "Serum ALT level, serum AST (aspartate transaminase) "
        "level, and their ratio (AST/ALT ratio) are commonly "
        "measured clinically as biomarkers for liver health.",
        synonyms=["ALT"],
        annotations=[
            (BQB.IS, "ncit/C64433"),
        ],
    ),
    Substance(
        sid="ldh",
        name="ldh",
        label="Lacate dehydrogenase (LDH)",
        description="Lactate dehydrogenase (LDH). A family of "
        "homotetrameric cytoplasmic enzymes involved in the "
        "conversion of L-lactate and NAD to pyruvate and "
        "NADH in the final step of anaerobic glycolysis.",
        synonyms=["LDH"],
        annotations=[
            (BQB.IS, "ncit/C25184"),
        ],
    ),
    Substance(
        sid="metformin",
        description="An agent belonging to the biguanide class of antidiabetics with antihyperglycemic activity. "
        "Metformin is associated with a very low incidence of lactic acidosis.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:6801"),
            (BQB.IS, "ncit/C61612"),
        ],
    ),
    Substance(
        sid="glipizide",
        description="A short-acting, second-generation sulfonylurea with hypoglycemic activity. Glipizide is "
        "rapidly absorbed, has a very quick onset of action and a short half-life. This agent is "
        "extensively metabolized in the liver and the metabolites as well as the unchanged form are "
        "excreted in the urine.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:5384"),
            (BQB.IS, "ncit/C29074"),
        ],
    ),
    Substance(
        sid="hydrochlorothiazide",
        description="Hydrochlorothiazide (HCTZ or HCT) is a diuretic medication often used to treat high "
        "blood pressure and swelling due to fluid build up.",
        annotations=[
            (BQB.IS, "ncit/C29098"),
            (BQB.IS, "chebi/CHEBI:5778"),
        ],
    ),
    Substance(
        sid="icg",
        name="indocyanine green",
        description="Indocyanine green (ICG) is a cyanine dye used in medical diagnostics. It is used for determining "
        "cardiac output, hepatic function, liver and gastric blood flow, and for ophthalmic angiography.",
        annotations=[
            (BQB.IS, "inchikey/MOFVSTNWEDAEEK-UHFFFAOYSA-M"),
            (BQB.IS, "chebi/CHEBI:31696"),
            (BQB.IS, "ncit/C65913"),
        ],
    ),
    Substance(
        sid="glycocholic acid",
        name="glycocholic acid",
        description="A bile acid glycine conjugate having cholic acid as the bile acid component.",
        annotations=[(BQB.IS, "chebi/CHEBI:17687")],
    ),
    Substance(
        sid="[14C]glycocholic acid",
        name="[14C]glycocholic acid",
        description="A bile acid glycine conjugate having cholic acid as the bile acid component.",
        annotations=[(BQB.IS_VERSION_OF, "chebi/CHEBI:17687")],
    ),
    Substance(
        sid="ergotamine",
        description="A naturally occurring ergot alkaloid with vasoconstrictor and analgesic property.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:64318"),
            (BQB.IS, "ncit/C61751"),
        ],
    ),
    Substance(
        sid="bile",
        description="Fluid composed of waste products, bile acids, salts, cholesterol, and electrolytes. "
        "It is secreted by the liver parenchyma and stored in the gallbladder.",
        annotations=[(BQB.IS, "ncit/C13192")],
        deprecated=True,
        # FIXME: remove; this is a tissue, not a substance, probably incorrect encoding
    ),
    Substance(
        sid="fentanyl",
        description="A synthetic, lipophilic phenylpiperidine opioid agonist with analgesic and anesthetic properties. "
        "Fentanyl selectively binds to and activates the mu-receptor in the central nervous system (CNS) "
        "thereby mimicking the effects of endogenous opiates.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:310077"),
            (BQB.IS, "ncit/C494"),
        ],
    ),
    Substance(
        sid="galactose",
        description="Galactose is a monosaccharide sugar that is about as sweet as glucose.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:28260"),
            (BQB.IS, "ncit/C68482"),
        ],
    ),
    Substance(
        sid="lidocaine",
        description="A synthetic aminoethylamide with local anesthetic and antiarrhythmic properties. "
        "Lidocaine stabilizes the neuronal membrane by binding to and inhibiting voltage-gated sodium "
        "channels, thereby inhibiting the ionic fluxes required for the initiation and conduction of "
        "impulses and effecting local anesthesia.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:6456"),
            (BQB.IS, "ncit/C614"),
        ],
        synonyms=["lignocaine"],
    ),
    Substance(
        sid="enflurane",
        description="A fluorinated ether and very potent and stable general anaesthetic agent. "
        "The mechanism through which enflurane exerts its effect is not clear, "
        "it probably acts on nerve cell membranes to disrupt neuronal transmission in "
        "the brain, probably via an action at the lipid matrix of the neuronal membrane.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:4792"),
            (BQB.IS, "ncit/C47511"),
        ],
    ),
    Substance(
        sid="vecuronium-bromide",
        name="vecuronium bromide",
        description="The bromide salt form of vecuronium, a synthetic steroid derivative of the naturally "
        "occurring alkaloids of curare with a muscle relaxant property.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:9940"),
            (BQB.IS, "ncit/C47782"),
        ],
    ),
    Substance(
        sid="etomidate",
        description="An imidazole derivative with short-acting sedative, hypnotic, and general "
        "anesthetic properties. Etomidate appears to have gamma-aminobutyric acid "
        "(GABA) like effects, mediated through GABA-A receptor.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:4910"),
            (BQB.IS, "ncit/C47527"),
        ],
    ),
    Substance(
        sid="isoflurane",
        description="A fluorinated ether with general anesthetic and muscle relaxant activities. "
        "Although the exact mechanism of action has not been established, inhaled "
        "isoflurane, appears to act on the lipid matrix of the neuronal cell membrane, "
        "which results in disruption of neuronal transmission.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:6015"),
            (BQB.IS, "ncit/C65978"),
        ],
    ),
    Substance(
        sid="succinylcholine",
        description="A quaternary ammonium compound and depolarizing agent with short-term muscle "
        "relaxant properties. Succinylcholine binds to nicotinic receptors at the "
        "neuromuscular junction and opening the ligand-gated channels in the same way "
        "as acetylcholine, resulting in depolarization and inhibition of neuromuscular transmission.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:45652"),
            (BQB.IS, "ncit/C61955"),
        ],
    ),
    Substance(
        sid="estradiol",
        description="The most potent form of the naturally occurring steroid sex hormone in humans, "
        "produced by ovary, placenta, testis, and in small amount by adrenal cortex. "
        "Estradiol binds to a specific intracellular estrogen receptor located in "
        "female organs, breasts, hypothalamus and pituitary.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:23965"),
            (BQB.IS, "ncit/C2295"),
        ],
    ),
    Substance(
        sid="obeticholic acid",
        description="Obeticholic acid (OCA), is a semi-synthetic bile acid analogue which has the "
        "chemical structure 6α-ethyl-chenodeoxycholic acid. It is used as a medication "
        "used to treat primary biliary cholangitis.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:43602"),
        ],
        synonyms=["obeticholic acid", "OCA"],
    ),
    Substance(
        sid="progesterone",
        description="Produced in the corpus luteum and by the placenta, as an antagonist "
        "of estrogens. Promotes proliferation of uterine mucosa and the "
        "implantation of the blastocyst, prevents further follicular development.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:17026"),
            (BQB.IS, "ncit/C2297"),
        ],
    ),
    Substance(
        sid="isradipine",
        description="A dihydropyridine calcium channel blockers with antihypertensive and "
        "vasodilator activities. Isradipine blocks the calcium entry through "
        "the calcium ion channels of coronary and peripheral vascular smooth "
        "muscle, thereby dilating coronary arteries and peripheral arterioles.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:6073"),
            (BQB.IS, "ncit/C47577"),
        ],
    ),
    Substance(
        sid="phenobarbitone",
        label="phenobarbital",
        description="A long-acting barbituric acid derivative with antipsychotic property. "
        "Phenobarbital binds to and activates the gamma-aminobutyric acid "
        "(GABA)-A receptor, thereby mimicking the inhibitory actions of GABA in the brain.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:8069"),
            (BQB.IS, "ncit/C739"),
        ],
        synonyms=["phenobarbitol", "phenobarbital"],
    ),
    Substance(
        sid="evans-blue",
        name="evans blue",
        description="An organic sodium salt that is the tetrasodium salt of "
        "6,6'-{(3,3'-dimethyl[1,1'-biphenyl]-4,4'-diyl)bis[diazene-2,1-diyl]}bis(4-amino-5-hydroxynaphthalene-1,3-disulfonate). "
        "It is sometimes used as a counterstain, especially in fluorescent methods to suppress "
        "background autofluorescence.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:82467"),
            (BQB.IS, "ncit/C65605"),
        ],
    ),
    Substance(
        sid="mdma",
        name="MDMA",
        label="3,4-Methylenedioxymethamphetamine (MDMA)",
        description="3,4-Methylenedioxymethamphetamine is a ring-substituted "
        "amphetamine derivative, structurally related to the hallucinogen "
        "mescaline, with entactogenic, neurotoxic, and motor-stimulatory "
        "activities. 3,4-methylenedioxymethamphetamine (MDMA) produces an "
        "acute, rapid enhancement in both the release of serotonin from "
        "and the inhibition of serotonin reuptake by serotonergic nerve "
        "endings in the brain.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:1391"),
            (BQB.IS, "pubchem.compound/1615"),
        ],
        synonyms=[
            "3,4-Methylenedioxymethamphetamine",
            "Ecstasy",
            "Midomafetamine",
        ],
    ),
    # acetaminophen/paracetamol
    Substance(
        sid="apap",
        name="paracetamol",
        description="A p-aminophenol derivative with analgesic and antipyretic activities. Although the "
        "exact mechanism through which acetaminophen exert its effects has yet to be fully "
        "determined, acetaminophen may inhibit the nitric oxide (NO) pathway mediated by a "
        "variety of neurotransmitter receptors including N-methyl-D-aspartate (NMDA) "
        "and substance P, resulting in elevation of the pain threshold.",
        annotations=[(BQB.IS, "chebi/CHEBI:46195"), (BQB.IS, "ncit/C198")],
        synonyms=["acetaminophen", "APAP"],
    ),
    Substance(
        sid="panadol-extend",
        name="panadol extend",
        description="Panadol Extend (PEx) is an over-the-counter, modified-release formulation of paracetamol."
        "Each 665 mg tablet contains 69% slow-release and 31% immediate-release paracetamol.",
        deprecated=True,  # FIXME: merge with apap. This is a special release tablet.
    ),
    Substance(
        sid="apapglu",
        name="paracetamol glucuronide",
        description="Paracetamol glucuronide. A metabolite of paracetamol.",
        annotations=[(BQB.IS, "chebi/CHEBI:32636")],
        synonyms=[
            "acetaminophen O-β-D-glucosiduronic acid",
            "acetaminophen glucuronide",
        ],
    ),
    Substance(
        sid="apapsul",
        name="paracetamol sulfate",
        description="Paracetamol sulfate. A metabolite of paracetamol. An aryl sulfate that is paracetamol in which "
        "the hydroxy group has been replaced by a sulfooxy group.",
        annotations=[(BQB.IS, "chebi/CHEBI:32635")],
        synonyms=["4-acetaminophen sulfate"],
    ),
    Substance(
        sid="apapcys",
        name="paracetamol cysteine",
        description="Paracetamol cysteine. A metabolite of paracetamol.",
        annotations=[(BQB.IS, "chebi/CHEBI:133066")],
        synonyms=["S-(5-acetamido-2-hydroxyphenyl)cysteine", "acetaminophen cysteine"],
    ),
    Substance(
        sid="apapgsh",
        name="paracetamol glutathione",
        description="Paracetamol glutathione. A metabolite of paracetamol. Acetaminophen glutathione conjugate.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:32639"),
            (BQB.IS_VERSION_OF, "chebi/CHEBI:24337"),
        ],
        synonyms=["AA-GSH", "acetaminophen glutathione"],
    ),
    Substance(
        sid="apapmer",
        name="paracetamol mercapturate",
        description="Paracetamol mercapturate. A metabolite of paracetamol.",
        mass=296.34,
        formula="C13H16N2O4S",
        annotations=[
            (BQB.IS, "pubchem.compound/171471"),
            (BQB.IS, "inchikey/NTEYFNUDSXITGC-LBPRGKRZSA-N"),
        ],
        synonyms=["acetaminophen mercapturate"],
    ),
    Substance(
        sid="phenacetin",
        description="A synthetic, white crystalline solid that is slightly soluble in water and benzene, "
        "soluble in acetone and very soluble in pyrimidine. It is used in research as the "
        "preferred marker for detecting CYP1A2-based inhibition potential in vitro.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:8050"),
            (BQB.IS, "ncit/C44432"),
        ],
    ),
    Substance(
        sid="propacetamol",
        description="A water-soluble para-aminophenol derivative and ester prodrug of acetaminophen in which "
        "acetaminophen is bound to the carboxylic acid diethylglycine, with analgesic and antipyretic "
        "activities. Upon intravenous administration, propacetamol is hydrolyzed by plasma esterases "
        "into its active form acetaminophen.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:135089"),
            (BQB.IS, "ncit/C75081"),
        ],
        synonyms=["proparacetamol"],
    ),
    Substance(
        sid="propanolol",
        description="Propranolol, sold under the brand name Inderal among others, is a medication of the beta "
        "blocker class. It is used to treat high blood pressure, a number of types of irregular "
        "heart rate, thyrotoxicosis, capillary hemangiomas, performance anxiety, and essential tremors.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:8499"),
        ],
        synonyms=["Inderal"],
    ),
    Substance(
        sid="apap+apapsul+apapglu+apapcys+apapmer",
        description="Sum of paracetamol metabolites: apap+apapsul+apapglu+apapcys+apapmer",
        parents=["apap", "apapsul", "apapcys", "apapglu", "apapmer"],
    ),
    Substance(
        sid="apap+apapsul+apapglu+apapcys+apapmer+apapgsh",
        description="Sum of paracetamol metabolites: apap+apapsul+apapglu+apapcys+apapmer+apapgsh",
        parents=["apap", "apapsul", "apapcys", "apapglu", "apapmer", "apapgsh"],
    ),
    Substance(
        sid="apap+apapsul+apapglu+apapgsh",
        description="Sum of paracetamol metabolites: apap+apapsul+apapglu+apapgsh",
        parents=["apap", "apapsul", "apapglu", "apapgsh"],
    ),
    Substance(
        sid="apapcys+apapmer",
        description="Sum of paracetamol metabolites: paracetamol cysteine + paracetamol mercapturate",
        parents=["apapcys", "apapmer"],
    ),
    Substance(
        sid="apapsul+apapglu",
        description="Sum of paracetamol metabolites: paracetamol sulfate + paracetamol glucuronide",
        parents=["apapsul", "apapglu"],
    ),
    Substance(
        sid="apapcys+apapglu",
        description="Sum of paracetamol metabolites: paracetamol cysteine + paracetamol glucuronide",
        parents=["apapcys", "apapglu"],
    ),
    Substance(
        sid="diethyldithiocarbamic acid",
        description="diethyldithiocarbamic acid",
        annotations=[
            (BQB.IS, "chebi/CHEBI:8987"),
        ],
        synonyms=["Ditiocarb"],
    ),
    # caffeine (CYP2A1)
    Substance(
        sid="caffeine-citrate",
        name="caffeine citrate",
        description="Commercial citrate of caffeine, though not a definite salt. It is the alkaloid caffeine, "
        "with a portion of adherent citric acid, as indicated by its pharmacopoeial name "
        "(citrated caffeine). Its general action and uses are the same as those given under caffeine. "
        "Caffeine citrate is used chiefly as a remedy for the idiopathic headache (migraine). "
        "This salt is very soluble in water, and is assimilated much more readily than pure caffeine "
        "when taken into the stomach.",
        annotations=[
            (BQB.IS, "ncit/C1033"),
        ],
        synonyms=["citrated caffeine", "Cafcit"],
    ),
    Substance(
        sid="caffeine-monohydrate",
        name="caffeine monohydrate",
        description="Caffeine monohydrate.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:31332"),
            (BQB.IS, "ncit/C83572"),
        ],
        synonyms=["3,7-Dihydro-1,3,7-trimethyl-1H-purine-2,6-dione monohydrate"],
    ),
    Substance(
        sid="caf",
        name="caffeine",
        label="caffeine (137X)",
        description="A methylxanthine alkaloid found in the seeds, nuts, or leaves of a number of plants native to "
        "South America and East Asia that is structurally related to adenosine and acts primarily as an "
        "adenosine receptor antagonist with psychotropic and anti-inflammatory activities.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:27732"),
            (BQB.IS, "ncit/C328"),
        ],
        synonyms=["137TMX", "1,3,7-TMX", "137MX", "137X"],
    ),
    Substance(
        sid="137u",
        name="137U",
        label="1,3,7-trimethyluric acid (137U)",
        description="1,3,7-trimethyluric acid is an oxopurine in which the purine ring "
        "is substituted by oxo groups at positions 2, 6, and 8, and the "
        "nitrogens at positions 1, 3, and 7 are substituted by methyl "
        "groups. It is a metabolite of caffeine. It has a role as a human "
        "xenobiotic metabolite, a human blood serum metabolite and a "
        "mouse metabolite. It is a conjugate acid of a "
        "1,3,7-trimethylurate.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:691622"),
            (BQB.IS, "pubchem.compound/79437"),
        ],
        synonyms=[
            "137TMU",
            "1,3,7-MU",
            "trimethyluric acid",
            "1,3,7-Trimethyluric acid",
            "1,3,7-trimethylurate",
            "8-oxy-caffeine",
        ],
    ),
    Substance(
        sid="px",
        name="paraxanthine",
        label="paraxanthine (17X)",
        description="A dimethylxanthine having the two methyl groups located at "
        "positions 1 and 7. It is a metabolite of caffeine and theobromine in animals.",
        annotations=[(BQB.IS, "chebi/CHEBI:25858")],
        synonyms=["17DMX", "1,7-dimethylxanthine", "1,7-DMX", "17X", "17MX"],
    ),
    Substance(
        sid="17u",
        name="17U",
        label="1,7-dimethyluric acid (17U)",
        description="Metabolite of caffeine.",
        annotations=[(BQB.IS, "chebi/CHEBI:68449")],
        synonyms=[
            "17DMU",
            "1,7-dimethyluric acid",
            "1,7 DMU",
            "1,7-DMU",
            "17MU",
            "17U",
        ],
    ),
    Substance(
        sid="tp",
        name="theophylline",
        label="theophylline (13X)",
        description="A natural alkaloid derivative of xanthine isolated from the plants "
        "Camellia sinensis and Coffea arabica. Theophylline appears to inhibit "
        "phosphodiesterase and prostaglandin production, regulate calcium flux and "
        "intracellular calcium distribution, and antagonize adenosine. "
        "Metabolite of caffeine.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:28177"),
            (BQB.IS, "ncit/C872"),
        ],
        synonyms=["13DMX", "1,3-dimethylxanthine", "1,3-DMX", "13X", "13MX"],
    ),
    Substance(
        sid="13u",
        name="13U",
        label="1,3-dimethyluric acid (13U)",
        description="Metabolite of caffeine. 1,3-dimethyluric acid is an oxopurine "
        "that is 7,9-dihydro-1H-purine-2,6,8(3H)-trionesubstituted by "
        "methyl groups at N-1 and N-3. It has a role as a metabolite. "
        "It derives from a 7,9-dihydro-1H-purine-2,6,8(3H)-trione. It is "
        "a conjugate acid of a 1,3-dimethylurate anion.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:68447"),
            (BQB.IS, "pubchem.compound/70346"),
        ],
        synonyms=["13DMU", "13MU", "13U"],
    ),
    Substance(
        sid="tb",
        name="theobromine",
        label="theobromine (37X)",
        description="A dimethylxanthine having the two methyl groups located at positions 3 and 7. "
        "A purine alkaloid derived from the cacao plant, it is found in chocolate, as well as in a "
        "number of other foods, and is a vasodilator, diuretic and heart stimulator. Metabolite of caffeine.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:28946"),
            (BQB.IS, "ncit/C87684"),
        ],
        synonyms=["37DMX", "3,7-dimethylxanthine", "3,7-DMX", "37X", "37MX"],
    ),
    Substance(
        sid="37u",
        name="37U",
        label="3,7-dimethyluric acid (37U)",
        description="Metabolite of caffeine. 3,7-dimethyluric acid is an oxopurine that is "
        "7,9-dihydro-1H-purine-2,6,8(3H)-trione substituted by methyl groups at N-3 and N-7. "
        "It has a role as a metabolite and a mouse metabolite. It derives from a "
        "7,9-dihydro-1H-purine-2,6,8(3H)-trione. It is a conjugate acid of a 3,7-dimethylurate anion.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:68531"),
            (BQB.IS, "pubchem.compound/83126"),
        ],
        synonyms=["37DMU", "37MU", "37U"],
    ),
    Substance(
        sid="1x",
        name="1X",
        label="1-methylxanthine (1X)",
        description="Metabolite of caffeine.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:68444"),
            (BQB.IS, "pubchem.compound/80220"),
        ],
        synonyms=["1MX", "1-MX", "1-X"],
    ),
    Substance(
        sid="1u",
        name="1U",
        label="1-methyluric acid (1U)",
        description="Metabolite of caffeine. 1-methyluric acid is an oxopurine that is "
        "7,9-dihydro-1H-purine-2,6,8(3H)-trione substituted by a methyl "
        "group at N-1. It is one of the metabolites of caffeine found in "
        "human urine. It has a role as a human xenobiotic metabolite and a "
        "mouse metabolite.",
        annotations=[
            (BQB.IS, "pubchem.compound/69726"),
            (BQB.IS, "chebi/CHEBI:68441"),
        ],
        synonyms=[
            "1MU",
            "1-MU",
            "1-U",
        ],
    ),
    Substance(
        sid="3x",
        name="3X",
        label="3-methylxanthine (3X)",
        description="Metabolite of caffeine.",
        annotations=[
            (BQB.IS, "pubchem.compound/70639"),
            (BQB.IS, "chebi/CHEBI:62207"),
        ],
        synonyms=[
            "3MX",
            "3-MX",
            "3-X",
        ],
    ),
    Substance(
        sid="3u",
        name="3U",
        label="3-methyluric acid (3U)",
        description="Metabolite of caffeine.",
        formula="C6H6N4O3",
        mass=182.14,
        annotations=[
            (BQB.IS, "pubchem.compound/11804"),
            (BQB.IS, "inchikey/ODCYDGXXCHTFIR-UHFFFAOYSA-N"),
        ],
        synonyms=[
            "3MU",
            "3-MU",
            "3-U",
            "3-methyl-7,9-dihydropurine-2,6,8-trione",
        ],
    ),
    Substance(
        sid="7x",
        name="7X",
        label="7-methylxanthine (7X)",
        description="Metabolite of caffeine. 7-methylxanthine is an oxopurine that is "
        "xanthine in which the hydrogen attached to the nitrogen at "
        "position 7 is replaced by a methyl group. It is an intermediate "
        "metabolite in the synthesis of caffeine. It has a role as a plant "
        "metabolite, a human xenobiotic metabolite and a mouse metabolite. "
        "It is an oxopurine and a purine alkaloid. It derives from a "
        "7H-xanthine.",
        annotations=[
            (BQB.IS, "pubchem.compound/68374"),
            (BQB.IS, "chebi/CHEBI:48991"),
        ],
        synonyms=[
            "7MX",
            "7-MX",
            "7-X",
        ],
    ),
    Substance(
        sid="7u",
        name="7U",
        label="7-methyluric acid (7U)",
        description="Metabolite of caffeine.",
        annotations=[
            (BQB.IS, "pubchem.compound/69160"),
            (BQB.IS, "chebi/CHEBI:80470"),
        ],
        synonyms=["7MU", "7-MU", "7-U"],
    ),
    Substance(
        sid="afmu",
        name="AFMU",
        label="5-Acetylamino-6-formylamino-3-methyluracil (AFMU)",
        description="Metabolite of caffeine. 5-acetamido-6-formamido-3-methyluracil is "
        "a formamidopyrimidine. It has a role as a mouse metabolite. "
        "It derives from a uracil.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:32643"),
            (BQB.IS, "pubchem.compound/108214"),
        ],
        synonyms=["5-Acetylamino-6-formylamino-3-methyluracil"],
    ),
    Substance(
        sid="aamu",
        name="AAMU",
        label="5-Acetylamino-6-amino-3-methyluracil (AAMU)",
        description="Metabolite of caffeine.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:80473"),
            (BQB.IS, "pubchem.compound/88299"),
        ],
        synonyms=["A1", "5-Acetylamino-6-amino-3-methyluracil", "5-Ammu"],
    ),
    Substance(
        sid="admu",
        name="ADMU",
        description="Metabolite of caffeine.",
        formula="C8H12N4O3",
        mass=212.21,
        annotations=[
            (BQB.IS, "pubchem.compound/92288"),
            (BQB.IS, "inchikey/DSJVDNYAPZJQQX-UHFFFAOYSA-N"),
        ],
        synonyms=[
            "6-Amino-5-(formyl-N-methylamino)-1,3-dimethyluracil",
            "1,3,7-Dau",
            "DTXSID50879208",
        ],
    ),
    Substance(
        sid="a1u",
        name="A1U",
        label="6-Amino-5-(formyl-N-methylamino)-1-methyluracil (A1U)",
        description="Metabolite of caffeine.",
        annotations=[],
        synonyms=[
            "6-Amino-5-(formyl-N-methylamino)-1-methyluracil",
            "6-Amino-5 (N-formylmethylamino) 1-methyluracil",
        ],
    ),
    Substance(
        sid="a3u",
        name="A3U",
        label="6-Amino-5-(formyl-N-methylamino)-1-methyluracil (A3U)",
        description="Metabolite of caffeine.",
        annotations=[],
        synonyms=[
            "6-Amino-5-(formyl-N-methylamino)-3-methyluracil",
            "6-Amino-5 (N-formylmethylamino) 3-methyluracil",
        ],
    ),
    # FIXME: This methobilite us not used in any study and not as a parent in an substance. Do we need this?
    Substance(
        sid="mx",
        name="methylxanthine",
        description="Metabolite of caffeine.",
        annotations=[(BQB.IS, "chebi/CHEBI:25348")],
    ),
    # caffeine derived
    Substance(
        sid="caf/px",
        label="caffeine/paraxanthine",
        description="Caffeine/paraxanthine ratio used for evaluating hepatic CYP1A2 metabolism.",
        parents=["px", "caf"],
    ),
    Substance(
        sid="px/caf",
        label="paraxanthine/caffeine",
        description="Paraxanthine/caffeine used for evaluating hepatic CYP1A2 metabolism.",
        parents=["px", "caf"],
        synonyms=["17X/137X"],
    ),
    Substance(
        sid="caf+px",
        label="caffeine+paraxanthine",
        description="Sum of caffeine and paraxanthine used for evaluating hepatic CYP1A2 metabolism.",
        parents=["px", "caf"],
    ),
    Substance(
        sid="tb/caf",
        label="theobromine/caffeine",
        description="Theobromine/caffeine ratio.",
        parents=["tb", "caf"],
    ),
    Substance(
        sid="tp/caf",
        label="theophylline/caffeine",
        description="Theophylline/caffeine ratio",
        parents=["tp", "caf"],
    ),
    Substance(
        sid="1x/caf",
        name="1X/caf",
        label="1X/caffeine",
        description="1X/caffeine ratio",
        parents=["1x", "caf"],
    ),
    Substance(
        sid="1x/px",
        name="1X/px",
        label="1X/paraxanthine",
        description="1x/paraxanthine ratio",
        parents=["1x", "px"],
    ),
    Substance(
        sid="px/tp",
        name="px/tp",
        label="paraxanthine/theophylline",
        description="paraxanthine/theophylline ratio",
        parents=["tp", "px"],
    ),
    Substance(
        sid="1X/37U",
        name="1X/37U",
        description="1X/37U ratio",
        parents=["1X", "37U"],
    ),
    Substance(
        sid="1U/(3X+7X)",
        name="1U/(3X+7X)",
        description="Caffeine metabolic ratio.",
        parents=["1U", "3X", "7X"],
    ),
    Substance(
        sid="1x/tp",
        name="1X/tp",
        label="1X/theophylline",
        description="1X/theophylline ratio",
        parents=["1x", "tp"],
    ),
    Substance(
        sid="afmu+1u+1x",
        name="AFMU+1U+1X",
        description="Caffeine metabolic ratio.",
        parents=["afmu", "1u", "1x"],
        synonyms=["AUX"],
    ),
    Substance(
        sid="afmu+1u+1x+17u",
        name="AFMU+1U+1X+17U",
        description="Caffeine metabolic ratio.",
        parents=["afmu", "1u", "1x", "17u"],
    ),
    Substance(
        sid="(aamu+1u+1x)/17u",
        name="(AAMU+1U+1X)/17U",
        description="Caffeine metabolic ratio.",
        parents=["aamu", "1u", "1x", "17u"],
    ),
    Substance(
        sid="(17u+px)/caf",
        name="(17U+px)/caf",
        description="Caffeine metabolic ratio.(Paraxanthine+17U)/caffeine used for evaluating hepatic CYP1A2 metabolism.",
        parents=["17u", "px", "caf"],
        synonyms=["(17U+17X)/137X"],
    ),
    Substance(
        sid="17u/px",
        name="17U/px",
        description="Caffeine metabolic ratio.",
        parents=["17u", "px"],
    ),
    Substance(
        sid="1u/(1u+1x)",
        name="1U/(1U+1X)",
        description="Caffeine metabolic ratio.",
        parents=["1u", "1x"],
    ),
    Substance(
        sid="1u/1x",
        name="1U/1X",
        description="Caffeine metabolic ratio.",
        parents=["1u", "1x"],
    ),
    # FIXME: Not used in any study. Remove me?
    Substance(
        sid="afmu/(afmu+1u+1x)",
        name="AFMU/(AFMU+1U+1X)",
        description="Caffeine metabolic ratio.",
        parents=["afmu", "1u", "1x"],
    ),
    Substance(
        sid="(afmu+1u+1x)/17u",
        name="(AFMU+1U+1X)/17U",
        description="Caffeine metabolic ratio.",
        parents=["afmu", "1u", "1x", "17u"],
    ),
    Substance(
        sid="afmu/1x",
        name="AFMU/1X",
        description="Caffeine metabolic ratio.",
        parents=["afmu", "1x"],
    ),
    Substance(
        sid="aamu/(aamu+1u+1x)",
        name="AAMU/(AAMU+1U+1X)",
        description="Caffeine metabolic ratio.",
        parents=["aamu", "1u", "1x"],
    ),
    Substance(
        sid="(afmu+1u+1x+17u+px)/caf",
        name="(AFMU+1U+1X+17U+px)/caf",
        description="Caffeine metabolic ratio.",
        parents=["afmu", "1u", "1x", "17u", "px", "caf"],
        synonyms=["(AFMU+1U+1X+17U+17X)/137X"],
    ),
    Substance(
        sid="tp+tb+px+1x+3x+7x+1u+7u+13u+17u+137u+caf",
        name="tp+tb+px+1X+3X+7X+1U+7U+13U+17U+137U+caf",
        description="Sum of caffeine metabolites: tp+tb+px+caf+1X+3X+7X+1U+7U+13U+17U+137U",
        parents=[
            "tp",
            "tb",
            "px",
            "1x",
            "3x",
            "7x",
            "1u",
            "7u",
            "13u",
            "17u",
            "137u",
            "caf",
        ],
    ),
    Substance(
        sid="1_methyl_14c_caf",
        name="1_methyl_14c_caffeine",
        description="14C-modified caffeine. C14 is positioned in the 1_methyl group",
        parents=["caf"],
    ),
    Substance(
        sid="2_14c_caf",
        name="2_14c_caffeine",
        description="14C-modified caffeine. C14 is positioned at C2",
        parents=["caf"],
    ),
    Substance(
        sid="all_14c_caffeine_equivalents",
        name="all_14c_caffeine_equivalents",
        description="sum of all 14C-modified caffeine equivalents",
    ),
    Substance(
        sid="tp+tb+px+caf",
        name="tp+tb+px+caf",
        description="Sum of caffeine metabolites: tp+tb+px+caf",
        parents=["tp", "tb", "px", "caf"],
    ),
    Substance(
        sid="17u/(17u+px+1x+1u+afmu)",
        name="17U/(17U+px+1X+1U+AFMU)",
        description="Caffeine metabolic ratio.",
        parents=["afmu", "1u", "1x", "px", "17u"],
    ),
    # caffeine interaction
    Substance(
        sid="etravirine",
        label="etravirine",
        description="An aminopyrimidine that consists of 2,6-diaminopyrimidine bearing a bromo substituent "
        "at position 5, a 4-cyano-2,6-dimethylphenoxy substituent at position 4 and having "
        "a 4-cyanophenyl substituent attached to the 2-amino group. NNRTI of HIV-1, "
        "binds directly to RT and blocks RNA-dependent and DNA-dependent DNA polymerase activities",
        annotations=[
            (BQB.IS, "chebi/CHEBI:63589"),
        ],
        synonyms=[],
    ),
    Substance(
        sid="L-ascorbic acid",
        label="vitamin c",
        description="A natural water-soluble vitamin (Vitamin C). Ascorbic acid is a potent "
        "reducing and antioxidant agent that functions in fighting bacterial infections, "
        "in detoxifying reactions, and in the formation of collagen in fibrous tissue, "
        "teeth, bones, connective tissue, skin, and capillaries.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:29073"),
            (BQB.IS, "ncit/C285"),
        ],
        synonyms=["vitamin c"],
    ),
    Substance(
        sid="cimetidine",
        description="A histamine H(2)-receptor antagonist. Enhancing anti-tumor cell-mediated responses, "
        "cimetidine blocks histamine's ability to stimulate suppressor T lymphocyte activity "
        "and to inhibit natural killer (NK) cell activity and interleukin-2 production.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:3699"),
            (BQB.IS, "ncit/C374"),
        ],
    ),
    Substance(
        sid="fluvoxamine",
        description="A 2-aminoethyl oxime ether of aralkylketones, with antidepressant, antiobsessive-compulsive, "
        "and anxiolytic properties. Fluvoxamine, chemically unrelated to other selective serotonin "
        "reuptake inhibitors, selectively blocks serotonin reuptake by inhibiting the serotonin reuptake "
        "pump at the presynaptic neuronal membrane.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:5138"),
            (BQB.IS, "ncit/C61769"),
        ],
    ),
    Substance(
        sid="alprazolam",
        description="A triazolobenzodiazepine agent with anxiolytic, sedative-hypnotic and anticonvulsant "
        "activities. Alprazolam binds to a specific site distinct from the inhibitory neurotransmitter "
        "gamma-aminobutyric acid (GABA) binding site on the benzodiazepine-GABA-A-chloride ionophore "
        "receptor complex located in the limbic, thalamic and hypothalamic regions of the central nervous "
        "system (CNS).",
        annotations=[
            (BQB.IS, "chebi/CHEBI:2611"),
            (BQB.IS, "ncit/C227"),
        ],
    ),
    Substance(
        sid="disulfiram",
        description="An orally bioavailable carbamoyl derivative and a proteasome inhibitor that is used in the "
        "treatment of alcoholism, with potential antineoplastic and chemosensitizing activities. "
        "Disulfiram (DSF) may help to treat alcoholism by irreversibly binding to and inhibiting "
        "acetaldehyde dehydrogenase, an enzyme that oxidizes the ethanol metabolite acetaldehyde into "
        "acetic acid.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:4659"),
            (BQB.IS, "ncit/C447"),
        ],
    ),
    Substance(
        sid="naringenin",
        description="A trihydroxyflavanone that is flavanone substituted by hydroxy groups at positions 5, 6 and 4'.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:50202"),
            (BQB.IS, "ncit/C68463"),
        ],
    ),
    Substance(
        sid="quinolone",
        description="A quinolone antibiotic is a member of a large group of broad-spectrum bacteriocidals that "
        "share a bicyclic core structure related to the substance 4-quinolone.[1] They are used in human "
        "and veterinary medicine to treat bacterial infections, as well as in animal husbandry.",
        annotations=[(BQB.IS, "chebi/CHEBI:23765")],
        synonyms=["quinolone antibiotic"],
    ),
    Substance(
        sid="ciprofloxacin",
        description="A synthetic broad spectrum fluoroquinolone antibiotic. Ciprofloxacin binds to and inhibits "
        "bacterial DNA gyrase, an enzyme essential for DNA replication. This agent is more active against "
        "Gram-negative bacteria than Gram-positive bacteria.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:100241"),
            (BQB.IS, "ncit/C375"),
        ],
    ),
    Substance(
        sid="sulfinpyrazone",
        description=" phenylbutazone derivative with uricosuric and antithrombotic properties. Sulfinpyrazone "
        "competitively inhibits reabsorption of urate at the proximal renal tubule in the kidney. "
        "This agent acts on the organic anion transport exchanger, thereby increasing uric acid "
        "excretion and decreasing serum uric acid levels resulting in the prevention of urate deposition.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:9342"),
            (BQB.IS, "ncit/C47739"),
        ],
    ),
    Substance(
        sid="thiabendazole",
        description="A benzimidazole derivative with anthelminthic property. Although the mechanism of action "
        "has not been fully elucidated, thiabendazole inhibits the helminth-specific mitochondrial "
        "enzyme fumarate reductase, thereby inhibiting the citric acid cycle, mitochondrial respiration "
        "and subsequent production of ATP, ultimately leading to helminth's death.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:45979"),
            (BQB.IS, "ncit/C873"),
        ],
    ),
    Substance(
        sid="artemisinin",
        description="A sesquiterpene lactone obtained from sweet wormwood, Artemisia annua, which is used as an "
        "antimalarial for the treatment of multi-drug resistant strains of falciparum malaria.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:223316"),
            (BQB.IS, "ncit/C78093"),
        ],
        synonyms=["(+)-artemisinin"],
    ),
    Substance(
        sid="voriconazole",
        description="Voriconazole. A synthetic triazole with antifungal activity. Voriconazole selectively "
        "inhibits 14-alpha-lanosterol demethylation in fungi, preventing the production of ergosterol, "
        "an essential constituent of the fungal cell membrane, and resulting in fungal cell lysis.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:10023"),
            (BQB.IS, "ncit/C1707"),
            (BQB.IS, "omit/0028746"),
        ],
    ),
    Substance(
        sid="zolpidem",
        description="Zolpidem. A drug used to treat insomnia (inability to sleep), and anxiety."
        " It is a type of imidazopyridine (sedative hypnotic).",
        annotations=[
            (BQB.IS, "chebi/CHEBI:10125"),
            (BQB.IS, "ncit/C62000"),
        ],
    ),
    Substance(
        sid="theacrine",
        description="Theacrine.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:139388"),
        ],
    ),
    Substance(
        sid="trimethadione",
        description="Trimethadione. A dione-type anticonvulsant with antiepileptic "
        "activity. Trimethadione reduces T-type calcium currents in "
        "thalamic neurons, thereby stabilizing neuronal membranes, "
        "raising the threshold for repetitive activities in the thalamus "
        "and inhibiting corticothalamic transmission.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:9727"),
            (BQB.IS, "ncit/C47772"),
        ],
    ),
    Substance(
        sid="dimethadione",
        description="Dimethadione.",
        annotations=[
            (BQB.IS, "pubchem.compound/3081"),
            (BQB.IS, "chebi/CHEBI:94613"),
            (BQB.IS, "ncit/C171703"),
        ],
        synonyms=[
            "5,5-Dimethyloxazolidine-2,4-dione",
            "5,5-Dimethyl-2,4-oxazolidinedione",
        ],
    ),
    # oral contraceptives
    Substance(
        sid="levonorgestrel",
        description="The levorotatory form of norgestrel and synthetic progestogen with progestational and "
        "androgenic activity. Levonorgestrel binds to the progesterone receptor in the nucleus of "
        "target cells, thereby stimulating the resulting hormone-receptor complex, initiating "
        "transcription, and increasing the synthesis of certain proteins. This results in a suppression "
        "of luteinizing hormone (LH) activity and an inhibition of ovulation, as well as an alteration in "
        "the cervical mucus and endometrium.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:6443"),
            (BQB.IS, "ncit/C47585"),
        ],
    ),
    Substance(
        sid="gestodene",
        description="Gestodene, sold under the brand names Femodene and Minulet among others, is a progestin "
        "medication which is used in birth control pills for women.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:135323"),
            (BQB.IS, "ncit/C87240"),
        ],
        synonyms=["Femodene", "Minulet"],
    ),
    Substance(
        sid="ee2",
        name="ethinylestradiol",
        description="A semisynthetic estrogen. Ethinyl estradiol binds to the estrogen receptor complex and enters "
        "the nucleus, activating DNA transcription of genes involved in estrogenic cellular responses. "
        "This agent also inhibits 5-alpha reductase in epididymal tissue, which lowers testosterone levels "
        "and may delay progression of prostatic cancer. In addition to its antineoplastic effects, "
        "ethinyl estradiol protects against osteoporosis.",
        annotations=[
            (BQB.IS, "ncit/C486"),
        ],
        synonyms=[
            "Ethinyl Estradiol",
        ],
    ),
    Substance(
        sid="estradiol-benzoate",
        name="estradiol benzoate",
        description="The synthetic benzoate ester of estradiol, a steroid sex hormone vital to the maintenance of fertility and secondary sexual characteristics in females. As the primary, most potent estrogen hormone produced by the ovaries, estradiol binds to and activates specific nuclear receptors.",
        annotations=[
            (BQB.IS, "ncit/C29769"),
        ],
        synonyms=[],
    ),
    # codeine/morphine
    Substance(
        sid="ccm",
        name="codeine containing medication",
        description="Codeine containing medication.",
    ),
    Substance(
        sid="cod",
        name="codeine",
        description="A naturally occurring phenanthrene alkaloid and opioid agonist with analgesic, "
        "antidiarrheal and antitussive activities. Codeine mimics the actions of endogenous opioids "
        "by binding to the opioid receptors at many sites within the central nervous system (CNS). "
        "Stimulation of mu-subtype opioid receptors results in a decrease in the release of "
        "nociceptive neurotransmitters such as substance P, GABA, dopamine, acetylcholine and "
        "noradrenaline;",
        annotations=[(BQB.IS, "chebi/CHEBI:16714"), (BQB.IS, "ncit/C383")],
    ),
    Substance(
        sid="cod-p",
        name="codeine phosphate",
        mass=397.4,
        formula="C18H24NO7P",
        description="The phosphate salt of codeine, a naturally occurring phenanthrene alkaloid and opioid "
        "agonist with analgesic, antidiarrheal and antitussive activities. Codeine mimics the "
        "actions of endogenous opioids by binding to the opioid receptors at many sites within "
        "the central nervous system (CNS).",
        annotations=[
            (BQB.IS, "pubchem.compound/5359227"),
            (BQB.IS, "ncit/C74548"),
            (BQB.IS, "inchikey/WUXLCJZUUHIXFY-FFHNEAJVSA-N"),
        ],
        synonyms=["Tricodein"],
    ),
    Substance(
        sid="cod-s",
        name="codeine sulphate",
        label="codeine sulfate anhydrous",
        mass=696.8,
        formula="C36H44N2O10S",
        description="Codeine Sulfate is the sulfate salt form of codeine, a naturally occurring phenanthrene "
        "alkaloid and opioid agonist with analgesic, antidiarrheal and antitussive activity. Codeine "
        "sulfate mimics the actions of opioids by binding to the opioid receptors at many sites within "
        "the central nervous system (CNS).",
        annotations=[
            (BQB.IS, "pubchem.compound/5359613"),
            (BQB.IS, "ncit/C53137"),
            (BQB.IS, "inchikey/BCXHDORHMMZBBZ-DORFAMGDSA-N"),
        ],
        synonyms=["codeine sulfate"],
    ),
    Substance(
        sid="c6g",
        name="codeine-6-glucuronide",
        description="Metabolite of codeine. Codeine-6-glucuronide belongs to the class of organic compounds known as "
        "morphinans. These are polycyclic compounds with a four-ring skeleton with three condensed "
        "six-member rings forming a partially hydrogenated phenanthrene moiety, one of which is aromatic "
        "while the two others are alicyclic.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:80580"),
            (BQB.IS, "pubchem.compound/5489029"),
            (BQB.IS, "inchikey/CRWVOYRJXPDBPM-HSCJLHHPSA-N"),
        ],
    ),
    Substance(
        sid="ncod",
        name="norcodeine",
        description="A morphinane-like compound that is the N-demethylated derivative of codeine.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:80579"),
            (BQB.IS, "ncit/C166634"),
            (BQB.IS, "pubchem.compound/9925873"),
        ],
        synonyms=["N-Desmethylcodeine", "Norcodeinum", "Norcodeina"],
    ),
    Substance(
        sid="ncg",
        name="norcodeine-glucuronide",
        label="norcodeine 6-glucuronide",
        description="Metabolite of norcodeine.",
        mass=461.5,
        formula="C23H27NO9",
        annotations=[
            (BQB.IS, "inchikey/YWEYZPZIMCQHFM-XDMGLTAESA-N"),
            (BQB.IS, "pubchem.compound/3084921"),
        ],
        synonyms=[
            "beta-D-Glucopyranosiduronic acid, (5alpha,6alpha)-7,8-didehydro-4,5-epoxy-3-methoxymorphinan-6-yl",
            "morphine-6-beta-d-glucuronide",
        ],
    ),
    Substance(
        sid="ncc", name="norcodeine-conjugates", description="Norcodeine conjugates."
    ),
    Substance(
        sid="mor",
        name="morphine",
        description="An opiate alkaloid isolated from the plant Papaver somniferum and produced synthetically. "
        "Morphine binds to and activates specific opiate receptors (delta, mu and kappa), each of which "
        "are involved in controlling different brain functions. In the central nervous and "
        "gastrointestinal systems, this agent exhibits widespread effects including analgesia, "
        "anxiolysis, euphoria, sedation, respiratory depression, and gastrointestinal system "
        "smooth muscle contraction.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:17303"),
            (BQB.IS, "ncit/C62051"),
        ],
    ),
    Substance(
        sid="mor-p",
        name="morphine phosphate",
        mass=383.3,
        formula="C17H22NO7P",
        description="The phosphate salt of morphine.",
        annotations=[
            (BQB.IS, "pubchem.compound/67408920"),
            (BQB.IS, "inchikey/KZSZGTYWWBPNKB-VYKNHSEDSA-N"),
        ],
        synonyms=[
            "Morphine monophosphate",
            "UNII-1LQ9207LZE",
            "1LQ9207LZE",
            "596-17-8",
        ],
    ),
    Substance(
        sid="mor-s",
        name="morphine sulfate",
        description="The sulfate salt of morphine, an opiate alkaloid isolated from the plant Papaver "
        "somniferum and produced synthetically. Morphine binds to and activates specific opiate "
        "receptors (delta, mu and kappa), each of which are involved in controlling different brain "
        "functions. In the central nervous and gastrointestinal systems, this agent has widespread effects "
        "including analgesia, anxiolysis, euphoria, sedation, respiratory depression, and "
        "gastrointestinal system smooth muscle contraction.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:7003"),
            (BQB.IS, "ncit/C669"),
        ],
        synonyms=["morphine sulphate"],
    ),
    Substance(
        sid="mor-h",
        name="morphine hydrochloride",
        description="Morphine hydrochloride is the hydrochloride salt of morphine.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:55340"),
            (BQB.IS, "ncit/C83973"),
            (BQB.IS, "pubchem.compound/5464110"),
        ],
        synonyms=["Morphine HCl"],
    ),
    Substance(
        sid="m3g",
        name="morphine-3-glucuronide",
        description="Metabolite of morphine. Morphine-3-glucuronide belongs to the class of organic compounds known "
        "as morphinans.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:80631"),
            (BQB.IS, "pubchem.compound/5484731"),
            (BQB.IS, "inchikey/WAEXKFONHRHFBZ-ZXDZBKESSA-N"),
        ],
        synonyms=["morphine-3-beta-D-glucuronide"],
    ),
    Substance(
        sid="m6g",
        name="morphine-6-glucuronide",
        description="Metabolite of morphine. Morphine-6-glucuronide belongs to the class of organic compounds known "
        "as morphinans.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:80581"),
            (BQB.IS, "pubchem.compound/5360621"),
            (BQB.IS, "inchikey/GNJCUHZOSOYIEC-GAROZEBRSA-N"),
        ],
    ),
    Substance(
        sid="nmor",
        name="normorphine",
        description="Normorphine is a morphinane alkaloid.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:7633"),
            (BQB.IS, "ncit/C170234"),
            (BQB.IS, "pubchem.compound/5462508"),
        ],
    ),
    Substance(
        # see: https://pubchem.ncbi.nlm.nih.gov/#query=normorphine%20glucuronide
        # either normorphine-3-glucuronide or normorphine-6-glucuronide
        sid="nmg",
        name="normorphine-glucuronide",
        mass=447.4,
        formula="C22H25NO9",
        description="Metabolite of normorphine.",
        annotations=[],
    ),
    # codeine/morphine derived
    Substance(
        sid="cod/mor",
        label="codeine/morphine",
        description="Codeine/morphine ratio. Used in CYP2D6 phenotyping.",
        parents=["cod", "mor"],
    ),
    Substance(
        sid="mor/cod",
        label="morphine/codeine",
        description="Morphine/codeine ratio. Used in CYP2D6 phenotyping.",
        parents=["cod", "mor"],
    ),
    Substance(
        sid="(mor+m3g+m6g)/(cod+c6g)",
        description="Metabolic ratio. Used in CYP2D6 phenotyping.",
        parents=["cod", "c6g", "mor", "m3g", "m6g"],
    ),
    Substance(
        sid="mor+m3g+m6g",
        description="Sum of morphine metabolites. Used in CYP2D6 phenotyping.",
        parents=["mor", "m3g", "m6g"],
    ),
    Substance(
        sid="cod+c6g+ncod",
        description="Sum of codeine metabolites, total codeine consisting of conjugated and non-conjugated codeine. "
        "Used in CYP2D6 phenotyping.",
        parents=["cod", "c6g", "ncod"],
    ),
    Substance(
        sid="mor+m3g+m6g+nmor+cod+ncod+c6g+ncg",
        description="Sum of codeine and morphine metabolites. Used in CYP2D6 phenotyping.",
        parents=["mor", "m3g", "m6g", "nmor", "cod", "ncod", "c6g", "ncg"],
    ),
    Substance(
        sid="mor+m3g+m6g+cod+ncod+c6g+ncc",
        description="Sum of codeine and morphine metabolites. Used in CYP2D6 phenotyping.",
        parents=["mor", "m3g", "m6g", "cod", "ncod", "c6g", "ncc"],
    ),
    Substance(
        sid="mor+ncod+c6g",
        description="Sum of codeine and morphine metabolites. Used in CYP2D6 phenotyping.",
        parents=["mor", "ncod", "c6g"],
    ),
    Substance(
        sid="c6g+cod+mor+ncod",
        description="Sum of codeine and morphine metabolites. Used in CYP2D6 phenotyping.",
        parents=["c6g", "cod", "mor", "ncod"],
    ),
    Substance(
        sid="cod/(mor+m3g+m6g+nmor)",
        description="Ratio of codeine and morphine metabolites. Used in CYP2D6 phenotyping.",
        parents=["mor", "m3g", "m6g", "nmor", "cod"],
    ),
    Substance(
        sid="(mor+m3g+m6g+nmor)/(cod+ncod+c6g)",
        description="Ratio of codeine and morphine metabolites for O-demethylation of codeine. "
        "Used in CYP2D6 phenotyping.",
        parents=["mor", "m3g", "m6g", "nmor", "cod", "ncod", "c6g"],
    ),
    Substance(
        sid="cod/(ncod+ncg+nmor)",
        description="Ratio of codeine and morphine metabolites for N-demethylation of codeine. "
        "Used in CYP2D6 phenotyping.",
        parents=["cod", "ncod", "ncg", "nmor"],
    ),
    Substance(
        sid="m3g+m6g",
        description="Sum of morphine metabolites. Used in CYP2D6 phenotyping.",
        parents=["m3g", "m6g"],
        synonyms=["M-G", "morphine-glucuronides"],
    ),
    Substance(
        sid="cod/c6g",
        description="Ratio of codeine metabolites for N-demethylation of codeine. "
        "Used in CYP2D6 phenotyping.",
        parents=["cod", "c6g"],
    ),
    Substance(
        sid="pholcodine",
        name="pholcodine",
        description="A morphinane alkaloid that is a derivative of morphine with a 2-morpholinoethyl group at "
        "the 3-position. Pholcodine is a drug which is an opioid cough suppressant (antitussive). "
        "It helps suppress unproductive coughs and also has a mild sedative effect, but has little or no "
        "analgesic effects.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:53579"),
            (BQB.IS, "ncit/C87365"),
        ],
        synonyms=["homocodein", "morpholinylethylmorphine"],
    ),
    Substance(
        sid="guaifenesin",
        name="guaifenesin",
        description="Guaifenesin is thought to act as an expectorant by increasing the volume and reducing the"
        "viscosity of secretions in the trachea and bronchi. It has been said to aid in the flow of"
        "respiratory tract secretions, allowing ciliary movement to carry the loosened secretions upward"
        "toward the pharynx. Thus, it may increase the efficiency of the cough reflex and facilitate"
        "removal of the secretions."
        "Guaifenesin has muscle relaxant and anticonvulsant properties and may act as an NMDA receptor antagonist.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:5551"),
        ],
        synonyms=["guaifenesin", "mucinex"],
    ),
    # CYP2D6 related
    Substance(
        sid="qui",
        name="quinidine",
        description="An alkaloid extracted from the bark of the Cinchona tree with class 1A antiarrhythmic and "
        "antimalarial effects. Quinidine stabilizes the neuronal membrane by binding to and inhibiting "
        "voltage-gated sodium channels, thereby inhibiting the sodium influx required for the initiation "
        "and conduction of impulses resulting in an increase of the threshold for excitation and "
        "decreased depolarization during phase 0 of the action potential.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:28593"),
            (BQB.IS, "ncit/C793"),
        ],
    ),
    Substance(
        sid="qui-s",
        name="quinidine sulphate",
        description="quinidine sulphate",
        annotations=[
            (BQB.IS, "chebi/CHEBI:28593"),
            (BQB.IS, "ncit/C793"),
        ],
    ),
    Substance(
        sid="deb",
        name="debrisoquine",
        description="Debrisoquine is a derivative of guanidine. It is an antihypertensive drug similar to "
        "guanethidine. Debrisoquine is frequently used for phenotyping the CYP2D6 enzyme, "
        "a drug-metabolizing enzyme.",
        annotations=[(BQB.IS, "chebi/CHEBI:34665")],
    ),
    Substance(
        sid="deb-sul",
        name="debrisoquine sulfate",
        description="Debrisoquine is a derivative of guanidine. It is an antihypertensive drug similar to "
        "guanethidine. Debrisoquine is frequently used for phenotyping the CYP2D6 enzyme, "
        "a drug-metabolizing enzyme.",
        annotations=[(BQB.IS, "chebi/CHEBI:50973")],
    ),
    Substance(
        sid="4hdeb",
        name="4-hydroxydebrisoquine",
        description="Metabolite of debrisoquine. A patient's CYP2D6 phenotype is often clinically determined via "
        "the administration of debrisoquine (a selective CYP2D6 substrate) and subsequent plasma "
        "concentration assay of the debrisoquine metabolite (4-hydroxydebrisoquine).",
        annotations=[(BQB.IS, "chebi/CHEBI:63800")],
    ),
    Substance(
        sid="deb/4hdeb",
        parents=["deb", "4hdeb"],
        description="debrisoquine/4-hydroxydebrisoquine ratio. Often used for CYP2D6 phenotyping.",
    ),
    Substance(
        sid="mep",
        name="mephenytoin",
        description="A heterocyclic organic compound with anticonvulsant property. Although the mechanism of "
        "action is not well established, mephenytoin potentially promotes sodium efflux from neurons "
        "in motor cortex, and stabilizes the threshold against hyperexcitability caused by excessive "
        "stimulation.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:6757"),
            (BQB.IS, "ncit/C66091"),
        ],
    ),
    Substance(
        sid="phenytoin",
        name="phenytoin",
        description="A hydantoin derivative and a non-sedative antiepileptic agent with anticonvulsant activity. "
        "Phenytoin potentially acts by promoting sodium efflux from neurons located in the motor cortex "
        "reducing post-tetanic potentiation at synapses.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:8107"),
            (BQB.IS, "ncit/C741"),
        ],
    ),
    Substance(
        sid="primidone",
        description="An analog of phenobarbital with antiepileptic property. Although the mechanism of action has "
        "not been fully elucidated, primidone probably exerts its actions, in a manner similar to "
        "phenobarbital, via activation of gamma-aminobutyric acid (GABA)-A receptor/chloride ionophore "
        "complex, which leads to prolonged and increased frequency of opening of the chloride channel "
        "within the receptor complex.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:8412"),
            (BQB.IS, "ncit/C47686"),
        ],
    ),
    Substance(
        sid="sodium-valproate",
        name="sodium valproate",
        description="The sodium salt form of valproic acid with anti-epileptic activity. Valproate sodium is "
        "converted into its active form, valproate ion, in blood. Although the mechanism of action "
        "remains to be elucidated, valproate sodium increases concentrations of gamma-aminobutyric acid "
        "(GABA) in the brain, probably due to inhibition of the enzymes responsible for the catabolism "
        "of GABA.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:9925"),
            (BQB.IS, "ncit/C48029"),
        ],
    ),
    Substance(
        sid="clonazepam",
        description="A synthetic benzodiazepine derivative used for myotonic or atonic seizures, absence seizures, "
        "and photosensitive epilepsy, anticonvulsant Clonazepam appears to enhance gamma-aminobutyric "
        "acid receptor responses, although its mechanism of action is not clearly understood.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:3756"),
            (BQB.IS, "ncit/C28935"),
        ],
    ),
    # sparteine
    Substance(
        sid="sparteine",
        name="sparteine",
        description="Sparteine is a quinolizidine alkaloid and a quinolizidine alkaloid fundamental parent."
        "Sparteine is a plant alkaloid derived from Cytisus scoparius and Lupinus mutabilis which may "
        "chelate calcium and magnesium. Often applied in CYP2D6 phenotyping.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:28827"),
            (BQB.IS, "ncit/C152414"),
            (BQB.IS, "pubchem.compound/644020"),
        ],
    ),
    Substance(
        sid="sparteine-sulfate",
        name="sparteine sulfate",
        description="Metabolite of sparteine.",
        mass=332.5,
        formula="C15H28N2O4S",
        annotations=[
            (BQB.IS, "pubchem.compound/23616742"),
            (BQB.IS, "inchikey/FCEHFCFHANDXMB-UMEYXWOPSA-N"),
        ],
    ),
    Substance(
        sid="2hspar",
        name="2-dehydrosparteine",
        description="2,3-didehydrosparteine is a quinolizidine alkaloid obtained by formal dehydrogenation at the "
        "2,3-position of sparteine. It derives from a sparteine.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:29130"),
            (BQB.IS, "pubchem.compound/3035890"),
            (BQB.IS, "inchikey/BWKNRAAXVUYXAH-XQLPTFJDSA-N"),
        ],
        synonyms=["2,3-didehydrosparteine"],
    ),
    Substance(
        sid="5hspar",
        name="5-dehydrosparteine",
        description="5,6-didehydrosparteine is a quinolizidine alkaloid obtained by formal dehydrogenation at the "
        "5,6-position of sparteine. It is a metabolite of sparteine found in human urine and plasma. "
        "It has a role as a human xenobiotic metabolite. It is a quinolizidine alkaloid, a "
        "tertiary amino compound and an organic heterotetracyclic compound.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:143195"),
            (BQB.IS, "pubchem.compound/160614"),
        ],
        synonyms=["5,6-didehydrosparteine"],
    ),
    Substance(
        sid="spar/(2hspar+5hspar)",
        label="sparteine/(2hspar+5hspar)",
        description="Sparteine metabolite ratio. Used for CYP2D6 phenotyping.",
        parents=["sparteine", "2hspar", "5hspar"],
    ),
    Substance(
        sid="spar+2hspar+5hspar",
        label="sparteine + 2hspar + 5hspar",
        description="Sparteine metabolite sum. Used for CYP2D6 phenotyping.",
        parents=["sparteine", "2hspar", "5hspar"],
    ),
    Substance(
        sid="2hspar+5hspar",
        label="2hspar+5hspar",
        description="Sparteine metabolite sum. Used for CYP2D6 phenotyping.",
        parents=["2hspar", "5hspar"],
    ),
    # medication
    Substance(
        sid="salbutamol",
        description="Salbutamol, also known as albuterol and marketed as Ventolin among other brand names, "
        "is a medication that opens up the medium and large airways in the lungs. It is a short-acting "
        "β2 adrenergic receptor agonist which works by causing relaxation of airway smooth muscle.",
        annotations=[(BQB.IS, "chebi/CHEBI:8746")],
        synonyms=["albuterol", "ventolin"],
    ),
    Substance(
        sid="beclometasone",
        description="Beclometasone, also known as beclometasone dipropionate, and sold under the brand name Qvar "
        "among others, is a steroid medication. It is available as an inhaler, cream, pills, and nasal spray."
        "A 17alpha-hydroxy steroid that is prednisolone in which the hydrogens at the 9alpha and 16beta "
        "positions are substituted by a chlorine and a methyl group, respectively.",
        annotations=[(BQB.IS, "chebi/CHEBI:3001")],
        synonyms=["beclometasone dipropionate", "Qvar"],
    ),
    Substance(
        sid="enalapril",
        description="A dicarbocyl-containing peptide and angiotensin-converting enzyme (ACE) inhibitor with "
        "antihypertensive activity. As a prodrug, enalapril is converted by de-esterification into its "
        "active form enalaprilat. Enalaprilat competitively binds to and inhibits ACE, thereby blocking "
        "the conversion of angiotensin I to angiotensin II. ",
        annotations=[
            (BQB.IS, "chebi/CHEBI:4784"),
            (BQB.IS, "ncit/C62027"),
        ],
    ),
    Substance(
        sid="atenolol",
        description="A synthetic isopropylamino-propanol derivative used as an "
        "antihypertensive, hypotensive and antiarrhythmic Atenolol acts as "
        "a peripheral, cardioselective beta blocker specific for beta-1 "
        "adrenergic receptors, without intrinsic sympathomimetic effects. "
        "It reduces exercise heart rates and delays atrioventricular "
        "conduction, with overall oxygen requirements decreasing.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:2904"),
            (BQB.IS, "ncit/C28836"),
        ],
    ),
    Substance(
        sid="diltiazem",
        description="A benzothiazepine derivative with anti-hypertensive, antiarrhythmic properties. Diltiazem "
        "blocks voltage-sensitive calcium channels in the blood vessels, by inhibiting the ion-control "
        "gating mechanisms, thereby preventing calcium levels increase by other revenues.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:101278"),
            (BQB.IS, "ncit/C61725"),
        ],
    ),
    Substance(
        sid="anticonvulsants",
        name="anticonvulsants",
        description="Medicine to stop, prevent, or control seizures (convulsions).",
        annotations=[
            (BQB.IS, "chebi/CHEBI:35623"),
            (BQB.IS, "ncit/C264"),
        ],
        synonyms=["Anticonvulsant Agent"],
    ),
    Substance(
        sid="ranitidine",
        name="ranitidine",
        description="A member of the class of histamine H2-receptor antagonists with antacid activity. Ranitidine is "
        "a competitive and reversible inhibitor of the action of histamine, released by "
        "enterochromaffin-like (ECL) cells, at the histamine H2-receptors on parietal cells in the "
        "stomach, thereby inhibiting the normal and meal-stimulated secretion of stomach acid.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:8776"),
            (BQB.IS, "ncit/C29412"),
        ],
    ),
    Substance(
        sid="analgesics",
        name="analgesics",
        description="Compounds that alleviate pain without loss of consciousness. Analgesics act by various mechanisms "
        "including binding with opioid receptors and decreasing inflammation. Choice of analgesic may be "
        "determined by the type of pain. These compounds include opioid, non-opioid and adjuvant "
        "analgesic agents.",
        annotations=[
            (BQB.IS, "ncit/C241"),
        ],
        synonyms=["Analgesic Agent"],
    ),
    Substance(
        sid="isoniazid",
        name="isoniazid",
        description="Isoniazid, also known as isonicotinic acid hydrazide (INH), is an antibiotic used "
        "for the treatment of tuberculosis.A carbohydrazide obtained by formal condensation between "
        "pyridine-4-carboxylic acid and hydrazine.",
        annotations=[(BQB.IS, "chebi/CHEBI:6030")],
        synonyms=["isonicotinic acid hydrazide", "INH"],
    ),
    Substance(
        sid="sunitinib",
        name="sunitinib",
        description="An indolinone derivative and tyrosine kinase inhibitor with potential antineoplastic activity. "
        "Sunitinib blocks the tyrosine kinase activities of vascular endothelial growth factor receptor "
        "2 (VEGFR2), platelet-derived growth factor receptor b (PDGFRb), and c-kit, thereby inhibiting "
        "angiogenesis and cell proliferation.",
        annotations=[(BQB.IS, "chebi/CHEBI:38940"), (BQB.IS, "ncit/C71622")],
    ),
    Substance(
        sid="armodafinil",
        description="The R-enantiomer of the racemic synthetic agent modafinil with central nervous system (CNS) "
        "stimulant and wakefulness-promoting activities. Although the exact mechanism of action has yet "
        "to be fully elucidated, armodafinil appears to inhibit the reuptake of dopamine by binding to "
        "the dopamine-reuptake pump, which leads to an increase in extracellular dopamine levels in some "
        "brain regions.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:77590"),
            (BQB.IS, "ncit/C65241"),
        ],
    ),
    Substance(
        sid="modafinil sulfone",
        name="modafinil sulfone",
        mass=289.4,
        formula="C15H15NO3S",
        description="Modafinil sulfone (code name CRL-41056) is an achiral, oxidized metabolite of modafinil, "
        "a wakefulness-promoting agent. It is one of two major circulating metabolites of modafinil, "
        "the other being modafinil acid. Modafinil sulfone is also a metabolite of the modafinil prodrug, "
        "adrafinil. Modafinil sulfone is also a metabolite of armodafinil, the (R)-(–)-enantiomer of "
        "modafinil.",
        annotations=[
            (BQB.IS, "pubchem.compound/6460146"),
            (BQB.IS, "inchikey/ZESNOWZYHYRSRY-UHFFFAOYSA-N"),
        ],
    ),
    Substance(
        sid="imatinib",
        description="An antineoplastic agent that inhibits the Bcr-Abl fusion protein tyrosine kinase, an abnormal "
        "enzyme produced by chronic myeloid leukemia cells that contain the Philadelphia chromosome.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:45783"),
            (BQB.IS, "ncit/C62035"),
        ],
    ),
    Substance(
        sid="phenobarbital",
        description="A long-acting barbituric acid derivative with antipsychotic property. Phenobarbital binds to "
        "and activates the gamma-aminobutyric acid (GABA)-A receptor, thereby mimicking the inhibitory "
        "actions of GABA in the brain.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:8069"),
            (BQB.IS, "ncit/C739"),
        ],
    ),
    Substance(
        sid="chlordiazepoxide",
        description="A long-acting benzodiazepine with anxiolytic, sedative and hypnotic activity. "
        "Chlordiazepoxide exerts its effect by binding to the benzodiazepine site at the "
        "gamma-aminobutyric acid (GABA) receptor-chloride ionophore complex in the central "
        "nervous system (CNS).",
        annotations=[
            (BQB.IS, "chebi/CHEBI:3611"),
            (BQB.IS, "ncit/C47443"),
        ],
        synonyms=["Librium"],
    ),
    # aspirin related
    Substance(
        sid="acetylsalicylic-acid",
        name="acetylsalicylic acid",
        description="An orally administered non-steroidal antiinflammatory agent. Acetylsalicylic acid "
        "binds to and acetylates serine residues in cyclooxygenases, resulting in decreased synthesis "
        "of prostaglandin, platelet aggregation, and inflammation. This agent exhibits analgesic, "
        "antipyretic, and anticoagulant properties.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:15365"),
            (BQB.IS, "ncit/C287"),
        ],
        synonyms=["aspirin"],
    ),
    Substance(
        sid="salicylamide",
        description="Salicylamide. Metabolite of acetylsalicylic acid. The simplest member of the class of "
        "salicylamides derived from salicylic acid.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:32114"),
            (BQB.IS, "ncit/C80566"),
        ],
    ),
    Substance(
        sid="salicylamide-glucuronide",
        name="salicylamide glucuronide",
        description="Salicylamide glucuronide. Metabolite of acetylsalicylic acid.",
        mass="313.26",
        formula="C13H15NO8",
        annotations=[
            (BQB.IS, "inchikey/AEMUKQHDNNVAES-CDHFTJPESA-N"),
            (BQB.IS, "pubchem.compound/161246"),
        ],
    ),
    Substance(
        sid="salicylamide-sulfate",
        name="salicylamide sulfate",
        description="Salicylamide sulfate. Metabolite of acetylsalicylic acid.",
        mass="235.22",
        formula="C7H9NO6S",
        annotations=[
            (BQB.IS, "inchikey/MHPZPRHLRNMUOW-UHFFFAOYSA-N"),
            (BQB.IS, "pubchem.compound/67804972"),
        ],
        synonyms=["2-Hydroxybenzamide;sulfuric acid"],
    ),
    Substance(
        sid="salicylic-acid",
        name="salicylic acid",
        description="Salicylic acid. Metabolite of acetylsalicylic acid. A beta hydroxy acid that occurs as a natural "
        "compound in plants. It has direct activity as an anti-inflammatory agent and acts as a topical "
        "antibacterial agent due to its ability to promote exfoliation.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:16914"),
            (BQB.IS, "ncit/C61934"),
        ],
    ),
    Substance(
        sid="1-salicylate-glucuronide",
        name="1-salicylate glucuronide",
        description="1-salicylate glucuronide. Metabolite of acetylsalicylic acid. A beta-D-glucosiduronic acid that "
        "is the glucuronide conjugate of salicyclic acid.",
        annotations=[(BQB.IS, "chebi/CHEBI:73961")],
    ),
    Substance(
        sid="salicyluric-acid",
        name="salicyluric acid",
        description="Salicyluric acid. Metabolite of acetylsalicylic acid. An N-acylglycine in which the acyl group "
        "is specified as 2-hydroxybenzoyl.",
        annotations=[(BQB.IS, "chebi/CHEBI:9008")],
    ),
    # misc
    Substance(
        sid="spironolactone",
        description="A steroid lactone that is 17α-pregn-4-ene-21,17-carbolactone substituted by an oxo group at "
        "position 3 and an α-acetylsulfanyl group at position 7.",
        annotations=[(BQB.IS, "chebi/CHEBI:9241")],
    ),
    Substance(
        sid="mefenamic acid",
        description="An anthranilic acid and non-steroidal anti-inflammatory drug (NSAID) with anti-inflammatory, "
        "antipyretic and analgesic activities. Mefenamic acid inhibits the activity of the enzymes "
        "cyclo-oxygenase I and II, resulting in a decreased formation of precursors of prostaglandins "
        "and thromboxanes.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:6717"),
            (BQB.IS, "ncit/C47599"),
        ],
    ),
    Substance(
        sid="amiloride",
        annotations=[(BQB.IS, "chebi/CHEBI:2639")],
        description="A member of the class of pyrazines resulting from the formal "
        "monoacylation of guanidine with the carboxy group of "
        "3,5-diamino-6-chloropyrazine-2-carboxylic acid.",
    ),
    Substance(
        sid="glibenclamide",
        name="glibenclamide",
        label="glibenclamide (glyburide)",
        description="Glyburide is a sulfonamide urea derivative with antihyperglycemic activity that can potentially "
        "be used to decrease cerebral edema. Upon administration, glyburide binds to and blocks the "
        "sulfonylurea receptor type 1 (SUR1) subunit of the ATP-sensitive inwardly-rectifying potassium "
        "(K(ATP)) channels on the membranes of pancreatic beta cells.",
        mass="494",
        formula="C23H28ClN3O5S",
        annotations=[
            (BQB.IS, "pubchem.compound/3488"),
            (BQB.IS, "inchikey/ZNNLBTZKUZBEKO-UHFFFAOYSA-N"),
        ],
        synonyms=["glyburide", "glybenclamide", "micronase"],
    ),
    Substance(
        sid="tizanidine",
        name="tizanidine",
        description="Tizanidine, sold under the brand name Zanaflex among others, is a medication that is used to "
        "treat muscle spasticity due to spinal cord injury or multiple sclerosis. Effectiveness appears "
        "similar to baclofen or diazepam. It is taken by mouth.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:63629"),
            (BQB.IS, "ncit/C61976"),
        ],
    ),
    Substance(
        sid="venlafaxine",
        name="venlafaxine",
        description="A synthetic phenethylamine bicyclic derivative with antidepressant activity. Venlafaxine and "
        "its active metabolite, O-desmethylvenlafaxine (ODV), are potent inhibitors of neuronal serotonin "
        "and norepinephrine reuptake and weak dopamine reuptake inhibitors.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:9943"),
            (BQB.IS, "ncit/C1278"),
        ],
    ),
    Substance(
        sid="lomefloxacin",
        name="lomefloxacin",
        description="A fluoroquinolone antibiotic, used (generally as the hydrochloride salt) to treat bacterial "
        "infections including bronchitis and urinary tract infections. A synthetic broad-spectrum "
        "fluoroquinolone with antibacterial activity. Lomefloxacin inhibits "
        "DNA gyrase, a type II topoisomerase involved in the induction or relaxation of supercoiling "
        "during DNA replication.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:116278"),
            (BQB.IS, "ncit/C61814"),
        ],
    ),
    Substance(
        sid="ephedrine",
        name="ephedrine",
        description="An alkaloid that is an hydroxylated form of phenethylamineand sympathomimetic amine, with "
        "potential bronchodilatory and anti-hypotensive activities. Following administration, "
        "ephedrine activates post-synaptic noradrenergic receptors.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:15407"),
            (BQB.IS, "ncit/C472"),
        ],
    ),
    Substance(
        sid="pseudoephedrine",
        name="pseudoephedrine",
        description="A phenethylamine and a diastereomer of ephedrine with sympathomimetic property. "
        "Pseudoephedrine displaces norepinephrine from storage vesicles in presynaptic neurones, "
        "thereby releasing norepinephrine into the neuronal synapses where it stimulates primarily "
        "alpha-adrenergic receptors.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:51209"),
            (BQB.IS, "ncit/C61914"),
        ],
    ),
    Substance(
        sid="ibuprofen",
        name="ibuprofen",
        description="A propionic acid derivate and nonsteroidal anti-inflammatory drug (NSAID) with "
        "anti-inflammatory, analgesic, and antipyretic effects. Ibuprofen inhibits the activity of "
        "cyclo-oxygenase I and II, resulting in a decreased formation of precursors of prostaglandins "
        "and thromboxanes. This leads to decreased prostaglandin synthesis, by prostaglandin synthase, "
        "the main physiologic effect of ibuprofen.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:5855"),
            (BQB.IS, "ncit/C561"),
        ],
    ),
    Substance(
        sid="flurbiprofen",
        name="flurbiprofen",
        description="A derivative of propionic acid, and a phenylalkanoic acid derivative of non-steroidal "
        "antiinflammatory drugs (NSAIDs) with analgesic, antiinflammatory and antipyretic effects. "
        "Flurbiprofen non-selectively binds to and inhibits cyclooxygenase (COX). This results in a "
        "reduction of arachidonic acid conversion into prostaglandins that are involved in the regulation "
        "of pain, inflammation and fever.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:5130"),
            (BQB.IS, "ncit/C508"),
        ],
    ),
    Substance(
        sid="4-hydroxyflurbiprofen",
        name="4-hydroxyflurbiprofen",
        description="Metabolite of flurbiprofen. 4'-Hydroxyflurbiprofen belongs to the class of organic compounds "
        "known as biphenyls and derivatives. These are organic compounds containing to benzene rings "
        "linked together by a C-C bond. 4'-Hydroxyflurbiprofen is considered to be a practically "
        "insoluble (in water) and relatively neutral molecule.",
        mass="260.26",
        formula="C15H13FO3",
        annotations=[
            (BQB.IS, "pubchem.compound/157678"),
            (BQB.IS, "inchikey/GTSMMBJBNJDFRA-UHFFFAOYSA-N"),
        ],
    ),
    Substance(
        sid="enoxacin",
        name="enoxacin",
        description="Enoxacin belongs to a group called fluoroquinolones. Its mode of action depends upon blocking "
        "bacterial DNA replication by binding itself to DNA gyrase and causing double-stranded breaks in "
        "the bacterial chromosome.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:157175"),
            (BQB.IS, "ncit/C65512"),
        ],
    ),
    Substance(
        sid="pipemidic-acid",
        name="pipemidic acid",
        description="A pyridopyrimidine antibiotic derivative of piromidic acid with activity against gram-negative "
        "bacteria, as well as some gram-positive bacteria. Pipemidic acid exhibits greater activity than "
        "piromidic acid or nalidixic acid.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:75250"),
            (BQB.IS, "ncit/C66394"),
        ],
    ),
    Substance(
        sid="norfloxacin",
        name="norfloxacin",
        description="A synthetic, broad-spectrum fluoroquinolone with antibacterial activity. Norfloxacin inhibits "
        "activity of DNA gyrase, thereby blocking bacterial DNA replication. Norfloxacin concentrates in "
        "the renal tubules and bladder and is bactericidal against a wide range of aerobic gram-positive "
        "and gram-negative organisms.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:100246"),
            (BQB.IS, "ncit/C47638"),
        ],
    ),
    Substance(
        sid="ofloxacin",
        name="ofloxacin",
        description="A fluoroquinolone antibacterial antibiotic. Ofloxacin binds to and inhibits bacterial "
        "topoisomerase II (DNA gyrase) and topoisomerase IV, enzymes involved in DNA replication and "
        "repair, resulting in cell death in sensitive bacterial species.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:7731"),
            (BQB.IS, "ncit/C712"),
        ],
    ),
    Substance(
        sid="ethanol",
        name="ethanol",
        description="A primary alcohol that is ethane in which one of the hydrogens is substituted by a hydroxy group. "
        "A volatile liquid prepared by fermentation of certain carbohydrates. Alcohol acts as a central "
        "nervous system (CNS) depressant, a diuretic, and a disinfectant. Although the exact mechanism of "
        "CNS depression is unknown, alcohol may act by inhibiting the opening of calcium channels, "
        "mediated by the binding of the inhibitory neurotransmitter gamma-amino butyric acid (GABA) "
        "to GABA-A receptors, or through inhibitory actions at N-methyl-D-aspartate (NMDA)-type glutamate "
        "receptors.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:16236"),
            (BQB.IS, "ncit/C2190"),
        ],
        synonyms=["alcohol"],
    ),
    Substance(
        sid="capsaicin",
        name="capsaicin",
        description="Capsaicin an active component of chili peppers, which are plants belonging to the genus Capsicum."
        "It is a chemical irritant for mammals, including humans, and produces a sensation of burning in "
        "any tissue with which it comes into contact.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:3374"),
        ],
        synonyms=["capsaicin"],
    ),
    Substance(
        sid="resveratrol",
        description="Resveratrol is a phytoalexin derived from grapes and other food products with antioxidant and "
        "potential chemopreventive activities. Resveratrol induces phase II drug-metabolizing enzymes ("
        "anti-initiation activity); mediates anti-inflammatory effects and inhibits cyclooxygenase and "
        "hydroperoxidase functions (anti-promotion activity); and induces promyelocytic leukemia cell differentiation "
        "(anti-progression activity), thereby exhibiting activities in three major steps of carcinogenesis.",
        annotations=[
            (BQB.IS, "pubchem.compound/445154"),
            (BQB.IS, "chebi/CHEBI:27881"),
            (BQB.IS, "ncit/C1215"),
            (BQB.IS, "inchikey/LUKBXSAWLPMMSZ-OWOJBTEDSA-N"),
        ],
        synonyms=[],
    ),
    Substance(
        sid="diosmin",
        description="Diosmin is a disaccharide derivative that consists of diosmetin substituted by a "
        "6-O-(alpha-L-rhamnopyranosyl)-beta-D-glucopyranosyl moiety at position 7 via a glycosidic linkage."
        " It has a role as an antioxidant and an anti-inflammatory agent. It is a glycosyloxyflavone, "
        "a rutinoside, a disaccharide derivative, a monomethoxyflavone and a dihydroxyflavanone. "
        "It derives from a diosmetin.",
        annotations=[
            (BQB.IS, "pubchem.compound/5281613"),
            (BQB.IS, "chebi/CHEBI:4631"),
            (BQB.IS, "ncit/C81663"),
            (BQB.IS, "inchikey/GZSOSUNBTXMUFQ-YFAPSIMESA-N"),
        ],
        synonyms=["diosmin", "520-27-4", "Barosmin", "Diosimin", "Venosmine"],
    ),
    Substance(
        sid="chlorzoxazone",
        description="A benzoxazolone derivative with mild sedative and centrally-acting muscle relaxant activities. "
        "Although its exact mechanism of action is unknown, chlorzoxazone (CZ) appears to act at the "
        "spinal cord and subcortical levels of the brain to inhibit multisynaptic reflex arcs involved "
        "in producing and maintaining muscle spasms. Liver function test substance used for testing "
        "CYP2E1.",
        annotations=[
            (BQB.IS, "pubchem.compound/2733"),
            (BQB.IS, "chebi/CHEBI:3655"),
            (BQB.IS, "ncit/C28926"),
            (BQB.IS, "inchikey/TZFWDZFKRBELIQ-UHFFFAOYSA-N"),
        ],
        synonyms=["95-25-0", "Paraflex", "Chlorzoxazon"],
    ),
    Substance(
        sid="6-hydroxychlorzoxazone",
        mass=185.56,
        formula="C7H4ClNO3",
        description="Metabolite of chlordiazepoxide. 6-Hydroxychlorzoxazone belongs to the class of organic "
        "compounds known as benzoxazolones. These are organic compounds containing a benzene fused to an "
        "oxazole ring (a five-member aliphatic ring with three carbon atoms, one oxygen atom, and one "
        "nitrogen atom) bearing a ketone group.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:184399"),
            (BQB.IS, "pubchem.compound/2734"),
            (BQB.IS, "inchikey/AGLXDWOTVQZHIQ-UHFFFAOYSA-N"),
        ],
        synonyms=[
            "1750-45-4",
            "5-Chloro-6-hydroxybenzo[d]oxazol-2(3H)-one",
            "6-hydroxy Chlorzoxazone",
            "5-chloro-6-hydroxy-3H-1,3-benzoxazol-2-one",
        ],
    ),
    Substance(
        sid="6-hydroxychlorzoxazone/chlorzoxazone",
        label="6-hydroxychlorzoxazone/chlorzoxazone",
        description="6-hydroxychlorzoxazone/chlorzoxazone used for evaluating hepatic CYP2E1 metabolism.",
        parents=["6-hydroxychlorzoxazone", "chlorzoxazone"],
        synonyms=[],
    ),
    Substance(
        sid="temocapril",
        name="temocapril",
        description="Temocapril is a prodrug-type angiotensin-I converting enzyme (ACE) "
        "inhibitor not approved for use in the United States, but is "
        "approved in Japan and South Korea. Temocapril can also be used in "
        "hemodialysis patients without risk of serious accumulation.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:135771"),
            (BQB.IS, "inchikey/FIQOFIRCTOWDOW-BJLQDIEVSA-N"),
            (BQB.IS, "pubchem.compound/443874"),
        ],
        synonyms=["111902-57-9"],
    ),
    Substance(
        sid="temocaprilat",
        name="temocaprilat",
        description="Temocaprilat is an angiotensin-converting enzyme (ACE) inhibitor "
        "with antihypertensive activity. Temocaprilat competitively binds "
        "to and inhibits ACE, thereby blocking the conversion of "
        "angiotensin I to angiotensin II.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:9436"),
            (BQB.IS, "inchikey/KZVWEOXAPZXAFB-BQFCYCMXSA-N"),
            (BQB.IS, "pubchem.compound/443151"),
        ],
        synonyms=["110221-53-9"],
    ),
    Substance(
        sid="valsartan",
        name="valsartan",
        description="Valsartan is an angiotensin II receptor blocker used alone or "
        "in combination with other agents to treat hypertension and reduce "
        "cardiovascular mortality after myocardial infarction.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:60846"),
            (BQB.IS, "inchikey/ACWBQPMHZXGDFX-QFIPXVFZSA-N"),
        ],
        synonyms=["137862-53-4"],
    ),
    Substance(
        sid="silymarin",
        name="silymarin",
        description="A mixture of flavonoids extracted from seeds of the MILK THISTLE, "
        "Silybum marianum. It consists primarily of silybin and its isomers, "
        "silicristin and silidianin. Silymarin displays antioxidant and "
        "membrane stabilizing activity. It protects various tissues and "
        "organs against chemical injury, and shows potential as an "
        "antihepatoxic agent.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:125451"),
            (BQB.IS, "pubchem.compound/5213"),
            (BQB.IS, "inchikey/ACWBQPMHZXGDFX-QFIPXVFZSA-N"),
        ],
        synonyms=["Legalon"],
    ),
    Substance(
        sid="aminopyrine",
        name="aminopyrine",
        description="Aminophenazone, also known as amidophen or aminopyrine, belongs to the class of organic "
        "compounds known as phenylpyrazoles. Phenylpyrazoles are compounds containing a phenylpyrazole "
        "skeleton, which consists of a pyrazole bound to a phenyl group. Aminophenazone is a drug which "
        "is used formerly widely used as an antipyretic and analgesic in rheumatism, neuritis, and common "
        "colds.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:160246"),
            (BQB.IS, "ncit/C76792"),
            (BQB.IS, "pubchem.compound/6009"),
        ],
        synonyms=["aminophenazone"],
    ),
    Substance(
        sid="14c_aminopyrine",
        name="[14C] aminopyrine",
        description="14C modified aminopyrine.",
        annotations=[(BQB.IS_VERSION_OF, "chebi/CHEBI:160246")],
        synonyms=["aminophenazone"],
    ),
    Substance(
        sid="antipyrine",
        name="antipyrine",
        description="Antipyrine, also known as phenazone or anodynin, belongs to the class of organic compounds known "
        "as phenylpyrazoles. Phenylpyrazoles are compounds containing a phenylpyrazole skeleton, which "
        "consists of a pyrazole bound to a phenyl group.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:31225"),
            (BQB.IS, "ncit/C76794"),
            (BQB.IS, "pubchem.compound/2206"),
        ],
        synonyms=["phenazone", "phenazon"],
    ),
    Substance(
        sid="bsp",
        name="bromsulpthalein",
        description="An organosulfonic acid that consists of phthalide bearing four bromo substituents at positions "
        "4, 5, 6 and 7 as well as two 4-hydroxy-3-sulfophenyl groups both located at position 1.",
        annotations=[(BQB.IS, "chebi/CHEBI:63836")],
        synonyms=["bromosulfophthalein"],
    ),
    Substance(
        sid="phenylalanine",
        name="phenylalanine",
        description="An essential aromatic amino acid in humans (provided by food). Phenylalanine plays a key role "
        "in the biosynthesis of other amino acids and is important in the structure and function of "
        "many proteins and enzymes. Phenylalanine is converted to tyrosine, used in the biosynthesis of "
        "dopamine and norepinephrine neurotransmitters.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:28044"),
            (BQB.IS, "ncit/C29601"),
        ],
    ),
    Substance(
        sid="diclofenac",
        name="diclofenac",
        description="A nonsteroidal benzeneacetic acid derivative with anti-inflammatory activity. "
        "As a nonsteroidal anti-inflammatory drug (NSAID), diclofenac binds and chelates both isoforms "
        "of cyclooxygenase (COX-1 and-2), thereby blocking the conversion of arachidonic acid to "
        "pro-inflammatory-proprostaglandins.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:47381"),
            (BQB.IS, "ncit/C28985"),
        ],
    ),
    Substance(
        sid="glycerol",
        name="glycerol",
        description="A trihydroxyalcohol with localized osmotic diuretic and laxative effects. Glycerin elevates "
        "the blood plasma osmolality thereby extracting water from tissues into interstitial fluid and "
        "plasma. This agent also prevents water reabsorption in the proximal tubule in the kidney "
        "leading to an increase in water and sodium excretion and a reduction in blood volume.",
        annotations=[(BQB.IS, "chebi/CHEBI:17754"), (BQB.IS, "ncit/C29077")],
        synonyms=["glycerin"],
    ),
    Substance(
        sid="ffa",
        name="FFA",
        label="free fatty acids (FFA)",
        description="Free fatty acids (FFA).",
        synonyms=["free fatty acids"],
    ),
    Substance(
        sid="carbamazepine",
        name="carbamazepine",
        description="A tricyclic compound chemically related to tricyclic antidepressants (TCA) with "
        "anticonvulsant and analgesic properties. Carbamazepine exerts its anticonvulsant activity by "
        "reducing polysynaptic responses and blocking post-tetanic potentiation.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:3387"),
            (BQB.IS, "ncit/C341"),
        ],
    ),
    Substance(
        sid="nizatidine",
        name="nizatidine",
        description="A competitive and reversible histamine H2-receptor antagonist with antacid activity. "
        "Nizatidine inhibits the histamine H2-receptors located on the basolateral membrane of the "
        "gastric parietal cell, thereby reducing basal and nocturnal gastric acid secretion, resulting in "
        "a reduction in gastric volume, acidity, and amount of gastric acid released.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:7601"),
            (BQB.IS, "ncit/C29295"),
        ],
    ),
    Substance(
        sid="piperine",
        name="piperine",
        description="A N-acylpiperidine that is piperidine substituted by a (1E,3E)-1-(1,"
        "3-benzodioxol-5-yl)-5-oxopenta-1,3-dien-5-yl group at the nitrogen atom. It is an "
        "alkaloid isolated from the plant Piper nigrum.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:93043"),
            (BQB.IS, "ncit/C72629"),
        ],
    ),
    Substance(
        sid="probenecid",
        name="probenecid",
        description="A benzoic acid derivative with antihyperuricemic property. Probenecid competitively "
        "inhibits the active reabsorption of urate at the proximal tubule in the kidney thereby "
        "increasing urinary excretion of uric acid and lowering serum urate concentrations. This prevents "
        "urate deposition and promotes resolution of existing urate deposits.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:8426"),
            (BQB.IS, "ncit/C772"),
        ],
    ),
    Substance(
        sid="sorbitol",
        name="sorbitol",
        description="A sugar alcohol found in fruits and plants with diuretic, laxative and cathartic property. "
        "Unabsorbed sorbitol retains water in the large intestine through osmotic pressure thereby "
        "stimulating peristalsis of the intestine and exerting its diuretic, laxative and cathartic "
        "effect. ",
        annotations=[
            (BQB.IS, "chebi/CHEBI:30911"),
            (BQB.IS, "ncit/C29462"),
        ],
    ),
    Substance(
        sid="cisapride",
        name="cisapride",
        description="A substituted piperidinyl benzamide prokinetic agent. Cisapride facilitates release of "
        "acetylcholine from the myenteric plexus, resulting in increased gastrointestinal motility. "
        "In addition, cisapride has been found to act as a serotonin agonist, stimulating type 4 "
        "receptors, and a serotonin 5-HT3 receptor antagonist.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:3720"),
            (BQB.IS, "ncit/C1210"),
        ],
    ),
    Substance(
        sid="sulfamethizole",
        name="sulfamethizole",
        description="A broad-spectrum sulfanilamide and a synthetic analog of para-aminobenzoic acid (PABA) with "
        "antibacterial property. Sulfamethizole competes with PABA for the bacterial enzyme "
        "dihydropteroate synthase, thereby preventing the incorporation of PABA into dihydrofolic acid, "
        "the immediate precursor of folic acid.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:9331"),
            (BQB.IS, "ncit/C47736"),
        ],
    ),
    Substance(
        sid="sulfamethizole-acetylated",
        name="sulfamethizole acetylated",
        description="Metabolite of sulfamethizole.",
    ),
    Substance(
        sid="phenylbutazone",
        name="phenylbutazone",
        description="A member of the class of pyrazolidines that is 1,2-diphenylpyrazolidine-3,5-dione "
        "carrying a butyl group at the 4-position. Phenylbutazone, often referred to as 'bute', "
        "is a nonsteroidal anti-inflammatory drug (NSAID) for the short-term treatment of "
        "pain and fever in animals. ",
        annotations=[
            (BQB.IS, "chebi/CHEBI:48574"),
            (BQB.IS, "ncit/C66377"),
        ],
    ),
    Substance(
        sid="l-cysteine",
        name="l-cysteine",
        label="L-cysteine",
        description="An optically active form of cysteine having L-configuration.",
        annotations=[(BQB.IS, "chebi/CHEBI:17561")],
    ),
    Substance(
        sid="atropine",
        name="atropine",
        description="A synthetically-derived form of the endogenous alkaloid isolated from the plant Atropa "
        "belladonna. Atropine functions as a sympathetic, competitive antagonist of muscarinic cholinergic "
        "receptors, thereby abolishing the effects of parasympathetic stimulation. This agent may induce "
        "tachycardia, inhibit secretions, and relax smooth muscles.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:16684"),
            (BQB.IS, "ncit/C28840"),
        ],
    ),
    Substance(
        sid="meperidine",
        name="meperidine",
        description="A synthetic piperidine ester with opioid analgesic activity. Meperidine mimics the actions of "
        "endogenous neuropeptides via opioid receptors, thereby producing the characteristic "
        "morphine-like effects on the mu-opioid receptor, including analgesia, euphoria, sedation, "
        "respiratory depression, miosis, bradycardia and physical dependence.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:6754"),
            (BQB.IS, "ncit/C71632"),
        ],
    ),
    Substance(
        sid="pentazocine",
        name="pentazocine",
        description="Pentazocine, sold under the brand name Talwin among others, is a painkiller used to treat "
        "moderate to severe pain. It is believed to work by activating (agonizing) κ-opioid receptors "
        "(KOR) and blocking (antagonizing) μ-opioid receptors (MOR)",
        annotations=[
            (BQB.IS, "chebi/CHEBI:7982"),
            (BQB.IS, "ncit/C61884"),
        ],
        synonyms=["Talwin"],
    ),
    Substance(
        sid="naloxone",
        name="naloxone",
        description="A thebaine derivate with competitive opioid antagonistic properties. Naloxone reverses the "
        "effects of opioid analgesics by binding to the opioid receptors in the CNS, and inhibiting the "
        "typical actions of opioid analgesics, including analgesia, euphoria, sedation, respiratory "
        "depression, miosis, bradycardia, and physical dependence.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:7459"),
            (BQB.IS, "ncit/C62054"),
        ],
    ),
    Substance(
        sid="pirenzepine",
        name="pirenzepine",
        description="Pirenzepine (Gastrozepin), an M1 selective antagonist, is used in the treatment of peptic "
        "ulcers, as it reduces gastric acid secretion and reduces muscle spasm. It is in a class of drugs "
        "known as muscarinic receptor antagonists - acetylcholine being the neurotransmitter of the "
        "parasympathetic nervous system which initiates the rest-and-digest state "
        "(as opposed to fight-or-flight), resulting in an increase in gastric motility and digestion.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:8247"),
            (BQB.IS, "ncit/C76002"),
        ],
        synonyms=["gastrozepin"],
    ),
    Substance(
        sid="desipramine",
        name="desipramine",
        description="An active metabolite of imipramine, a tertiary amine and a synthetic tricyclic derivative of "
        "the antidepressant. Desipramine enhances monoamine neurotransmission in certain areas of the "
        "brain by inhibiting the re-uptake of noradrenaline and serotonin at the noradrenergic and "
        "serotoninergic nerve endings, respectively.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:47781"),
            (BQB.IS, "ncit/C61700"),
        ],
    ),
    Substance(
        sid="metoclopramide",
        name="metoclopramide",
        description="A substituted benzamide and a derivative of para-aminobenzoic acid (PABA) that is "
        "structurally related to procainamide, with gastroprokinetic and antiemetic effects. "
        "Metoclopramide exerts its prokinetic effect by antagonizing dopamine mediated relaxation effect "
        "on gastrointestinal smooth muscle. This enhances the response of the gastrointestinal smooth "
        "muscle to cholinergic stimulation, thereby leading to an increase of gastric emptying into "
        "the intestines.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:107736"),
            (BQB.IS, "ncit/C62046"),
        ],
    ),
    Substance(
        sid="propantheline",
        name="propantheline",
        description="Propantheline (INN) is an antimuscarinic agent used for the treatment of excessive sweating "
        "(hyperhidrosis), cramps or spasms of the stomach, intestines (gut) or bladder, and involuntary "
        "urination (enuresis). It can also be used to control the symptoms of irritable bowel syndrome "
        "and similar conditions.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:8481"),
            (BQB.IS, "ncit/C78077"),
        ],
    ),
    Substance(
        sid="chloroquine",
        name="chloroquine",
        description="A 4-aminoquinoline with antimalarial, anti-inflammatory, and potential chemosensitization "
        "and radiosensitization activities. Although the mechanism is not well understood, chloroquine "
        "is shown to inhibit the parasitic enzyme heme polymerase that converts the toxic heme into "
        "non-toxic hemazoin, thereby resulting in the accumulation of toxic heme within the parasite.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:3638"),
            (BQB.IS, "ncit/C61671"),
        ],
    ),
    Substance(
        sid="halothane",
        name="halothane",
        description="A nonflammable, halogenated, hydrocarbon and general inhalation anesthetic. Although the exact "
        "mechanism of action is unknown, halothane provides relatively rapid induction of anesthesia "
        "by depressing the central nervous system, thereby producing a reversible loss of consciousness "
        "and sensation.",
        annotations=[(BQB.IS, "chebi/CHEBI:5615"), (BQB.IS, "ncit/C47554")],
    ),
    Substance(
        sid="tetrachloromethane",
        name="tetrachloromethane",
        description="Carbon tetrachloride is an organic compound with the chemical formula CCl4.",
        annotations=[(BQB.IS, "chebi/CHEBI:27385")],
    ),
    # FIXME: check and update as protons; used in acid output secretion rate (acid)
    Substance(
        sid="acid",
        name="acid",
        description="Protons determined by titration to pH with base.",
        annotations=[],
    ),
    # ----------------------
    # bicarbonate
    # ----------------------
    Substance(
        sid="hydrogencarbonate",
        name="hydrogencarbonate",
        description="The carbon oxoanion resulting from the removal of a proton from carbonic acid.",
        annotations=[(BQB.IS, "chebi/CHEBI:17544")],
    ),
    Substance(
        sid="sodium hydrogencarbonate",
        name="sodium hydrogencarbonate",
        description="Sodium bicarbonate (IUPAC name: sodium hydrogen carbonate), commonly known as baking soda "
        "(especially in North America and New Zealand) or bicarbonate of soda, is a chemical compound "
        "with the formula NaHCO3.",
        annotations=[(BQB.IS, "chebi/CHEBI:32139")],
    ),
    # ----------------------
    # benzodiazepenes
    # ----------------------
    Substance(
        sid="lorazepam",
        name="lorazepam",
        description="A benzodiazepine with anxiolytic, anti-anxiety, anticonvulsant, anti-emetic and sedative "
        "properties. Lorazepam enhances the effect of the inhibitory neurotransmitter gamma-aminobutyric "
        "acid on the GABA receptors by binding to a site that is distinct from the GABA binding site in "
        "the central nervous system.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:6539"),
            (BQB.IS, "ncit/C619"),
        ],
    ),
    Substance(
        sid="lorazepam-glucuronide",
        name="lorazepam glucuronide",
        description="Metabolite of lorazepam. Lorazepam glucuronide belongs to the class of organic compounds "
        "known as o-glucuronides.",
        mass=497.3,
        formula="C21H18Cl2N2O8",
        annotations=[
            (BQB.IS, "pubchem.compound/62966"),
            (BQB.IS, "inchikey/IWOJSSFCRQKNKN-IFBJMGMISA-N"),
        ],
    ),
    Substance(
        sid="midazolam",
        description="Midazolam, marketed under the trade name Versed, among others, is a benzodiazepine "
        "medication used for anesthesia, procedural sedation, trouble sleeping, and severe agitation.",
        annotations=[
            (BQB.IS, "pubchem.compound/4192"),
            (BQB.IS, "chebi/CHEBI:6931"),
            (BQB.IS, "ncit/C62049"),
            (BQB.IS, "inchikey/DDLIGBOFAVUZHB-UHFFFAOYSA-N"),
        ],
        synonyms=["Versed"],
    ),
    Substance(
        sid="midazolam hydrochloride",
        description="Midazolam, marketed under the trade name Versed, among others, is a benzodiazepine "
        "medication used for anesthesia, procedural sedation, trouble sleeping, and severe agitation.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:6932"),
        ],
    ),
    Substance(
        sid="15n3-midazolam",
        name="15N3-midazolam",
        description="15N3 labeled midazolam.",
    ),
    Substance(
        sid="1-hydroxymidazolam",
        name="1-hydroxymidazolam",
        description="1-hydroxymidazolam. Metabolite of midazolam.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:145330"),
            (BQB.IS, "pubchem.compound/107917"),
            (BQB.IS, "inchikey/QHSMEGADRFZVNE-UHFFFAOYSA-N"),
        ],
    ),
    Substance(
        sid="1-hydroxymidazolam/midazolam",
        name="1-hydroxymidazolam/midazolam",
        description="Midazolam metabolic ratio.",
        parents=["1-hydroxymidazolam", "midazolam"],
    ),
    Substance(
        sid="4-hydroxymidazolam",
        name="4-hydroxymidazolam",
        description="Metabolite of midazolam.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:145331"),
            (BQB.IS, "pubchem.compound/124449"),
            (BQB.IS, "inchikey/ZYISITHKPKHPKG-UHFFFAOYSA-N"),
        ],
    ),
    Substance(
        sid="1,4-dihydroxymidazolam",
        name="1,4-dihydroxymidazolam",
        description="Metabolite of midazolam.",
        annotations=[(BQB.IS, "chebi/CHEBI:145332")],
    ),
    Substance(
        sid="1-hydroxymidazolam glucuronide",
        name="1-hydroxymidazolam glucuronide",
        description="Metabolite of midazolam.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:145334"),
            (BQB.IS, "pubchem.compound/133640"),
            (BQB.IS, "inchikey/ICIUMXQTLQXWGL-QMDPOKHVSA-N"),
        ],
        synonyms=["1-hydroxymidazolam beta-D-glucuronide", "Midazolam-N-glucuronide"],
    ),
    Substance(
        sid="4-hydroxymidazolam glucuronide",
        name="4-hydroxymidazolam glucuronide",
        description="Metabolite of midazolam.",
        annotations=[(BQB.IS, "chebi/CHEBI:145335")],
        synonyms=["4-hydroxymidazolam beta-D-glucuronide"],
    ),
    Substance(
        sid="diazepam",
        name="diazepam",
        description="A benzodiazepine derivative with anti-anxiety, sedative, hypnotic and anticonvulsant properties. "
        "Diazepam potentiates the inhibitory activities of gamma-aminobutyric acid (GABA) by binding to "
        "the GABA receptor, located in the limbic system and the hypothalamus.",
        annotations=[(BQB.IS, "chebi/CHEBI:49575")],
    ),
    Substance(
        sid="nordazepam",
        name="nordazepam",
        description="Nordazepam (INN; marketed under brand names Nordaz, Stilny, Madar, Vegesan, and Calmday; also "
        "known as nordiazepam, desoxydemoxepam, and desmethyldiazepam) is a 1,4-benzodiazepine derivative. "
        "Like other benzodiazepine derivatives, it has amnesic, anticonvulsant, anxiolytic, "
        "muscle relaxant, and sedative properties. However, it is used primarily in the treatment of "
        "anxiety disorders. It is an active metabolite of diazepam, chlordiazepoxide, clorazepate, "
        "prazepam, pinazepam, and medazepam.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:111762"),
            (BQB.IS, "ncit/C87675"),
        ],
        synonyms=["desmethyldiazepam"],
    ),
    Substance(
        sid="oxazepam",
        name="oxazepam",
        description="A synthetic benzodiazepine derivative with anxiolytic and sedative hypnotic properties. "
        "Although the mechanism of action has not been fully elucidated, oxazepam appears to "
        "enhance gamma-aminobutyric acid (GABA) receptor affinity for GABA, thereby prolonging "
        "synaptic actions of GABA.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:7823"),
            (BQB.IS, "ncit/C47642"),
        ],
    ),
    Substance(
        sid="oxazepam-glucuronide",
        name="oxazepam_glucuronide",
        label="oxazepam glucuronide",
        description="Oxazepam glucuronide belongs to the class of organic compounds known as o-glucuronides. "
        "These are glucuronides in which the aglycone is linked to the carbohydrate unit through an "
        "O-glycosidic bond.",
        mass=462.8,
        formula="C21H19ClN2O8",
        annotations=[
            (BQB.IS, "pubchem.compound/160870"),
            (BQB.IS, "inchikey/FIKQKGFUBZQEBL-IFBJMGMISA-N"),
            (BQB.IS, "ncit/C28982"),
        ],
    ),
    Substance(
        sid="oxaz+oxazglu",
        label="oxazepam + oxazepam glucuronide",
        description="Sum of oxazepam metabolites.",
        parents=["oxazepam", "oxazepam_glucuronide"],
    ),
    Substance(
        sid="temazepam",
        label="temazepam",
        description="Temazepam is a benzodiazepine derivative with antidepressant, sedative, hypnotic and "
        "anticonvulsant properties.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:9435"),
            (BQB.IS, "pubchem.compound/5391"),
        ],
        synonyms=["methyloxazepam"],
    ),
    Substance(
        sid="temazepam-glucuronide",
        name="temazepam_glucuronide",
        label="temazepam glucuronide",
        description="Metabolite of temazepam.",
        mass=476.9,
        formula="C22H21ClN2O8",
        annotations=[
            (BQB.IS, "pubchem.compound/76973794"),
            (BQB.IS, "inchikey/KFYGTOURBGCWNQ-RYQNVSPKSA-N"),
        ],
        synonyms=["methyloxazepam glucuronide"],
    ),
    Substance(
        sid="desmethyldiazepam-conjugated",
        name="desmethyldiazepam conjugated",
        description="Metabolite of desmethyldiazepam.",
    ),
    Substance(
        sid="triazolam",
        description="A triazolobenzodiazepinederivative with sedative-hypnotic property. Triazolam interacts "
        "directly with a specific site on the gamma-aminobutyric acid (GABA)-A-chloride-ionophore receptor "
        "complex located on the neuronal membrane.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:9674"),
            (BQB.IS, "ncit/C29520"),
            (BQB.IS, "omit/0015068"),
        ],
    ),
    Substance(
        sid="diflunisal",
        description="A difluorophenyl derivate of salicylic acid and a nonsteroidal anti-inflammatory drug (NSAID) "
        "with antipyretic, analgesic and anti-inflammatory properties.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:39669"),
            (BQB.IS, "ncit/C47489"),
        ],
    ),
    Substance(
        sid="metoprolol",
        description="Metoprolol, marketed under the tradename Lopressor among others, "
        "is a selective β1 receptor blocker medication.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:6904"),
            (BQB.IS, "inchikey/IUBSYMUCCVWXPE-UHFFFAOYSA-N"),
        ],
        synonyms=["Lopressor"],
    ),
    Substance(
        sid="s-metoprolol",
        name="(S)-metoprolol",
        label="(-)-(S)-metoprolol",
        description="Enantiomer of metoprolol, marketed under the tradename Lopressor among others, "
        "is a selective β1 receptor blocker medication.",
        mass=267.36,
        formula="C15H25NO3",
        charge=0,
        annotations=[
            (BQB.IS_VERSION_OF, "chebi/CHEBI:6904"),
            (BQB.IS, "pubchem.compound/157716"),
            (BQB.IS, "inchikey/IUBSYMUCCVWXPE-AWEZNQCLSA-N"),
        ],
        synonyms=["Lopressor"],
    ),
    Substance(
        sid="r-metoprolol",
        name="(R)-metoprolol",
        label="(-)-(R)-metoprolol",
        description="Enantiomer of metoprolol, marketed under the tradename Lopressor among others, "
        "is a selective β1 receptor blocker medication.",
        mass=267.36,
        formula="C15H25NO3",
        charge=0,
        annotations=[
            (BQB.IS_VERSION_OF, "chebi/CHEBI:6904"),
            (BQB.IS, "pubchem.compound/157717"),
            (BQB.IS, "inchikey/IUBSYMUCCVWXPE-CQSZACIVSA-N"),
        ],
        synonyms=["Lopressor"],
    ),
    Substance(
        sid="alpha-hydroxymetoprolol",
        description="Main metabolite of metoprolol.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:165230"),
            (BQB.IS, "inchikey/OFRYBPCSEMMZHR-UHFFFAOYSA-N"),
        ],
        synonyms=["HM", "H119/66", "H119-66" "H 119/66"],
    ),
    Substance(
        sid="metoprolol-acidic-metabolite",
        name="metoprolol acidic metabolite",
        description="Metabolite of metoprolol.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:83478"),
            (BQB.IS, "pubchem.compound/62936"),
        ],
        synonyms=["MAM", "H117-04", "H117/04", "metoprolol acid", "atenolol acid"],
    ),
    Substance(
        sid="s-metoprolol-acidic-metabolite",
        name="(S)-metoprolol acidic metabolite",
        description="Metabolite of metoprolol.",
        annotations=[],
        synonyms=["S-MAM", "(S)-MAM"],
    ),
    Substance(
        sid="r-metoprolol-acidic-metabolite",
        name="(R)-metoprolol acidic metabolite",
        description="Metabolite of metoprolol.",
        annotations=[],
        synonyms=["R-MAM", "(R)-MAM"],
    ),
    Substance(
        sid="1s-2r-alpha-hydroxymetoprolol",
        name="(1S,2R)-alpha-hydroxymetoprolol",
        description="Main metabolite of metoprolol.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:165230"),  # FIXME: not correct, but mass is identical
        ],
        synonyms=["HM", "H 119/66"],
    ),
    Substance(
        sid="1s-2s-alpha-hydroxymetoprolol",
        name="(1S,2S)-alpha-hydroxymetoprolol",
        description="Main metabolite of metoprolol.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:165230"),  # FIXME: not correct, but mass is identical
        ],
        synonyms=["HM", "H 119/66"],
    ),
    Substance(
        sid="1r-2r-alpha-hydroxymetoprolol",
        name="(1R,2R)-alpha-hydroxymetoprolol",
        description="Main metabolite of metoprolol.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:165230"),  # FIXME: not correct, but mass is identical
        ],
        synonyms=["HM", "H 119/66"],
    ),
    Substance(
        sid="1r-2s-alpha-hydroxymetoprolol",
        name="(1R,2S)-alpha-hydroxymetoprolol",
        description="Main metabolite of metoprolol.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:165230"),  # FIXME: not correct, but mass is identical
        ],
        synonyms=["HM", "H 119/66"],
    ),
    # metoprolol metabolites sum
    Substance(
        sid="met+metoh+mam",
        label="metoprolol + alpha-hydroxymetoprolol + metoprolol-acidic-metabolite",
        description="Sum of metoprolol and its metbolites (often used in radioactivity assays).",
        parents=[
            "metoprolol",
            "alpha-hydroxymetoprolol",
            "metoprolol-acidic-metabolite",
        ],
    ),
    Substance(
        sid="metoh+mam",
        label="alpha-hydroxymetoprolol + metoprolol-acidic-metabolite",
        description="Sum of metoprolol and its metbolites (often used in radioactivity assays).",
        parents=["alpha-hydroxymetoprolol", "metoprolol-acidic-metabolite"],
    ),
    # metoprolol ratios
    Substance(
        sid="s-metoprolol/r-metoprolol",
        label="(S)-metoprolol/(R)-metoprolol",
        description="Metoprolol ratio.",
        parents=["(S)-metoprolol", "(R)-metoprolol"],
    ),
    Substance(
        sid="1s-2r-alpha-hydroxymetoprolol/r-metoprolol",
        label="(1S,2R)-alpha-hydroxymetoprolol/(R)-metoprolol",
        description="Metoprolol ratio.",
        parents=["(1S,2R)-alpha-hydroxymetoprolol", "(R)-metoprolol"],
    ),
    Substance(
        sid="1r-2r-alpha-hydroxymetoprolol/r-metoprolol",
        label="(1R,2R)-alpha-hydroxymetoprolol/(R)-metoprolol",
        description="Metoprolol ratio.",
        parents=["(1R,2R)-alpha-hydroxymetoprolol", "(R)-metoprolol"],
    ),
    Substance(
        sid="1s-2s-alpha-hydroxymetoprolol/s-metoprolol",
        label="(1S,2S)-alpha-hydroxymetoprolol/(S)-metoprolol",
        description="Metoprolol ratio.",
        parents=["(1S,2S)-alpha-hydroxymetoprolol", "(S)-metoprolol"],
    ),
    Substance(
        sid="1r-2s-alpha-hydroxymetoprolol/s-metoprolol",
        label="(1R,2S)-alpha-hydroxymetoprolol/(S)-metoprolol",
        description="Metoprolol ratio.",
        parents=["(1R,2S)-alpha-hydroxymetoprolol", "(S)-metoprolol"],
    ),
    Substance(
        sid="r-metoprolol-acidic-metabolite/r-metoprolol",
        label="(R)-metoprolol acidic metabolite/(R)-metoprolol",
        description="Metoprolol ratio.",
        parents=["(R)-metoprolol acidic metabolite", "(R)-metoprolol"],
    ),
    Substance(
        sid="s-metoprolol-acidic-metabolite/s-metoprolol",
        label="(S)-metoprolol acidic metabolite/(S)-metoprolol",
        description="Metoprolol ratio.",
        parents=["(S)-metoprolol acidic metabolite", "(S)-metoprolol"],
    ),
    Substance(
        sid="metoprolol/alpha-hydroxymetoprolol",
        label="metoprolol/alpha-hydroxymetoprolol",
        description="Metoprolol/alpha-hydroxymetoprolol ratio.",
        parents=["metoprolol", "alpha-hydroxymetoprolol"],
    ),
    Substance(
        sid="metoprolol-tartrate",
        name="metoprolol tartrate",
        description="The tartrate salt form of metoprolol, a cardioselective "
        "competitive beta-1 adrenergic receptor antagonist with "
        "antihypertensive properties and devoid of intrinsic "
        "sympathomimetic activity. Metoprolol tartrate antagonizes "
        "beta 1-adrenergic receptors in the myocardium, thereby reducing "
        "the rate and force of myocardial contraction, and consequently "
        "a diminished cardiac output.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:6906"),
            (BQB.IS, "ncit/C29255"),
        ],
        synonyms=[],
    ),
    Substance(
        sid="warfarin",
        name="warfarin",
        description="A synthetic anticoagulant. Warfarin inhibits the regeneration of "
        "vitamin K1 epoxide and so the synthesis of vitamin K dependent clotting "
        "factors, which include Factors II, VII, IX and X, and the anticoagulant "
        "proteins C and S.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:10033"),
            (BQB.IS, "ncit/C945"),
        ],
    ),
    Substance(
        sid="r-warfarin",
        name="r-warfarin",
        description="A synthetic anticoagulant. Warfarin inhibits the regeneration of "
        "vitamin K1 epoxide and so the synthesis of vitamin K dependent clotting "
        "factors, which include Factors II, VII, IX and X, and the anticoagulant "
        "proteins C and S.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:87737"),
        ],
    ),
    Substance(
        sid="s-warfarin",
        name="s-warfarin",
        description="A synthetic anticoagulant. Warfarin inhibits the regeneration of "
        "vitamin K1 epoxide and so the synthesis of vitamin K dependent clotting "
        "factors, which include Factors II, VII, IX and X, and the anticoagulant "
        "proteins C and S.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:87738"),
        ],
    ),
    Substance(
        sid="rifampicin",
        name="rifampicin",
        description="A member of the class of rifamycins that is a a semisynthetic "
        "antibiotic derived from Amycolatopsis rifamycinica (previously known as "
        "Amycolatopsis mediterranei and Streptomyces mediterranei).",
        annotations=[(BQB.IS, "chebi/CHEBI:28077")],
        synonyms=["rifampin", "Rifampicin"],
    ),
    Substance(
        sid="rifaximin",
        description="An orally administered, semi-synthetic, nonsystemic antibiotic derived "
        "from rifamycin SV with antibacterial activity. Rifaximin binds to the "
        "beta-subunit of bacterial DNA-dependent RNA polymerase, inhibiting "
        "bacterial RNA synthesis and bacterial cell growth.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:75246"),
            (BQB.IS, "ncit/C61926"),
        ],
    ),
    Substance(
        sid="ketoconazole",
        description="Ketoconazole. A synthetic derivative of phenylpiperazine with broad antifungal properties and "
        "potential antineoplastic activity.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:47519"),
            (BQB.IS, "ncit/C605"),
        ],
    ),
    Substance(
        sid="alfentanil",
        description="Alfentanil (R-39209, trade name Alfenta, Rapifen in Australia) is a potent but "
        "short-acting synthetic opioid analgesic drug, used for anaesthesia in surgery. "
        "It is an analogue of fentanyl with around 1/4 to 1/10 the potency of fentanyl and "
        "around 1/3 of the duration of action, but with an onset of effects 4x faster than fentanyl.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:2569"),
        ],
        synonyms=["Alfentanil", "R-39209", "Alfenta", "Rapifen"],
    ),
    Substance(
        sid="sufentanil",
        description="Sufentanil is an opioid analgesic that is used as an adjunct in anesthesia, in balanced "
        "anesthesia, and as a primary anesthetic agent. It is administered by the intravenous, epidural "
        "and sublingual routes.",
        annotations=[
            (BQB.IS, "pubchem.substance/41693"),
            (BQB.IS, "chebi/CHEBI:9316"),
        ],
        synonyms=["Sufentanil"],
    ),
    Substance(
        sid="efavirenz",
        description="A synthetic non-nucleoside reverse transcriptase (RT) inhibitor with antiviral activity. "
        "Efavirenz binds directly to the human immunodeficiency virus type 1 (HIV-1) RT, an "
        "RNA-dependent DNA polymerase, blocking its function in viral DNA replication.",
        annotations=[
            (BQB.IS, "ncit/C29027"),
            (BQB.IS, "chebi/CHEBI:119486"),
        ],
        synonyms=["Efavirenz"],
    ),
    Substance(
        sid="paclitaxel",
        description="A compound extracted from the Pacific yew tree Taxus brevifolia with antineoplastic activity. "
        "Paclitaxel binds to tubulin and inhibits the disassembly of microtubules, thereby resulting "
        "in the inhibition of cell division.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:45863"),
            (BQB.IS, "ncit/C1411"),
        ],
        synonyms=["Paclitaxel"],
    ),
    Substance(
        sid="troleandomycin",
        description="Troleandomycin (TAO) is a macrolide antibiotic. It was sold in Italy (branded Triocetin) and "
        "Turkey (branded Tekmisin).",
        annotations=[
            (BQB.IS, "chebi/CHEBI:45735"),
            (BQB.IS, "ncit/C66643"),
        ],
        synonyms=["TAO"],
    ),
    Substance(
        sid="erythromycin",
        description="Erythromycin is an antibiotic used for the treatment of a number of bacterial infections.",
        annotations=[(BQB.IS, "chebi/CHEBI:48923")],
        synonyms=["Erythromycin"],
    ),
    Substance(
        sid="[14C N-methyl] erythromycin",
        description="14C modified erythromycin.",
        annotations=[(BQB.IS_VERSION_OF, "chebi/CHEBI:48923")],
    ),
    Substance(
        sid="amikacin",
        description="Amikacin is an antibiotic used for a number of bacterial infections.",
        annotations=[(BQB.IS, "chebi/CHEBI:2637")],
        synonyms=["Amikacin"],
    ),
    Substance(
        sid="vancomycin",
        description="Vancomycin is an antibiotic used to treat a number of bacterial infections.",
        annotations=[(BQB.IS, "chebi/CHEBI:28001")],
        synonyms=["Vancomycin"],
    ),
    Substance(
        sid="itraconazole",
        description="A synthetic triazole agent with antimycotic properties. Formulated for both topical and "
        "systemic use, itraconazole preferentially inhibits fungal cytochrome P450 enzymes, resulting in "
        "a decrease in fungal ergosterol synthesis.",
        annotations=[
            (BQB.IS, "ncit/C1138"),
            (BQB.IS, "chebi/CHEBI:6076"),
        ],
        synonyms=["Itraconazole"],
    ),
    Substance(
        sid="hydroxyitraconazole",
        description="Active metabolite of itraconazole",
        mass="721.6",
        formula="C35H38Cl2N8O5",
        annotations=[
            (BQB.IS, "pubchem.substance/108222"),
            (BQB.IS, "inchikey/ISJVOEOJQLKSJU-UHFFFAOYSA-N"),
            (BQB.IS, "wikidata/Q27237315"),
        ],
        synonyms=["Hydroxy-Itraconazole", "Hydroxy Itraconazole"],
    ),
    Substance(
        sid="ketoitraconazole",
        description="Metabolite of itraconazole",
        mass="719.6",
        formula="C35H36Cl2N8O5",
        annotations=[
            (BQB.IS, "pubchem.substance/53865186"),
            (BQB.IS, "inchikey/GZEZATDDANETAV-CEAPFGRNSA-N"),
        ],
        synonyms=["Keto-Itraconazole"],
    ),
    Substance(
        sid="n-desalkyl-itraconazole",
        description="Metabolite of itraconazole",
        mass="649.5",
        formula="C31H30Cl2N8O4",
        annotations=[
            (BQB.IS, "pubchem.substance/53789808"),
            (BQB.IS, "inchikey/FBAPZOQKYAPBHI-DLFZDVPBSA-N"),
        ],
        synonyms=["N-desalkyl-Itraconazole"],
    ),
    Substance(
        sid="clarithromycin",
        description="The 6-O-methyl ether of erythromycin A, clarithromycin is a macrolide antibiotic used in the "
        "treatment of respiratory-tract, skin and soft-tissue infections. It is also used to eradicate "
        "Helicobacter pylori in the treatment of peptic ulcer disease.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:3732"),
            (BQB.IS, "ncit/C1054"),
        ],
    ),
    Substance(
        sid="14-hydroxyclarithromycin",
        description="Metabolite of clarithromycin.",
        mass=764,
        formula="C38H69NO14",
        annotations=[
            (BQB.IS, "pubchem.substance/84020"),
            (BQB.IS, "inchikey/BLPFDXNVUDZBII-KNPZYKNQSA-N"),
        ],
        synonyms=[
            "14-OH-Clarithromycin",
            "14-ahydroxy-a6-aO-amethyl-Erythromycin",
            "14-Hydroxy-6-O-methylerythromycin",
        ],
    ),
    Substance(
        sid="n-desmethylclarithromycin",
        label="N-Desmethylclarithromycin",
        description="Metabolite of clarithromycin.",
        mass=733.9,
        formula="C37H67NO13",
        annotations=[
            (BQB.IS, "pubchem.substance/11072636"),
            (BQB.IS, "inchikey/CIJTVUQEURKBDL-RWJQBGPGSA-N"),
        ],
        synonyms=["N-Desmethyl Clarithromycin", "N-Desmethylclarithromycin"],
    ),
    Substance(
        sid="clotrimazole",
        description="A synthetic, imidazole derivate with broad-spectrum, antifungal activity. Clotrimazole inhibits "
        "biosynthesis of sterols, particularly ergosterol, an essential component of the fungal cell "
        "membrane, thereby damaging and affecting the permeability of the cell membrane.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:3764"),
            (BQB.IS, "ncit/C381"),
            (BQB.IS, "omit/0004332"),
        ],
    ),
    Substance(
        sid="xanthine",
        description="A purine nucleobase found in humans and other organisms.",
        annotations=[(BQB.IS, "chebi/CHEBI:15318")],
    ),
    # tolbutamide
    Substance(
        sid="tolbutamide",
        description="A short-acting, first-generation sulfonylurea with hypoglycemic activity. Compared to "
        "second-generation sulfonylureas, tolbutamide is more likely to cause adverse effects, such as "
        "jaundice. This agent is rapidly metabolized by CYPC29.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:27999"),
            (BQB.IS, "ncit/C66610"),
        ],
    ),
    Substance(
        sid="4-hydroxytolbutamide",
        description="Metabolite of tolbutamide. A urea that consists of 1-butylurea having a "
        "4-hydroxymethylbenzenesulfonyl group attached at the 3-position.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:63799"),
        ],
    ),
    Substance(
        sid="losartan",
        description="A non-peptide angiotensin II antagonist with antihypertensive activity. Upon administration, "
        "losartan and its active metabolite selectively and competitively blocks the binding of "
        "angiotensin II to the angiotensin I (AT1) receptor.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:6541"),
            (BQB.IS, "ncit/C66869"),
        ],
    ),
    Substance(
        sid="exp3174",
        name="exp3174",
        label="Losartan carboxylic acid (E3174)",
        description="Metabolite of losartan. Losartan carboxylic acid is a biphenylyltetrazole that is losartan with "
        "the hydroxymethyl group at position 5 on the imidazole ring replaced with a carboxylic acid.",
        synonyms=["E3174", "Losartan carboxylic acid"],
        annotations=[
            (BQB.IS, "pubchem.compound/108185"),
            (BQB.IS, "chebi/CHEBI:74125"),
        ],
    ),
    Substance(
        sid="omeprazole",
        description="A benzimidazole with selective and irreversible proton pump inhibition activity. Omeprazole "
        "forms a stable disulfide bond with the sulfhydryl group of the hydrogen-potassium (H+ - K+) "
        "ATPase found on the secretory surface of parietal cells, thereby inhibiting the final "
        "transport of hydrogen ions (via exchange with potassium ions) into the gastric lumen and "
        "suppressing gastric acid secretion.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:7772"),
            (BQB.IS, "ncit/C716"),
            (BQB.IS, "inchikey/SUBDBMMJDZJVOS-UHFFFAOYSA-N"),
        ],
        formula="C17H19N3O3S",
        mass=345.4,
    ),
    Substance(
        sid="5-hydroxyomeprazole",
        description="Metabolite of omeprazole. A sulfoxide that is omeprazole in which one of the methyl hydrogens "
        "at position 5 on the pyridine ring is substituted by a hydroxy group.",
        annotations=[(BQB.IS, "chebi/CHEBI:63840")],
    ),
    Substance(
        sid="omeprazole-sulfone",
        name="omeprazole sulfone",
        description="Metabolite of omeprazole.",
        annotations=[(BQB.IS, "chebi/CHEBI:166518")],
        synonyms=["omeprazole sulphone"],
    ),
    Substance(
        sid="5home/ome",
        label="5-hydroxyomeprazole/omeprazole",
        description="Metabolite ratio of omeprazole. 5-hydroxyomeprazole/omeprazole",
        parents=["omeprazole", "5-hydroxyomeprazole"],
    ),
    Substance(
        # FIXME: this is not complete, other possible metabolites: omeprazole acid, omeprazole sulfide,
        sid="omeprazole-metabolites",
        name="omeprazole metabolites",
        description="Omeprazole and omeprazole metabolites",
        parents=["omeprazole", "5-hydroxyomeprazole", "omeprazole-sulfone"],
    ),
    Substance(
        sid="pepsin",
        description="Pepsin. Pepsin is an endopeptidase that breaks down proteins into smaller peptides.",
        parents=[],
    ),
    Substance(
        sid="pentagastrin",
        description="entagastrin is a synthetic polypeptide that has effects like gastrin when given parenterally. "
        "It stimulates the secretion of gastric acid, pepsin, and intrinsic factor, and has been used as a"
        " diagnostic aid as the pentagastrin-stimulated calcitonin test.",
        parents=[],
        annotations=[(BQB.IS, "chebi/CHEBI:31974")],
    ),
    Substance(
        sid="fexofenadine",
        name="fexofenadine",
        description="Fexofenadine is an antihistamine pharmaceutical drug used in the treatment of allergy symptoms, "
        "such as hay fever and urticaria."
        "Fexofenadine is a selective peripheral H1 receptor antagonist. Blockage prevents the activation of the H1 receptors "
        "by histamine, preventing the symptoms associated with allergies from occurring."
        "Taking erythromycin or ketoconazole while taking fexofenadine does increase the plasma levels of fexofenadine, "
        "but this increase does not influence the QT interval. The reason for this effect is likely due to transport-related effects, "
        "specifically involving p-glycoprotein (p-gp).",
        annotations=[
            (BQB.IS, "chebi/CHEBI:5050"),
        ],
    ),
    # dextromethorphan
    Substance(
        sid="dmthbr",
        name="dextromethorphan hydrobromide",
        description="An acid salt containing dextromethorphan and used as dosing substance. "
        "Dextromethorphan Hydrobromide is the hydrobromide salt form of "
        "dextromethorphan, a synthetic, methylated dextrorotary analogue of "
        "levorphanol, a substance related to codeine and a non-opioid "
        "derivate of morphine.",
        mass=352.3,
        annotations=[
            (BQB.IS, "pubchem.compound/5464025"),
            (BQB.IS, "inchikey/MISZALMBODQYFT-URVXVIKDSA-N"),
        ],
        synonyms=["Dormethan", "Metrorat", "Dextromethorphan HBr"],
    ),
    Substance(
        sid="dmt",
        name="dextromethorphan",
        description="A synthetic, methylated dextrorotary analogue of levorphanol, a substance related to codeine "
        "and a non-opioid derivate of morphine. Dextromethorphan exhibits antitussive activity and is "
        "devoid of analgesic or addictive property. This agent crosses the blood-brain-barrier and "
        "activates sigma opioid receptors on the cough center in the central nervous system, thereby "
        "suppressing the cough reflex.",
        # mass=271.4,
        annotations=[
            (BQB.IS, "chebi/CHEBI:4470"),
            (BQB.IS, "ncit/C62022"),
        ],
        synonyms=["DEX", "dex"],
    ),
    Substance(
        sid="dtf",
        name="dextrorphan",
        description="Metabolite of dextromethorphan. Often used in metabolic ratios with dextromethorphan.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:29133"),
            (BQB.IS, "ncit/C171857"),
        ],
        synonyms=["DOR", "dor"],
    ),
    Substance(
        sid="dtfglu",
        name="dextrorphan-glucuronide",
        label="dextrorphan O-glucuronide",
        description="Metabolite of dextromethorphan. Glucuronidation of dextrorphan.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:32645"),
            (BQB.IS, "pubchem.compound/24883428"),
            (BQB.IS, "inchikey/YQAUTKINOXBFCA-DCWOAAMISA-N"),
        ],
        synonyms=["dextrorphan O-glucosiduronic acid"],
    ),
    Substance(
        sid="hm3",
        name="3-hydroxymorphinan",
        description="Metabolite of dextromethorphan.",
        mass=243.34,
        formula="C16H21NO",
        annotations=[
            (BQB.IS, "pubchem.compound/5463854"),
            (BQB.IS, "inchikey/IYNWSQDZXMGGGI-NUEKZKHPSA-N"),
        ],
    ),
    Substance(
        sid="hm3glu",
        name="3-hydroxymorphinan-glucuronide",
        label="3-hydroxymorphinan O-glucuronide",
        description="Metabolite of 3-hydroxymorphinan. Glucuronidation of 3-hydroxymorphinan.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:32645"),
            (BQB.IS, "pubchem.compound/24883428"),
            (BQB.IS, "inchikey/YQAUTKINOXBFCA-DCWOAAMISA-N"),
        ],
        synonyms=["3-hydroxymorphinan O-glucosiduronic acid"],
    ),
    Substance(
        sid="mom3",
        name="3-methoxymorphinan",
        description="Metabolite of dextromethorphan.",
        mass=257.37,
        formula="C17H23NO",
        annotations=[
            (BQB.IS, "pubchem.compound/5484286"),
            (BQB.IS, "inchikey/ILNSWVUXAPSPEH-USXIJHARSA-N"),
        ],
    ),
    Substance(
        sid="dtf+dtfglu",
        description="Sum of dextrorphan and dextrorphan-glucuronide.",
        parents=["dtf", "dtfglu"],
    ),
    Substance(
        sid="hm3+hm3glu",
        description="Sum of 3-hydroxymorphinan and 3-hydroxymorphinan-glucuronide.",
        parents=["hm3", "hm3glu"],
    ),
    Substance(
        sid="(dtf+hm3)/(dmt+mom3)",
        description="Metabolite ratio dextromethorphan.",
        parents=["dtf", "dmt", "hm3", "mom3"],
    ),
    Substance(
        sid="(dtf+dtfglu)/(dmt)",
        description="Less popular metabolite ratio dextromethorphan.",
        parents=["dtf", "dmt", "dtfglu"],
    ),
    Substance(
        sid="(dmt)/(dtf+dtfglu)",
        description="Metabolite ratio dextromethorphan.",
        parents=["dtf", "dmt", "dtfglu"],
    ),
    Substance(
        sid="dmt/(dtf+hm3)",
        description="Dextromethorphan metabolite ratio.",
        parents=["dmt", "dtf", "hm3"],
    ),
    Substance(
        sid="(dmt)/(dtf+dtfglu+hm3+hm3glu)",
        description="Dextromethorphan metabolite ratio. Total dextrorphan (dtf+dtfglu) and total 3-hydroxymorphinan (hm3+hm3glu) are actually measured, if the probe is treated with some form of beta-glucuronidase during the analytic procedure. This ist mostly the case for urine.",
        parents=["dmt", "dtf", "dtfglu", "hm3", "hm3glu"],
    ),
    Substance(
        sid="dmt/dtf",
        label="dextromethorphan/dextrorphan",
        description="Dextromethorphan metabolite ratio. dextromethorphan/dextrorphan.",
        parents=["dmt", "dtf"],
    ),
    Substance(
        sid="dtf/dmt",
        label="dextrorphan/dextromethorphan",
        description="Dextromethorphan metabolite ratio.",
        parents=["dtf", "dmt"],
    ),
    Substance(
        sid="dtf/hm3",
        label="dextrorphan/3-hydroxymorphinan",
        description="Dextrorphan metabolite ratio. dextrorphan/3-hydroxymorphinan.",
        parents=["dtf", "hm3"],
    ),
    Substance(
        sid="(dtf+dtfglu)/(hm3+hm3glu)",
        label="total dextrorphan/ total 3-hydroxymorphinan",
        description="Dextrorphan (metabolite ratio. total dextrorphan (dtf+dtfglu) / total 3-hydroxymorphinan (hm3+hm3glu).",
        parents=["dtf", "dtfglu", "hm3", "dtfglu"],
    ),
    Substance(
        sid="dmt/mom3",
        label="dextromethorphan/3-methoxymorphinan",
        description="Dextromethorphan metabolite ratio. dextrorphan/3-methoxymorphinan.",
        parents=["dmt", "mom3"],
    ),
    Substance(
        sid="dmt/hm3",
        label="dextromethorphan/3-hydroxymorphinan",
        description="Dextromethorphan metabolite ratio. dextrorphan/3-hydroxymorphinan.",
        parents=["dmt", "hm3"],
    ),
    Substance(
        sid="(dmt)/(hm3+hm3glu)",
        label="dextromethorphan/3-hydroxymorphinan",
        description="Dextromethorphan metabolite ratio. dextrorphan/ total 3-hydroxymorphinan (hm3+hm3glu).",
        parents=["dmt", "hm3", "hm3glu"],
    ),
    Substance(
        sid="dtf/mom3",
        label="dextrorphan/3-methoxymorphinan",
        description="Dextromethorphan metabolite ratio. dextrorphan/3-methoxymorphinan",
        parents=["dmt", "hm3"],
    ),
    Substance(
        sid="hm3/mom3",
        label="3-hydroxymorphinan/3-methoxymorphinan",
        description="Dextromethorphan metabolite ratio. 3-hydroxymorphina/3-methoxymorphinan",
        parents=["hm3", "mom3"],
    ),
    Substance(
        sid="(hm3+hm3glu)/(mom3)",
        label="3-hydroxymorphinan/3-methoxymorphinan",
        description="Dextromethorphan metabolite ratio. total 3-hydroxymorphinan (hm3+hm3glu) /3-methoxymorphinan",
        parents=["hm3", "hm3glu", "mom3"],
    ),
    Substance(
        sid="hm3+hm3glu+dtf+dtfglu+dex+mom3",
        description="Total dextrorphan",
        parents=["hm3", "dtf", "dmt", "mom3"],
    ),
    Substance(
        sid="propiverine",
        description="Propiverine is an antimuscarinic agent used to treat urinary incontinence or"
        " increased urinary frequency or urgency.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:8493"),
        ],
        synonyms=[],
    ),
    Substance(
        sid="proguanil",
        description="Proguanil, also known as chlorguanide and chloroguanide, is a medication used "
        "to treat and prevent malaria. It is often used together with chloroquine "
        "or atovaquone. It is taken by mouth. When used alone, proguanil functions as "
        "a prodrug. Its active metabolite, cycloguanil, is an inhibitor of dihydrofolate reductase (DHFR)",
        annotations=[
            (BQB.IS, "chebi/CHEBI:8455"),
        ],
        synonyms=["Proguanil", "Chlorguanide", "Chloroguanide"],
    ),
    Substance(
        sid="proguanil hydrochloride",
        label="proguanil hydrochloride",
        description="Proguanil, also known as chlorguanide and chloroguanide, is a medication used "
        "to treat and prevent malaria. It is often used together with chloroquine "
        "or atovaquone. It is taken by mouth. When used alone, proguanil functions as "
        "a prodrug. Its active metabolite, cycloguanil, is an inhibitor of dihydrofolate reductase (DHFR)",
        parents=["hm3", "mom3"],
        synonyms=[
            "Proguanil hydrochloride",
            "Chlorguanide hydrochloride",
            "Chloroguanide hydrochloride",
        ],
    ),
    Substance(
        sid="digoxin",
        description="Digoxin. A cardiac glycoside. Digoxin inhibits the sodium potassium adenosine triphosphatase "
        "(ATPase) pump, thereby increasing intracellular calcium and enhancing cardiac contractility. "
        "This agent also acts directly on the atrioventricular node to suppress conduction, thereby "
        "slowing conduction velocity.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:4551"),
            (BQB.IS, "ncit/C28990"),
            (BQB.IS, "omit/0005346"),
        ],
        synonyms=["Digoxin"],
    ),
    Substance(
        sid="cinacalcet hydrochloride",
        description="Cinacalcet is a medication used to treat secondary hyperparathyroidism, "
        "parathyroid carcinoma, and primary hyperparathyroidism. "
        "Cinacalcet acts as a calcimimetic (i.e., it mimics the action of calcium on tissues) "
        "by allosteric activation of the calcium-sensing receptor that is expressed in various "
        "human organ tissues. "
        "Cinacalcet is a strong inhibitor of the liver enzyme CYP2D6 and is partially metabolized by CYP3A4 and CYP1A2.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:48391"),
        ],
        synonyms=["cinacalcet hydrochloride"],
    ),
    Substance(
        sid="cinacalcet",
        description="Cinacalcet is a medication used to treat secondary hyperparathyroidism, "
        "parathyroid carcinoma, and primary hyperparathyroidism. "
        "Cinacalcet acts as a calcimimetic (i.e., it mimics the action of calcium on tissues) "
        "by allosteric activation of the calcium-sensing receptor that is expressed in various "
        "human organ tissues. "
        "Cinacalcet is a strong inhibitor of the liver enzyme CYP2D6 and is partially metabolized by CYP3A4 and CYP1A2.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:48390"),
        ],
        synonyms=["cinacalcet"],
    ),
    Substance(
        sid="propofol",
        description="Propofol. A hypnotic alkylphenol derivative. Formulated for intravenous induction of sedation "
        "and hypnosis during anesthesia, propofol facilitates inhibitory neurotransmission mediated by "
        "gamma-aminobutyric acid (GABA).",
        annotations=[
            (BQB.IS, "chebi/CHEBI:44915"),
            (BQB.IS, "ncit/C29384"),
            (BQB.IS, "omit/0016393"),
        ],
        synonyms=["Propofol"],
    ),
    Substance(
        sid="terbinafine",
        description="Terbinafine is an antifungal medication used to treat pityriasis versicolor, fungal nail infections, "
        "and ringworm including jock itch and athlete's foot. It is either taken by mouth or applied to the skin as a cream or ointment. "
        "Like other allylamines, terbinafine inhibits ergosterol synthesis by inhibiting squalene epoxidase, an enzyme that catalyzes the conversion of squalene to lanosterol. "
        "In fungi, lanosterol is then converted to ergosterol; in humans, lanosterol becomes cholesterol. ",
        annotations=[
            (BQB.IS, "chebi/CHEBI:9448"),
        ],
        synonyms=["Terbinafine"],
    ),
    Substance(
        sid="ritonavir",
        description="An L-valine derivative that is L-valinamide in which α-amino group has been acylated by a "
        "[(2-isopropyl-1,3-thiazol-4-yl)methyl]methylcarbamoyl group and in which a hydrogen of "
        "the carboxamide amino group has been replaced by a "
        "(2R,4S,5S)-4-hydroxy-1,6-diphenyl-5-{[(1,3-thiazol-5-ylmethoxy)carbonyl]amino}hexan-2-yl group. "
        "A CYP3A inhibitor and antiretroviral drug from the protease inhibitor class used to treat HIV "
        "infection and AIDS, it is often used as a fixed-dose combination with another protease inhibitor, "
        "lopinavir. Also used in combination with dasabuvir sodium hydrate, ombitasvir and paritaprevir "
        "(under the trade name Viekira Pak) for treatment of chronic hepatitis C virus genotype 1 "
        "infection as well as cirrhosis of the liver.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:45409"),
        ],
        synonyms=["RTV", "Norvir"],
    ),
    Substance(
        sid="paroxetine",
        description="Paroxetine is an antidepressant of the selective serotonin reuptake inhibitor (SSRI) class. "
        "It is used to treat major depressive disorder, obsessive-compulsive disorder, panic disorder, "
        "social anxiety disorder, posttraumatic stress disorder, generalized anxiety disorder and "
        "premenstrual dysphoric disorder. It has also been used in the treatment of premature ejaculation "
        "and hot flashes due to menopause. It is taken by mouth."
        "Paroxetine interacts with the following cytochrome P450 enzymes: "
        "CYP2D6 for which it is both a substrate and a potent inhibitor. "
        "CYP2B6 (strong) inhibitor. "
        "CYP3A4 (weak) inhibitor. "
        "CYP1A2 (weak) inhibitor. "
        "CYP2C9 (weak) inhibitor. "
        "CYP2C19 (weak) inhibitor.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:7936"),
        ],
        synonyms=["paroxetine"],
    ),
    Substance(
        sid="tipranavir",
        description="A pyridine-2-sulfonamide substituted at C-5 by a trifluoromethyl group and at the sulfonamide "
        "nitrogen by a dihydropyrone-containing m-tolyl substituent. It is an HIV-1 protease inhibitor.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:63628"),
        ],
    ),
    Substance(
        sid="vitamin-k",
        name="vitamin K",
        label="vitamin K",
        description="A fat-soluble vitamin required for the synthesis of "
        "prothrombin and certain other blood coagulation factors.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:28384"),
        ],
    ),
    Substance(
        sid="clozapine",
        description="A synthetic dibenzo-diazepine derivative, atypical antipsychotic "
        "Clozapine blocks several neurotransmitter receptors in the brain "
        "(dopamine type 4, serotonin type 2, norepinephrine, acetylcholine, "
        "and histamine receptors). Unlike traditional antipsychotic agents, "
        "it weakly blocks dopamine type 2 receptors. It relieves schizophrenic "
        "symptoms (hallucinations, delusions, dementia).",
        annotations=[
            (BQB.IS, "chebi/CHEBI:3766"),
            (BQB.IS, "ncit/C28936"),
        ],
    ),
    Substance(
        sid="carbon monoxide",
        label="carbon monoxide (CO)",
        description="An odorless, tasteless, poisonous gas, CO, that results from the incomplete "
        "combustion of carbon. Inhalation causes central nervous system damage and "
        "asphyxiation.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:17245"),
            (BQB.IS, "ncit/C76742"),
        ],
    ),
    Substance(
        sid="dihydrogen",
        label="dihydrogen (H2)",
        description="An elemental molecule consisting of two hydrogens joined by a single bond.",
        annotations=[(BQB.IS, "chebi/CHEBI:18276")],
    ),
    Substance(
        sid="sulfasalazine",
        description="A synthetic salicylic acid derivative with affinity for "
        "connective tissues containing elastin and formulated as a "
        "prodrug, antiinflammatory Sulfasalazine acts locally in the "
        "intestine through its active metabolites, sulfamide 5-aminosalicylic "
        "acid and salicylic acid, by a mechanism that is not clear. It appears "
        "inhibit cyclooxygenase and prostaglandin production and is used in the "
        "management of inflammatory bowel diseases.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:9334"),
            (BQB.IS, "ncit/C29469"),
        ],
    ),
    Substance(
        sid="sulfapyridine",
        description="A short-acting sulfonamide antibiotic and by-product of the non-steroidal "
        "anti-inflammatory drug sulfasalazine. Its manufacture and use were "
        "discontinued in 1990.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:132842"),
            (BQB.IS, "ncit/C66570"),
        ],
    ),
    Substance(
        sid="silexan",
        label="Lavender essential oil (Silexan)",
        description="Lavender essential oil (Silexan). The essential oil extracted from "
        "the flowers of several species of Lavandula. Lavender oil is used "
        "primarily for its aromatic properties in parfumery, aromatherapy, "
        "skincare products, and other consumer products.",
        synonyms=["lavender essential oil"],
        annotations=[(BQB.IS, "ncit/C66002")],
    ),
    # ----------------------
    # glucose metabolism
    # ----------------------
    Substance(
        sid="glucose",
        name="glucose",
        label="D-glucose",
        description="A simple sugar monosaccharide having two isoforms, alpha and beta, with a chemical structure "
        "of C6H12O6 that acts as an energy source for both plants and animals by reacting with oxygen, "
        "generating carbon dioxide and water, and releasing energy.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:4167"),
            (BQB.IS, "ncit/C2831"),
        ],
        synonyms=["D-glucopyranose"],
    ),
    Substance(
        sid="lactate",
        name="lactate",
        label="L-lactate",
        description="Lactic acid is an organic acid. In animals, L-lactate is constantly "
        "produced from pyruvate via the enzyme lactate dehydrogenase (LDH) in "
        "a process of fermentation during normal metabolism and exercise.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:24996"),
            (BQB.IS, "ncit/C76926"),
        ],
        synonyms=["lactic acid"],
    ),
    Substance(
        sid="2-3h-glucose",
        name="[2-3H]glucose",
        description="[2-3H] modified glucose used for tracing studies.",
        annotations=[
            (BQB.IS, "pubchem.substance/168037"),
            (BQB.IS, "inchikey/GZCGUPFRVQAUEE-KGHOSXRCSA-N"),
        ],
        synonyms=[
            "(2R,3S,4R,5R)-2,3,4,5,6-Pentahydroxy-2-tritiohexanal",
            "D-(2-3H)Glucose",
        ],
    ),
    Substance(
        sid="6-3h-glucose",
        name="[6-3H]glucose",
        description="[6-3H] modified glucose used for tracing studies.",
        annotations=[
            (BQB.IS, "pubchem.substance/165139"),
            (BQB.IS, "inchikey/GZCGUPFRVQAUEE-WYGJDOTESA-N"),
        ],
        synonyms=[
            "DTXSID40957564",
            "(6-3H)Glucose",
        ],
    ),
    Substance(
        sid="u-13c-glucose",
        name="[U-13C]glucose",
        description="[U-13C] modified glucose used for tracing studies.",
    ),
    Substance(
        sid="3-omg-glucose",
        name="[3-OMG]glucose",
        description="[3-OMG] modified glucose used for tracing studies.",
    ),
    Substance(
        sid="insulin",
        name="insulin",
        description="A protein hormone formed from proinsulin in the beta cells of the pancreatic "
        "islets of Langerhans. The major fuel-regulating hormone, it is secreted into the blood "
        "in response to a rise in concentration of blood glucose or amino acids. Insulin promotes "
        "the storage of glucose and the uptake of amino acids, increases protein and lipid "
        "synthesis, and inhibits lipolysis and gluconeogenesis.",
        annotations=[
            # (BQB.IS, "chebi/CHEBI:5931"),
            (BQB.IS, "ncit/C2271"),
        ],
    ),
    Substance(
        sid="cpeptide",
        name="c-peptide",
        label="C-peptide",
        description="C peptide (31 aa, ~3 kDa) is encoded by the human INS gene. This protein is involved "
        "in both signal transduction and the modulation of blood flow. he connecting peptide, or "
        "C-peptide, is a short 31-amino-acid polypeptide that connects insulin's A-chain to its B-chain in "
        "the proinsulin molecule. In the context of diabetes or hypoglycemia, a measurement of C-peptide "
        "blood serum levels can be used to distinguish between different conditions with similar "
        "clinical features.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:80332"),
            (BQB.IS, "ncit/C94608"),
        ],
    ),
    Substance(
        sid="cortisol",
        name="cortisol",
        description="Cortisol is a steroid hormone, in the glucocorticoid class of hormones. "
        "When used as a medication, it is known as hydrocortisone.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:17650"),
            (BQB.IS, "ncit/C2290"),
        ],
        synonyms=["hydrocortisone"],
    ),
    Substance(
        sid="6beta-hydroxycortisol",
        description="6beta-hydroxycortisol is a C21-steroid that is cortisol bearing an additional hydroxy "
        "substituent at the 6beta-position. In humans, it is produced as a metabolite of cortisol by "
        "cytochrome p450-3A4 (CYP3A4, an important enzyme involved in the metabolism of a variety of "
        "exogenous and endogenous compounds) and can be used to detect moderate and potent CYP3A4 "
        "inhibition in vivo.",
        annotations=[(BQB.IS, "chebi/CHEBI:139271")],
    ),
    Substance(
        sid="6beta-hydroxycortisol/cortisol",
        description="Metabolic ratio for evaluation of CYP3A4 metabolism.",
        parents=["6beta-hydroxycortisol", "cortisol"],
    ),
    Substance(
        sid="epinephrine",
        name="epinephrine",
        description="Adrenaline, also known as epinephrine, is a hormone and medication. Adrenaline is normally produced by "
        "both the adrenal glands and a small number of neurons in the medulla oblongata, where it acts as a "
        "neurotransmitter involved in regulating visceral functions (e.g., respiration).",
        annotations=[
            (BQB.IS, "chebi/CHEBI:33568"),
            (BQB.IS, "ncit/C2292"),
        ],
        synonyms=["adrenaline"],
    ),
    Substance(
        sid="somatostatin",
        name="somatostatin",
        description="Somatostatin, also known as growth hormone-inhibiting hormone (GHIH) or by several other names, "
        "is a peptide hormone that regulates the endocrine system and affects neurotransmission and "
        "cell proliferation via interaction with G protein-coupled somatostatin receptors and "
        "inhibition of the release of numerous secondary hormones.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:64628"),
            (BQB.IS, "ncit/C28418"),
        ],
    ),
    Substance(
        sid="rosuvastatin",
        name="rosuvastatin",
        description="Rosuvastatin is a statin with antilipidemic and potential antineoplastic activities. "
        "Rosuvastatin selectively and competitively binds to and inhibits hepatic hydroxymethyl-glutaryl "
        "coenzyme A (HMG-CoA) reductase",
        annotations=[
            (BQB.IS, "chebi/CHEBI:38545"),
            (BQB.IS, "pubchem.compound/446157"),
        ],
        synonyms=["Crestor"],
    ),
    Substance(
        sid="pitavastatin",
        name="pitavastatin",
        description="Pitavastatin, also known as the brand name product Livalo, is a lipid-lowering drug belonging to "
        "the statin class of medications. By inhibiting the endogenous production of cholesterol within the "
        "liver, statins lower abnormal cholesterol and lipid levels and ultimately reduce the risk of "
        "cardiovascular disease.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:32020"),
            (BQB.IS, "pubchem.compound/5282452"),
            (BQB.IS, "inchikey/VGYFMXBACGZSIL-MCBHFWOFSA-N"),
        ],
        synonyms=["Livalo"],
    ),
    Substance(
        sid="norepinephrine",
        description="Norepinephrine (NE), also called noradrenaline (NA) or noradrenalin, is an organic chemical in "
        "the catecholamine family that functions in the brain and body as a hormone and neurotransmitter.",
        annotations=[(BQB.IS, "chebi/CHEBI:33569")],
        synonyms=["noradrenaline"],
    ),
    Substance(
        sid="growth-hormone",
        name="growth hormone",
        description="A hormone that specifically regulates growth.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:37845"),
        ],
    ),
    Substance(
        sid="glucagon",
        name="glucagon",
        description="Glucagon is a peptide hormone, produced by alpha cells of the pancreas. It works to raise the "
        "concentration of glucose and fatty acids in the bloodstream, and is considered to be the main "
        "catabolic hormone of the body.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:5391"),
            (BQB.IS, "ncit/C2268"),
        ],
    ),
    Substance(
        sid="total-amino-acids",
        name="TAA",
        label="Total amino acids (TAA)",
        description="Total amino acids (TAA).",
    ),
    Substance(
        sid="essential-amino-acids",
        name="EAA",
        label="Essential amino acids (EAA)",
        description="Refer to those amino acids that can not be synthesized in the body and can only be "
        "obtained through food supply.",
        annotations=[
            (BQB.IS, "ncit/C29595"),
            (BQB.IS, "omit/0002018"),
        ],
    ),
    Substance(
        name="non-essential-amino-acids",
        sid="NEAA",
        label="Non-essential amino acids (NEAA)",
        description="Refers to those amino acids that your body can create out of other chemicals found in your body.",
        annotations=[
            (BQB.IS, "ncit/C29596"),
        ],
    ),
    Substance(
        sid="BCAA",
        label="Branch-chained amino acids (BCAA)",
        description="Any amino acid in which the parent hydrocarbon chain has one or more alkyl substituents.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:22918"),
            (BQB.IS, "omit/0002014"),
        ],
    ),
    Substance(
        sid="gip",
        name="GIP",
        label="gastric inhibitory polypeptide (GIP)",
        description="Gastric inhibitory polypeptide (GIP), or gastric inhibitory peptide, also known as glucose-dependent "
        "insulinotropic polypeptide (also abbreviated as GIP), is an inhibiting hormone of the secretin "
        "family of hormones.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:80165"),
            (BQB.IS, "uniprot/P09681"),
        ],
        synonyms=[
            "Glucose-dependent insulinotropic peptide",
            "Gastric inhibitory polypeptide",
            "GIP",
        ],
    ),
    Substance(
        sid="glp-1",
        name="GLP-1",
        label="glucagon-like peptide-1 (GLP-1)",
        description="Glucagon-like peptide-1 (GLP-1) is a 30 or 31 amino acid long peptide hormone deriving from "
        "the tissue-specific posttranslational processing of the proglucagon peptide. It is produced and "
        "secreted by intestinal enteroendocrine L-cells and certain neurons within the nucleus of the "
        "solitary tract in the brainstem upon food consumption.",
    ),
    Substance(
        sid="exenatide",
        description="GLP1 analoque. A 39 amino acid peptide and synthetic version of exendin-4, a hormone found in "
        "the saliva of the venomous lizard Gila monster, with insulin secretagogue and antihyperglycemic "
        "activity. Exenatide is administered subcutaneously and mimics human glucagon-like peptide-1 "
        "(GLP-1).",
        annotations=[(BQB.IS, "ncit/C65611")],
    ),
    Substance(
        sid="insulin/glucose",
        name="ins/glc",
        label="Insulin/Glucose",
        description="Insulin/Glucose ratio, used in the evaluation of glucose tolerance.",
        parents=["insulin", "glucose"],
    ),
    # --- statins ---
    Substance(
        sid="pra",
        name="pravastatin",
        description="A synthetic lipid-lowering agent. Pravastatin competitively "
        "inhibits hepatic hydroxymethyl-glutaryl coenzyme A (HMG-CoA) reductase, "
        "the enzyme which catalyzes the conversion of HMG-CoA to mevalonate, "
        "a key step in cholesterol synthesis.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:63618"),
            (BQB.IS, "pubchem.compound/54687"),
            (BQB.IS, "ncit/C62070"),
        ],
    ),
    Substance(
        sid="sq31906",
        name="SQ 31906 (3'alpha-isopravastatin)",
        description="3'alpha-Isopravastatin metabolite of pravastatin metabolism. "
        "SQ31906 is formed from pravastatin predominantly in the stomach "
        "at acidic pH.",
        annotations=[
            (BQB.IS, "pubchem.compound/157787"),
            (BQB.IS, "inchikey/HIZIJHNJVQOXLO-YMUQFYNDSA-N"),
        ],
        synonyms=["3'alpha-Isopravastatin", "SQ31906", "SQ-31906", "RMS-416"],
    ),
    Substance(
        sid="sq31945",
        name="SQ 31945",
        description="SQ 31945. Metabolite of pravastatin. "
        "3'alpha,5'beta,6'beta-trihydroxy pravastatin",
        annotations=[
            (BQB.IS, "pubchem.compound/131903"),
            (BQB.IS, "inchikey/BVWLCXJEPYNBRS-DJMRDGBJSA-N"),
        ],
        synonyms=["SQ31945", "SQ-31945"],
    ),
    Substance(
        sid="pra+sq31906+sq31945",
        name="pravastatin + SQ 31906 + SQ 31945",
        description="Sum of pravastatin and pravastatin metabolites.",
        parents=["pra", "sq31906", "sq31945"],
    ),
    Substance(
        sid="active-pra-inhibitors",
        name="active pra inhibitors",
        label="Active HMG-CoA reductase inhibitors (pravastatin)",
        description="The combination of all pravastatin derived HMG-CoA inhibitor metabolites. "
        "The latent metabolites are not included (see also 'total pravastatin inhibitors').",
        synonyms=["Active HMG-CoA reductase inhibitors"],
    ),
    Substance(
        sid="total-pra-inhibitors",
        name="total pra inhibitors",
        label="Total HMG-CoA reductase inhibitors (pravastatin)",
        description="The combination of all pravastatin derived HMG-CoA inhibitor metabolites. "
        "The latent metabolites are included (see also 'active pra inhibitors').",
        synonyms=["Total HMG-CoA reductase inhibitors"],
    ),
    Substance(
        sid="cholestyramine",
        name="cholestyramine",
        label="Cholestyramine",
        description=" is a bile acid sequestrant, which binds bile in the gastrointestinal tract to prevent its reabsorption. It is a strong ion exchange resin, which means it can exchange its chloride anions with anionic bile acids in the gastrointestinal tract and bind them strongly in the resin matrix. The functional group of the anion exchange resin is a quaternary ammonium group attached to an inert styrene-divinylbenzene copolymer.",
        synonyms=[
            "colestyramine",
            "[4-[3-(4-Ethylphenyl)butyl]phenyl]-trimethylazanium",
        ],
        annotations=[(BQB.IS, "pubchem.compound/70695641")],
    ),
    Substance(
        sid="lova",
        name="lovastatin",
        description="A lactone metabolite isolated from the fungus Aspergillus terreus with "
        "cholesterol-lowering and potential antineoplastic activities. "
        "Lovastatin is hydrolyzed to the active beta-hydroxyacid form, "
        "which competitively inhibits 3-hydroxyl-3-methylgutarylcoenzyme A "
        "(HMG-CoA) reductase, an enzyme involved in cholesterol biosynthesis.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:40303"),
            (BQB.IS, "ncit/C620"),
        ],
    ),
    Substance(
        sid="lovaacid",
        name="lovastatin acid",
        description="Lovastatin Acid is the active, acid form of lovastatin. "
        "In the body lovastatin is hydrolysed to its beta-hydroxy acid active form.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:82985"),
            (BQB.IS, "inchikey/QLJODMDSTUBWDW-BXMDZJJMSA-N"),
        ],
    ),
    Substance(
        sid="active-lova-inhibitors",
        name="active lova inhibitors",
        label="Active HMG-CoA reductase inhibitors (lovastatin)",
        description="The combination of all lovastatin derived HMG-CoA inhibitor metabolites. "
        "The latent metabolites are not included (see also 'total lova inhibitors').",
        synonyms=["Active HMG-CoA reductase inhibitors"],
    ),
    Substance(
        sid="total-lova-inhibitors",
        name="total lova inhibitors",
        label="Total HMG-CoA reductase inhibitors (lovastatin)",
        description="The combination of all lovastatin derived HMG-CoA inhibitor metabolites. "
        "The latent metabolites are included (see also 'active lova inhibitors').",
        synonyms=["Total HMG-CoA reductase inhibitors"],
    ),
    Substance(
        sid="fluvastatin",
        name="fluvastatin",
        description="A racemate comprising equimolar amounts of (3R,5S)- and (3S,5R)-fluvastatin."
        "An HMG-CoA reductase inhibitor, it is used (often as the corresponding"
        "sodium salt) to reduce triglycerides and LDL-cholesterol,"
        "and increase HDL-chloesterol, in the treatment of hyperlipidaemia.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:38561"),
            (BQB.IS, "ncit/C61768"),
        ],
    ),
    Substance(
        sid="atorvastatin",
        name="atorvastatin",
        description="A synthetic lipid-lowering agent. Atorvastatin competitively inhibits "
        "hepatic hydroxymethyl-glutaryl coenzyme A (HMG-CoA) reductase, the enzyme "
        "which catalyzes the conversion of HMG-CoA to mevalonate, a key step in "
        "cholesterol synthesis.",
        annotations=[(BQB.IS, "chebi/CHEBI:39548"), (BQB.IS, "ncit/C61527")],
        synonyms=["DIHYDROXY-HEPTANOIC ACID"],
    ),
    Substance(
        sid="atorvastatin-acid",
        name="atorvastatin acid",
        description="Major metabolite of atorvastatin.",
        mass=1117.3,
        annotations=[
            (BQB.IS, "pubchem.substance/70680954"),
            (BQB.IS, "inchikey/BJGBAZAEWKCPHZ-MQSFZEHASA-N"),
        ],
        synonyms=[],
    ),
    Substance(
        sid="atovarstatin-lactone",
        name="atorvastatin lactone",
        description="Active administered form of atorvastatin.",
        annotations=[
            (BQB.IS, "pubchem.substance/6483036"),
            (BQB.IS, "inchikey/OUCSEDFVYPBLLF-KAYWLYCHSA-N"),
        ],
        mass=540.6,
        formula="C33H33FN2O4",
    ),
    # inactive form of atorvastatin after hepatic metabolism
    Substance(
        sid="2-hydroxyatorvastatin-acid",
        name="2-hydroxyatorvastatin acid",
        description="Metabolite of atorvastatin.",
        synonyms=["ortho-hydroxyatorvastatin acid"],
        mass=574.6,
        annotations=[],
    ),
    Substance(
        sid="4-hydroxyatorvastatin-acid",
        name="4-hydroxyatorvastatin acid",
        description="Metabolite of atorvastatin.",
        synonyms=["para-hydroxyatorvastatin acid"],
        mass=574.6,
    ),
    Substance(
        sid="2-hydroxyatorvastatin-lactone",
        name="2-hydroxyatorvastatin lactone",
        description="Metabolite of atorvastatin.",
        synonyms=[],
        mass=556.6,
    ),
    Substance(
        sid="4-hydroxyatorvastatin-lactone",
        name="4-hydroxyatorvastatin lactone",
        description="Metabolite of atorvastatin.",
        synonyms=[],
        mass=556.6,
    ),
    Substance(
        sid="active-atorva-inhibitors",
        name="active atorva inhibitors",
        label="Active HMG-CoA 	reductase inhibitors (atorvastatin)",
        description="The combination of all atorvastatin derived HMG-CoA inhibitor metabolites. "
        "The latent metabolites are not included (see also 'total atorva inhibitors').",
        synonyms=["Active HMG-CoA reductase inhibitors"],
    ),
    Substance(
        sid="total-atorva-inhibitors",
        name="total atorva inhibitors",
        label="Total HMG-CoA reductase inhibitors (atorvastatin)",
        description="The combination of all atorvastatin derived HMG-CoA inhibitor metabolites. "
        "The latent metabolites are included (see also 'active atorva inhibitors').",
        synonyms=["Total HMG-CoA reductase inhibitors"],
    ),
    # simvastatin
    Substance(
        sid="simvastatin",
        description="A lipid-lowering agent derived synthetically from a fermentation product of the fungus "
        "Aspergillus terreus. Hydrolyzed in vivo to an active metabolite, simvastatin competitively "
        "inhibits hepatic hydroxymethyl-glutaryl coenzyme A (HMG-CoA) reductase.",
        annotations=[
            (BQB.IS, "ncit/C29454"),
            (BQB.IS, "chebi/CHEBI:9150"),
            (BQB.IS, "omit/0019802"),
        ],
        synonyms=["MK-733", "synvinolin"],
    ),
    Substance(
        sid="simvastatin-acid",
        name="simvastatin acid",
        description="Metabolite of simvastatin. Active form of simvastatin after hydrolysis of simvastatin.",
        mass=436.6,
        formula="C25H40O6",
        annotations=[
            (BQB.IS, "ncit/C96309"),
            (BQB.IS, "pubchem.substance/64718"),
            (BQB.IS, "inchikey/XWLXKKNPFMNSFA-HGQWONQESA-N"),
        ],
        synonyms=[
            "Tenivastatin",
            "simvastatin hydroxy acid",
            "simvastatin-beta-hydroxy-acid",
        ],
    ),
    Substance(
        sid="simva+simacid",
        label="simvastatin + simvastatin acid",
        description="Sum of simvastatin and simvastatin acid. Lactone is converted to the acid form"
        "and the sum of both is determined in the assay (see Morris1993)",
        synonyms=[],
        parents=["simvastatin", "simvastatin acid"],
    ),
    Substance(
        sid="active-simva-inhibitors",
        name="active simva inhibitors",
        label="Active HMG-CoA reductase inhibitors (simvastatin)",
        description="The combination of all simvastatin derived HMG-CoA inhibitor metabolites."
        "The latent metabolites are not included (see also 'total simva inhibitors').",
        synonyms=["Active HMG-CoA reductase inhibitors"],
    ),
    Substance(
        sid="total-simva-inhibitors",
        name="total simva inhibitors",
        label="Total HMG-CoA reductase inhibitors (simvastatin)",
        description="The combination of all simvastatin derived HMG-CoA inhibitor metabolites. "
        "The latent metabolites are included (see also 'active simva inhibitors').",
        synonyms=["Total HMG-CoA reductase inhibitors"],
    ),
    Substance(
        sid="total-simva",
        name="total simva",
        label="total simvastatin metabolites",
        description="Total simvastatin used for measurements with radioactive marked carbon; equivalent to simvastatin dose."
        "This is the combination of all simvastatin and derived metabolites.",
        synonyms=["Total simvastatin"],
    ),
    Substance(
        sid="st-johns-wort-extract",
        name="st john's wort extract",
        label="St. John's wort extract",
        description="An herbal extract prepared from the plant Hypericum perforatum (St. John's wort) "
        "with photodynamic, antineoplastic, and antidepressant activities. Hypericin, one "
        "of the active compounds found in Hypericum perforatum, is a photosensitizer that, "
        "when exposed to a particular wavelength and intensity of light, may induce tumor "
        "cell apoptosis.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:83161"),
            (BQB.IS, "ncit/C2589"),
        ],
    ),
    Substance(sid="panax-ginseng", name="panax ginseng", annotations=[]),
    Substance(sid="garlic-oil", name="garlic oil", annotations=[]),
    Substance(sid="ginkgo-biloba", name="ginkgo biloba", annotations=[]),
    Substance(
        sid="goldenseal-root-extract", name="goldenseal root extract", annotations=[]
    ),
    Substance(
        sid="kava-kava-root-extract", name="kava kava root extract", annotations=[]
    ),
    Substance(
        sid="black-cohosh-root-extract",
        name="black cohosh root extract",
        annotations=[],
    ),
    Substance(
        sid="valerian-root-extract", name="valerian root extract", annotations=[]
    ),
    # --- statins ---
    Substance(
        sid="lacidipine",
        description="Lacidipine (tradenames Lacipil or Motens) is a calcium channel blocker.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:135737"),
            (BQB.IS, "ncit/C80881"),
        ],
        synonyms=["Lacipil", "Motens"],
    ),
    Substance(
        sid="gemfibrozil",
        description="A fibric acid derivative with hypolipidemic effects. Gemfibrozil interacts with peroxisome "
        "proliferator-activated receptors (PPARalpha) resulting in PPARalpha-mediated stimulation of "
        "fatty acid oxidation and an increase in lipoprotein lipase (LPL) synthesis.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:5296"),
            (BQB.IS, "ncit/C29071"),
        ],
        synonyms=["2,2-Dimethyl-5-(2,5-xylyloxy)valeric acid"],
    ),
    Substance(
        sid="verapamil",
        description="A phenylalkylamine calcium channel blocking agent. Verapamil inhibits the transmembrane "
        "influx of extracellular calcium ions into myocardial and vascular smooth muscle cells, "
        "causing dilatation of the main coronary and systemic arteries and decreasing myocardial "
        "contractility.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:9948"),
            (BQB.IS, "ncit/C928"),
            (BQB.IS, "omit/0015532"),
        ],
    ),
    Substance(
        sid="norverapamil",
        description="A racemate comprising equimolar amounts of (R)- and (S)-norverapamil. The major active metabolite of verapamil.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:132050"),
        ],
    ),
    Substance(
        sid="dexverapamil",
        description="Dexverapamil is the R-enantiomer of the calcium channel blocker verapamil. Dexverapamil competitively "
        "inhibits the multidrug resistance efflux pump P-glycoprotein (MDR-1), thereby potentially increasing the"
        " effectiveness of a wide range of antineoplastic drugs which are inactivated by MDR-1 mechanisms. "
        "This agent exhibits decreased calcium antagonistic activity and toxicity compared to racemic verapamil. (NCI04)",
        synonyms=[
            "r-verapamil",
        ],
        annotations=[
            (BQB.IS, "chebi/CHEBI:77734"),
            (BQB.IS, "ncit/C1563"),
            (BQB.IS, "omit/0015532"),
        ],
    ),
    Substance(
        sid="mibefradil",
        description="The mechanism of action of mibefradil is characterized by the selective blockade of transient, low-voltage-activated "
        "(T-type) calcium channels over long-lasting, high-voltage-activated (L-type) calcium channels, which is probably "
        "responsible for many of its unique properties.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:6920"),
            (BQB.IS, "pubchem.compound/60663"),
            (BQB.IS, "inchikey/HBNPJJILLOYFJU-VMPREFPWSA-N"),
        ],
    ),
    Substance(
        sid="setipiprant",
        description="Setipiprant (INN; developmental code names ACT-129968, KYTH-105) is an investigational drug "
        "developed for the treatment of asthma and scalp hair loss.",
        formula="C24H19FN2O3",
        mass=402.4,
        annotations=[
            (BQB.IS, "ncit/C152348"),
            (BQB.IS, "pubchem.substance/49843471"),
            (BQB.IS, "inchikey/IHAXLPDVOWLUOS-UHFFFAOYSA-N"),
        ],
        synonyms=["ACT-129968", "KYTH-105"],
    ),
    Substance(
        sid="cilostazol",
        description="A quinolinone derivative and cellular phosphodiesterase inhibitor, more specific for "
        "phosphodiesterase III (PDE III). Although the exact mechanism of action of is unknown, "
        "cilostazol and its metabolites appears to inhibit PDE III activity, thereby suppressing cyclic "
        "adenosine monophosphate (cAMP) degradation.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:31401"),
            (BQB.IS, "ncit/C1051"),
        ],
    ),
    Substance(
        sid="nelfinavir",
        description="A synthetic antiviral agent that selectively binds to and inhibits human immunodeficiency virus "
        "(HIV) protease. Nelfinavir has activity against HIV 1 and 2.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:7496"),
            (BQB.IS, "ncit/C29285"),
        ],
    ),
    Substance(
        sid="fenofibrate",
        description="A synthetic phenoxy-isobutyric acid derivate and prodrug with antihyperlipidemic activity.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:5001"),
            (BQB.IS, "ncit/C29047"),
        ],
    ),
    Substance(
        sid="osimertinib",
        description="A third-generation, orally available, irreversible, mutant-selective, epidermal growth factor "
        "receptor (EGFR) inhibitor, with potential antineoplastic activity.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:90943"),
            (BQB.IS, "ncit/C116377"),
        ],
    ),
    Substance(
        sid="irbesartan",
        description="A biphenylyltetrazole that is an angiotensin II receptor antagonist used mainly for the "
        "treatment of hypertension.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:5959"),
            (BQB.IS, "ncit/C29130"),
        ],
    ),
    Substance(
        sid="troglitazone",
        description="An orally-active thiazolidinedione with antidiabetic and hepatotoxic properties and potential "
        "antineoplastic activity. Troglitazone activates peroxisome proliferator-activated receptor "
        "gamma (PPAR-gamma), a ligand-activated transcription factor, thereby inducing cell "
        "differentiation and inhibiting cell growth and angiogenesis.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:9753"),
            (BQB.IS, "ncit/C1522"),
        ],
    ),
    Substance(
        sid="pioglitazone",
        description="An orally-active thiazolidinedione with antidiabetic properties and potential antineoplastic "
        "activity. Pioglitazone activates peroxisome proliferator-activated receptor gamma (PPAR-gamma), "
        "a ligand-activated transcription factor, thereby inducing cell differentiation and inhibiting "
        "cell growth and angiogenesis.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:8228"),
            (BQB.IS, "ncit/C71633"),
        ],
    ),
    Substance(
        sid="orlistat",
        description="A reversible active-site inhibitor of gastrointestinal lipases. Orlistat forms a covalent bond "
        "with the active serine site in gastric and pancreatic lipases, thereby inhibiting their activity "
        "and preventing dietary fat from being hydrolyzed and absorbed.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:94686"),
            (BQB.IS, "ncit/C29303"),
        ],
    ),
    Substance(
        sid="amlodipine",
        description="A synthetic dihydropyridine and a calcium channel blocker with antihypertensive and antianginal "
        "properties. Amlodipine inhibits the influx of extracellular calcium ions into myocardial and "
        "peripheral vascular smooth muscle cells, thereby preventing vascular and myocardial contraction.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:2668"),
            (BQB.IS, "ncit/C61635"),
        ],
    ),
    Substance(
        sid="bile acids",
        name="bile acids",
        description="Any member of a group of hydroxy steroids occuring in bile, "
        "where they are present as the sodium salts of their amides with glycine or taurine. "
        "In mammals bile acids almost invariably have 5beta-configuration, while in lower vertebrates, some bile acids, "
        "known as allo-bile acids, have 5alpha-configuration.",
        synonyms=["BA"],
        annotations=[(BQB.IS, "chebi/CHEBI:138366")],
    ),
    Substance(
        sid="campesterol",
        description="A steroid derivative that is the simplest sterol, characterized by the hydroxyl group in "
        "position C-3 of the steroid skeleton, and saturated bonds throughout the sterol structure, "
        "with the exception of the 5-6 double bond in the B ring. Marker of cholesterol absorption.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:28623"),
            (BQB.IS, "ncit/C68328"),
        ],
    ),
    Substance(
        sid="stigmasterol",
        description="A steroid derivative characterized by the hydroxyl group in position C-3 of the steroid "
        "skeleton, and unsaturated bonds in position 5-6 of the B ring, and position 22-23 in the alkyl "
        "substituent. Marker of cholesterol absorption.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:28824"),
            (BQB.IS, "ncit/C68427"),
        ],
    ),
    Substance(
        sid="sitosterol",
        description="A member of the class of phytosterols that is stigmast-5-ene substituted by a beta-hydroxy group "
        "at position 3. Marker of cholesterol absorption.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:27693"),
        ],
    ),
    # --- talinolol ---
    Substance(
        sid="talinolol",
        description="Talinolol is a beta-blocker and subtrate of the P-glycoprotein. "
        "Talinolol contains a stereocenter and consists of two enantiomers. "
        "This is a racemate, i.e. a 1: 1 mixture of (R)- and the (S)-forms.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:135533"),
            (BQB.IS, "pubchem.compound/68770"),
        ],
        synonyms=["57460-41-0", "Cordanum"],
    ),
    Substance(
        sid="rtalinolol",
        name="R-talinolol",
        description="R enantiomer of talinolol.",
        annotations=[
            (BQB.IS, "inchikey/MXFWWQICDIZSOA-QGZVFWFLSA-N"),
            (BQB.IS, "pubchem.compound/156154"),
        ],
        synonyms=["(+)-Talinolol", "(+)-talinolol, (R)-talinolol"],
    ),
    Substance(
        sid="stalinolol",
        name="S-talinolol",
        description="S enantiomer of talinolol.",
        annotations=[],
        synonyms=["(-)-Talinolol", "(-)-talinolol, (S)-talinolol"],
    ),
    Substance(
        sid="talinolol2oh",
        name="2-hydroxytalinolol",
        description="2-hydroxytalinolol, metabolite of talinolol.",
        annotations=[
            (BQB.IS, "inchikey/GQOOSCJXWCJCTL-UHFFFAOYSA-N"),
            (BQB.IS, "pubchem.compound/101683410"),
        ],
        synonyms=["2-trans hydroxytalinolol"],
    ),
    Substance(
        sid="talinolol3cisoh",
        name="3-cis hydroxytalinolol",
        description="3-cis hydroxytalinolol, metabolite of talinolol.",
        annotations=[
            (BQB.IS, "inchikey/BDPLDDGLJNMXHE-UHFFFAOYSA-N"),
            (BQB.IS, "pubchem.compound/101683411"),
        ],
        synonyms=[],
    ),
    Substance(
        sid="talinolol3transoh",
        name="3-trans hydroxytalinolol",
        description="3-trans hydroxytalinolol, metabolite of talinolol.",
        annotations=[],
        synonyms=[],
    ),
    Substance(
        sid="talinolol4cisoh",
        name="4-cis hydroxytalinolol",
        description="4-cis hydroxytalinolol, metabolite of talinolol.",
        annotations=[],
        synonyms=[],
    ),
    Substance(
        sid="talinolol4transoh",
        name="4-trans hydroxytalinolol",
        description="4-trans hydroxytalinolol, metabolite of talinolol.",
        annotations=[
            (BQB.IS, "inchikey/GBGGMSXUDHTSLR-UHFFFAOYSA-N"),
            (BQB.IS, "pubchem.compound/101676524"),
        ],
        synonyms=[],
    ),
    Substance(
        sid="bifendate",
        name="bifendate",
        description="Bifendate is a synthetic intermediate of schizandrin."
        "Bifendate has known human metabolites that include Mono-O-demethylated bdd and methyl "
        "4-(2,3-dihydroxy-4-methoxy-6-methoxycarbonylphenyl)-7-methoxy-1,3-benzodioxole-5-carboxylate.",
        annotations=[
            (BQB.IS, "pubchem.compound/108213"),
            (BQB.IS, "inchikey/JMZOMFYRADAWOG-UHFFFAOYSA-N"),
        ],
        synonyms=[
            "73536-69-3",
            "Bifendatatum",
        ],
    ),
    Substance(
        sid="tpgs",
        name="TPGS",
        label="D-alpha-tocopheryl polyethylene glycol 1000 succinate (TPGS)",
        description="D-alpha-tocopheryl polyethylene glycol 1000 succinate (TPGS), a surfactant.",
        annotations=[],
        synonyms=[],
    ),
    Substance(
        sid="poloxamer188",
        name="Poloxamer 188",
        description="Poloxamer 188, a surfactant that does not interact with P-gp.",
        annotations=[],
        synonyms=["synperonic F68"],
    ),
    Substance(
        sid="schisandra chinensis",
        name="schisandra chinensis",
        label="",
        description="",
        annotations=[],
        synonyms=[],
    ),
    Substance(
        sid="deoxyschizandrin",
        name="deoxyschizandrin",
        label="",
        description="",
        annotations=[],
        synonyms=[],
    ),
    # --- torasemide ---
    Substance(
        sid="torasemide",
        name="torasemide",
        description="An anilinopyridine sulfonylurea belonging to the class of loop diuretics. Torsemide has a "
        "prolonged duration of action compared to other loop diuretics, is extensively protein bound "
        "in plasma and has a relatively long half-life.",
        annotations=[
            (BQB.IS, "ncit/C29506"),
            (BQB.IS, "chebi/CHEBI:9637"),
        ],
    ),
    Substance(
        sid="torasemide-M1",
        name="torasemide-M1",
        description="An aromatic primary alcohol resulting from the hydroxylation of the 3'-methyl group of the "
        "phenyl ring of torasemide. It is a metabolite of torasemide.",
        synonyms=["hydroxytorsemide"],
        annotations=[
            (BQB.IS, "chebi/CHEBI:155897"),
            (BQB.IS, "inchikey/WCYVLAMJCQZUCR-UHFFFAOYSA-N"),
        ],
    ),
    Substance(
        sid="torasemide-M3",
        name="torasemide-M3",
        description="A member of the class of phenols that is torasemide which carries a hydroxy group at position "
        "4' of the phenyl ring. It is a metabolite of torasemide.",
        synonyms=["4'-hydroxy torasemide"],
        annotations=[
            (BQB.IS, "chebi/CHEBI:155915"),
            (BQB.IS, "inchikey/BJCCDWZGWOVSPR-UHFFFAOYSA-N"),
        ],
    ),
    Substance(
        sid="torasemide-M5",
        name="torasemide-M5",
        description="A monocarboxylic acid resulting from the replacement of the 3'-methyl group of the "
        "phenyl ring of torasemide by a carboxy group. It is a metabolite of torasemide.",
        synonyms=["torasemide carboxylic acid"],
        annotations=[
            (BQB.IS, "chebi/CHEBI:155916"),
            (BQB.IS, "inchikey/PGPRBNDLCZQUST-UHFFFAOYSA-N"),
        ],
    ),
    Substance(
        sid="furosemide",
        name="furosemide",
        synonyms=[
            "Lasix (TN)",
            "Frusemide",
        ],
        description="A chlorobenzoic acid that is 4-chlorobenzoic acid substituted by a (furan-2-ylmethyl)amino and a "
        "sulfamoyl group at position 2 and 5 respectively. It is a diuretic used in the treatment of "
        "congestive heart failure.",
        annotations=[
            (BQB.IS, "inchikey/ZZUFCTLCJUWOSV-UHFFFAOYSA-N"),
            (BQB.IS, "chebi/CHEBI:47426"),
        ],
    ),
    Substance(
        sid="THC",
        name="THC",
        synonyms=[
            "Delta(9)-tetrahydrocannabinol",
        ],
        description="The principal psychoactive constituent of the cannabis plant, it is used for treatment of anorexia associated with AIDS as well as nausea and vomiting associated with cancer chemotherapy.",
        annotations=[
            (BQB.IS, "inchikey/CYQFCXCEBYINGO-IAGOWNOFSA-N"),
            (BQB.IS, "chebi/CHEBI:66964"),
        ],
    ),
    Substance(
        sid="cocaine",
        name="cocaine",
        synonyms=[],
        description="A tropane alkaloid obtained from leaves of the South American shrub Erythroxylon coca.",
        annotations=[
            (BQB.IS, "inchikey/ZPUCINDJVBIVPJ-LJISPDSOSA-N"),
            (BQB.IS, "chebi/CHEBI:27958"),
        ],
    ),
    Substance(
        sid="amphetamine",
        name="amphetamine",
        synonyms=[],
        description="A racemate comprising equimolar amounts of (R)-amphetamine (also known as levamphetamine or levoamphetamine) and (S)-amphetamine (also known as dexamfetamine or dextroamphetamine.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:2679"),
        ],
    ),
    Substance(
        sid="probucol",
        name="probucol",
        synonyms=["Lorelco", "Biphenabid", "Bisphenabid"],
        description="Probucol is a dithioketal that is propane-2,2-dithiol in which the"
        "hydrogens attached to both sulfur atoms are replaced by 3,5-di-tert-butyl-4-"
        "hydroxyphenyl groups. An anticholesteremic drug with antioxidant and anti-inflammatory "
        "properties, it is used to treat high levels of cholesterol in blood. It has a role as "
        "an anticholesteremic drug, an antioxidant, an anti-inflammatory drug, a cardiovascular drug"
        "and an antilipemic drug. It is a dithioketal and a polyphenol.",
        annotations=[
            (BQB.IS, "inchikey/FYPMFJGVHOHGLL-UHFFFAOYSA-N"),
            (BQB.IS, "chebi/CHEBI:8427"),
        ],
    ),
    Substance(
        sid="butylscopolamine",
        name="butylscopolamine",
        description="Hyoscine butylbromide, also known as scopolamine butylbromide and "
        "sold under the brandname Buscopan among others, is an anticholinergic "
        "medication used to treat crampy abdominal pain, esophageal spasms, "
        "renal colic, and bladder spasms.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:145701"),
            (BQB.IS, "ncit/C83571"),
        ],
        synonyms=[
            "N-butylscopolamine",
            "Hyoscine butylbromide",
            "Buscopan",
            "scopolamine butylbromide",
        ],
    ),
    Substance(
        sid="bromazepam",
        name="bromazepam",
        description="Bromazepam, sold under many brand names, is a benzodiazepine. "
        "It is mainly an anti-anxiety agent with similar side effects to "
        "diazepam (Valium). In addition to being used to treat anxiety or "
        "panic states, bromazepam may be used as a premedicant prior to "
        "minor surgery.",
        annotations=[(BQB.IS, "chebi/CHEBI:31302"), (BQB.IS, "ncit/C87454")],
        synonyms=[],
    ),
    Substance(
        sid="propatyl-nitrate",
        name="propatyl nitrate",
        description="Propatylnitrate is a nitrate ester.",
        annotations=[
            (BQB.IS, "ncit/C74425"),
            (BQB.IS, "pubchem.compound/66261"),
            (BQB.IS, "chebi/CHEBI:135104"),
        ],
        synonyms=["propatylnitrate"],
    ),
    Substance(
        sid="osilodostrat",
        name="osilodostrat",
        description="Osilodrostat is an orally bioavailable inhibitor of both steroid 11beta-hydroxylase (cytochrome P450 (CYP) 11B1) and aldosterone synthase (CYP11B2; steroid 18-hydroxylase),"
        "with potential anti-adrenal activity and ability to treat Cushing disease (CD). Upon administration, osilodrostat binds to and inhibits the activity of CYP11B1, the enzyme that"
        "catalyzes the final step of cortisol synthesis from the precursor 11-deoxycortisol, and CYP11B2, the enzyme that catalyzes aldosterone synthesis from corticosterone and"
        "11-deoxycorticosterone in the adrenal gland. The inhibition of CYP11B1 prevents the production of excess cortisol, thereby decreasing and normalizing the levels of cortisol."
        "CD is most often caused by an adrenocorticotropic hormone (ACTH)-secreting pituitary tumor.",
        annotations=[
            (BQB.IS, "inchikey/USUZGMWDZDXMDG-CYBMUJFWSA-N"),
        ],
    ),
    Substance(
        sid="quercetin",
        name="quercetin",
        description="A pentahydroxyflavone having the five hydroxy groups placed at the 3-, 3'-, 4'-, 5- and 7-positions. It is one of the most abundant flavonoids in edible vegetables,"
        "fruit and wine",
        annotations=[
            (BQB.IS, "chebi/CHEBI:16243"),
        ],
    ),
    Substance(
        sid="mexiletine",
        name="mexiletine",
        description="Mexiletine (INN) (sold under the brand names Mexitil and NaMuscla) is a medication used to treat abnormal heart rhythms, chronic pain, and some causes of muscle stiffness."
        "Common side effects include abdominal pain, chest discomfort, drowsiness, headache, and nausea. It works as a non-selective voltage-gated sodium channel blocker and belongs"
        "to the Class IB group of anti-arrhythmic medications.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:6916"),
        ],
    ),
    ###################### Not sorted substances used in caffeine studies ################################
    Substance(
        sid="curcumin",
        name="curcumin",
        description="A β-diketone that is methane in which two of the hydrogens are substituted by feruloyl groups. "
        "A natural dyestuff found in the root of Curcuma longa.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:3962"),
        ],
    ),
    Substance(
        sid="bupropion",
        name="bupropion",
        description="An aromatic ketone that is propiophenone carrying a tert-butylamino group at position 2 "
        "and a chloro substituent at position 3 on the phenyl ring.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:3219"),
        ],
    ),
    Substance(
        sid="hydroxybupropion",
        name="hydroxybupropion",
        description="",
        annotations=[
            (BQB.IS, "chebi/CHEBI:166487"),
        ],
    ),
    Substance(
        sid="isavuconazole",
        name="isavuconazole",
        description="A 1,3-thiazole that is butan-2-ol which is substituted at positions 1, 2, and "
        "3 by 1,2,4-triazol-1-yl, 2,5-difluorophenyl, and 4-(p-cyanophenyl)-1,3-thiazol-2-yl "
        "groups, respectively. It is an antifungal drug used for the treatment of invasive "
        "aspergillosis and invasive mucormycosis.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:85979"),
        ],
    ),
    Substance(
        sid="5-MeO-DALT",
        name="5-MeO-DALT",
        description="5-MeO-DALT or N,N-di allyl-5-methoxy tryptamine is a psychedelic tryptamine "
        "first synthesized by Alexander Shulgin. ",
        annotations=[
            (BQB.IS, "chebi/CHEBI:8805"),
        ],
    ),
    Substance(
        sid="methadone-hydrochloride",
        name="methadone hydrochloride",
        description="",
        annotations=[
            (BQB.IS, "chebi/CHEBI:50140"),
        ],
    ),
    Substance(
        sid="dextromethadone",
        name="dextromethadone",
        description="A 6-(dimethylamino)-4,4-diphenylheptan-3-one that has (S)-configuration. "
        "It is the less active enantiomer of methadone and has very little activity "
        "on opioid receptors and mainly responsible for the inhibition of hERG K+ channels "
        "and thus for cardiac toxicity. The drug is currently under clinical development for "
        "the treatment of major depressive disorder.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:167308"),
        ],
        synonyms=["s-methadone"],
    ),
    Substance(
        sid="levomethadone",
        name="levomethadone",
        description="A 6-(dimethylamino)-4,4-diphenylheptan-3-one that has (R)-configuration. "
        "It is the active enantiomer of methadone and its hydrochloride salt is used to "
        "treat adults who are addicted to drugs such as heroin and morphine.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:136003"),
        ],
        synonyms=["l-methadone"],
    ),
    Substance(
        sid="sodium-tanshinone-2a-sulfonate",
        name="Sodium tanshinone II A sulfonate",
        description="Sodium tanshinone II A sulfonate",
        annotations=[
            (BQB.IS, "chebi/CHEBI:108595"),
        ],
        synonyms=[
            "1,6,6-trimethyl-8,9-dihydro-7H-naphtho[1,2-g]benzofuran-10,11-dione"
        ],
    ),
    Substance(
        sid="pefloxacin",
        name="pefloxacin",
        description="A quinolone that is 4-oxo-1,4-dihydroquinoline which is substituted at positions "
        "1, 3, 6 and 7 by ethyl, carboxy, fluorine, and 4-methylpiperazin-1-yl groups, respectively.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:50199"),
        ],
    ),
    Substance(
        sid="isosorbide-dinitrate",
        name="isosorbide dinitrate",
        description="Isosorbide dinitrate",
        annotations=[
            (BQB.IS, "chebi/CHEBI:6061"),
        ],
    ),
    Substance(
        sid="acetylcysteine",
        name="acetylcysteine",
        description="Acetylcysteine",
        annotations=[
            (BQB.IS, "chebi/CHEBI:22198"),
        ],
    ),
    Substance(
        sid="digitoxin",
        name="digitoxin",
        description="A cardenolide glycoside in which the 3β-hydroxy group of digitoxigenin carries a "
        "2,6-dideoxy-β-D-ribo-hexopyranosyl-(1→4)-2,6-dideoxy-β-D-ribo-hexopyranosyl-(1→4)-2,"
        "6-dideoxy-β-D-ribo-hexopyranosyl trisaccharide chain.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:28544"),
        ],
    ),
    Substance(
        sid="heparin",
        name="heparin",
        description="A highly sulfated linear glycosaminoglycan comprising complex patterns of "
        "uronic acid-(1→4)-D-glucosamine repeating subunits. Used as an injectable anticoagulant, "
        "it has the highest negative charge density of any known biological molecule.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:28304"),
        ],
    ),
    Substance(
        sid="nifedipine",
        name="nifedipine",
        description="Nifedipine, sold under the brand name Adalat among others, is a calcium channel blocker "
        "medication used to manage angina, high blood pressure, Raynaud's phenomenon, and premature labor",
        annotations=[
            (BQB.IS, "chebi/CHEBI:7565"),
        ],
    ),
    Substance(
        sid="aluminium-hydroxide",
        name="aluminium hydroxide",
        description="Aluminium hydroxide, Al(OH)3, is found in nature as the mineral gibbsite "
        "(also known as hydrargillite) and its three much rarer polymorphs: "
        "bayerite, doyleite, and nordstrandite.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:33130"),
        ],
    ),
    Substance(
        sid="allopurinol",
        name="allopurinol",
        description="Allopurinol, sold under the brand name Zyloprim among others, is a medication used to decrease "
        "high blood uric acid levels.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:33130"),
        ],
    ),
    Substance(
        sid="ipratropium bromide",
        name="ipratropium bromide",
        description="The anhydrous form of the bromide salt of ipratropium. An anticholinergic drug, "
        "ipratropium bromide blocks the muscarinic cholinergic receptors in the smooth muscles of "
        "the bronchi in the lungs. This opens the bronchi, so providing relief in chronic obstructive "
        "pulmonary disease and acute asthma.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:46659"),
        ],
    ),
    Substance(
        sid="Repaglinide",
        name="repaglinide",
        description="A nonsulfonylurea insulin secretagogue belonging to the melgitinide class with hypoglycemic activity. Repaglinide is rapidly absorbed and has a rapid onset and short duration"
        "of action. This agent is metabolized in the liver by CYP2C8 and CYP3A4 and its metabolites are excreted in the bile. Repaglinide has a half-life of one hour.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:8805"),
            (BQB.IS, "ncit/C47703"),
        ],
    ),
    Substance(
        sid="hydroxy repaglinide",
        name="hydroxy repaglinide",
        description="hydroxy repaglinide",
        annotations=[
            # (BQB.IS, "chebi/CHEBI:183883"),
        ],
    ),
    Substance(
        sid="Meamntine",
        name="memantine",
        description="Memantine is a medication used to slow the progression of moderate-to-severe Alzheimer's disease."
        "It is taken by mouth. Common side effects include headache, constipation, sleepiness, and dizziness."
        "Severe side effects may include blood clots, psychosis, and heart failure.[3] It is believed to work by blocking NMDA receptors.",
        annotations=[
            (BQB.IS, "chebi/CHEBI:64312"),
        ],
    ),
]
