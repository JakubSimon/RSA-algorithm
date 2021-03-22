class Encode:
    """
    Encodes the passed message using the public key and ASCII. Before encoding, the passed message is
    divided into groups of 2 signs and converted into a number with using
    followed pattern 'ord(first_sign) * 1000 + ord(second_sign)'. It helps easily interpret both signs
    after decoding. The first sign is chr(received_number // 1000)
    and the second sign is chr(received_number % 1000). Also, it complicates the
    encoded message more than encoding every single sign separately.
    """

    def __init__(self, e, n, plain_message):
        """
        Initialises public exponent e, totient n, plain_message and invokes
        'encode' in order to encode the message and assigns it as encoded_message.
        """
        self.e = e
        self.n = n
        self.plain_message = plain_message
        self.encoded_message = self.encode()

    def encode(self):
        """
        Encodes the message with the public key and the above-mentioned method.
        """

        block_encoded_message = []

        if not self.plain_message:
            print("Nothing to encode")
            return "Nothing to encode"

        # Splits the plain_message into pairs and creates the list with those pairs of characters
        split_plain_message = [self.plain_message[i:i+2] for i in range(0, len(self.plain_message), 2)]

        # Converts the split message into numbers by the use of ASCII decimal format
        # and the following pattern 'ord(first_sign) * 1000 + ord(second_sign)'
        if len(self.plain_message) % 2:
            convert_to_ascii = [(ord(split_plain_message[i][0]) * 1000 + ord(split_plain_message[i][1]))
                                for i in range(len(split_plain_message) - 1)]
            convert_to_ascii.append(ord(split_plain_message[-1]))
        else:
            convert_to_ascii = [(ord(split_plain_message[i][0]) * 1000 + ord(split_plain_message[i][1]))
                                for i in range(len(split_plain_message))]

        # Encodes the message with using public key and the following pattern:
        # number_to_code ** e % n and change it into a string
        for i in range(len(convert_to_ascii)):
            block_encoded_message.append(str(pow(convert_to_ascii[i], self.e, self.n)))

        # Joins encoded number into one continuous text by using 'O' ('o' as office, not zero) as a joiner
        encoded_message = 'O'.join(block_encoded_message)

        return encoded_message
