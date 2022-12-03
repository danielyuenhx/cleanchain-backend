# Business Logic

1. Wallet creation/linking existing wallet handled by JS SDK on FE or calls Python SDK code available on the Backend

2. Anyone with an algorand wallet can donate money to the Dapp


# Contract 

**1. Opt in**
 - Called by FE when user either wants to perform lake clean/donation.
 - Initialize variables (donation/chosen_lake)

**2. Donation**
 - Smart contract should record user's donation under user's local account

**3. Lake selection**
 - Record user's lake selection (Off chain??) --> Look into layer 2

**4. Lake cleaned confirmation**
 - Validation  (Off chain logic to check pH??)
 - Trigger money sending transaction

**5. Lake rejection**