# Cleanchain-Backend 

![CleanChain](images/logo.png)

This repository contains the smart contracts written for the CleanChain Application, developed for ACE-SIP Blockchain Hackathon.


## Setup:
Use the Algorand sandbox to deploy the code to the testnet 

1. Git clone the Algorand Sandbox to a directory of your choosing
https://github.com/algorand/sandbox.git

2. Modify the docker-compose file in the Algorand sandbox with the following.
```
services:
    algod:
        ....
        volumes:
            - type: bind
              source: <directory>/project
              target: /data
```

3. Access the testnet with the Algorand Sandbox and enter the running container
```
./sandbox up testnet -v
./sandbox enter algod
```

## Getting Started:
The smart contract is included in the following directory 
>  cleanchain-backend/project/contracts/contract.py

The contract.py file consists of the PyTeal code for the smart contract.
The contract supports four operations
1. Donate
2. Select (Express interest for a particular project)
3. Deselect 
4. Claim (Claim the bounty upon completion of the project)

Install the required dependencies for the file in either a venv or a conda virtual environment. (https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/, https://docs.python.org/3/library/venv.html)

```pip install -r ./requirements.txt```

### Compiling the smart contract
Run the build.sh shell script in 
> cleanchain-backend/project/

to compile the smart contract. This shell script runs compile.py and generates a build folder which contains the approval.teal and clear.teal files.

Run the script with <code>./build.sh contracts.contract</code>

### Usage

You will need to setup a wallet on the Testnet and import your PeraWallet account, as well as create a new app using the compiled teal code in the build folder. Instructions are provided in the following Lab by Algo-Hub.

https://github.com/Algo-Hub-io/pyteal-course/tree/main/Lab2

Some useful commands are contained in the `cleanchain-backend/env_variables.txt` files which can be used for reference.

The contracts folder contains scripts for running the main operations
1. Donate
2. Select
3. Claim
The relevant environment variables including APP_ID, DONOR_ACCOUNT etc. which are required for the above operations are stored in the config.sh file.

You may run these scripts in the algod container.
``` 
./sandbox enter algod
> bash ./donate.sh
```

## Linking with CleanChain-Frontend:

Run data fetching API in the backend by using:

python server.py

Make note of the App ID of your smart contract app and enter it in the `appIndex` variable within the App.js file of the React app.
