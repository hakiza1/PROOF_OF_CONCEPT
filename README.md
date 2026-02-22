(DRAFT)




# HAKIZA-1i (MMB-basic & MMB-lite)                                                           




HAKIZA-1i (Money-Maker-Bot or MMB) is an informational version of the mechanical one known as the HAKIZA-1 (Energy-Maker-Machine or EMM) 

For more details, read both the **DESCRIPTION.md  and  informational-mutation-theory.md**.

To dig deeper, see the mechanical version (google the HAKIZA 1).  


# USER GUIDE (with AI help)       
        
Below is a **comprehensive step-by-step guide** for deploying the MMB on **Amazon EC2** and execute automated trades on Deriv platform:


Step 1: Launch an EC2 Instance

1. Log in to the AWS Management Console
- Go to the [AWS Management Console](https://aws.amazon.com/console/).
- Create an AWS account if you don't already have one, Sign in with your AWS account credentials and set your location preferably to Western-Europe.

2. Navigate to the EC2 Dashboard
- In the AWS Management Console, search for **EC2** in the search bar at the top.
- Click on **EC2** to open the EC2 Dashboard.

3. Launch a New Instance
1. In the EC2 Dashboard, click **Launch Instance** under the "Instances" section.
2. You will be taken to the **Create Instance Wizard**. Follow these steps:

---



Step 2: Configure the Instance

a. Choose an Amazon Machine Image (AMI)
- Select an operating system image for your instance:
  - For example, choose **Amazon Linux 2** or **Debian** (free tier eligible).
  - Click **Select** to proceed.

b. Choose an Instance Type
- Select the instance type. For lightweight workloads like your trading bot, choose:
  - **t2.micro** or **t3.micro** (free tier eligible).
  - Click **Next: Configure Instance Details**.

c. Configure Instance Details
- On this page, configure the following:
  - **Number of Instances**: Leave as `1` unless you need multiple instances.
  - **Network**: Use the default VPC or select a custom one.
  - **Subnet**: Choose a subnet (default is fine for most use cases).
  - **Auto-assign Public IP**: Ensure this is set to **Enable** so the instance gets a public IP address.
  - Click **Next: Add Storage**.

d. Add Storage
- By default, AWS provides 8 GB of storage for free-tier instances. You can increase this if needed.
- Click **Next: Add Tags**.

e. Add Tags
- Tags are optional but useful for organizing resources. For example:
  - Key: `Name`
  - Value: `Trading-Bot-Instance`
- Click **Next: Configure Security Group**.

f. Configure Security Group
- A security group acts as a virtual firewall for your instance.
- Create a new security group or use an existing one:
  - Add a rule to allow **SSH** access (port 22) from your IP address:
    - Type: `SSH`
    - Protocol: `TCP`
    - Port Range: `22`
    - Source: Your IP (`0.0.0.0/0` allows access from anywhere, but this is less secure).
  - Optionally, add rules for other services (e.g., HTTP/HTTPS if hosting a web server).
- Click **Review and Launch**.

---



Step 3: Review and Launch
1. Review all the settings you configured.
2. If everything looks correct, click **Launch**.

---



Step 4: Create or Select an SSH Key Pair    
- When prompted, choose:
  - **Create a new key pair**: Provide a name (e.g., `MMB`) and download the `MMB.pem` file.
  - **Use an existing key pair**: Select a key pair you already created.
- Store the `.pem` file securely and set permissions:

      chmod 400 /path/to/MMB.pem

- Click **Launch Instances**.

---



Step 5: Find the Public IP Address of Your EC2 Instance

1. Go to the EC2 Dashboard
- After launching the instance, go back to the **EC2 Dashboard**.

2. Locate Your Instance
- In the left-hand navigation pane, click **Instances** under the "Instances" section.
- You’ll see a list of all your instances.

3. Check the Public IP Address
- Select your instance from the list.
- In the **Description** tab at the bottom, look for:
  - **Public IPv4 address and Public domain**: This is the public IP address and Public domain assigned to your instance.
  - Example: `2-3-67-77-244`.
         ==> `ec2-3-67-76-244.eu-central-1.compute.amazonaws.com`
 




* CONNECTION TO EC2     


Amazon-linux is recommended for its low stealing-time; FOR Debian, use admin instead of ec2-user; since deriv servers are located in EU, make sure the amazon virtual private server is also located in EU to minimize latency.

Open the terminal (Linux/Debian), access the folder where your key pair is located (saved by default in Downloads folder) and connect to your instance via SSH as follows:
 
 To connect to the instance
      
        └─$ cd Downloads           
        └─$ chmod 400 "MMB.pem"
 
e.g.:    

        └─$ ssh -i "MMB.pem" ec2-user@ec2-3-67-77-244.eu-central-1.compute.amazonaws.com
 


 To prepare the system environment (FOR Debian, use apt-get instead of dnf) 
   
        └─$ sudo dnf update                            

        └─$ sudo dnf upgrade                                   

        └─$ sudo dnf install git                    

        └─$ sudo dnf install make

        └─$ python3 --version

        └─$ python3.* -m venv bot-env

        └─$ source bot-env/bin/activate
        
        └─$ pip install --upgrade pip

        └─$ pip install pipenv

        └─$ pip install websocket-client 

        └─$ pip install rx




        └─$ mkdir HAKIZA-1i

        └─$ cd HAKIZA-1i

        └─$ git clone https://github.com/deriv-com/python-deriv-api

        └─$ cd python-deriv-api

        └─$ make setup

        └─$ make all

        └─$ make test



 
 (replace the content of the Pipfile FOR Debian otherwise the "make setup" won't work, NOT NECESSARILY NEEDED FOR Amazon-linux):


        └─$ nano Pipfile

        =======================
        [packages]
        websockets = "==10.3"
        reactivex = "*"
        python-deriv-api = "*"
        mako = ">=1.3.6"
        rx = "*"

        [dev-packages]
        pytest = "*"
        pytest-runner = "*"
        pytest-mock = "*"
        pytest-asyncio = "*"
        pdoc3 = "*"
        coverage = "===4.5.4"
        ======================






 
 
* SESSION CREATION 1

 To start a new session

        └─$ screen -S bot-session                                        

 To activate virtual environment
    
        └─$ source bot-env/bin/activate       

 To aceess the folder where to download the HAKIZA-1i-basic.py
      
        └─$ cd HAKIZA-1i/python-deriv-api/
        
        └─$ mkdir test
        
        └─$ chmod 700 test
        
        └─$ cd test   

e.g.:        

        └─$ git clone https://username:**************************@github.com/HAKIZA-1i-basic.git
            
 To manually Copy paste the content of the MMB into the blank file and create the  HAKIZA-1i-basic.py
    
        └─$ nano HAKIZA-1i-basic.py 
        
        (ctrl O and Enter to save, ctrl X to exit) 
 
 To  protect the created HAKIZA-1i-basic.py file from corruption

        └─$ chmod 400 HAKIZA-1i-basic.py
        

 To set the APIs token and WEBSOCKET (Register a deriv account on app.deriv.com and pass the KYC; go to api.deriv.com and generate your own API-token and APP ID)
e.g.:

        └─$ export DERIV_TOKEN=KkW7Jy74m5ugqAw     
        └─$ export DERIV_WEBSOCKET=wss://ws.derivws.com/websockets/v3?app_id=85895                  

 To  unset the APIs token
        
        └─$ unset DERIV_TOKEN                                             

 To  check the APIs token

        └─$ echo $DERIV_TOKEN   

 TO START THE THE HAKIZA-1i-basic.py

        └─$ python3 HAKIZA-1i-basic.py   
        
 TO STOP THE HAKIZA-1i-basic.py 
        
        (ctrl C)     

 TO DETACH

        (ctrl A D  or  screen -d bot-session)  

 To resume the session  

        └─$ screen -r bot-session 

 To resume a specific session 

        └─$ screen -r ****.bot-session   
     
 To terminate a specific session
     
        └─$ screen -X -S ****.bot-session quit                            


 To START THE HAKIZA-1i-basic.py while both saving the process and making sure it won't stop even if the shell is closed.

        └─$ nohup python  HAKIZA-1i-basic.py >  HAKIZA_output.log 2>&1 &   
         
        (An ID=***** of your started session will appear)
          
 To monitor in real time
  
        └─$ tail -f HAKIZA_output.log                                                                                      

 To stop the HAKIZA-1i-basic.py using the session ID

        └─$ kill ***** 




* SESSION CREATION 2  (recommended) 

 Alternative for SESSION CREATION (VERY RECOMMENDED for Interactive Use):

        └─$ source bot-env/bin/activate

 Install tmux (if not installed):

        └─$ sudo dnf update && sudo dnf install tmux        
     
        (use apt instead of dnf for Debian)


 Start a new session:

        └─$ source bot-env/bin/activate

        └─$ tmux new -s MMB

        └─$ cd HAKIZA-1i/python-deriv-api/test

e.g.:

        └─$ export DERIV_TOKEN=g9ZnBXIxRhQeoYq
        
        └─$ export DERIV_WEBSOCKET=wss://ws.derivws.com/websockets/v3?app_id=85869


 Inside the session, run the MMB if already downloaded or manually created:

        └─$ python3 HAKIZA-1i-basic.py

 Then **detach** from the session with:  

        (`Ctrl+B`, then press `D`).
 
 Later, reattach:
      
        └─$ tmux attach -t MMB







NOTE:

      
The HAKIZA-1i basic and lite shares the same way of deployment  but the later one comes with 4 additional patterns (with diversified time-frames and ticks-skipping) forming in total 100 pattern detectors with more secure threshold...It is still aimed for educators (educational purpose), but professional traders with coding skills can refine it for real trading (not recommended).

The already existing Pattern within the MMB-basic (counting the number of consecutive reversal sequences but actually with 19 as a threshold for the lite version): 

        /0\0/0\0/0\0/0\0/0\0/0\0/0\0/0\0/0\0/-1\+2
     

First lite Additional Pattern to the already used patterns within the MMB-basic (counting the number of consecutive isolated-single-reversal sequences with 19 as a threshold): 

        /0   \0    /0   \0    /0   \0    /0   \0    /0   \0   /0      \0          /0  \0    /0    \0   /0    \0    /-1     \+2/...  
     
      
Second lite Additional Pattern to the already used patterns within the MMB-basic (counting the number of consecutive isolated-multiple-reversal sequences with 19 as a threshold):  
     
        \0/   \0/\/  \0/\  /0\   /0\/\  /0\/\/   /0\  /0\  /0\/     \0/\/  \0/  \0/\   /0\/    \0/\/\/\   /0\   /0\/\/    \0/\  /0\/   \-1/\/   \+2  

        

All of those examples are very effectively already tested and turned out to be very simple and practically efficient in real world (within the «HAKIZA-1i-lite, the first additional pattern is used for instance in informational INGOMA4 and any of its consequential non reversal sequences version is used for instance in informational INGOMA3;  the second additional pattern is used for instance in informational INGOMA12 and any of its consequential non reversal sequences version is deployed for instance in informational INGOMA11; the rest of the 14 informational INGOMA among the 20 informational INGOMA witin the MMB-lite come from diversified time-frames)... For more details, see the informational-mutation theory. 



=== 
Use demo APP-ID & API-token either for educational or regulation purpose. The present MMB is just a proof of concept; be aware that any retail broker has the capability to manipulate, alter tick data feeds or even delay trade executions, which can lead to discrepancies and affect the MMB performance. 
INTUMVA ZAMAHO,NDASUBIYEMWO: "Don't use the basic version in real trading without further refinement otherwise you may loose your funds due to arbitrage".

 
 
=== 
Caution with Real Funds: Proceed with caution and do thorough testing before committing real capital (if one's goal is to trade with real money, be more than paranoiac in refining the HAKIZA-1i "basic & lite" before claiming triumph over brokers' paranoia). At some extent, be aware that retail brokers may even sometimes target demo accounts to anticipate traders' strategies".


 

N.B.: The HAKIZA-1i (basic & lite) is aimed for educators (educational purpose) and regulatory institutions (data-integrity regulation purpose).

 



# RUN YOUR OWN TEST AND EMBRACE THE FACTS                                                                  hakiza1@proton.me


