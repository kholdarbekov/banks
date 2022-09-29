import os
import pytest
from io import BytesIO
from datetime import datetime
from banks import Parser1, Parser2, Parser3, main


def test_parsers():
    parser = Parser1()
    parser.set_line("Oct 1 2019,remove,99.10,182,198")
    assert parser.get_transaction_time() == datetime(2019, 10, 1).strftime(
        parser.transaction_time_to_format
    )
    assert parser.get_transaction_type() == "remove"
    assert parser.get_transaction_amount() == "99.10"
    assert parser.get_transaction_to() == "182"
    assert parser.get_transaction_from() == "198"
    # invalid row (missing from field)
    parser.set_line("Oct 1 2019,99.10,182")
    with pytest.raises(IndexError):
        parser.get_transaction_from()
    with pytest.raises(ValueError):
        parser.get_transaction_type()

    parser = Parser2()
    parser.set_line("03-10-2019,remove,99.99,182,198")
    assert parser.get_transaction_time() == datetime(2019, 10, 3).strftime(
        parser.transaction_time_to_format
    )
    assert parser.get_transaction_type() == "remove"
    assert parser.get_transaction_amount() == "99.99"
    assert parser.get_transaction_to() == "182"
    assert parser.get_transaction_from() == "198"
    # invalid row (missing from field)
    parser.set_line("03-10-2019,99.99,182,198")
    with pytest.raises(IndexError):
        parser.get_transaction_from()

    parser = Parser3()
    parser.set_line("5 Oct 2019,add,5,44,182,198")
    assert parser.get_transaction_time() == datetime(2019, 10, 5).strftime(
        parser.transaction_time_to_format
    )
    assert parser.get_transaction_type() == "add"
    assert parser.get_transaction_amount() == "5.44"
    assert parser.get_transaction_to() == "182"
    assert parser.get_transaction_from() == "198"
    # invalid row (missing from field)
    parser.set_line("5 Oct 2019,add,5,44,182")
    with pytest.raises(IndexError):
        parser.get_transaction_from()


def test_e2e():
    TEST_CSV_1 = """timestamp,type,amount,to,from
Oct 1 2019,remove,99.10,182,198
"""
    TEST_CSV_2 = """date,transaction,amounts,to,from
03-10-2019,remove,99.99,182,198
"""

    with open("test_csv_1.csv", "w") as test_file:
        test_file.write(TEST_CSV_1)
    
    with open("test_csv_2.csv", "w") as test_file:
        test_file.write(TEST_CSV_2)
    
    os.environ["CSV_FILES_AND_PARSERS"] = '{"test_csv_1.csv":"Parser1","test_csv_2.csv":"Parser2"}'

    main()

    with open("combined.csv") as file:
        # TRANSACTION_TIME_TO_FORMAT=%d.%m.%Y
        assert file.readline() == "transaction_time,transaction_type,transaction_amount,transaction_to,transaction_from\n"
        assert file.readline() == "01.10.2019,remove,99.10,182,198\n"
        assert file.readline() == "03.10.2019,remove,99.99,182,198\n"

    os.remove("test_csv_1.csv")
    os.remove("test_csv_2.csv")
    os.remove("combined.csv")
