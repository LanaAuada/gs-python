import re
import json

# função que verifica se o nome tem números ou está vazio
def validaNome(nome):
    erro=""
    if re.search("\d",nome) or nome == '':
        erro = "Campo obrigatório.Por favor, insira um nome válido, sem números."
    return erro

# verifica se o email está na estrutura padrão aceita
def validaEmail(email):
    erro=""
    if not re.search("\w+@\w+\.\w+", email) or email == '':
        erro = "Campo obrigatório. Por favor, insira um e-mail válido."
    return erro

# verifica se a senha possui 6 números
def validaSenha(senha):
    erro=""
    if not re.search("\d{6}",senha) or len(senha) > 6 or senha == '':
        erro = "Campo obrigatório. Por favor, insira uma senha válida de 6 dígitos."
    return erro

# percorre o json de dados para exibir as especialidades
def exibir_especialidades(dados):
    print("Especialidades disponíveis:")
    for especialidade in dados["especialidades"]:
        print(especialidade["nome"])

def validar_especialidade(dados, especialidade_escolhida):
    for especialidade in dados["especialidades"]:
        if especialidade["nome"] == especialidade_escolhida:
            return True
    return False

# percorre o json de dados para exibir a clínica
def exibir_clinicas(dados, especialidade_escolhida):
    for especialidade in dados["especialidades"]:
        if especialidade["nome"] == especialidade_escolhida:
            print(f"\nClínicas de {especialidade['nome']}:")
            for clinica in especialidade["clinicas"]:
                print(clinica["nome"])

def validar_clinica(dados, especialidade_escolhida, clinica_escolhida):
    for especialidade in dados["especialidades"]:
        if especialidade["nome"] == especialidade_escolhida:
            for clinica in especialidade["clinicas"]:
                if clinica["nome"] == clinica_escolhida:
                    return True
    return False


# percorre o json de dados para exibir os profissionais
def exibir_profissionais(dados, especialidade_escolhida, clinica_escolhida):
    for especialidade in dados["especialidades"]:
        if especialidade["nome"] == especialidade_escolhida:
            for clinica in especialidade["clinicas"]:
                if clinica["nome"] == clinica_escolhida:
                    print(f"\nProfissionais de {especialidade['nome']} na {clinica['nome']}:")
                    for profissional in clinica["profissionais"]:
                        print(profissional["nome"])

def validar_profissional(dados, especialidade_escolhida, clinica_escolhida, profissional_escolhido):
    for especialidade in dados["especialidades"]:
        if especialidade["nome"] == especialidade_escolhida:
            for clinica in especialidade["clinicas"]:
                if clinica["nome"] == clinica_escolhida:
                    for profissional in clinica["profissionais"]:
                        if profissional["nome"] == profissional_escolhido:
                            return True
    return False

# percorre o json de dados para exibir as datas e hprários
def exibir_horarios(dados,especialidade_escolhida, clinica_escolhida, profissional_escolhido):
    for especialidade in dados["especialidades"]:
        if especialidade["nome"] == especialidade_escolhida:
            for clinica in especialidade["clinicas"]:
                if clinica["nome"] == clinica_escolhida:
                    for profissional in clinica["profissionais"]:
                        if profissional["nome"] == profissional_escolhido:
                            print(f"\nHorários disponíveis para {profissional['nome']} ({especialidade['nome']}) na {clinica['nome']}:")
                            for data, horarios in profissional["horarios_disponiveis"].items():
                                print(f"{data}:")
                                for horario in horarios:
                                    print(horario)

def validar_data_hora(dados, especialidade_escolhida, clinica_escolhida, profissional_escolhido, data_escolhida, horario_escolhido):
    try:
        horarios_disponiveis = None
        for especialidade in dados["especialidades"]:
            if especialidade["nome"] == especialidade_escolhida:
                for clinica in especialidade["clinicas"]:
                    if clinica["nome"] == clinica_escolhida:
                        for profissional in clinica["profissionais"]:
                            if profissional["nome"] == profissional_escolhido:
                                horarios_disponiveis = profissional["horarios_disponiveis"]
                                break
                        if horarios_disponiveis:
                            break

        if horarios_disponiveis and data_escolhida in horarios_disponiveis and horario_escolhido in horarios_disponiveis[data_escolhida]:
            return True
        else:
            return False

    except ValueError:
        return False
    
def agendar_consulta(dados,agendamentos,novosAgendamentos, especialidade_escolhida, clinica_escolhida, profissional_escolhido, data_escolhida, horario_escolhido, email):
    agendamento = {
        "especialidade": especialidade_escolhida,
        "clinica": clinica_escolhida,
        "profissional": profissional_escolhido,
        "data": data_escolhida,
        "horario": horario_escolhido,
        "paciente": email
    }

    for especialidade in dados["especialidades"]:
        if especialidade["nome"] == especialidade_escolhida:
            for clinica in especialidade["clinicas"]:
                if clinica["nome"] == clinica_escolhida:
                    for profissional in clinica["profissionais"]:
                        if profissional["nome"] == profissional_escolhido:
                            profissional["horarios_disponiveis"][data_escolhida].remove(horario_escolhido)
    agendamentos.append(agendamento)
    novosAgendamentos.append(agendamento)
    print("\nConsulta agendada com sucesso!")

def busca_agendamento (agendamentos, infocadastro, agendamentosAnteriores):
        for item in agendamentos:
            if 'paciente' in item and infocadastro['email'] == item['paciente']:
                agendamentosAnteriores.append(item)
def exibir_resumo_cliente(infocadastro):
    print("*" * 70)
    print("INFORMAÇÕES DO CLIENTE:")
    print(f"Nome: {infocadastro['nome']}")
    print(f"E-mail: {infocadastro['email']}")
    print("*" * 70)

def exibir_resumo(novosAgendamentos,email):
    print("\nResumo do Agendamento:")
    for agendamento in novosAgendamentos:
        print(f"\nEspecialidade: {agendamento['especialidade']}")
        print(f"Clínica: {agendamento['clinica']}")
        print(f"Profissional: {agendamento['profissional']}")
        print(f"Data: {agendamento['data']}")
        print(f"Horário: {agendamento['horario']}")
        print(f"Paciente: {email}")

def salvar_agendamentos_json(agendamentos):
    with open("agendamentos.json", "w") as file:
        json.dump(agendamentos, file)
    print("\nAgendamento(s) realizado(s)")


    # criar outro agendamento para exibir só os dessas sessão