import os 
import sys

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from carprice.exception import CarPriceException
from carprice.logger import logging
from carprice.entity.config_entity import DataIngestionConfig
from carprice.entity.artifact_entity import DataIngestionArtifact
from carprice.data_access.car_data import CarData
from carprice.utils.main_utils import read_yaml_file
from carprice.constant import SCHEMA_FILE_PATH


class DataIngestion:    
    def __init__(self, data_ingestion_config: DataIngestionConfig=DataIngestionConfig()):
        """
        :param data_ingestion_config: configuration for data ingestion
        """
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CarPriceException(e, sys) from e
        
    """    
    def get_data_from_gcloud(self) -> pd.DataFrame:
        try:
            logging.info("Entered the get_data_from_gcloud method of Data ingestion class")
            os.makedirs(self.data_ingestion_config.data_ingestion_dir, exist_ok=True)
            
            self.gcloud.sync_folder_from_gcloud(self.data_ingestion_config.bucket_name,
                                                self.data_ingestion_config.file_name,
                                                self.data_ingestion_config.data_ingestion_dir,
                                                )
            
            logging.info("Exited the get_data_from_gcloud method of Data ingestion class")
            

            
        except Exception as e:
            raise CarPriceException(e, sys) from e
            
    """
        

    def export_data_into_feature_store(self) -> DataFrame:
        """
        Method Name :   export_data_into_feature_store
        Description :   This method exports data from mongodb to csv file
        
        Output      :   data is returned as artifact of data ingestion components
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            logging.info(f"Exporting data from mongodb")
            car_db = CarData()
            dataframe = car_db.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)
            logging.info(f"Shape of dataframe: {dataframe.shape}")
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"Saving exported data into feature store file path: {feature_store_file_path}")
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            
            return dataframe
        except Exception as e:
            raise CarPriceException(e, sys) from e
    
        
       
    def split_data_as_train_test(self, dataframe: DataFrame) -> None:
        """
        Method Name :   split_data_as_train_test
        Description :   This method splits the dataframe into train set and test set based on split ratio 
        
        Output      :   Folder is created in s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        """
        logging.info("Entered split_data_as_train_test method of Data_Ingestion class")
        
        try:
            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed train test split on the dataframe")
            logging.info(
                "Exited split_data_as_train_test method of Data_Ingestion class"
            )
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            
            logging.info(f"Exporting train and test file path.")
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
            
            logging.info(f"Exported train and test file path.")
        except Exception as e:
            raise CarPriceException(e, sys) from e
        
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Method Name :   initiate_data_ingestion
        Description :   This method initiates the data ingestion components of training pipeline 
        
        Output      :   train set and test set are returned as the artifacts of data ingestion components
        On Failure  :   Write an exception log and then raise an exception
        """
        logging.info("Entered initiate_data_ingestion method of Data_Ingestion class")
        
        try:
            
            dataframe = self.export_data_into_feature_store()
            
            _schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
            
            dataframe = dataframe.drop(_schema_config["drop_columns"], axis=1)
            
            logging.info("Got the data from gcloud")
            
            self.split_data_as_train_test(dataframe)
            
            logging.info("Performed train test split on the dataset")

            logging.info(
                "Exited initiate_data_ingestion method of Data_Ingestion class"
            )
            
            data_ingestion_artifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                            test_file_path=self.data_ingestion_config.testing_file_path)
            
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise CarPriceException(e, sys) from e
        