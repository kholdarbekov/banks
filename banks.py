import os
import json
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, List, Type, Optional
from dotenv import load_dotenv


class AbstractParser(ABC):
    def __init__(self) -> None:
        self.current_filename = ""
        self.elements: List[str] = []
        self.transaction_time_from_format = ""
        self.transaction_time_to_format = os.getenv(
            "TRANSACTION_TIME_TO_FORMAT", "%d.%m.%Y"
        )

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


class ParserValidator(AbstractParser):
    # No need for extra validation for time format
    # because datetime will raise ValueError
    # if given string does not fit the format

    # validation for type, currently assumes that only 2 types are valid
    def validate_transaction_type(self, value: str):
        if value not in ("add", "remove"):
            raise ValueError(
                f"{self.current_filename} Line {','.join(self.elements)}: Transaction type can be either add or remove"
            )

    # this will be used for amount, to, and from fields
    def validate_numeric(self, column_name: str, value: str):
        try:
            float(value)
        except ValueError:
            print(
                f"{self.current_filename} Line {','.join(self.elements)}: {column_name} must be numeric"
            )
            raise


class Parser1(ParserValidator, AbstractParser):
    def __init__(self) -> None:
        super().__init__()
        # Oct 1 2019
        self.transaction_time_from_format = "%b %d %Y"

    def get_transaction_time(self) -> str:
        return datetime.strptime(
            self.get_element(0), self.transaction_time_from_format
        ).strftime(self.transaction_time_to_format)

    def get_transaction_type(self) -> str:
        value = self.get_element(1)
        self.validate_transaction_type(value)
        return value

    def get_transaction_amount(self) -> str:
        value = self.get_element(2)
        self.validate_numeric(column_name="Transction amount", value=value)
        return value

    def get_transaction_to(self) -> str:
        value = self.get_element(3)
        self.validate_numeric(column_name="Transction to", value=value)
        return value

    def get_transaction_from(self) -> str:
        value = self.get_element(4)
        self.validate_numeric(column_name="Transction from", value=value)
        return value


class Parser2(ParserValidator, AbstractParser):
    def __init__(self) -> None:
        super().__init__()
        # 03-10-2019
        self.transaction_time_from_format = "%d-%m-%Y"

    def get_transaction_time(self) -> str:
        return datetime.strptime(
            self.get_element(0), self.transaction_time_from_format
        ).strftime(self.transaction_time_to_format)

    def get_transaction_type(self) -> str:
        value = self.get_element(1)
        self.validate_transaction_type(value)
        return value

    def get_transaction_amount(self) -> str:
        value = self.get_element(2)
        self.validate_numeric(column_name="Transction amount", value=value)
        return value

    def get_transaction_to(self) -> str:
        value = self.get_element(3)
        self.validate_numeric(column_name="Transction to", value=value)
        return value

    def get_transaction_from(self) -> str:
        value = self.get_element(4)
        self.validate_numeric(column_name="Transction from", value=value)
        return value


class Parser3(ParserValidator, AbstractParser):
    def __init__(self) -> None:
        super().__init__()
        # 5 Oct 2019
        self.transaction_time_from_format = "%d %b %Y"

    def get_transaction_time(self) -> str:
        return datetime.strptime(
            self.get_element(0), self.transaction_time_from_format
        ).strftime(self.transaction_time_to_format)

    def get_transaction_type(self) -> str:
        value = self.get_element(1)
        self.validate_transaction_type(value)
        return value

    def get_transaction_amount(self) -> str:
        # euro and cents
        value = f"{self.get_element(2)}.{self.get_element(3)}"
        self.validate_numeric(column_name="Transction amount", value=value)
        return value

    def get_transaction_to(self) -> str:
        value = self.get_element(4)
        self.validate_numeric(column_name="Transction to", value=value)
        return value

    def get_transaction_from(self) -> str:
        value = self.get_element(5)
        self.validate_numeric(column_name="Transction from", value=value)
        return value


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
        output_file_name: Optional[str] = None,
        time_header: Optional[str] = None,
        type_header: Optional[str] = None,
        amount_header: Optional[str] = None,
        to_header: Optional[str] = None,
        from_header: Optional[str] = None,
    ) -> None:
        super().__init__(cvs_to_parser_dict)
        self.output_file_name = str(
            output_file_name or os.getenv("CSV_OUTPUT_FILE_NAME", "combined.csv")
        )

        self.time_header = time_header or os.getenv(
            "CSV_TIME_HEADER", "transaction_time"
        )
        self.type_header = type_header or os.getenv(
            "CVS_TYPE_HEADER", "transaction_type"
        )
        self.amount_header = amount_header or os.getenv(
            "CVS_AMOUNT_HEADER", "transaction_amount"
        )
        self.to_header = to_header or os.getenv("CVS_TO_HEADER", "transaction_to")
        self.from_header = from_header or os.getenv(
            "CVS_FROM_HEADER", "transaction_from"
        )

    def consolidate(self) -> None:
        with open(self.output_file_name, "w") as output_file:
            # define headers
            output_file.write(
                f"{self.time_header},{self.type_header},{self.amount_header},{self.to_header},{self.from_header}\n"
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


def get_parser(name: str) -> Type[AbstractParser]:
    if name == "Parser1":
        return Parser1
    elif name == "Parser2":
        return Parser2
    elif name == "Parser3":
        return Parser3
    else:
        raise ValueError(f"Parser class with name {name} not found")


def main():
    load_dotenv()
    cvs_to_parser_dict = {}
    CSV_FILES_AND_PARSERS = json.loads(
        os.getenv(
            "CSV_FILES_AND_PARSERS",
            '{"bank1.csv":"Parser1","bank2.csv":"Parser2","bank3.csv":"Parser3"}',
        )
    )
    for cvs_file, parser in CSV_FILES_AND_PARSERS.items():
        cvs_to_parser_dict[cvs_file] = get_parser(parser)
    csv_formatter = CSVFormatter(cvs_to_parser_dict)
    csv_formatter.consolidate()


if __name__ == "__main__":
    main()
