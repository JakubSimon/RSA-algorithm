from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from fastapi.responses import PlainTextResponse
import prime_numbers_gen
import RSA_algorithm
import encode
import decode


# Creates instance FastAPI
app = FastAPI(
    title='RSA Algorithm API',
    description='This API: generates public and private keys, '
                'encodes and decodes message from plain text or file.')

# Creates a "security scheme" using HTTPBasic
security = HTTPBasic()


# Use a dependency to check if the username and password are correct.
def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "Admin")
    correct_password = secrets.compare_digest(credentials.password, "12345")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


# Creates method to generate public and private keys
@app.post("/key-generation/", tags=["Key generation"])
async def send_notification(length: int, auth: str = Depends(get_current_username)):

    # Prime numbers length constraint
    if length < 16 or length > 768:
        return "Length of the prime numbers should be within the range from 16-bit to 768-bit."

    prime = prime_numbers_gen.PrimeNumGen(length)
    keys = RSA_algorithm.RSA(prime.prime_numbers)

    return {"public key - e": '{:}'.format(keys.public_key[0]),
            "public key - n": '{:}'.format(keys.public_key[1]),
            "private key - d": '{:}'.format(keys.private_key[0]),
            "private key - n": '{:}'.format(keys.private_key[1])}


# Creates method to encode message from plain text
@app.post("/encode-from-text/", tags=["Encode message"], response_class=PlainTextResponse)
async def send_notification(e: int, n: int, message: str, auth: str = Depends(get_current_username)):

    # Tonient n should be greater than the highest value of possible number to encode (in this case it is 127127)
    if n <= 127127:
        return "Too short totient n."

    encoded_message = encode.Encode(e, n, message)

    return encoded_message.encoded_message


# Creates method to encode message from .txt file
@app.post("/encode-from-file/", tags=["Encode message"], response_class=PlainTextResponse)
async def send_notification(e: int, n: int, file: UploadFile = File(...), auth: str = Depends(get_current_username)):

    # This program accept only .txt extension
    if file.filename[-4:] != '.txt':
        return "Upload message in .txt extension"

    with open(file.filename) as file_object:
        message_to_encode = file_object.read()

    if len(message_to_encode) == 0:
        return "Nothing to encode."

    elif n <= 127127:
        return "Too short totient n."

    encoded_message = encode.Encode(e, n, message_to_encode)

    return encoded_message.encoded_message


# Creates method to decode message from text
@app.post("/decode-from-text/", tags=["Decode message"], response_class=PlainTextResponse)
async def send_notification(d: int, n: int, message: str, auth: str = Depends(get_current_username)):

    decoded_message = decode.Decode(d, n, message)

    if not decoded_message.decoded_message:
        return "Wrong input data to decode the message."

    return decoded_message.decoded_message


# Creates method to decode message from .txt file
@app.post("/decode-from-file/", tags=["Decode message"], response_class=PlainTextResponse)
async def send_notification(d: int, n: int, file: UploadFile = File(...), auth: str = Depends(get_current_username)):
    if file.filename[-4:] != '.txt':
        return "Upload encoded message in .txt extension"

    with open(file.filename) as file_object:
        message_to_decode = file_object.read()
    if len(message_to_decode) == 0:
        return "Nothing to decode."
    print(message_to_decode)
    decoded_message = decode.Decode(d, n, message_to_decode)
    if not decoded_message.decoded_message:
        return "Wrong input data to decode the message."

    return decoded_message.decoded_message
