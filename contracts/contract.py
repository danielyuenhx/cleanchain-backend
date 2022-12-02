from pyteal import *
from pyteal.ast.bytes import Bytes
from pyteal_helpers import program

def approval():
    global_cleaned_count = Bytes("Cleaned") #uint64
    global_cleaning_count = Bytes("Cleaning") # uint64

    local_donation = Bytes("Donation") #uint64

    return program.event(
        init = Seq(
            App.globalPut(global_cleaned_count, Int(0)),
            App.globalPut(global_cleaning_count, Int(0)),
            Approve()
        ),
        opt_in = Seq(
            App.localPut(Txn.sender(), local_donation, Int(0)),
            Approve()
        ),
        no_op = Seq(

        )
    )
    

def clear():
    return Approve()

