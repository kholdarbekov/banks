import pytest
from datetime import datetime
from banks import Parser1, Parser2, Parser3

def test_parsers():
    parser = Parser1()
    parser.set_line("Oct 1 2019,remove,99.10,182,198")
    assert parser.get_transaction_time() == datetime(2019, 10, 1).strftime(parser.transaction_time_to_format)
    assert parser.get_transaction_type() == "remove"
    assert parser.get_transaction_amount() == "99.10"
    assert parser.get_transaction_to() == "182"
    assert parser.get_transaction_from() == "198"
    # invalid row (missing from field)
    parser.set_line("Oct 1 2019,remove,99.10,182")
    with pytest.raises(IndexError):
        parser.get_transaction_from()
    

    parser = Parser2()
    parser.set_line("03-10-2019,remove,99.99,182,198")
    assert parser.get_transaction_time() == datetime(2019, 10, 3).strftime(parser.transaction_time_to_format)
    assert parser.get_transaction_type() == "remove"
    assert parser.get_transaction_amount() == "99.99"
    assert parser.get_transaction_to() == "182"
    assert parser.get_transaction_from() == "198"
    # invalid row (missing from field)
    parser.set_line("03-10-2019,remove,99.99,182")
    with pytest.raises(IndexError):
        parser.get_transaction_from()


    parser = Parser3()
    parser.set_line("5 Oct 2019,add,5,44,182,198")
    assert parser.get_transaction_time() == datetime(2019, 10, 5).strftime(parser.transaction_time_to_format)
    assert parser.get_transaction_type() == "add"
    assert parser.get_transaction_amount() == "5.44"
    assert parser.get_transaction_to() == "182"
    assert parser.get_transaction_from() == "198"
    # invalid row (missing from field)
    parser.set_line("5 Oct 2019,add,5,44,182")
    with pytest.raises(IndexError):
        parser.get_transaction_from()
