import os
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, List, Type


class AbstractParser(ABC):
    def __init__(self) -> None:
        self.current_filename = ""
        self.elements: List[str] = []
        self.transaction_time_from_format = ""
        self.transaction_time_to_format = os.getenv("TRANSACTION_TIME_TO_FORMAT", "%d.%m.%Y")

    def set_line(self, line: str) -> None:
        self.elements = line.split(",")

    def set_filename(self, filename: str) -> None:
        self.current_filename = filename

    @abstractmethod
    def get_transaction_time(self) -> str:
        pass

    @abstractmethod
    def get_transaction_type(self) -> str:
        pass

    @abstractmethod
    def get_transaction_amount(self) -> str:
        pass

    @abstractmethod
    def get_transaction_to(self) -> str:
        pass

    @abstractmethod
    def get_transaction_from(self) -> str:
        pass

    def get_element(self, index: int) -> str:
        try:
            return self.elements[index]
        except IndexError:
            print(
                f"{self.current_filename} Line {','.join(self.elements)} is incorrect, missing some field(s)"
            )
            raise


class Parser1(AbstractParser):
    def __init__(self) -> None:
        super().__init__()
        # Oct 1 2019
        self.transaction_time_from_format = "%b %d %Y"

    def get_transaction_time(self) -> str:
        return datetime.strptime(
            self.get_element(0), self.transaction_time_from_format
        ).strftime(self.transaction_time_to_format)

    def get_transaction_type(self) -> str:
        return self.get_element(1)

    def get_transaction_amount(self) -> str:
        return self.get_element(2)

    def get_transaction_to(self) -> str:
        return self.get_element(3)

    def get_transaction_from(self) -> str:
        return self.get_element(4)


class Parser2(AbstractParser):
    def __init__(self) -> None:
        super().__init__()
        # 03-10-2019
        self.transaction_time_from_format = "%d-%m-%Y"

    def get_transaction_time(self) -> str:
        return datetime.strptime(
            self.get_element(0), self.transaction_time_from_format
        ).strftime(self.transaction_time_to_format)

    def get_transaction_type(self) -> str:
        return self.get_element(1)

    def get_transaction_amount(self) -> str:
        return self.get_element(2)

    def get_transaction_to(self) -> str:
        return self.get_element(3)

    def get_transaction_from(self) -> str:
        return self.get_element(4)


class Parser3(AbstractParser):
    def __init__(self) -> None:
        super().__init__()
        # 5 Oct 2019
        self.transaction_time_from_format = "%d %b %Y"

    def get_transaction_time(self) -> str:
        return datetime.strptime(
            self.get_element(0), self.transaction_time_from_format
        ).strftime(self.transaction_time_to_format)

    def get_transaction_type(self) -> str:
        return self.get_element(1)

    def get_transaction_amount(self) -> str:
        # euro and cents
        return f"{self.get_element(2)}.{self.get_element(3)}"

    def get_transaction_to(self) -> str:
        return self.get_element(4)

    def get_transaction_from(self) -> str:
        return self.get_element(5)


class Formatter(ABC):
    def __init__(self, cvs_to_parser_dict: Dict[str, Type[AbstractParser]]) -> None:
        super().__init__()
        self.cvs_to_parser_dict = cvs_to_parser_dict

    @abstractmethod
    def consolidate(self) -> Any:
        pass


class CSVFormatter(Formatter):
    def __init__(
        self,
        cvs_to_parser_dict: Dict[str, Type[AbstractParser]],
        output_file_name: str = "combined.csv",
    ) -> None:
        super().__init__(cvs_to_parser_dict)
        self.output_file_name = output_file_name

    def consolidate(self) -> None:
        with open(self.output_file_name, "w") as output_file:
            # define headers
            output_file.write(
                "transaction_time,transaction_type,transaction_amount,transaction_to,transaction_from\n"
            )
            for csv_file, parser_class in self.cvs_to_parser_dict.items():
                parser: AbstractParser = parser_class()
                parser.set_filename(csv_file)
                with open(csv_file) as file:
                    next(file)  # skipp first line, headers
                    for line in file:
                        if not line or line == "\n":
                            continue
                        parser.set_line(line)
                        output_file.write(
                            "{time},{type},{amount},{to},{_from}".format(
                                time=parser.get_transaction_time(),
                                type=parser.get_transaction_type(),
                                amount=parser.get_transaction_amount(),
                                to=parser.get_transaction_to(),
                                _from=parser.get_transaction_from(),
                            )
                        )


if __name__ == "__main__":
    cvs_to_parser_dict = {
        "bank1.csv": Parser1,
        "bank2.csv": Parser2,
        "bank3.csv": Parser3,
    }
    csv_formatter = CSVFormatter(cvs_to_parser_dict)
    csv_formatter.consolidate()
