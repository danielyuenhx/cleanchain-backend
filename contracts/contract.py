from pyteal import *
from pyteal.ast.bytes import Bytes
from pyteal_helpers import program

def approval():
    global_cleaned_count = Bytes("Cleaned") #uint64
    global_cleaning_count = Bytes("Cleaning") # uint64

    local_tot_donation = Bytes("Donation") #uint64

    # Operations
    op_donate = Bytes("Donate") # byteslice

    @Subroutine(TealType.none)
    def donate():
        donation = ScratchVar(TealType.uint64)

        return Seq(
            program.check_self(
                group_size = Int(1),
                group_index = Int(0)
            ),
            program.check_rekey_zero(2),
            Assert(
                And(
                    # Check if account has opted in
                    App.optedIn(Txn.sender(), Global.current_application_id()),

                    Txn.type_enum() == TxnType.Payment,
                    Txn.receiver() == Global.current_application_address(),
                    Txn.close_remainder_to == Global.zero_address(),

                    # Check if donation amount is specified
                    Txn.application_args.length() == Int(2)
                )
            ),
            donation.store(App.localGet(local_tot_donation)),
            App.localPut(Txn.sender(), local_tot_donation, donation.load() + Int(1)),
            Approve()
        )

    return program.event(
        init = Seq(
            App.globalPut(global_cleaned_count, Int(0)),
            App.globalPut(global_cleaning_count, Int(0)),
            Approve()
        ),
        opt_in = Seq(
            App.localPut(Txn.sender(), local_tot_donation, Int(0)),
            Approve()
        ),
        no_op = Seq(
            Cond(
                [Txn.application_args[0] == op_donate, donate()]
            )
        )
    )
    

def clear():
    return Approve()

