""" Info nodes with calculation types."""
from pkdb_data.management.info_node import CalculationType, DType
from pkdb_data.metadata.annotation import BQB


CALCULATION_NODES = [
    CalculationType(
        "calculation", description="", parents=[], dtype=DType.ABSTRACT, annotations=[]
    ),
    CalculationType(
        "geometric mean",
        description="The geometric mean is defined as the nth root of the product of n numbers, i.e., for a set of "
        "numbers \{x_i\}_{i=1}^N, the geometric mean is defined as \left(\prod_{i=1}^N x_i\right)^{1/N}.",
        parents=["calculation"],
        dtype=DType.CATEGORICAL,
        annotations=[
            (BQB.IS, "stato/STATO:0000396"),
        ],
    ),
    CalculationType(
        "sample mean",
        description="the sample mean of sample of size n with n observations is an arithmetic mean computed over "
        "n number of observations on a statistical sample. The sample mean, denoted x¯ and read “x-bar,” is"
        "simply the average of the n data points x1, x2, ..., xn: x¯=x1+x2+⋯+xnn=1n∑i=1nxi The sample mean"
        " summarizes the “location“ or “center“ of the data. the sample mean is a measure of dispersion "
        "of the observations made on the sample and provides an unbias estimate of the population mean",
        parents=["calculation"],
        dtype=DType.CATEGORICAL,
        annotations=[
            (BQB.IS, "stato/STATO:0000401"),
        ],
    ),
]
