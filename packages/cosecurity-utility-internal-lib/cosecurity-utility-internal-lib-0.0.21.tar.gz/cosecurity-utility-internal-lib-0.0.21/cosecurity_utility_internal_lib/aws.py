import os
import uuid
import boto3
import psycopg2

from typing import Any, Dict, List, Tuple

class BucketType:
    DATA='BUCKET_DATA'
    MODEL='BUCKET_MODEL'
    DATASET='BUCKET_DATASET'

class SimpleStorageService:
    """
    Util class for AWS S3 file and folder management

    Attributes:
        session (boto3.Session): session to connect to aws
        bucket (str): range name of files and folder
        resource (Any): instance connected to aws to reference aws s3
    """
    def __init__(self) -> None:
        self._session = boto3.Session(
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
        self._resource = self._session.resource('s3')

    def exists(self, path:str, bucket_name:str=BucketType.DATA) -> bool:
        """        
        Method that validates whether a file exists or not
        
        Parameters:
            path (str): remote path of the file to be published
            bucket_name (BucketType | None): remote storage name

        Returns:
            bool: return whether a file exists or not
        """
        try:
            self._resource.Object(os.getenv(bucket_name), path).load()
            return True
        except:
            return False

    def push(self, object:Any, path:str, hash:bool=False, extension:str=None, bucket_name:str=BucketType.DATA) -> str:
        """        
        Method to publish files to storage
        
        Parameters:
            object (Any): file content to be published
            path (str): remote path of the file to be published
            hash (bool | None): defines whether the new file will have a dynamic name
            extension (str | None): defines whether the new file will have a fixed extension
            bucket_name (BucketType | None): remote storage name

        Returns:
            str: returns the remote path of the published file
        """
        if hash:
            path += f'/{uuid.uuid4()}.{extension}'
        self._resource.Object(os.getenv(bucket_name), path).put(Body=object)
        return path

    def get_bytes(self, path:str, bucket_name:str=BucketType.DATA) -> Any:
        """        
        Method to get a byte string from a file
        
        Parameters:
            path (str): remote path of the file to be published
            bucket_name (BucketType | None): remote storage name

        Returns:
            any: return the bytes of the file
        """
        bucket = self._resource.Bucket(os.getenv(bucket_name))
        return bucket.Object(path).get().get('Body').read()

    def download(self, source:str, destine:str, bucket_name:str=BucketType.DATA) -> None:
        """        
        Method to download files
        
        Parameters:
            source (str): remote path of the file to be published
            destine (str): local path to save the file
            bucket_name (BucketType | None): remote storage name
        """
        bucket = self._resource.Bucket(os.getenv(bucket_name))
        bucket.download_file(source, destine)

    def download_all(self, source:str, destine:str, bucket_name:str=BucketType.DATA) -> None:
        """        
        Method to download all files
        
        Parameters:
            source (str): remote path of the file to be published
            destine (str): local path to save the file
            bucket_name (BucketType | None): remote storage name
        """
        bucket = self._resource.Bucket(os.getenv(bucket_name))

        for file_object in bucket.objects.filter(Prefix=source):
            local_path = os.path.join(destine, file_object.key)

            try:
                if not os.path.exists(os.path.dirname(local_path)):
                    os.makedirs(os.path.dirname(local_path))
                bucket.download_file(file_object.key, local_path)
            except:
                continue

class PostgresRelationalDatabaseService:
    """
    Useful class to manage the specific relational database service for postgres

    Attributes:
        connection (Any): database connection
    """
    def __init__(self) -> None:
        self._connection = psycopg2.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME")
        )

    def _convert_columns_to_tuple(self, columns:Any) -> Tuple[str, Tuple[Any]]:
        if type(columns) == dict:
            keys = list(columns.keys())
            typed_key = ['%s' for _ in range(len(keys))]
            return ', '.join(keys), list(columns.values()), ', '.join(typed_key)
        else:
            return ', '.join(columns), None, ', '.join(['%s' for _ in range(len(columns))])

    def get(self, query:str, vars:tuple) -> list:
        with self._connection.cursor() as cursor:
            cursor.execute(query, vars)
            response = cursor.fetchall()
            self._connection.commit()
            return response

    def get_column(self, table_name:str, return_column:str, condition_column:str, condition_value:Any) -> Any:
        with self._connection.cursor() as cursor:
            cursor.execute(
                query=f'SELECT {return_column} FROM {table_name} WHERE {condition_column} = %s;',
                vars=(condition_value,)
            )

            return_value = cursor.fetchone()
            self._connection.commit()
            
            if return_value is not None:
                return return_value[0]

    def update(self, table_name:str, condition_column:str, condition_value:Any, update_column:str, update_value:Any) -> None:
        """        
        Function to update record in a table in database
        
        Parameters:
            table_name (str): table name to insert
            condition_column (str): column for filtering
            condition_value (Any): value for filtering
            update_column (str): column to change
            update_value (Any): value to change
        """
        with self._connection.cursor() as cursor:
            cursor.execute(
                query=f'UPDATE {table_name} SET {update_column} = %s WHERE {condition_column} = %s;',
                vars=(update_value, condition_value)
            )
            self._connection.commit()

    def create(self, table_name:str, return_column:str='id', **columns:Dict) -> int:
        """        
        Function to create record in a table in database
        
        Parameters:
            table_name (str): table name to insert
            return_column (str | None): column name to return after inserted
            columns (**kwards): name of columns to be inserted
            
        Returns:
            int: returns the id of the current run
        """
        keys, values, typed_key = self._convert_columns_to_tuple(columns)
        return_value = None

        with self._connection.cursor() as cursor:
            cursor.execute(
                query=f'INSERT INTO {table_name} ({keys}) VALUES ({typed_key}) RETURNING {return_column};',
                vars=values
            )
            return_value = cursor.fetchone()[0]
            self._connection.commit()
        
        return return_value

    def create_many(self, table_name:str, column_name:List[str], values:List[Tuple]) -> None:
        """        
        Function to create multiple records in a table in the database
        
        Parameters:
            table_name (str): table name to insert
            column_name (List[str]): columns to be inserted
            values (List[Tuple]): list of values for columns, each row must be a tuple following the special column order
        """
        keys, _, typed_key = self._convert_columns_to_tuple(column_name)
        with self._connection.cursor() as cursor:
            cursor.executemany(
                query=f'INSERT INTO {table_name} ({keys}) VALUES ({typed_key});', 
                vars_list=values
            )
            self._connection.commit()
