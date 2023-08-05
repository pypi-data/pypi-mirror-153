import os
import ssl
import json
import base64
from polly import helpers
from pathlib import Path
import requests
import logging
import pandas as pd
from polly.auth import Polly
from polly import constants as const
from polly.omixatlas import OmixAtlas
from polly.errors import (
    InvalidCohortNameException,
    InvalidCohortOperationException,
    paramException,
    InvalidParameterException,
    InvalidPathException,
    InvalidRepoException,
    InvalidDatasetException,
    CohortEditException,
    EmptyCohortException,
    InvalidCohortPathException,
    InvalidCohortMergeOperation,
    error_handler,
)
from polly.constants import OBSOLETE_METADATA_FIELDS, dot
import shutil
from joblib import Parallel, delayed
import datetime
from deprecated import deprecated
from cmapPy.pandasGEXpress.parse import parse
from cmapPy.pandasGEXpress.concat import assemble_data
from polly.help import example, doc


class Cohort:
    """
    The Cohort class contains functions which can be used to create cohorts, add or remove samples,\
merge metadata and data-matrix of samples/datasets in a cohort and edit or delete a cohort.

    ``Args:``
        |  ``token (str):`` token copy from polly.

    .. code::


            from polly.cohort import Cohort
            # To use this class initialize a object like this if you are not authorised on polly
            cohort = Cohort(token)

    If you are authorised then you can initialize object without token to know about :ref:`authentication <auth>`.
    """

    _cohort_info = None
    example = classmethod(example)
    doc = classmethod(doc)

    def __init__(self, token=None, env="", default_env="polly") -> None:
        # check if COMPUTE_ENV_VARIABLE present or not
        # if COMPUTE_ENV_VARIABLE, give priority
        env = helpers.get_platform_value_from_env(
            const.COMPUTE_ENV_VARIABLE, default_env, env
        )
        self.session = Polly.get_session(token, env=env)
        self.base_url = f"https://v2.api.{self.session.env}.elucidata.io"
        self.folder_path = None
        self._cohort_details = None
        if self._cohort_info is None:
            self._cohort_info = helpers.get_cohort_constants()

    def _read_gcts(self, dataset_ids: list, file_path: str) -> pd.DataFrame:
        gct_files = [
            f"{file_path}/{self._cohort_details.get('entity_id',{}).get(dataset_id)[0]}_{dataset_id}.gct"
            for dataset_id in dataset_ids
        ]
        results_gct = Parallel(n_jobs=4)(
            delayed(parse)(gct_file) for gct_file in gct_files
        )
        return results_gct

    @deprecated(reason="use function merge_data")
    def merge_sample_metadata(self):
        """
        Function to merge the sample level metadata from all the gct files in a cohort.
        Returns:
            | A pandas dataframe containing the merged metadata for analysis.

        :meta private:
        """
        if self._cohort_details is None:
            raise InvalidCohortOperationException
        file_path = self.folder_path
        sample_list = list(self._cohort_details["entity_id"].keys())
        if len(sample_list) == 0:
            raise EmptyCohortException
        results_gct = self._read_gcts(sample_list, file_path)
        for i in range(0, len(results_gct)):
            df = results_gct[i].col_metadata_df
            index_l = len(df.index)
            new_dataset = [sample_list[i]] * index_l
            results_gct[i].col_metadata_df.insert(
                loc=0, column="dataset_id", value=new_dataset
            )
        All_Metadata = pd.concat([i.col_metadata_df for i in results_gct])
        return All_Metadata

    @deprecated(reason="use function merge_data")
    def merge_data_matrix(self) -> pd.DataFrame:
        """
        Function to merge the data-matrix level metadata from all the gct files in a cohort.
        Returns:
            | A pandas dataframe containing the merged data for analysis.

        :meta private:
        """
        if self._cohort_details is None:
            raise InvalidCohortOperationException
        file_path = self.folder_path
        sample_list = list(self._cohort_details["entity_id"].keys())
        if len(sample_list) == 0:
            raise EmptyCohortException
        results_gct = self._read_gcts(sample_list, file_path)
        All_data_matrix = assemble_data(
            [i.data_df for i in results_gct], concat_direction="horiz"
        )
        return All_data_matrix

    @deprecated(reason="use function merge_data")
    def merge_dataset_metadata(self) -> pd.DataFrame:
        """
        Function to merge the dataset level metadata from all the jpco files in a cohort.
        Returns:
            | A pandas dataframe containing the merged data for analysis.

        :meta private:
        """
        if self._cohort_details is None:
            raise InvalidCohortOperationException
        file_path = self.folder_path
        entity_list = list(self._cohort_details["entity_id"].keys())
        if len(entity_list) == 0:
            raise EmptyCohortException
        jpco_files = [
            f"{file_path}/{self._cohort_details.get('entity_id',{}).get(entity_id)[0]}_{entity_id}.jpco"
            for entity_id in entity_list
        ]
        df_dict = []
        for files in jpco_files:
            with open(files, "r") as infile:
                temp_df = json.load(infile)
                df_dict.append(temp_df["_source"])
        df = pd.json_normalize(df_dict)
        first_column = df.pop("dataset_id")
        df.insert(loc=0, column="dataset_id", value=first_column)
        for col in OBSOLETE_METADATA_FIELDS:
            if col in df.columns:
                del df[col]
        return df

    @deprecated(reason="use function merge_data")
    def merge_feature_metadata(self) -> pd.DataFrame:
        """
        Function to merge the feature level metadata from all the gct files in a cohort.
        Returns:
            | A pandas dataframe containing the merged data for analysis.

        :meta private:
        """
        if self._cohort_details is None:
            raise InvalidCohortOperationException
        file_path = self.folder_path
        sample_list = list(self._cohort_details["entity_id"].keys())
        if len(sample_list) == 0:
            raise EmptyCohortException
        results_gct = self._read_gcts(sample_list, file_path)
        for i in range(0, len(results_gct)):
            df = results_gct[i].row_metadata_df
            index_l = len(df.index)
            new_dataset = [sample_list[i]] * index_l
            results_gct[i].row_metadata_df.insert(
                loc=0, column="dataset_id", value=new_dataset
            )
        All_Metadata = pd.concat([i.row_metadata_df for i in results_gct])
        return All_Metadata

    def merge_data(self, data_level: str):
        """
        Function to merge metadata (dataset, sample and feature level metadata) or data-matrix of all the samples\
or datasets in the cohort.

        Args:
            | data_level(str): identifier to specify the data to be merged - "dataset", "sample", "feature" or \
"data_matrix"
        Returns:
            | A pandas dataframe containing the merged data which is ready for analysis
        """
        if self._cohort_details is None:
            raise InvalidCohortOperationException
        if not (data_level and isinstance(data_level, str)):
            raise InvalidParameterException("data_level")
        if data_level == "sample":
            sample_df = self.merge_sample_metadata()
            return sample_df
        if data_level == "dataset":
            dataset_df = self.merge_dataset_metadata()
            return dataset_df
        if data_level == "data_matrix":
            datamatrix_df = self.merge_data_matrix()
            return datamatrix_df
        if data_level == "feature":
            feature_df = self.merge_feature_metadata()
            return feature_df
        raise InvalidCohortMergeOperation

    def edit_cohort(self, new_cohort_name=None, new_description=None):
        """
        This function is used to edit the cohort level metadata such as cohort name and description.

        ``Args:``
            |  ``new_cohort_name(str):`` Optional Argument: new identifier name for the cohort.
            |  ``new_description(str):`` Optional Argument: new description about the cohort.

        ``Returns:``
            |  A confirmation message on updation of cohort.

        ``Errors:``
            |  ``InvalidCohortOperationException:`` This operation is not valid as no cohort has been \
instantiated.
            |  ``CohortEditException:`` No parameter specified for editing in cohort

        |  Example-
        .. code::


                cohort.edit_cohort("edited-cohort-name","edited-cohort-description")

        """
        if self._cohort_details is None:
            raise InvalidCohortOperationException
        if new_cohort_name is None and new_description is None:
            raise CohortEditException
        if new_cohort_name:
            self._edit_cohort_name(new_cohort_name)
        if new_description:
            self._edit_cohort_description(new_description)

    def _edit_cohort_name(self, new_cohort_name: str):
        if not (new_cohort_name and isinstance(new_cohort_name, str)):
            return
        if dot in new_cohort_name:
            logging.error("The cohort name is not valid. Please try again.")
            return
        p = Path(self.folder_path)
        parent = p.parent
        str_parent = str(parent.resolve())
        new_path = helpers.make_path(str_parent, f"{new_cohort_name}.pco")
        existing_path = self.folder_path
        os.rename(existing_path, new_path)
        self.folder_path = new_path
        logging.basicConfig(level=logging.INFO)
        logging.info("Cohort Name Updated!")

    def _edit_cohort_description(self, new_description: str):
        if not (new_description and isinstance(new_description, str)):
            return
        existing_path = self.folder_path
        meta_path = helpers.make_path(existing_path, "cohort.meta")
        with open(meta_path, "r+b") as openfile:
            byte = openfile.read()
            data = base64.b64decode((byte))
            json_data = json.loads(data.decode("utf-8"))
            json_data["description"] = new_description
            self._cohort_details = json_data
            input = json.dumps(json_data)
            encoded_data = base64.b64encode(input.encode("utf-8"))
            openfile.seek(0)
            openfile.write(encoded_data)
            openfile.truncate()
        logging.basicConfig(level=logging.INFO)
        logging.info("Cohort Description Updated!")

    def is_valid(self) -> bool:
        """
        This function is used to check the validity of a cohort.

        ``Returns:``
            |  A boolean result based on the validity of the cohort.

        ``Errors:``
            |  ``InvalidPathException:`` Cohort path does not represent a file or a directory.
            |  ``InvalidCohortOperationException:`` This operation is not valid as no cohort has been \
instantiated.

        .. code::


                cohort.is_valid()
        """
        if self._cohort_details is None:
            raise InvalidCohortOperationException
        if not os.path.exists(self.folder_path):
            raise InvalidPathException
        meta_path = helpers.make_path(self.folder_path, "cohort.meta")
        if not os.path.exists(meta_path):
            return False
        sample_list = list(self._cohort_details["entity_id"].keys())
        if len(sample_list) == 0:
            return True
        for sample in sample_list:
            omixatlas = self._cohort_details.get("entity_id", {}).get(sample)[0]
            gct_path = f"{self.folder_path}/{omixatlas}_{sample}.gct"
            jpco_path = f"{self.folder_path}/{omixatlas}_{sample}.jpco"
            if not (os.path.exists(gct_path) and os.path.exists(jpco_path)):
                return False
        return True

    def delete_cohort(self) -> None:
        """
        This function is used to delete a cohort.

        Returns:
            | A confirmation message on deletion of cohort
        """
        shutil.rmtree(self.folder_path, ignore_errors=True)
        logging.basicConfig(level=logging.INFO)
        logging.info("Cohort Deleted Successfuly!")
        self.folder_path = None
        self._cohort_details = None

    def remove_from_cohort(self, entity_id: list) -> None:
        """
        This function is used for removing datasets or samples from a cohort.

        ``Args:``
            |  ``entity_id(list):`` list of dataset IDs or sample IDs which is to be removed from the cohort.

        ``Returns:``
            |  A confirmation message on removal of datasets or samples from cohort.

        ``Errors:``
            |  ``InvalidParameterException:`` Empty or Invalid Parameters
            |  ``InvalidCohortOperationException:`` This operation is not valid as no cohort has been \
instantiated.

        |  Example-
        .. code::


                cohort.remove_from_cohort(list_of_datasets)

        """
        if self._cohort_details is None:
            raise InvalidCohortOperationException
        if not (entity_id and isinstance(entity_id, list)):
            raise InvalidParameterException("entity_id")
        dataset_count = 0
        verified_dataset = []
        file_meta = helpers.make_path(self.folder_path, "cohort.meta")
        entity_id = list(set(entity_id))
        with open(file_meta, "r+b") as openfile:
            byte = openfile.read()
            data = base64.b64decode((byte))
            json_data = json.loads(data.decode("utf-8"))
            dataset_id = list(json_data["entity_id"].keys())
            for dataset in entity_id:
                if dataset not in dataset_id:
                    logging.basicConfig(level=logging.INFO)
                    logging.info(f"Dataset Id - {dataset} not present in the Cohort.")
                    continue
                dataset_count += 1
                verified_dataset.append(dataset)
                omixatlas = json_data.get("entity_id", {}).get(dataset)[0]
                gct_path = f"{self.folder_path}/{omixatlas}_{dataset}.gct"
                json_path = f"{self.folder_path}/{omixatlas}_{dataset}.jpco"
                os.remove(gct_path)
                os.remove(json_path)
                del json_data.get("entity_id")[dataset]
                json_data.get("source_omixatlas").get(omixatlas).remove(dataset)
            omixatlas_dict = json_data.get("source_omixatlas")
            empty_keys = []
            for key, value in omixatlas_dict.items():
                if value == []:
                    empty_keys.append(key)
            for key in empty_keys:
                del omixatlas_dict[key]
            json_data["number_of_samples"] -= dataset_count
            json_data["source_omixatlas"] = omixatlas_dict
            if not bool(json_data.get("entity_id")):
                if "entity_type" in json_data:
                    del json_data["entity_type"]
            self._cohort_details = json_data
            input = json.dumps(json_data)
            encoded_data = base64.b64encode(input.encode("utf-8"))
            openfile.seek(0)
            openfile.write(encoded_data)
            openfile.truncate()
        logging.basicConfig(level=logging.INFO)
        logging.info(f"'{dataset_count}' dataset/s removed from Cohort!")

    def add_to_cohort(self, repo_key: str, entity_id: list) -> None:
        """
        This function is used to add datasets or samples to a cohort.

        ``Args:``
            |  ``repo_key(str):`` repo_key(repo_name OR repo_id) for the omixatlas where datasets or samples belong.
            |  ``entity_id(list):`` list of dataset ID or sample ID to be added to the cohort.

        ``Returns:``
            |  A confirmation message for number of datasets or samples which are added to the cohort.

        ``Errors:``
            |  ``InvalidParameterException:`` Empty or Invalid Parameters.
            |  ``InvalidCohortOperationException:`` This operation is not valid as no cohort has been \
instantiated.

        | After creating cohort we can add datasets or samples to cohort.
        | Example-
        .. code::


                cohort.add_to_cohort("repo_id",list_of_dataset_ids)

        """
        if self._cohort_details is None:
            raise InvalidCohortOperationException
        if not (repo_key and isinstance(repo_key, str)):
            raise InvalidParameterException("repo_key")
        if not (entity_id and isinstance(entity_id, list)):
            raise InvalidParameterException("entity_id")
        obj = OmixAtlas()
        local_path = self.folder_path
        response_omixatlas = obj.omixatlas_summary(repo_key)
        data = response_omixatlas.get("data")
        repo_name = data.get("repo_name")
        dataset_id = self._validate_repo(repo_name, entity_id)
        entity_type = self._get_entity(repo_name)
        status_gct = Parallel(n_jobs=len(dataset_id), require="sharedmem")(
            delayed(self._gctfile)(repo_name, i, local_path) for i in dataset_id
        )
        status_jpco = Parallel(n_jobs=len(dataset_id), require="sharedmem")(
            delayed(self._add_metadata)(repo_name, i, local_path) for i in dataset_id
        )
        dataset_id, deleted_id = self._rollback_files(
            status_gct, status_jpco, repo_name, local_path, dataset_id
        )
        file_meta = helpers.make_path(local_path, "cohort.meta")
        with open(file_meta, "r+b") as openfile:
            byte = openfile.read()
            data = base64.b64decode((byte))
            json_data = json.loads(data.decode("utf-8"))
            source_omixatlas = json_data.get("source_omixatlas")
            if "entity_type" not in json_data:
                json_data["entity_type"] = entity_type
            if repo_name not in source_omixatlas:
                source_omixatlas[repo_name] = dataset_id
            else:
                [source_omixatlas[repo_name].append(i) for i in dataset_id]
            for i in dataset_id:
                metadata = self._get_metadata(repo_name, i)
                dataset_tuple = [
                    repo_name,
                    metadata.get("_source", {}).get("data_type"),
                ]
                json_data["entity_id"][i] = dataset_tuple
                json_data["number_of_samples"] += 1
            self._cohort_details = json_data
            input = json.dumps(json_data)
            encoded_data = base64.b64encode(input.encode("utf-8"))
            openfile.seek(0)
            openfile.write(encoded_data)
            openfile.truncate()
        logging.basicConfig(level=logging.INFO)
        if deleted_id:
            logging.info("The following entities were not added : ")
            for id in deleted_id:
                print(f"{id}\n")
        logging.info(f"'{len(dataset_id)}' dataset/s added to Cohort!")

    def _add_metadata(self, repo_key: str, dataset_id: str, local_path: str) -> None:
        """
        Function to add dataset level metadata to a cohort.
        Returns 0 on successful download, dataset_id on failure.
        """
        if not (repo_key and isinstance(repo_key, str)):
            raise InvalidParameterException("repo_id/repo_name")
        if not (dataset_id and isinstance(dataset_id, str)):
            raise InvalidParameterException("dataset_id")
        try:
            metadata = self._get_metadata(repo_key, dataset_id)
            file_name = f"{repo_key}_{dataset_id}.jpco"
            file_name = helpers.make_path(local_path, file_name)
            with open(file_name, "w") as outfile:
                json.dump(metadata, outfile)
            return 0
        except Exception:
            return dataset_id

    def _gctfile(self, repo_info: str, dataset_id: str, file_path: str) -> None:
        """
        Function to add gct file to a cohort
        Returns 0 on successful download, dtaset_id on failure.
        """
        try:
            if not (repo_info and isinstance(repo_info, str)):
                raise InvalidParameterException("repo_name/repo_id")
            if not (dataset_id and isinstance(dataset_id, str)):
                raise InvalidParameterException("dataset_id")
            ssl._create_default_https_context = ssl._create_unverified_context
            obj = OmixAtlas()
            download_dict = obj.download_data(repo_info, dataset_id)
            url = (
                download_dict.get("data", {}).get("attributes", {}).get("download_url")
            )
            file_name = f"{repo_info}_{dataset_id}.gct"
            dest_path = helpers.make_path(file_path, file_name)
            r = requests.get(url)
            with open(dest_path, "w") as fd:
                fd.write(r.text)
            return 0
        except Exception:
            return dataset_id

    def _rollback_files(
        self,
        status_gct: list,
        status_jpco: list,
        repo_name: str,
        local_path: str,
        dataset_id: list,
    ) -> tuple:
        """
        Returns a list of dataset_ids and deleted_ids
        """
        deleted_id = []
        for i in status_gct:
            if i != 0:
                gct_file = f"{repo_name}_{i}.gct"
                gct_path = helpers.make_path(local_path, gct_file)
                jpco_file = f"{repo_name}_{i}.jpco"
                jpco_path = helpers.make_path(local_path, jpco_file)
                if os.path.exists(gct_path):
                    os.remove(gct_path)
                if os.path.exists(jpco_path):
                    os.remove(jpco_path)
                deleted_id.append(i)
                dataset_id.remove(i)
        for i in status_jpco:
            if i != 0 and i not in deleted_id:
                gct_file = f"{repo_name}_{i}.gct"
                gct_path = helpers.make_path(local_path, gct_file)
                jpco_file = f"{repo_name}_{i}.jpco"
                jpco_path = helpers.make_path(local_path, jpco_file)
                if os.path.exists(gct_path):
                    os.remove(gct_path)
                if os.path.exists(jpco_path):
                    os.remove(jpco_path)
                deleted_id.append(i)
                dataset_id.remove(i)
        return dataset_id, deleted_id

    def create_cohort(
        self,
        local_path: str,
        cohort_name: str,
        description: str,
        repo_key=None,
        entity_id=None,
    ) -> None:
        """
        This function is used to create a cohort.

        ``Args:``
            |  ``local_path(str):`` local path to instantiate the cohort.
            |  ``cohort_name(str):`` identifier name for the cohort.
            |  ``description(str):`` description about the cohort.
            |  ``repo_key(str):`` Optional argument: repo_key(repo_name/repo_id) for the omixatlas from where \
datasets or samples is to be added.
            |  ``entity_id(list):`` Optional argument: list of dataset_id or sample_id to be added to the \
cohort.

        ``Returns:``
            |  A confirmation message on creation of cohort.

        ``Errors:``
            |  ``InvalidParameterException:`` Empty or Invalid Parameters
            |  ``InvalidCohortNameException:`` The cohort_name does not represent a valid cohort name.
            |  ``InvalidPathException:`` Provided path does not represent a file or a directory.

        | After making Cohort Object you can create cohort.
        | Example-
        | 1. while passing argument of repo and dataset.

        .. code::


                cohort.create_cohort("/import/tcga_cohort","cohort_name","cohort_description",\
"repo_id",list_of_datasets)

        | 2. without passing argument of repo and dataset.

        .. code::


                cohort2.create_cohort("/path","cohort_name","cohort_description")


        """
        if not (local_path and isinstance(local_path, str)):
            raise InvalidParameterException("local_path")
        if not (cohort_name and isinstance(cohort_name, str)):
            raise InvalidParameterException("cohort_name")
        if not (description and isinstance(description, str)):
            raise InvalidParameterException("description")
        if not os.path.exists(local_path):
            raise InvalidPathException
        if dot in cohort_name:
            raise InvalidCohortNameException(cohort_name)
        file_path = os.path.join(local_path, f"{cohort_name}.pco")
        user_id = self._get_user_id()
        os.makedirs(file_path)
        metadata = {
            "number_of_samples": 0,
            "entity_id": {},
            "source_omixatlas": {},
            "description": description,
            "user_id": user_id,
            "date_created": str(datetime.datetime.now()),
            "version": "0.1",
        }
        file_name = os.path.join(file_path, "cohort.meta")
        input = json.dumps(metadata)
        with open(file_name, "wb") as outfile:
            encoded_data = base64.b64encode(input.encode("utf-8"))
            outfile.write(encoded_data)
        self.folder_path = str(file_path)
        self._cohort_details = metadata
        if entity_id is not None and repo_key is not None:
            self.add_to_cohort(repo_key, entity_id)
        logging.basicConfig(level=logging.INFO)
        logging.info("Cohort Created !")

    def _get_user_id(self):
        """
        Function to get user id
        """
        me_url = f"{self.base_url}/users/me"
        details = self.session.get(me_url)
        error_handler(details)
        user_id = details.json().get("data", {}).get("attributes", {}).get("user_id")
        return user_id

    def summarize_cohort(self):
        """
        Function to return cohort level metadata and dataframe with datasets or samples added in the cohort.

        ``Returns:``
            |  A tuple with the first value as cohort metadata information (name, description and number of \
dataset(s) or sample(s) in the cohort) and the second value as dataframe containing the source, \
dataset_id or sample_id and data type available in the cohort.

        ``Errors:``
            |  ``InvalidCohortOperationException:`` This operation is not valid as no cohort has been \
instantiated.

        | Example-

        .. code::


                metadata, cohort_details = cohort.summarize_cohort()
        | metadata will contain a object like this.

        .. code::


                {
                'cohort_name': 'cohort_name',
                'number_of_samples': 6,
                'description': 'cohort_description'
                }
        | cohort detail will contain a table like that
        .. csv-table::
            :header: "", "source_omixatlas",  "datatype", "dataset_id"
            :delim: |

            0 |	tcga |	Mutation |	BRCA_Mutation_TCGA-A8-A09Q-01A-11W-A019-09
            1 |	tcga |	Mutation |	BRCA_Mutation_TCGA-AN-A0FL-01A-11W-A050-09
            2 |	tcga |	Mutation |	BRCA_Mutation_TCGA-AR-A254-01A-21D-A167-09
            3 |	tcga |	Mutation |	BRCA_Mutation_TCGA-D8-A1XO-01A-11D-A14K-09
            4 |	tcga |	Mutation |	BRCA_Mutation_TCGA-EW-A1J2-01A-21D-A13L-09
            5 |	tcga |	Mutation |	BRCA_Mutation_TCGA-LL-A50Y-01A-11D-A25Q-09
        """
        if self._cohort_details is None:
            raise InvalidCohortOperationException
        meta_details = self._get_metadetails()
        df_details = self._get_df()
        return meta_details, df_details

    def load_cohort(self, local_path: str):
        """
        Function to load an existing cohort into an object. Once loaded, the functions described in the \
documentation can be used for the object where the cohort is loaded.

        ``Args:``
            |  ``local_path(str):`` local path of the cohort.

        ``Returns:``
            |  A confirmation message on instantiation of the cohort.

        ``Errors:``
            |  ``InvalidPathException:`` This path does not represent a file or a directory.
            |  ``InvalidCohortPathException:`` This path does not represent a Cohort.

        |  Example-
        .. code::


                cohort.load_cohort("/path/cohort_name.pco")

        """
        if not os.path.exists(local_path):
            raise InvalidPathException(local_path)
        file_meta = helpers.make_path(local_path, "cohort.meta")
        if not os.path.exists(file_meta):
            raise InvalidCohortPathException
        file = open(file_meta, "r")
        byte = file.read()
        file.close()
        data = base64.b64decode((byte))
        str_data = data.decode("utf-8")
        json_data = json.loads(str_data)
        self._cohort_details = json_data
        self.folder_path = local_path
        logging.basicConfig(level=logging.INFO)
        logging.info("Cohort Loaded !")

    def _get_metadetails(self) -> dict:
        """
        Function to return metadata details of a cohort
        """
        data = self._cohort_details
        meta_dict = {}
        folder_name = os.path.basename(self.folder_path)
        cohort_name = folder_name.split(".")[0]
        meta_dict["cohort_name"] = cohort_name
        meta_details = ["description", "number_of_samples"]
        for key, value in data.items():
            if key.lower() in meta_details:
                meta_dict[key] = value
        return meta_dict

    def _get_df(self) -> pd.DataFrame:
        """
        Function to return cohort summary in a dataframe
        """
        data = self._cohort_details
        df_dict = {"source_omixatlas": [], "datatype": [], "entity_id": []}
        dataset_list = list(data["entity_id"].keys())
        for entity in dataset_list:
            omixatlas = data.get("entity_id", {}).get(entity, {})[0]
            data_type = data.get("entity_id", {}).get(entity, {})[1]
            df_dict["entity_id"].append(entity)
            df_dict["source_omixatlas"].append(omixatlas)
            df_dict["datatype"].append(data_type)
        if len(dataset_list) > 0:
            entity = data["entity_type"]
            if entity == "dataset":
                df_dict["dataset_id"] = df_dict.pop("entity_id")
            else:
                df_dict["sample_id"] = df_dict.pop("entity_id")
        dataframe = pd.DataFrame.from_dict(df_dict)
        return dataframe

    def _get_metadata(self, repo_key: str, dataset_id: str) -> dict:
        """
        Function to return metadata for a dataset
        """
        obj = OmixAtlas()
        response_omixatlas = obj.omixatlas_summary(repo_key)
        data = response_omixatlas.get("data")
        index_name = data.get("indexes", {}).get("files")
        if index_name is None:
            raise paramException(
                title="Param Error", detail="Repo entered is not an omixatlas."
            )
        elastic_url = f"{obj.elastic_url}/{index_name}/_search"
        query = helpers.elastic_query(index_name, dataset_id)
        metadata = helpers.get_metadata(obj, elastic_url, query)
        return metadata

    def _validate_repo(self, repo_name: str, dataset_id: list) -> list:
        """
        Function to validate repo and datasets given as argument for adding to cohort
        """
        dataset_list = list(self._cohort_details["entity_id"].keys())
        if repo_name not in self._cohort_info:
            valid_repos = list(self._cohort_info.keys())
            raise InvalidRepoException(valid_repos)
        valid_dataset_id = []
        dataset_id = list(set(dataset_id))
        for dataset in dataset_id:
            if dataset in dataset_list:
                logging.basicConfig(level=logging.INFO)
                logging.info(
                    f"The entity_id - {dataset} is already existing in the cohort."
                )
                continue
            valid_dataset_id.append(dataset)
        if len(valid_dataset_id) == 0:
            raise InvalidDatasetException
        return valid_dataset_id

    def _get_entity(self, repo_name: str) -> str:
        """
        Function to get the entity type of repo
        """
        for repo, dict in self._cohort_info.items():
            if repo_name == repo:
                if dict["file_structure"] == "single":
                    entity_type = "dataset"
                else:
                    entity_type = "sample"
        return entity_type
