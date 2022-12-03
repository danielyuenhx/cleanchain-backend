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

    # Operations
    op_donate = Bytes("donate") # byteslice
    op_select = Bytes("select") # byteslice
    op_claim = Bytes("claim") # byteslice

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
                    App.optedIn(Txn.sender(), Global.current_application_id()),

                    Gtxn[1].type_enum() == TxnType.Payment,
                    Gtxn[1].receiver() == Global.current_application_address(),
                    Gtxn[1].close_remainder_to() == Global.zero_address(),

                )
            ),

            # Store local donation for the specific user and add to the global donation
            scratch_donation.store(App.globalGet(global_donation)),
            App.localPut(Txn.sender(), local_donation, Gtxn[1].amount()),
            App.globalPut(global_donation, scratch_donation.load() + Gtxn[1].amount()),
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
                And(
                    App.optedIn(Txn.sender(), Global.current_application_id()),

                    Txn.type_enum() != TxnType.Payment,

                    # Ensure that no one has already selected the project
                    App.globalGet(global_claimant) == Bytes(""),
                    Txn.application_args.length() == Int(1)
                ),
            ),
            App.globalPut(global_claimant, Txn.sender()),
            Approve()
        )
        

    @Subroutine(TealType.none)
    def claim():
        return Seq(
            program.check_self(
                group_size = Int(1),
                group_index = Int(0)
            ),
            program.check_rekey_zero(2),
            Assert(
                And(
                    # Whoever selected the project needs to claim funds
                    App.globalGet(global_claimant) != Bytes(""),
                    Txn.sender() == App.globalGet(global_claimant),

                    Txn.application_args.length() == Int(2),  
                ),
            ),

            If (
                Btoi(Txn.application_args[1]) >= App.globalGet(global_clean_threshold)
            ).Then(
                Seq(
                    Assert(Txn.fee() >= Global.min_txn_fee() * Int(2)),
                    send_bounty(Txn.sender(), App.globalGet(global_donation))
                ),
            ).Else(
                Reject()
            ),
            Approve()
        )

    @Subroutine(TealType.none)
    def send_bounty(account:Expr, amount: Expr):
        return Seq(
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.Payment,
                TxnField.receiver: account,
                TxnField.amount: amount,
                TxnField.fee: Int(0)
            }),
            InnerTxnBuilder.Submit()
        )
        

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
                [Txn.application_args[0] == op_donate, donate()],
                [Txn.application_args[0] == op_select, select()],
                [Txn.application_args[0] == op_claim, claim()]
            ),
            Reject()
        ),
        delete=Seq(
            Assert(Txn.sender() == Global.creator_address()),
            Approve()
        )
    )
    

def clear():
    return Approve()

