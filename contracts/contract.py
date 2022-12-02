from pyteal import *
from pyteal.ast.bytes import Bytes
from pyteal_helpers import program

def approval():
    return program.event(
        init = Seq(),
        opt_in = Seq(),
        no_op = Seq()
    )
    

def clear():
    return Approve()

