import socket


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def mod_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi // e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi


def generate_keypair(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)

    # Escolher um valor 'e' como um número primo menor que phi
    e = 2
    while e < phi:
        if gcd(e, phi) == 1:
            break
        e += 1

    # Calcular o inverso modular de 'e' em relação a phi
    d = mod_inverse(e, phi)

    # Retornar chave pública e chave privada
    # Chave pública é (e, n), chave privada é (d, n)
    return ((e, n), (d, n))


def encrypt(message, public_key):
    e, n = public_key
    encrypted_message = [pow(ord(char), e, n) for char in message]
    return encrypted_message


def decrypt(encrypted_message, private_key):
    d, n = private_key
    decrypted_message = [chr(pow(char, d, n)) for char in encrypted_message]
    return ''.join(decrypted_message)


def client_program():
    host = socket.gethostname()
    port = 5013

    client_socket = socket.socket()
    client_socket.connect((host, port))

    # Gerar chaves pública e privada para criptografia RSA do cliente
    p_client = 101
    q_client = 103
    public_key_client, private_key_client = generate_keypair(
        p_client, q_client)

    # Receber a chave pública do servidor
    public_key_server = eval(client_socket.recv(1024).decode())

    # Enviar a chave pública do cliente para o servidor
    client_socket.send(str(public_key_client).encode())

    print("Para encerrar a conversa digite 'vlw flw'.\n")

    print("Sua chave pública: ", public_key_client)
    print("Sua chave privada: ", private_key_client)
    print("Chave pública do servidor: ", public_key_server, "\n\n")

    message = input(" -> ")
    while message.lower().strip() != "vlw flw":
        # Criptografar a mensagem usando a chave pública do servidor antes de enviá-la
        encrypted_message = encrypt(message, public_key_server)

        client_socket.send(str(encrypted_message).encode())
        data = client_socket.recv(1024).decode()

        print("Mensagem do servidor criptada: " + str(data))

        # Descriptografar a mensagem recebida do servidor usando a chave privada do cliente
        decrypted_data = decrypt(eval(data), private_key_client)
        print("Mensagem do servidor decriptada: " + decrypted_data)

        message = input(" -> ")

    client_socket.close()


if __name__ == "__main__":
    client_program()
