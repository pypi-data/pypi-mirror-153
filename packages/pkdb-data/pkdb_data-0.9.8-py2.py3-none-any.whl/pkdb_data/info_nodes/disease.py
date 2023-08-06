"""
Definition of diseases and health status
"""
from pkdb_data.management.info_node import Choice, DType, MeasurementType

from ..metadata.annotation import BQB
from .units import NO_UNIT


DISEASE_NODES = [
    MeasurementType(
        sid="health-status",
        name="health status",
        description="Health status. The state of a subject's mental or physical condition.",
        parents=["measurement"],
        dtype=DType.ABSTRACT,
        annotations=[
            (BQB.IS, "ncit/C16669"),
            (BQB.IS, "opmi/OPMI:0000281"),
            (BQB.IS, "hp/HP:0032319"),
        ],
    ),
    MeasurementType(
        sid="healthy",
        description="Individual or subjects are described as healthy. If "
        "subjects are not healthy the disease or impairment "
        "should be described by a combination of `disease`, "
        "`disease severity` and `disease duration`. "
        "If abnormal blood biochemistry "
        "is reported code the respective biochemistry.",
        parents=["health status"],
        dtype=DType.BOOLEAN,
        annotations=[
            (BQB.IS, "ncit/C115935"),
        ],
    ),
    MeasurementType(
        sid="disease",
        description="Disease of individual or subjects with disease encoded by `choice` "
        "field. Disease duration of individual "
        "or subjects (duration should be provided via the min/mean numerical "
        "fields in combination with unit). To encode the family history for"
        "disease use 'family history disease'.",
        parents=["health status"],
        dtype=DType.NUMERIC_CATEGORICAL,
        units=["year", NO_UNIT],
        annotations=[
            (BQB.IS, "efo/0000408"),
            (BQB.IS_VERSION_OF, "ncit/C2991"),
            (BQB.IS, "doid/DOID:4"),
        ],
    ),
    Choice(
        sid="cancer",
        description="Cancer. A disease characterized by abnormal and uncontrolled cell division.",
        parents=["disease"],
        annotations=[
            (BQB.IS, "efo/0000311"),
            (BQB.IS, "doid/DOID:162"),
        ],
    ),
    Choice(
        sid="leukaemia",
        label="leukemia",
        description="A cancer of the blood and bone marrow characterized by an abnormal "
        "proliferation of leukocytes.",
        parents=["cancer"],
        annotations=[
            (BQB.IS, "ncit/C3161"),
            (BQB.IS, "omit/0009028"),
        ],
        synonyms=["leukemia", "leukaemia"],
    ),
    Choice(
        sid="chronic-myelogenous-leukemia",
        name="chronic myelogenous leukemia",
        description="A chronic myeloproliferative neoplasm characterized by the expression of the "
        "BCR-ABL1 fusion gene. It presents with neutrophilic leukocytosis. It can appear at any "
        "age, but it mostly affects middle aged and older individuals.",
        parents=["leukaemia"],
        annotations=[
            (BQB.IS, "efo/0000339"),
        ],
    ),
    MeasurementType(
        sid="hematopoietic-and-lymphoid-system-disorder",
        name="hematopoietic and lymphoid system disorder",
        description="Any deviation from the normal structure or function of the blood or "
        "lymphatic system that is manifested by a characteristic set of "
        "symptoms and signs.",
        parents=["disease"],
        dtype=DType.ABSTRACT,
        annotations=[(BQB.IS, "ncit/C35814")],
    ),
    Choice(
        sid="sickle-cell-disease",
        name="sickle cell disease",
        description="A blood disorder characterized by the appearance of "
        "sickle-shaped red blood cells and anemia.",
        parents=["hematopoietic and lymphoid system disorder"],
        annotations=[(BQB.IS, "ncit/C34383")],
    ),
    Choice(
        sid="gilbert-syndrome",
        name="Gilbert syndrome",
        description="An autosomal recessive inherited disorder characterized by "
        "unconjugated hyperbilirubinemia, resulting in harmless "
        "intermittent jaundice.",
        parents=["disease"],
        annotations=[
            (BQB.IS, "ncit/C84729"),
            (BQB.IS, "efo/0005556"),
            (BQB.IS, "doid/DOID:2739"),
        ],
    ),
    Choice(
        sid="endocrine-system-disease",
        name="endocrine system disease",
        description="A disease of anatomical entity that is located_in endocrine glands "
        "which secretes a type of hormone directly into the bloodstream to "
        "regulate the body.",
        parents=["disease"],
        annotations=[(BQB.IS, "doid/DOID:28")],
    ),
    Choice(
        sid="thyroid-disease",
        name="thyroid disease",
        description="Thyroid disease. A disease involving the thyroid gland. A "
        "non-neoplastic or neoplastic disorder that affects the thyroid "
        "gland. Representative examples include hyperthyroidism, "
        "hypothyroidism, thyroiditis, follicular adenoma, and carcinoma.",
        parents=["endocrine system disease"],
        annotations=[
            (BQB.IS, "efo/1000627"),
            (BQB.IS, "ncit/C26893"),
        ],
        synonyms=["Thyroiditis", "thyroid gland disorders"],
    ),
    Choice(
        sid="hyperthyroidism",
        description="Overactivity of the thyroid gland resulting in overproduction of "
        "thyroid hormone and increased metabolic rate. Causes include "
        "diffuse hyperplasia of the thyroid gland (Graves disease), "
        "single nodule in the thyroid gland, and thyroiditis. The symptoms "
        "are related to the increased metabolic rate and include weight "
        "loss, fatigue, heat intolerance, excessive sweating, diarrhea, "
        "tachycardia, insomnia, muscle weakness, and tremor.",
        parents=["thyroid disease"],
        annotations=[
            (BQB.IS, "ncit/C3123"),
        ],
    ),
    Choice(
        sid="hypothyroidism",
        description="Abnormally low levels of thyroid hormone.",
        parents=["thyroid disease"],
        annotations=[
            (BQB.IS, "ncit/C26800"),
        ],
    ),
    Choice(
        sid="liver-disease",
        name="liver disease",
        description="A disease involving the liver. "
        "A non-neoplastic or neoplastic disorder that affects the "
        "liver parenchyma and/or intrahepatic bile ducts. Representative "
        "examples of non-neoplastic disorders include hepatitis, cirrhosis, "
        "cholangitis, and polycystic liver disease. Representative examples of "
        "neoplastic disorders include hepatocellular adenoma, "
        "hepatocellular carcinoma, intrahepatic cholangiocarcinoma, "
        "lymphoma, and angiosarcoma.",
        parents=["endocrine system disease"],
        annotations=[
            (BQB.IS, "efo/0001421"),
            (BQB.IS, "doid/DOID:409"),
            (BQB.IS, "ncit/C3196"),  # Liver and Intrahepatic Bile Duct Disorder
        ],
    ),
    Choice(
        sid="liver-disease-minimal",
        name="liver disease (minimal)",
        description="Minimal liver disease",
        parents=["liver disease"],
        annotations=[
            (BQB.IS_VERSION_OF, "efo/0001421"),
            (BQB.IS_VERSION_OF, "doid/DOID:409"),
            (BQB.IS_VERSION_OF, "ncit/C3196"),
        ],
    ),
    Choice(
        sid="liver-disease-mild",
        name="liver disease (mild)",
        description="Mild liver disease",
        parents=["liver disease"],
        annotations=[
            (BQB.IS_VERSION_OF, "efo/0001421"),
            (BQB.IS_VERSION_OF, "doid/DOID:409"),
            (BQB.IS_VERSION_OF, "ncit/C3196"),
        ],
    ),
    Choice(
        sid="liver-disease-moderate",
        name="liver disease (moderate)",
        description="Moderate liver disease",
        parents=["liver disease"],
        annotations=[
            (BQB.IS_VERSION_OF, "efo/0001421"),
            (BQB.IS_VERSION_OF, "doid/DOID:409"),
            (BQB.IS_VERSION_OF, "ncit/C3196"),
        ],
    ),
    Choice(
        sid="liver-disease-severe",
        name="liver disease (severe)",
        description="Severe or end-stage liver disease",
        parents=["liver disease"],
        annotations=[
            (BQB.IS_VERSION_OF, "efo/0001421"),
            (BQB.IS_VERSION_OF, "doid/DOID:409"),
            (BQB.IS_VERSION_OF, "ncit/C3196"),
        ],
    ),
    Choice(
        sid="hemochromatosis",
        name="hemochromatosis",
        description="Accumulation of iron in internal organs. Disorder due to the "
        "deposition of hemosiderin in the parenchymal cells, causing tissue "
        "damage and dysfunction of the liver, pancreas, heart, and pituitary.",
        parents=["liver disease"],
        annotations=[
            (BQB.IS_VERSION_OF, "ncit/C82892"),
            (BQB.IS_VERSION_OF, "efo/1000642"),
        ],
        synonyms=["HC"],
    ),
    Choice(
        sid="liver-damage",
        name="liver damage",
        description="Damage of the liver, e.g., necrosis due to acetaminophen overdose.",
        parents=["liver disease"],
        annotations=[],
    ),
    Choice(
        sid="subacute hepatic necrosis",
        name="subacute hepatic necrosis",
        description="Subacute hepatic necrosis.",
        parents=["liver-damage"],
        annotations=[],
        synonyms=["SHN"],
    ),
    Choice(
        sid="ascites",
        description="Ascites. An abdominal symptom consisting of an abnormal accumulation of serous fluid in the "
        "spaces between tissues and organs in the cavity of the abdomen. "
        "The accumulation of fluid in the peritoneal cavity, which may be serous, "
        "hemorrhagic, or the result of tumor metastasis to the peritoneum.",
        parents=["disease"],
        annotations=[
            (BQB.IS, "ncit/C2885"),
            (BQB.IS, "omit/0002587"),
        ],
    ),
    Choice(
        sid="stasis",
        description="Stasis. Cessation of movement of a body fluid or liquid.",
        parents=["disease"],
        annotations=[],
    ),
    Choice(
        sid="biliary-stasis",
        name="biliary stasis",
        description="Biliary stasis. Cessation of the flow of bile due to bile duct "
        "blockage or overproduction.",
        parents=["stasis"],
        annotations=[],
        synonyms=["intrahepatic billiary stasis"],
    ),
    Choice(
        sid="liver-stasis",
        name="liver stasis",
        description="Liver stasis. Cessation of the hepatic blood flow",
        parents=["stasis"],
        annotations=[],
        synonyms=[],
    ),
    Choice(sid="oedem", description="oedem", parents=["disease"], annotations=[]),
    Choice(
        sid="liver-oedem",
        name="liver oedem",
        description="Liver oedem",
        parents=["liver disease", "oedem"],
        annotations=[],
    ),
    Choice(
        sid="hepatocellular carcinoma",
        name="hepatocellular carcinoma",
        description="Hepatocellular carcinoma. A malignant tumor that arises from hepatocytes.",
        parents=["liver disease"],
        annotations=[(BQB.IS, "ncit/C3099")],
    ),
    MeasurementType(
        sid="cirrhotic-liver-disease",
        name="cirrhotic liver disease",
        description="Any type of cirrhotic liver disease. See also `liver cirrhosis` or"
        "`non-cirrhotic liver disease`.",
        parents=["liver disease"],
        dtype=DType.ABSTRACT,
        annotations=[],
    ),
    Choice(
        sid="liver-cirrhosis",
        name="liver cirrhosis",
        description="Liver disease in which the normal microcirculation, the gross "
        "vascular anatomy, and the hepatic architecture have been variably "
        "destroyed and altered with fibrous septa surrounding regenerated "
        "or regenerating parenchymal nodules.",
        parents=["cirrhotic liver disease"],
        annotations=[(BQB.IS, "doid/DOID:5082")],
    ),
    Choice(
        sid="decompensated-liver-cirrhosis",
        name="decompensated liver cirrhosis",
        description="Decompensated liver cirrhosis",
        parents=["liver cirrhosis"],
        annotations=[],
    ),
    Choice(
        sid="shock",
        name="shock",
        description="Shock. Shock is the state of insufficient blood flow to the "
        "tissues of the body as a result of problems with the circulatory "
        "system. A life-threatening condition that requires immediate "
        "medical intervention. It is characterized by reduced blood flow "
        "that may result in damage of multiple organs. Types of shock "
        "include cardiogenic, hemorrhagic, septic, anaphylactic, "
        "and traumatic shock.",
        parents=["disease"],
        annotations=[],
        synonyms=[],
    ),
    Choice(
        sid="shock-liver",
        name="shock liver",
        description="Shock liver. Profound and widespread reduction of effective "
        "tissue perfusion leads first to reversible, and then if "
        "prolonged, to irreversible cellular injury.",
        parents=["liver disease"],
        annotations=[],
        synonyms=[],
    ),
    Choice(
        sid="alcoholic-liver-disease",
        name="alcoholic liver disease",
        description="Alcoholic liver disease. A disorder caused by damage to the "
        "liver parenchyma due to alcohol consumption. It may present with "
        "an acute onset or follow a chronic course, leading to cirrhosis.",
        parents=["liver disease"],
        annotations=[
            (BQB.IS, "ncit/C34783"),
            (BQB.IS, "efo/0008573"),
        ],
        synonyms=["alcohol liver disease", "ALD"],
    ),
    Choice(
        sid="alcoholic-liver-cirrhosis",
        name="alcoholic liver cirrhosis",
        description="alcoholic liver cirrhosis",
        parents=["liver cirrhosis", "alcoholic liver disease"],
        annotations=[(BQB.IS, "doid/DOID:14018")],
    ),
    Choice(
        sid="postnecrotic-cirrhosis",
        name="postnecrotic cirrhosis",
        description="Postnecrotic cirrhosis",
        parents=["liver cirrhosis"],
        annotations=[],
    ),
    Choice(
        sid="cryptogenic-cirrhosis",
        name="cryptogenic cirrhosis",
        description="Cirrhosis in which no causative agent can be identified.",
        parents=["liver cirrhosis"],
        annotations=[(BQB.IS, "ncit/C84411")],
    ),
    Choice(
        sid="non-cirrhotic-liver-disease",
        name="non-cirrhotic liver disease",
        description="non-cirrhotic liver disease",
        parents=["liver disease"],
    ),
    Choice(
        sid="hepatitis",
        description="Hepatitis. Inflammation of the liver; usually from a viral "
        "infection, but sometimes from toxic agents.",
        parents=["liver disease"],
        annotations=[
            (BQB.IS, "ncit/C3095"),
            (BQB.IS, "hp/HP:0012115"),
            (BQB.IS, "doid/DOID:2237"),
        ],
    ),
    Choice(
        sid="alcoholic-hepatitis",
        name="alcoholic-hepatitis",
        description="Alcoholic hepatitis.",
        parents=["hepatitis"],
        annotations=[
            (BQB.IS, "doid/DOID:12351"),
        ],
    ),
    Choice(
        sid="drug-induced-hepatitis",
        name="drug-induced hepatitis",
        description="Drug-induced hepatitis.",
        parents=["hepatitis"],
        annotations=[
            (BQB.IS, "doid/DOID:2044"),
        ],
    ),
    Choice(
        sid="viral-hepatitis",
        name="viral hepatitis",
        description="A hepatitis that involves viral infection causing inflammation of "
        "the liver.",
        parents=["hepatitis"],
        annotations=[
            (BQB.IS, "doid/DOID:1844"),
        ],
    ),
    Choice(
        sid="hepatitis-b",
        name="hepatitis B",
        description="A hepatitis that involves viral infection by Hepatitis B virus causing inflammation of "
        "the liver.",
        parents=["viral-hepatitis"],
        annotations=[
            (BQB.IS, "doid/DOID:2043"),
        ],
        synonyms=["HBV"],
    ),
    Choice(
        sid="hcv",
        name="hcv",
        label="Hepatitis C virus (HCV)",
        description="Hepatitis C virus (HCV) infection. A viral infectious disease that results_in "
        "inflammation located_in liver, has_material_basis_in Hepatitis C virus, "
        "which is transmitted_by blood from an infected person enters the body of an "
        "uninfected person. The infection has_symptom fever, has_symptom fatigue, "
        "has_symptom loss of appetite, has_symptom nausea, has_symptom vomiting, "
        "has_symptom abdominal pain, has_symptom clay-colored bowel movements, "
        "has_symptom joint pain, and has_symptom jaundice.",
        parents=["viral hepatitis"],
        annotations=[
            (BQB.IS_VERSION_OF, "doid/DOID:1883"),
            (BQB.IS_VERSION_OF, "ncit/C14312"),
        ],
        synonyms=["hepatitis C"],
    ),
    Choice(
        sid="chronic-hepatitis",
        name="chronic hepatitis",
        description="An active inflammatory process affecting the liver for more than "
        "six months. Causes include viral infections, autoimmune "
        "disorders, drugs, and metabolic disorders.",
        parents=["hepatitis"],
        annotations=[
            (BQB.IS, "ncit/C82978"),
            (BQB.IS, "efo/0008496"),
        ],
    ),
    Choice(
        sid="biliary-liver-disease",
        name="biliary liver disease",
        description="A non-neoplastic or neoplastic disorder that affects the intrahepatic "
        "or extrahepatic bile ducts or the gallbladder. Representative "
        "examples of non-neoplastic disorders include cholangitis and "
        "cholecystitis. Representative examples of neoplastic disorders "
        "include extrahepatic bile duct adenoma, intrahepatic and "
        "extrahepatic cholangiocarcinoma, and gallbladder carcinoma.",
        parents=["liver disease"],
        annotations=[
            (BQB.IS_VERSION_OF, "ncit/C2899"),
        ],
    ),
    Choice(
        sid="biliary-obstruction",
        name="biliary obstruction",
        description="Blockage in the biliary tract that carries bile from the liver "
        "to the gallbladder and small intestine. Causes include gallstones, "
        "biliary tract strictures and inflammation, pancreatitis, cirrhosis, "
        "lymph node enlargement, and bile duct and pancreas neoplasms.",
        parents=["biliary liver disease"],
        annotations=[
            (BQB.IS_VERSION_OF, "ncit/C60698"),
        ],
    ),
    Choice(
        sid="pbc",
        name="pbc",
        label="PBC",
        description="Primary biliary cholangitis or primary biliary cirrhosis (PBC)."
        "(autoimune disease of the liver)",
        parents=["biliary liver disease"],
        annotations=[
            (BQB.IS_VERSION_OF, "ncit/C26718"),
        ],
    ),
    Choice(
        sid="fatty-liver-disease",
        name="fatty liver disease",
        description="Fatty liver disease. A reversible condition wherein large vacuoles "
        "of triglyceride fat accumulate in liver cells via the process "
        "of steatosis. ",
        parents=["non-cirrhotic liver disease"],
        annotations=[(BQB.IS, "mondo/MONDO:0004790")],
    ),
    Choice(
        sid="nafld",
        name="nafld",
        label="NAFLD",
        description="Non-alcoholic fatty liver disease (NAFLD). "
        "A term referring to fatty replacement of the hepatic parenchyma "
        "which is not related to alcohol use.",
        parents=["fatty liver disease"],
        annotations=[(BQB.IS, "ncit/C84444"), (BQB.IS, "efo/0003095")],
    ),
    Choice(
        sid="nash",
        name="nash",
        label="NASH",
        description="Non-alcoholic steato-hepatitis (NASH). Fatty replacement and "
        "damage to the hepatocytes not related to alcohol use. "
        "It may lead to cirrhosis and liver failure.",
        parents=["nafld"],
        annotations=[
            (BQB.IS, "efo/1001249"),
            (BQB.IS, "ncit/C84445"),
        ],
    ),
    Choice(
        sid="miscellaneous-liver-disease",
        name="miscellaneous liver disease",
        description="Liver disease not clearly characterized in any other "
        "liver disease.",
        parents=["liver disease"],
    ),
    Choice(
        sid="liver-fibrosis",
        name="liver fibrosis",
        description="Fibrosis of the liver.",
        parents=["liver disease"],
        annotations=[
            (BQB.IS, "hp/HP:0001395"),
            (BQB.IS_VERSION_OF, "ncit/C3044"),  # fibrosis
            (BQB.IS_VERSION_OF, "efo/0006890"),  # fibrosis
        ],
    ),
    Choice(
        sid="liver-fibrosis-f1",
        name="liver fibrosis (F1)",
        description="Fibrosis of the liver (F1 stage).",
        parents=["liver fibrosis"],
    ),
    Choice(
        sid="liver-fibrosis-f2",
        name="liver fibrosis (F2)",
        description="Fibrosis of the liver (F4 stage).",
        parents=["liver fibrosis"],
    ),
    Choice(
        sid="liver-fibrosis-f3",
        name="liver fibrosis (F3)",
        description="Fibrosis of the liver (F4 stage).",
        parents=["liver fibrosis"],
    ),
    Choice(
        sid="liver-fibrosis-f4",
        name="liver fibrosis (F4)",
        description="Fibrosis of the liver (F4 stage).",
        parents=["liver fibrosis"],
    ),
    Choice(
        sid="renal-disease",
        name="renal disease",
        description="Renal disease or kidney disorder. "
        "A neoplastic or non-neoplastic condition affecting the kidney. "
        "Representative examples of non-neoplastic conditions include "
        "glomerulonephritis and nephrotic syndrome. Representative examples of "
        "neoplastic conditions include benign processes "
        "(e.g., renal lipoma and renal fibroma) and malignant processes "
        "(e.g., renal cell carcinoma and renal lymphoma).",
        parents=["disease"],
        synonyms=["kidney disease"],
        annotations=[
            (BQB.IS, "ncit/C3149"),
            (BQB.IS, "efo/0003086"),
        ],
    ),
    Choice(
        sid="renal-disease-mild",
        name="renal disease (mild)",
        description="Mild renal disease.",
        parents=["renal disease"],
    ),
    Choice(
        sid="renal-disease-moderate",
        name="renal disease (moderate)",
        description="moderate renal disease (not requiring dialysis)",
        parents=["renal disease"],
    ),
    Choice(
        sid="renal-disease-end-stage",
        name="renal disease (end-stage)",
        description="severe or end-stage renal disease (requiring dialysis)",
        synonyms=["chronic renal failure"],
        parents=["renal disease"],
    ),
    Choice(
        sid="pyelonephritis",
        description="Pyelonephritis. An inflammatory process affecting "
        "the kidney. The cause is most often bacterial, but may "
        "also be fungal in nature. Signs and symptoms may "
        "include fever, chills, flank pain, painful and frequent "
        "urination, cloudy or bloody urine, and confusion.",
        parents=["renal disease"],
        annotations=[(BQB.IS, "ncit/C34965"), (BQB.IS, "efo/1001141")],
    ),
    Choice(
        sid="chronic-pyelonephritis",
        name="chronic pyelonephritis",
        description="Chronic pyelonephritis. Persistent pyelonephritis.",
        parents=["pyelonephritis"],
        annotations=[
            (BQB.IS, "ncit/C123216"),
        ],
    ),
    Choice(
        sid="cystic-kidney-disease",
        name="cystic kidney disease",
        description="Cystic kidney disease. A congenital or acquired kidney disorder characterized by the presence of renal cysts.",
        synonyms=["cystic degeneration of the kidney"],
        parents=["renal disease"],
        annotations=[
            (BQB.IS, "efo/0008615"),
        ],
    ),
    Choice(
        sid="anephric",
        description="Loss of kidneys mostly surgically.",
        parents=["renal disease (end-stage)"],
    ),
    Choice(
        sid="glomerulonephritis",
        description="Glomerulonephritis. A renal disorder characterized by "
        "damage in the glomeruli. It may be acute or chronic, "
        "focal or diffuse, and it may lead to renal failure. "
        "Causes include autoimmune disorders, infections, "
        "diabetes, and malignancies.",
        parents=["renal disease"],
        annotations=[(BQB.IS, "ncit/C26784")],
    ),
    Choice(
        sid="chronic-glomerulonephritis",
        name="chronic glomerulonephritis",
        description="Chronic glomerulonephritis. A chronic, persistent "
        "inflammation of the glomeruli, which is slowly progressive, "
        "leading to impaired kidney function.",
        parents=["glomerulonephritis"],
        annotations=[
            (BQB.IS, "ncit/C35173"),
        ],
    ),
    Choice(
        sid="acute-glomerulonephritis",
        name="acute glomerulonephritis",
        description="Acute glomerulonephritis.",
        parents=["glomerulonephritis"],
        annotations=[(BQB.IS_VERSION_OF, "ncit/C26784")],
    ),
    Choice(
        sid="focal-glomerulonephritis",
        name="focal glomerulonephritis",
        description="Focal glomerulonephritis.",
        parents=["glomerulonephritis"],
        annotations=[(BQB.IS_VERSION_OF, "ncit/C26784")],
    ),
    Choice(
        sid="diffuse-glomerulonephritis",
        name="diffuse glomerulonephritis",
        description="Diffuse glomerulonephritis.",
        parents=["glomerulonephritis"],
        annotations=[(BQB.IS_VERSION_OF, "ncit/C26784")],
    ),
    Choice(
        sid="heart-disease",
        name="heart disease",
        description="Pathological conditions involving the HEART including its structural "
        "and functional abnormalities.",
        parents=["disease"],
        annotations=[
            (BQB.IS, "efo/0003777"),
            (BQB.IS, "doid/DOID:114"),
        ],
    ),
    Choice(
        sid="heart-failure",
        name="heart failure",
        description="Heart failure. Inability of the heart to pump blood at an adequate rate to meet tissue "
        "metabolic requirements. Clinical symptoms of heart failure include: unusual dyspnea on light "
        "exertion, recurrent dyspnea occurring in the supine position, fluid retention or rales, "
        "jugular venous distension, pulmonary edema on physical exam.",
        parents=["heart disease"],
        annotations=[
            (BQB.IS, "ncit/C50577"),
            (BQB.IS, "efo/0003144"),
        ],
    ),
    Choice(
        sid="cardiac-arrhythmia",
        name="cardiac arrhythmia",
        description="Cardiac arrythmia. Any disturbances of the normal rhythmic "
        "beating of the heart or myocardial contraction. Cardiac arrhythmias "
        "can be classified by the abnormalities in HEART RATE, disorders of "
        "electrical impulse generation, or impulse conduction.",
        parents=["heart disease"],
        annotations=[
            (BQB.IS, "omit/0002531"),
            (BQB.IS, "efo/0004269"),
        ],
    ),
    Choice(
        sid="ischemic-heart-disease",
        name="ischemic heart disease",
        description="A disorder of cardiac function caused by insufficient blood flow "
        "to the muscle tissue of the heart. The decreased blood flow may "
        "be due to narrowing of the coronary arteries,"
        "to obstruction by a thrombus, or less commonly, to diffuse narrowing of arterioles and other small vessels within the heart. Severe interruption of the blood supply to the"
        "myocardial tissue may result in necrosis of cardiac muscle (myocardial infarction).",
        parents=["heart disease"],
        annotations=[
            (BQB.IS, "ncit/C50625"),
        ],
    ),
    Choice(
        sid="myocardial-infarction",
        name="myocardial infarction",
        description="Gross necrosis of the myocardium, as a result of interruption of the blood supply to the area, as in coronary thrombosis.",
        parents=["heart disease"],
        annotations=[
            (BQB.IS, "ncit/C27996"),
        ],
    ),
    Choice(
        sid="premature-ventricular-contraction",
        name="premature ventricular contraction",
        description="Extra beats beginning in the ventricles, that can disrupt the regular heart rhythm.",
        parents=["heart disease"],
        synonyms=["VPB", "PVC"],
        annotations=[
            (BQB.IS, "ncit/C54936"),
        ],
    ),
    Choice(
        sid="ventricular-fibrillation",
        name="ventricular fibrillation",
        description="A disorder characterized by an electrocardiographic finding of a "
        "rapid grossly irregular ventricular rhythm with marked variability "
        "in QRS cycle length, morphology, and amplitude. "
        "The rate is typically greater than 300 bpm.",
        parents=["heart disease"],
        synonyms=[],
        annotations=[
            (BQB.IS, "ncit/C50799"),
            (BQB.IS, "omit/0015525"),
            (BQB.IS, "efo/0004287"),
        ],
    ),
    Choice(
        sid="primary-ventricular-fibrillation",
        name="primary ventricular fibrillation",
        description="PVF is defined as ventricular fibrillation not preceded by heart "
        "failure or shock, in contrast to secondary ventricular "
        "fibrillation, which is. Ventricular fibrillation is characterized "
        "by an electrocardiographic finding of a rapid grossly irregular ventricular rhythm.",
        parents=["ventricular fibrillation"],
        synonyms=["PVF"],
        annotations=[
            (BQB.IS_VERSION_OF, "ncit/C50799"),
            (BQB.IS_VERSION_OF, "omit/0015525"),
            (BQB.IS_VERSION_OF, "efo/0004287"),
        ],
    ),
    Choice(
        sid="hypercholesterolemia",
        description="A laboratory test result indicating an increased amount of"
        "cholesterol in the blood; Abnormally high level of cholesterol"
        "in the blood. See also 'FH', 'homozygote FH' and 'heterozygote FH'",
        parents=["disease"],
        annotations=[(BQB.IS, "ncit/C37967"), (BQB.IS, "efo/0003124")],
    ),
    Choice(
        sid="mixed-hypercholesterolemia",
        name="mixed hypercholesterolemia",
        description="A type of hypercholesterolemia with elevated LDL-C and triglyceride plasma levels.",
        parents=["hypercholesterolemia"],
        annotations=[],
        synonyms=["combined hypercholesterolemia"],
    ),
    Choice(
        sid="familial-hypercholesterolemia",
        name="FH",
        label="familial hypercholesterolemia (FH)",
        description="A familial hyperlipidemia characterized by very high levels of "
        "low-density lipoprotein (LDL) and early cardiovascular disease.",
        parents=["hypercholesterolemia"],
        annotations=[(BQB.IS, "doid/DOID:13810"), (BQB.IS, "efo/0004911")],
    ),
    Choice(
        sid="homozygous-familial-hypercholesterolemia",
        name="homozygous FH",
        label="homozygous familial hypercholesterolemia (FH)",
        description=" A familial hypercholesterolemia that is characterized by very "
        "high levels of low-density lipoprotein (LDL) cholesterol "
        "(usually above 400 mg/dl) and increased risk of premature "
        "atherosclerotic cardiovascular disease, and has_material_basis_in "
        "autosomal recessive homozygous mutation in the low density "
        "lipoprotein receptor adaptor protein 1 gene (LDLRAP1) "
        "on chromosome 1p36. "
        "See also 'heterozygous FH'.",
        parents=["familial hypercholesterolemia"],
        synonyms=["autosomal recessive hypercholesterolemia"],
        annotations=[
            (BQB.IS, "doid/DOID:0090105"),
        ],
    ),
    Choice(
        sid="heterozygous-familial-hypercholesterolemia",
        name="heterozygous FH",
        label="heterozygous familial hypercholesterolemia (FH)",
        description="An autosomal dominant condition caused by mutation(s) in the "
        "APOB gene, encoding apolipoprotein B-100. It is characterized by "
        "hypercholesterolemia and abnormal low-density lipoproteins. "
        "See also 'homozygous FH'.",
        parents=["familial hypercholesterolemia"],
        synonyms=["autosomal dominant hypercholesterolemia"],
        annotations=[
            (BQB.IS, "ncit/C176014"),
        ],
    ),
    Choice(
        sid="infectious-disorder",
        name="infectious disorder",
        description="A disorder resulting from the presence and activity of a microbial, "
        "viral, fungal, or parasitic agent. It can be transmitted by direct or "
        "indirect contact.",
        parents=["disease"],
        annotations=[
            (BQB.IS, "ncit/C26726"),
        ],
    ),
    Choice(
        sid="malaria",
        description="Malaria or plasmodium falciparum infection. "
        "A protozoan infection caused by the genus Plasmodium. There are four "
        "species of Plasmodium that can infect humans: Plasmodium falciparum, "
        "vivax, ovale, and malariae. It is transmitted to humans by infected "
        "mosquitoes. Signs and symptoms include paroxysmal high fever, "
        "sweating, chills, and anemia.",
        parents=["infectious disorder"],
        annotations=[
            (BQB.IS, "ncit/C34797"),
            (BQB.IS, "efo/0001068"),
            (BQB.IS, "doid/DOID:12365"),
        ],
    ),
    Choice(
        sid="neuronal-disease",
        name="neuronal disease",
        description="Neuronal or brain disease. A disease affecting the brain or part "
        "of the brain.",
        parents=["disease"],
        annotations=[(BQB.IS, "efo/0005774")],
    ),
    Choice(
        sid="psychatric-disorder",
        name="psychatric disorder",
        description="A disorder characterized by behavioral and/or psychological "
        "abnormalities, often accompanied by physical symptoms. The symptoms "
        "may cause clinically significant distress or impairment in social and "
        "occupational areas of functioning. Representative examples include "
        "anxiety disorders, cognitive disorders, mood disorders and "
        "schizophrenia.",
        parents=["neuronal disease"],
        annotations=[
            (BQB.IS, "ncit/C2893"),
        ],
    ),
    Choice(
        sid="schizophrenia",
        description="Schizophrenia. A major psychotic disorder characterized by "
        "abnormalities in the perception or expression of reality. "
        "It affects the cognitive and psychomotor functions. Common clinical "
        "signs and symptoms include delusions, hallucinations, disorganized "
        "thinking, and retreat from reality.",
        parents=["neuronal disease"],
        annotations=[(BQB.IS, "ncit/C3362"), (BQB.IS, "efo/0000692")],
    ),
    Choice(
        sid="epilepsy",
        description="Epilepsy is a disorder characterized by recurrent episodes of "
        "paroxysmal brain dysfunction due to a sudden, disorderly, and "
        "excessive neuronal discharge. Epilepsy classification systems are "
        "generally based upon: (1) clinical features of the seizure episodes "
        "(e.g., motor seizure), (2) etiology (e.g., post-traumatic), "
        "(3) anatomic site of seizure origin (e.g., frontal lobe seizure), "
        "(4) tendency to spread to other structures in the brain, and "
        "(5) temporal patterns (e.g., nocturnal epilepsy).",
        parents=["neuronal disease"],
        annotations=[(BQB.IS, "efo/0000474")],
    ),
    Choice(
        sid="migraine",
        description="A common, severe type of vascular headache often associated with "
        "increased sympathetic activity, resulting in nausea, vomiting, "
        "and light sensitivity. A class of disabling primary headache disorders, "
        "characterized by recurrent unilateral pulsatile headaches. "
        "The two major subtypes are common migraine (without aura) and "
        "classic migraine (with aura or neurological symptoms).",
        parents=["neuronal disease"],
        annotations=[
            (BQB.IS, "efo/0003821"),
            (BQB.IS, "doid/DOID:6364"),
            (BQB.IS, "ncit/C89715"),
        ],
    ),
    Choice(
        sid="disease-of-glucose-metabolism",
        name="disease of glucose metabolism",
        description="Disease of glucose metabolism or abnormality of glucose homeostasis.",
        parents=["disease"],
        annotations=[
            (BQB.IS_VERSION_OF, "hp/HP:0011014"),
            (BQB.IS_VERSION_OF, "go/GO:0042593"),
        ],
    ),
    Choice(
        sid="impaired-glucose-tolerance",
        name="impaired glucose tolerance",
        label="impaired glucose tolerance (IGT)",
        description="Impaired glucose tolerance (IGT) is an abnormal resistance to "
        "glucose, i.e., a reduction in the ability to maintain glucose levels "
        "in the blood stream within normal limits following oral or "
        "intravenous administration of glucose.",
        parents=["disease of glucose metabolism"],
        annotations=[
            (BQB.IS, "hp/HP:0040270"),
            (BQB.IS, "mp/MP:0005293"),
            (BQB.IS, "efo/0002546"),
        ],
    ),
    Choice(
        sid="diabetes",
        description="Diabetes is a metabolic disorder characterized by abnormally high "
        "blood sugar levels due to diminished production of insulin or "
        "insulin resistance/desensitization.",
        parents=["disease of glucose metabolism"],
        annotations=[
            (BQB.IS, "ncit/C2985"),
            (BQB.IS, "efo/0000400"),
        ],
    ),
    Choice(
        sid="type-1-diabetes-mellitus",
        name="t1dm",
        label="type 1 diabetes mellitus (T1DM)",
        description="Diabetes mellitus type 1",
        parents=["diabetes"],
        annotations=[
            (BQB.IS, "ncit/C2986"),
            (BQB.IS, "efo/0001359"),
        ],
    ),
    Choice(
        sid="type-2-diabetes-mellitus",
        name="t2dm",
        label="type 2 diabetes mellitus (T2DM)",
        description="Diabetes mellitus type 2. A type of diabetes mellitus that is "
        "characterized by insulin resistance or desensitization and increased "
        "blood glucose levels. This is a chronic disease that can develop "
        "gradually over the life of a patient and can be linked to both "
        "environmental factors and heredity.",
        parents=["diabetes"],
        annotations=[
            (BQB.IS, "ncit/C26747"),
            (BQB.IS, "doid/DOID:9352"),
            (BQB.IS, "efo/0001360"),
        ],
    ),
    Choice(
        sid="diabetic-nephropathy",
        name="diabetic nephropathy",
        description="Diabetic nephropathy. Progressive kidney disorder "
        "caused by vascular damage to the glomerular "
        "capillaries, in patients with diabetes mellitus. "
        "It is usually manifested with nephritic syndrome and glomerulosclerosis.",
        parents=["renal disease", "diabetes"],
        annotations=[
            (BQB.IS, "ncit/C84417"),
            (BQB.IS, "efo/0000401"),
        ],
    ),
    Choice(
        sid="lung-cancer",
        name="lung cancer",
        description="Lung cancer. (LNCR) - A common malignancy affecting "
        "tissues of the lung. The most common form of lung cancer "
        "is non-small cell lung cancer (NSCLC) that can be divided "
        "into 3 major histologic subtypes - squamous cell carcinoma, "
        "adenocarcinoma, and large cell lung cancer.",
        parents=["cancer"],
        synonyms=["Lung carcinoma", "LNCR"],
        annotations=[(BQB.IS, "ncit/C2926")],
    ),
    Choice(
        sid="nsclc",
        name="NSCLC",
        label="Non small cell lung cancer (NSCLC)",
        description="Non small cell lung cancer (NSCLC). The most common form of lung cancer "
        "is non-small cell lung cancer (NSCLC) that can be divided "
        "into 3 major histologic subtypes - squamous cell carcinoma, "
        "adenocarcinoma, and large cell lung cancer."
        "NSCLC is often diagnosed at an advanced stage and has a "
        "poor prognosis.",
        parents=["lung cancer"],
        synonyms=["Lung Non-Small Cell Carcinoma."],
        annotations=[(BQB.IS, "efo/0003060")],
    ),
    Choice(
        sid="pancreatic-disease",
        name="pancreatic disease",
        description="Pancreatic disease. A non-neoplastic or neoplastic disorder "
        "that affects the pancreas. Representative examples of "
        "non-neoplastic disorders include pancreatitis and "
        "pancreatic insufficiency. Representative examples of "
        "neoplastic disorders include cystadenomas, carcinomas, "
        "lymphomas, and neuroendocrine neoplasms.",
        parents=["disease"],
        annotations=[
            (BQB.IS, "efo/0009605"),
        ],
    ),
    Choice(
        sid="chronic-pancreatitis",
        name="chronic pancreatitis",
        description="long-standing inflammation of the pancreas",
        parents=["pancreatic disease"],
        annotations=[(BQB.IS, "efo/0000342"), (BQB.IS, "ncit/C84637")],
    ),
    Choice(
        sid="extrahepatic-portal-obstruction",
        name="extrahepatic portal obstruction",
        description="Extrahepatic Portal Obstruction. An obstruction of the "
        "extrahepatic portal vein.",
        parents=["liver disease"],
        annotations=[],
    ),
    Choice(
        sid="asthma",
        name="asthma",
        description="Asthma. A chronic respiratory disease manifested as difficulty "
        "breathing due to the narrowing of bronchial passageways. "
        "Asthma is characterized by increased responsiveness of the "
        "tracheobronchial tree to multiple stimuli, leading to narrowing "
        "of the air passages with resultant dyspnea, cough, and wheezing.",
        parents=["disease"],
        annotations=[
            (BQB.IS, "ncit/C28397"),
            (BQB.IS, "efo/0000270"),
        ],
    ),
    Choice(
        sid="central sleep apnea",
        name="central sleep apnea",
        description="Central Sleep Apnea. The periodic cessation of breathing while "
        "asleep that occurs secondary to the decreased responsiveness of "
        "the respiratory center of the brain to carbon dioxide, resulting "
        "in alternating cycles of apnea and hyperpnea.",
        parents=["disease"],
        annotations=[
            (BQB.IS, "ncit/C116046"),
        ],
    ),
    Choice(
        "hypertension",
        description="Blood pressure that is abnormally high. "
        "Persistently high systemic arterial blood pressure. Based on "
        "multiple readings, hypertension is currently defined as when "
        "systolic pressure is consistently greater than 140 mm Hg or when "
        "diastolic pressure is consistently 90 mm Hg or more ."
        "Use in addition 'blood pressure (categorical)' with choice 'elevated'. "
        "See also 'blood pressure'.",
        parents=["disease"],
        # dtype=DType.BOOLEAN,
        annotations=[
            (BQB.IS, "ncit/C3117"),
            (BQB.IS, "efo/0000537"),
        ],
        synonyms=["hypertensive"],
    ),
    Choice(
        sid="cardiovascular_disease",
        name="cardiovascular disease",
        description="A disease involving the cardiovascular system.",
        parents=["disease"],
        annotations=[
            (BQB.IS, "ncit/C2931"),
            (BQB.IS, "doid/DOID:1287"),
            (BQB.IS, "efo/0000319"),
        ],
    ),
    Choice(
        sid="chronic-bronchitis",
        name="chronic bronchitis",
        description="A type of chronic obstructive pulmonary disease characterized by chronic inflammation in the bronchial tree that results in edema, mucus production,"
        "obstruction, and reduced airflow to and from the lung alveoli. The most common cause is tobacco smoking. Signs and symptoms include coughing with excessive mucus production,"
        "and shortness of breath.",
        parents=["disease"],
        annotations=[
            (BQB.IS, "ncit/C26722"),
        ],
    ),
    Choice(
        sid="stroke",
        name="stroke",
        description="A disorder characterized by a decrease or absence of blood supply to the brain caused by obstruction (thrombosis or embolism) of an artery resulting in neurological damage.",
        parents=["disease"],
        annotations=[
            (BQB.IS, "ncit/C143862"),
        ],
    ),
    # -------------------------------------------------------------------------
    # Disease history
    # -------------------------------------------------------------------------
    MeasurementType(
        sid="family-history-disease",
        name="family history disease",
        description="Family history of disease. To encode the actual disease use "
        "'disease'.",
        parents=["health status"],
        dtype=DType.NUMERIC_CATEGORICAL,
        units=["year", NO_UNIT],
        annotations=[],
    ),
    MeasurementType(
        "family-history-diabetes",
        name="family history diabetes",
        description="Family history of diabetes.",
        parents=["family-history-disease"],
        dtype=DType.BOOLEAN,
    ),
]
