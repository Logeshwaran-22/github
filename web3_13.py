import cv2
import hashlib
from web3 import Web3

# Connect to the blockchain network
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

# Get the contract address
contract_address = '0x42b1BFC2A2e8a87Fd5F05D6fFBe3A7764eAd6E49'
from_address = '0x7cEdE23A583886e0F6563d6857cD288dCA175197'

# Create a contract object
contract = w3.eth.contract(address=contract_address, abi=[
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "hash",
                "type": "string"
            }
        ],
        "name": "uploadVideo",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getVideos",
        "outputs": [
            {
                "components": [
                    {
                        "internalType": "string",
                        "name": "hash",
                        "type": "string"
                    },
                    {
                        "internalType": "uint256",
                        "name": "timestamp",
                        "type": "uint256"
                    }
                ],
                "internalType": "struct SurveillanceCamera.Video[]",
                "name": "",
                "type": "tuple[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
])

hashed_frame = ""

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # Hash the video footage
    hashed_frame = hashlib.sha256(frame).hexdigest()
    try:
        contract.functions.uploadVideo(hashed_frame).transact({'from': from_address})
        print("Video uploaded successfully.")
        
    except Exception as e:
        print(f"Failed to send data to the blockchain: {e}")
        break

    # Show the video footage
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam
cap.release()

# Close all windows
cv2.destroyAllWindows()
