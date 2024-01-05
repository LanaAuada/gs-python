from funcao import *
import json
import os
continua = "sim"
agendamentos=[]
novosAgendamentos = []
agendamentosAnteriores =[]
continuacao = False

try:

    # coloca os agendamentos que já existem em uma lista, ara recoloca-los no json depois da seção
    with open(f'agendamentos.json', 'r', encoding='utf-8') as arquivo:
        itensAgendamento = json.loads(arquivo.read())
        for item in itensAgendamento:
                agendamentos.append(item)

    cadastro = input("Você já possui cadastro? (Digite 'sim' ou 'não') ").lower()

    if cadastro == "não":
        #área de cadastro e validação dos dados do usuário
        print("CADASTRO")
        
        nome = input("Informe seu nome: ")
        erro = validaNome(nome)
        if erro:
            raise ValueError(erro)
        
        email = input("Informe seu e-mail: ")
        erro = validaEmail(email)
        if erro:
            raise ValueError(erro)
        
        senha = input("Crie uma senha de 6 dígitos: ")
        erro = validaSenha(senha)
        if erro:
            raise ValueError(erro)

        # as informações de cadastro do usuário novo são armazenadas no dicionário
        infoCliente = {
            "nome": nome,
            "email": email,
            "senha": senha
        }

        #verifica se o email já foi cadastrado
        if os.path.exists(f'usuarios/{email}.json'):
            erro = "Email já cadastrado."
            raise FileNotFoundError
        # armazena as informações do cliente em um documento json
        else:
            with open(f'usuarios/{email}.json', 'w', encoding='utf-8') as arquivo:
                json.dump(infoCliente,arquivo)
            print("Cadastro realizado com sucesso!!")

    elif cadastro=="sim":
        #verifica as informações do cadastro
        email = input("Informe seu e-mail: ")
        erro = validaEmail(email)
        if erro:
            raise ValueError(erro)
        
        # se o cadastro com o email informado existir, o arquivo é lido e as informações são validadas para o login
        if os.path.exists(f'usuarios/{email}.json'):
            with open(f'usuarios/{email}.json', 'r', encoding='utf-8') as arquivo:
                infocadastro = json.loads(arquivo.read())
                senha = input("Digite sua senha de 6 dígitos: ")
                erro = validaSenha(senha)
                if erro:
                    raise ValueError(erro)
                if email == infocadastro['email'] and senha == infocadastro['senha']:
                    print(f"Acesso permitido! Bem-vindo(a), {infocadastro['nome']}")
                else:
                    erro = "Senha incorreta"
                    raise ValueError
        
        # caso o email não exista, é exibida a mensagem de erro
        else:
            erro = "E-mail incorreto"
            raise FileNotFoundError  
    else:
        erro= "Por favor, digite sim ou não."
        raise ValueError

    while True:
        # coloca os dados do json na variável "dados"
        with open(f'dados.json', 'r', encoding='utf-8') as arquivo:
                dados = json.loads(arquivo.read())

        print("MENU PRINCIPAL")
        print("Digite (1) para solicitar um agendamento\nDigite(2) para consultar seus agendamentos\nDigite(3) para encerrar seção")
        escolha = input()

        if escolha == '1':
        
            # inicio do menu de opções para o agendamento
            print("\nSOLICITAÇÃO DE AGENDAMENTO")
            print("Por favor, digite os opções exatamente como elas estão escritas!")
            exibir_especialidades(dados)

            # se o usuário escolher uma especialidade, vai para o próximo passo
            # se eel sair sai do loop while
            especialidade_escolhida = input("\nEscolha uma especialidade (ou 'sair' para encerrar): ")

            # realiza a validação de cada informação e caso a informação seja inválida, pede ao usuário para digitar novamente
            if validar_especialidade(dados, especialidade_escolhida):
                exibir_clinicas(dados, especialidade_escolhida)
                clinica_escolhida = input("\nEscolha uma clínica: ")
            
                if validar_clinica(dados, especialidade_escolhida, clinica_escolhida):
                        exibir_profissionais(dados, especialidade_escolhida, clinica_escolhida)
                        profissional_escolhido = input("\nEscolha um profissional: ")

                        if validar_profissional(dados, especialidade_escolhida, clinica_escolhida, profissional_escolhido):
                            exibir_horarios(dados, especialidade_escolhida, clinica_escolhida, profissional_escolhido)
                            data_escolhida = input("\nEscolha uma data (formato: YYYY-MM-DD): ")
                            horario_escolhido = input("Escolha um horário: ")

                            if validar_data_hora(dados, especialidade_escolhida, clinica_escolhida, profissional_escolhido, data_escolhida, horario_escolhido):
                                with open(f'usuarios/{email}.json', 'r', encoding='utf-8') as arquivo:
                                    infocadastro = json.loads(arquivo.read())
                                    nome = infocadastro['nome']
                                agendar_consulta(dados,agendamentos,novosAgendamentos, especialidade_escolhida, clinica_escolhida, profissional_escolhido, data_escolhida, horario_escolhido, email)
                                continuacao = True
                                if novosAgendamentos == []:
                                    erro = "Solcitação de Agendamento incompleto"
                                    raise ValueError
                        
                                elif novosAgendamentos!=[] and continuacao==True:
                                    with open(f'usuarios/{email}.json', 'r', encoding='utf-8') as arquivo:
                                        infocadastro = json.loads(arquivo.read())
                                    exibir_resumo_cliente(infocadastro)
                                    # exibe o resumo e coloca no json
                                    exibir_resumo(novosAgendamentos,infocadastro['email'])
                                    salvar_agendamentos_json(agendamentos)
                                    print("*" * 70)
                            else:
                                print("Data ou horário inválidos. Por favor, escolha novamente.")
                        else:
                            print("Profissional inválido. Por favor, escolha novamente.")
                else:
                    print("Clínica inválida. Por favor, escolha novamente.")
            else:
                print("Especialidade inválida. Por favor, escolha novamente.")

            # if novosAgendamentos == []:
            #     erro = "Solcitação de Agendamento incompleto"
            #     raise ValueError
    
            # elif novosAgendamentos!=[] and continuacao==True:
            #     with open(f'usuarios/{email}.json', 'r', encoding='utf-8') as arquivo:
            #         infocadastro = json.loads(arquivo.read())
            #     exibir_resumo_cliente(infocadastro)
            #     # exibe o resumo e coloca no json
            #     exibir_resumo(novosAgendamentos,infocadastro['email'])
            #     salvar_agendamentos_json(agendamentos)
            #     print("*" * 70)
        
        elif escolha == '2':
            with open(f'usuarios/{email}.json', 'r', encoding='utf-8') as arquivo:
                infocadastro = json.loads(arquivo.read())
            busca_agendamento(agendamentos, infocadastro, agendamentosAnteriores)

        #exibe as mensagens finais: informações do cliente, resumo da operação e agradecimento
            if agendamentosAnteriores == []:
                erro = "Agendamentos não encontrados"
                raise ValueError
            
            else:
                print("CONSULTA DE EXAMES AGENDADOS")
                with open(f'usuarios/{email}.json', 'r', encoding='utf-8') as arquivo:
                    infocadastro = json.loads(arquivo.read())
                exibir_resumo_cliente(infocadastro)
                # exibe o resumo e coloca no json
                exibir_resumo(agendamentosAnteriores,infocadastro['email'])
                print("*" * 70)
        elif escolha == '3':
            break
        else:
            print("Opção inválida, digite novamente.")
         
except ValueError:
    print(f"\n{erro}")
except FileNotFoundError:
    print(f"\n{erro}")
except FileExistsError:
    print(f"\n{erro}")
finally:
    print("Fim da sessão do agendamento")
