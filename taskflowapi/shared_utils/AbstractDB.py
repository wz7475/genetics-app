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
    async def input_file(self, filepath: str) -> None:
        """
        gets task id and returns the filepath if file exists
        :param filepath: path to file that is to be writen into DB
        :return: filepath
        """
        pass