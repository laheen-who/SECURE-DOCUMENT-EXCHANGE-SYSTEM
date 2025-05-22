# SECURE-DOCUMENT-EXCHANGE-SYSTEM
Overview
Welcome to the Secure Document Exchange System, a project I built for a hackathon on May 22, 2025! This system is like a super-safe mailbox for two offices—let’s call them Ministry 1 and Ministry 2—to send secret messages (like XML documents) to each other without anyone snooping. I used a security trick called mTLS (mutual Transport Layer Security) to ensure only the right people can send and receive messages.
The system has two main parts:

SEG-Sender: The messenger who delivers the secret message.
SEG-Receiver: The secure mailbox that receives the message.

My test message was about a lunch party on Saturday, and I made sure it was delivered securely using certificates (like digital ID cards).
Check out the code here: https://github.com/laheen-who/SECURE-DOCUMENT-EXCHANGE-SYSTEM
Features

Securely sends XML documents using mTLS.
Uses certificates to verify identities (Root CA, server, and client certificates).
Works on your computer (localhost) or across a network (using your IP).

Prerequisites
Before you start, install these tools:

Python 3: To run the SEG programs.
OpenSSL: To create certificates. Install it on Windows, Mac, or Linux.
Python Libraries:
Flask (for SEG-Receiver): pip install flask
Requests (for SEG-Sender): pip install requests



Setup Instructions
Step 1: Clone the Repository
Download this project:
git clone https://github.com/laheen-who/SECURE-DOCUMENT-EXCHANGE-SYSTEM.git
cd SECURE-DOCUMENT-EXCHANGE-SYSTEM

Or download the ZIP file from GitHub and unzip it.
Step 2: Create Certificates
We need digital ID cards (certificates) for security. Use these OpenSSL commands in a command window (e.g., PowerShell on Windows).
1. Create the Root CA (Principal’s Signature)
This acts like a principal who signs the ID cards.
openssl genrsa -out rootCA.key 2048
openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 1024 -out rootCA.pem


Enter details:
Country: BD
Organization: Ministry
Common Name: Root CA
Press Enter for others.



2. Create the Server Certificate (SEG-Receiver’s ID)
For the mailbox (SEG-Receiver).
openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr


Details:
Country: BD
State: Some-State
Organization: Internet Widgits Pty Ltd
Common Name: localhost
Press Enter for others.



Add a note with a Subject Alternative Name (SAN):
echo "[server_ext]" > server.ext
echo "extendedKeyUsage=serverAuth" >> server.ext
echo "subjectAltName=DNS:localhost" >> server.ext

Sign it:
openssl x509 -req -in server.csr -CA rootCA.pem -CAkey rootCA.key -CAcreateserial -out server.crt -days 500 -sha256 -extfile server.ext -extensions server_ext

3. Create the Client Certificate (SEG-Sender’s ID)
For the messenger (SEG-Sender).
openssl genrsa -out client.key 2048
openssl req -new -key client.key -out client.csr


Details:
Country: BD
State: Some-State
Organization: Internet Widgits Pty Ltd
Common Name: SEG-Sender
Press Enter for others.



Add a note:
echo "[client_ext]" > client.ext
echo "extendedKeyUsage=clientAuth" >> client.ext

Sign it:
openssl x509 -req -in client.csr -CA rootCA.pem -CAkey rootCA.key -CAcreateserial -out client.crt -days 500 -sha256 -extfile client.ext -extensions client_ext

4. Clean Up
Remove extra files:
del server.csr client.csr server.ext client.ext rootCA.srl

You should now have:

rootCA.pem, rootCA.key
server.crt, server.key
client.crt, client.key

Step 3: Create the Secret Message (document.xml)
The message is a secret note in document.xml. Create it with:
<CriticalDocument id="doc123">
    <SenderID>MINISTRY 1_SEG01</SenderID>
    <ReceiverID>MINISTRY 2_SEG01</ReceiverID>
    <TimestampForSignature>2025-05-22T12:43:00+06:00</TimestampForSignature>
    <Payload>
        <SensitiveData>Lunch party at Saturday</SensitiveData>
        <Instructions>Deliver by 0300.</Instructions>
    </Payload>
</CriticalDocument>

Use Notepad or this command:
echo ^<CriticalDocument id="doc123"^> > document.xml
echo     ^<SenderID^>MINISTRY 1_SEG01^</SenderID^> >> document.xml
echo     ^<ReceiverID^>MINISTRY 2_SEG01^</ReceiverID^> >> document.xml
echo     ^<TimestampForSignature^>2025-05-22T12:43:00+06:00^</TimestampForSignature^> >> document.xml
echo     ^<Payload^> >> document.xml
echo         ^<SensitiveData^>Lunch party at Saturday^</SensitiveData^> >> document.xml
echo         ^<Instructions^>Deliver by 0300.^</Instructions^> >> document.xml
echo     ^</Payload^> >> document.xml
echo ^</CriticalDocument^> >> document.xml

Step 4: Run SEG-Receiver (The Mailbox)
Open a command window and start the mailbox:
python seg_receiver.py

You’ll see:
 * Running on https://127.0.0.1:8000
 * Running on https://<your-ip>:8000

Keep this window open!
Step 5: Run SEG-Sender (The Messenger)
Open a new command window and send the message:
python seg_sender.py

You’ll see:
Server response: Received

And in SEG-Receiver:
Successful mTLS connection established.
Received XML: <CriticalDocument id="doc123">...</CriticalDocument>

Testing Across the Network (Optional)
SEG-Receiver runs on your network IP (e.g., 192.168.143.85:8000). To test from another computer:

Copy seg_sender.py, client.crt, client.key, rootCA.pem, and document.xml to the other computer.
Edit seg_sender.py to use your IP:response = requests.post('https://<your-ip>:8000', data=xml_data, cert=('client.crt', 'client.key'), verify='rootCA.pem')


Allow port 8000 on the SEG-Receiver computer:netsh advfirewall firewall add rule name="Allow Python 8000" dir=in action=allow protocol=TCP localport=8000


Run python seg_sender.py on the other computer.

Troubleshooting

“No module named flask”: Run pip install flask.
“No module named requests”: Run pip install requests.
Certificate Errors: Ensure server.crt’s Common Name and SAN match localhost or your IP.
“Address already in use”: Change the port in seg_receiver.py to 8001 and update seg_sender.py.

Acknowledgments

Big thanks to Grok (xAI) for guiding me through debugging and learning mTLS!
Built for a hackathon on May 22, 2025.

Demo
To see it in action:

Run python seg_receiver.py in one window.
Run python seg_sender.py in another window.
Watch SEG-Receiver display the XML and SEG-Sender confirm “Received”!


