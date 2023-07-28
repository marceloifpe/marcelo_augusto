import socket

# Equipe: Marcelo, Henrique e Davi.
# Atividade de Chatbot Servidor/CLiente utilizando Criptografia Assimétrica(RSA).
# Professor: Waldemar Neto.
# Disciplina: Segurança da Informaçao.


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


def server_program():
    host = socket.gethostname()
    port = 5013

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)

    conn, address = server_socket.accept()
    print("Conexão estabelecida: " + str(address))

    # Gerar chaves pública e privada para criptografia RSA do servidor
    p_server = 211
    q_server = 223
    public_key_server, private_key_server = generate_keypair(
        p_server, q_server)

    # Enviar a chave pública do servidor para o cliente
    conn.send(str(public_key_server).encode())

    # Receber a chave pública do cliente
    public_key_client = eval(conn.recv(1024).decode())

    print("Sua chave pública: ", public_key_server)
    print("Sua chave privada: ", private_key_server)
    print("Chave pública do cliente: ", public_key_client, "\n\n")

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break

        print("Mensagem do cliente criptada: " + str(data))

        # Descriptografar a mensagem recebida do cliente usando a chave privada do servidor
        decrypted_data = decrypt(eval(data), private_key_server)

        print("Mensagem do cliente decriptada: " + decrypted_data)

        message = input(" -> ")
        # Criptografar a mensagem usando a chave pública do cliente antes de enviá-la
        encrypted_message = encrypt(message, public_key_client)

        conn.send(str(encrypted_message).encode())

    conn.close()


if __name__ == "__main__":
    server_program()
