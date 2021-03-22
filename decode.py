class Decode:
    """
    Decodes the encoded message using the private key. First, divides
    the encoded message by 'O' and create a list with encoded pairs of signs. Then,
    decodes the message using the private key, transforms the received number
    encoded with ASCII to correspond glyph and return the decoded and joined message.
    """

    def __init__(self, d, n, encoded_message):
        """
        Initialises private exponent d, totient n, encoded message and invokes 'decode'
        in order to decode the received message.
        """
        self.d = d
        self.n = n
        self.encoded_message = encoded_message
        self.decoded_message = self.decode()

    def decode(self):
        """
        Decodes the message using the private key and the above-mentioned method.
        """

        block_decoded_message = []
        ascii_list = []

        # Splits the encoded message removing 'O' and create a list
        block_encoded_message = self.encoded_message.split('O')

        # Converts elements of list into a integer
        try:
            block_encoded_message = [int(string) for string in block_encoded_message]
        except ValueError:
            return False

        # Decodes the message with the following pattern number_to_decode ** d % n
        for t in block_encoded_message:
            block_decoded_message.append(pow(t, self.d, self.n))

        # Divides calculated numbers into ASCII decimal format
        for i in range(len(block_decoded_message)):
            ascii_list.append(block_decoded_message[i] // 1000)
            ascii_list.append(block_decoded_message[i] % 1000)

        # If there exist 0 it is remove
        try:
            ascii_list.remove(0)
        except ValueError:
            pass

        # Joins the decoded sings into a one message.
        try:
            decoded_message = ''.join([chr(i) for i in ascii_list])
        except:
            return False

        return decoded_message
