from pyteal import *
from pyteal.ast.bytes import Bytes
from pyteal_helpers import program

def approval():
    # Global attributes
    global_donation = Bytes("Total") #uint64
    global_clean_threshold = Bytes("Clean_Threshold") # uint64
    global_claimant = Bytes("Claimant") # byteslice

    # Local attributes
    local_donation = Bytes("Donation")  # uint64

    # Utility functions
    app_address = Global.current_application_address()
    is_creator =  Txn.sender() == Global.creator_address()

    # Operations
    op_donate = Bytes("Donate") # byteslice
    op_select = Bytes("Select") # byteslice
    op_claim = Bytes("Claim") # byteslice

    @Subroutine(TealType.none)
    def donate():
        scratch_donation = ScratchVar(TealType.uint64)
        return Seq(
            program.check_self(
                group_size = Int(2),
                group_index = Int(0),
            ),
            program.check_rekey_zero(2),
            Assert(
                And(
                    # Check if account has opted in
                    App.optedIn(Txn.sender(), app_address),

                    Gtxn[1].type_enum() == TxnType.Payment,
                    Gtxn[1].receiver() == app_address,
                    Gtxn[1].close_remainder_to == Global.zero_address(),

                    # Check if donation amount is specified
                    Txn.application_args.length() == Int(2)
                )
            ),

            # Store local donation for the specific user and add to the global donation
            scratch_donation.store(App.globalGet(global_donation)),
            App.localPut(Txn.sender(), local_donation, Txn.application_args[1]),
            App.globalPut(global_donation, scratch_donation.load() + Btoi(Txn.application_args[1])),
            Approve()
        )

    @Subroutine(TealType.none)
    def select():
        return Seq(
            program.check_self(
                group_size = Int(1),
                group_index = Int(0)
            ),
            program.check_rekey_zero(2),
            Assert(
                App.optedIn(Txn.sender(), app_address),

                Txn.type_enum() != TxnType.Payment,

                # Ensure that no one has already selected the project
                App.globalGet(global_claimant) == Bytes(""),
                Txn.application_args.length() == Int(0)
            ),
            App.globalPut(global_claimant, Txn.sender()),
            Approve()
        )
        

    @Subroutine(TealType.none)
    def claim():
        pass

    return program.event(
        init = Seq(
            # Initialize total donation amount, cleanliness threshold, and selector
            App.globalPut(global_donation, Int(0)),
            App.globalPut(global_clean_threshold, Btoi(Txn.application_args[0])),
            App.globalPut(global_claimant, Bytes("")),
            Approve()
        ),
        opt_in = Seq(
            App.localPut(Txn.sender(), local_donation, Int(0)),
            Approve()
        ),
        no_op = Seq(
            Cond(
                [Txn.application_args[0] == op_donate, donate()]
                [Txn.application_args[0] == op_select, select()]
                [Txn.application_args[0] == op_claim, claim()]
            )
        )
    )
    

def clear():
    return Approve()

