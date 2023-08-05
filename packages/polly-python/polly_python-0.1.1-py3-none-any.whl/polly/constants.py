DATA_TYPES = {
    "Mutation": [
        {
            "format": ["maf"],
            "supported_repo": [
                {
                    "name": "cbioportal",
                    "header_mapping": {
                        "gene": "Hugo_Symbol",
                        "chr": "Chromosome",
                        "startPosition": "Start_Position",
                        "endPosition": "End_Position",
                        "referenceAllele": "Reference_Allele",
                        "variantAllele": "Tumor_Seq_Allele2",
                        "mutationType": "Variant_Classification",
                        "variantType": "Variant_Type",
                        "uniqueSampleKey": "Tumor_Sample_Barcode",
                    },
                },
                {"name": "tcga", "header_mapping": {}},
            ],
        }
    ]
}

# endpoints
CONSTANTS_ENDPOINT = "/constants"
REPOSITORIES_ENDPOINT = "/repositories"
REPOSITORY_PACKAGE_ENDPOINT = REPOSITORIES_ENDPOINT + "/{}/packages"
IMAGE_URL_ENDPOINT = (
    "https://elucidatainc.github.io/PublicAssets/discover-fe-assets/omixatlas_hex.svg"
)

# statuscodes
OK = 200
CREATED = 201
COMPUTE_ENV_VARIABLE = "POLLY_TYPE"

# cohort constants
COHORT_CONSTANTS_URL = (
    "https://elucidatainc.github.io/PublicAssets/cohort_constants.txt"
)
OBSOLETE_METADATA_FIELDS = [
    "package",
    "region",
    "bucket",
    "key",
    "file_type",
    "file_location",
    "src_uri",
    "timestamp_",
]
dot = "."
