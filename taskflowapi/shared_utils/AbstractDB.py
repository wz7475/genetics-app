from abc import ABC, abstractmethod


class AbstractDB(ABC):
    @abstractmethod
    async def get_data(self, key) -> None:
        pass

    @abstractmethod
    async def input_data(self, key, value) -> None:
        """
        input data into database
        :param value: value for db
        :param key: redis key
        """
        pass

    @abstractmethod
    async def save_annotation_from_file_to_db(self, filepath: str, alg_name) -> None:
        """
        stores annotation from file to db
        :param filepath: path to file that is adnotated to be calculated
        :param alg_name: name of algorithm added to key and to name of column with annotation
        """
        pass

    @abstractmethod
    def get_filtered_input_file_for_alg(self, task_id: str, algorythm: str) -> str:
        """

        :param task_id: id of task
        :param algorythm: name of algorithm eg. pangolin
        :return:
        """