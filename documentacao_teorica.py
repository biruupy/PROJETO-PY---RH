# =====================================================================
# RESUMO DE ESTUDOS - PROJETO RH (VANGUARD SOLUTIONS) - A3
# Engenharia de Software - 1º semestre
#
# Como usar este arquivo:
#   - Ler os comentários (é a parte da teoria)
#   - Rodar com:  python documentacao_teorica.py
#     cada parte imprime um exemplo pequeno funcionando
#   - Este arquivo NÃO pede nada pelo teclado, só mostra os exemplos
#
# Cada item tem:
#   NA PRÁTICA     -> o que o comando faz, explicado simples
#   NO NOSSO CÓDIGO -> onde ele aparece no plataforma_rh.py
# =====================================================================


print("=" * 60)
print("RESUMO DE ESTUDOS - PROJETO RH")
print("=" * 60)


# #####################################################################
# PARTE 1 - LÓGICA BÁSICA
# #####################################################################
print("\n--- PARTE 1: LOGICA BASICA ---")


# ---------------------------------------------------------------------
# def (criar função)
# NA PRÁTICA: cria um "bloco de código com nome". Escrevo uma vez e uso
#   quantas vezes quiser só chamando o nome. Evita repetir código.
#   O que vai entre parênteses são os PARÂMETROS (as coisas que a
#   função recebe para trabalhar).
# NO NOSSO CÓDIGO:
#   def formatar_cpf(cpf):
#       return cpf[0:3] + "." + cpf[3:6] + "." + cpf[6:9] + "-" + cpf[9:11]
#   -> toda vez que a folha precisa mostrar um CPF, chama formatar_cpf(...)
# ---------------------------------------------------------------------
def dobro(numero):
    return numero * 2

print("def ->", dobro(5))  # 10


# ---------------------------------------------------------------------
# str, int e float (tipos de dados)
# NA PRÁTICA: todo valor no Python tem um TIPO.
#   str   = texto (string), sempre entre aspas: "Ana", "12345678901"
#   int   = número inteiro, sem vírgula: 0, 2, 160
#   float = número com casas decimais: 5000.0, 189.59
#   Os nomes também viram funções que CONVERTEM um tipo no outro:
#   int("2") -> 2      float("5000.50") -> 5000.5      str(2) -> "2"
# NO NOSSO CÓDIGO:
#   numero = float(texto)            -> transforma o salário digitado em número
#   return int(texto)                -> transforma a qtd de dependentes em inteiro
#   str(self.__dependentes) + " dep" -> transforma o número em texto pra juntar
#   OBS: o CPF fica como str (texto) de propósito, porque não fazemos
#   conta com ele e ele pode começar com zero.
# ---------------------------------------------------------------------
texto = "5000.50"
salario = float(texto)
print("float ->", salario + 100)          # 5100.5 (agora dá pra somar)
print("int   ->", int("2") + 1)            # 3
print("str   ->", str(2) + " dependentes")  # "2 dependentes"


# ---------------------------------------------------------------------
# input()
# NA PRÁTICA: mostra uma mensagem, PARA o programa e espera o usuário
#   digitar e apertar ENTER. O que ele digitou volta SEMPRE como texto
#   (str), mesmo se digitar número. Por isso depois precisa converter.
# NO NOSSO CÓDIGO:
#   opcao = input(" Escolha uma opcao: ").strip()
#   texto = input(mensagem).strip()   (dentro do ler_numero)
# (não tem exemplo rodando aqui porque ia travar esperando digitar)
# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
# try / except e ValueError
# NA PRÁTICA: "tenta fazer isso, se der erro faz aquilo".
#   try    -> bloco que PODE dar erro
#   except -> o que fazer SE der erro (em vez do programa fechar)
#   ValueError é o nome do erro que acontece quando o valor é inválido,
#   tipo tentar float("abc"). Não dá pra transformar "abc" em número.
# NO NOSSO CÓDIGO (ler_numero):
#   try:
#       numero = float(texto)
#       ...
#   except ValueError:
#       print("Valor invalido! Digite so numeros.")
#   -> se o usuário digitar letra no salário, o programa avisa e pede
#      de novo, em vez de quebrar.
# ---------------------------------------------------------------------
try:
    numero = float("abc")
except ValueError:
    print("try/except -> deu ValueError, mas o programa continuou")


# ---------------------------------------------------------------------
# while (laço de repetição)
# NA PRÁTICA: repete o bloco ENQUANTO a condição for verdadeira.
#   Quando a condição fica falsa, sai do laço.
#   while True = repete pra sempre, só sai com return (ou break).
# NO NOSSO CÓDIGO:
#   while opcao != "4":      -> o menu fica repetindo até escolher Sair
#   while len(cpf) != 11 or not cpf.isdigit():  -> pede o CPF de novo
#                                                  até ficar certo
# ---------------------------------------------------------------------
contador = 1
while contador <= 3:
    print("while -> volta", contador)
    contador = contador + 1


# ---------------------------------------------------------------------
# if / elif / else (estrutura de decisão)
# NA PRÁTICA: escolhe qual caminho o programa segue.
#   if   -> "se" (testa a primeira condição)
#   elif -> "senão, se" (só testa se as de cima foram falsas)
#   else -> "senão" (nenhuma das de cima deu certo)
#   Só UM dos blocos é executado.
# NO NOSSO CÓDIGO:
#   o menu:  if opcao == "1": ... elif opcao == "2": ... else: Opcao invalida
#   o IRRF:  if base <= 2428.80: isento  elif base <= 2826.65: 7,5% ...
# ---------------------------------------------------------------------
base = 3000.00
if base <= 2428.80:
    faixa = "isento"
elif base <= 2826.65:
    faixa = "7,5%"
elif base <= 3751.05:
    faixa = "15%"
else:
    faixa = "faixa maior"
print("if/elif/else -> base 3000 cai na faixa de", faixa)


# ---------------------------------------------------------------------
# return
# NA PRÁTICA: é a "resposta" da função. Devolve um valor para quem
#   chamou e ENCERRA a função na hora (o que vem depois não roda).
# NO NOSSO CÓDIGO:
#   def calcular_fgts(self):
#       return round(self.__salario_base * self.get_percentual_fgts(), 2)
#   -> a folha chama calcular_fgts() e recebe o valor de volta
# ---------------------------------------------------------------------
def calcular_vt(salario):
    return salario * 0.06

print("return ->", calcular_vt(5000))  # 300.0


# ---------------------------------------------------------------------
# print()
# NA PRÁTICA: mostra coisas na tela. Pode mostrar várias separadas
#   por vírgula (ele coloca espaço entre elas).
#   print() vazio pula uma linha.  "=" * 10 repete o "=" 10 vezes.
# NO NOSSO CÓDIGO:
#   print("=" * LARGURA)   -> as linhas de ===== do holerite
#   print(" Colaboradores cadastrados:", len(colaboradores))
# ---------------------------------------------------------------------
print("print ->", "texto", 123, "-" * 10)


# ---------------------------------------------------------------------
# f-strings  (f"...")
# NA PRÁTICA: texto com um "f" antes das aspas. Dentro dele, o que vai
#   entre { } é trocado pelo valor da variável. Também dá pra formatar:
#   {valor:.2f}   -> 2 casas decimais
#   {valor:,.2f}  -> 2 casas e vírgula separando milhar (padrão americano)
#   {texto:<20}   -> alinha na esquerda ocupando 20 espaços
#   {texto:>20}   -> alinha na direita
#   {texto:^20}   -> centraliza
# NO NOSSO CÓDIGO:
#   texto = f"{valor:,.2f}"      -> 10000.5 vira "10,000.50" (depois o
#                                   replace arruma pro padrão BR)
#   print(f"{EMPRESA:^{LARGURA}}") -> nome da empresa centralizado
# ---------------------------------------------------------------------
nome = "Ana"
valor = 10000.5
print(f"f-string -> Olá {nome}, valor {valor:,.2f}")
print(f"f-string -> [{'esquerda':<12}] [{'direita':>12}] [{'meio':^12}]")


# ---------------------------------------------------------------------
# for (laço que percorre uma lista)
# NA PRÁTICA: passa por CADA item de uma lista, um de cada vez.
#   A variável do for (ex: colaborador) vira o item da vez.
#   Diferente do while: o for já sabe quando parar (acabou a lista).
# NO NOSSO CÓDIGO (emitir_folha):
#   for colaborador in lista:
#       liquido = colaborador.calcular_salario_liquido()
#   -> gera o holerite de cada colaborador cadastrado
#
#   CPF ÚNICO (cpf_ja_cadastrado) também usa for:
#   for colaborador in lista:
#       if colaborador.get_cpf() == cpf:
#           return True      -> achou repetido, para tudo e cancela
#   return False             -> passou por todos e não achou
# ---------------------------------------------------------------------
nomes = ["Ana", "Lucas", "Bia"]
for pessoa in nomes:
    print("for -> holerite de", pessoa)

cpfs_cadastrados = ["12345678901", "55566677788"]
cpf_novo = "12345678901"
repetido = False
for cpf_da_vez in cpfs_cadastrados:
    if cpf_da_vez == cpf_novo:
        repetido = True
print("for (cpf unico) -> cpf ja existe?", repetido)


# #####################################################################
# PARTE 2 - STRINGS E LISTAS
# #####################################################################
print("\n--- PARTE 2: STRINGS E LISTAS ---")


# ---------------------------------------------------------------------
# .strip()
# NA PRÁTICA: tira os espaços do COMEÇO e do FIM do texto.
#   "  Ana  ".strip() -> "Ana"
#   Serve pra quando o usuário digita um espaço sem querer.
# NO NOSSO CÓDIGO:
#   nome = input("Nome: ").strip()
#   -> se digitar só espaços, vira "" (vazio) e o while pede de novo
# ---------------------------------------------------------------------
print("strip ->", "[" + "   Ana Souza  ".strip() + "]")


# ---------------------------------------------------------------------
# .replace(velho, novo)
# NA PRÁTICA: troca um pedaço do texto por outro. Devolve um texto
#   NOVO (o original não muda, por isso guarda de volta na variável).
# NO NOSSO CÓDIGO:
#   texto = texto.replace(",", ".")  -> aceita "5000,50" no input
#   na formatar_valor, 3 replaces seguidos:
#     "10,000.50" -> troca "," por "#" -> "10#000.50"
#                 -> troca "." por "," -> "10#000,50"
#                 -> troca "#" por "." -> "10.000,50"
#   o "#" é só um lugar temporário pra vírgula não se misturar com o ponto
# ---------------------------------------------------------------------
texto = "10,000.50"
texto = texto.replace(",", "#")
texto = texto.replace(".", ",")
texto = texto.replace("#", ".")
print("replace -> R$", texto)


# ---------------------------------------------------------------------
# .isdigit()
# NA PRÁTICA: responde True se o texto tiver SÓ números (0 a 9), e
#   False se tiver qualquer outra coisa (letra, ponto, traço, espaço).
# NO NOSSO CÓDIGO:
#   while len(cpf) != 11 or not cpf.isdigit():   -> CPF só com números
#   if texto.isdigit():                          -> dependentes inteiros
# ---------------------------------------------------------------------
print("isdigit ->", "12345678901".isdigit(), "/", "123.456.789-01".isdigit())


# ---------------------------------------------------------------------
# len()
# NA PRÁTICA: conta o tamanho. Num texto conta os caracteres, numa
#   lista conta quantos itens tem.
# NO NOSSO CÓDIGO:
#   len(cpf) != 11          -> CPF precisa ter 11 dígitos
#   if len(lista) == 0:     -> lista vazia = ninguém cadastrado
#   len(colaboradores)      -> mostra quantos tem no menu
# ---------------------------------------------------------------------
print("len ->", len("12345678901"), "caracteres /", len(["Ana", "Bia"]), "itens")


# ---------------------------------------------------------------------
# Fatiamento de strings  texto[inicio:fim]
# NA PRÁTICA: pega um pedaço do texto. A contagem começa no ZERO.
#   O início ENTRA e o fim NÃO entra.
#   cpf = "12345678901"
#   posições: 0 1 2 3 4 5 6 7 8 9 10
#   cpf[0:3] -> "123"  (posições 0, 1 e 2)
#   cpf[3:6] -> "456"
#   cpf[6:9] -> "789"
#   cpf[9:11] -> "01"
# NO NOSSO CÓDIGO (formatar_cpf):
#   return cpf[0:3] + "." + cpf[3:6] + "." + cpf[6:9] + "-" + cpf[9:11]
#   -> junta os pedaços com ponto e traço: 123.456.789-01
# ---------------------------------------------------------------------
cpf = "12345678901"
print("fatiamento ->", cpf[0:3] + "." + cpf[3:6] + "." + cpf[6:9] + "-" + cpf[9:11])


# ---------------------------------------------------------------------
# Lista vazia  []  e  .append()
# NA PRÁTICA: lista é uma variável que guarda VÁRIOS valores em ordem.
#   [] cria uma lista vazia. .append(item) coloca um item no FINAL.
#   A lista cresce sozinha, não precisa dizer o tamanho antes.
#   Ela fica na memória RAM: fechou o programa, apagou.
# NO NOSSO CÓDIGO:
#   colaboradores = []             -> começa sem ninguém
#   lista.append(colaborador)      -> cada cadastro entra na lista
#   OBS: a lista guarda OBJETOS (CLT, Aprendiz, Estagiário e PJ juntos)
# ---------------------------------------------------------------------
cadastrados = []
cadastrados.append("Ana")
cadastrados.append("Lucas")
print("lista/append ->", cadastrados, "- total:", len(cadastrados))


# ---------------------------------------------------------------------
# Códigos de cor ANSI
# NA PRÁTICA: são "códigos secretos" dentro do texto que o terminal
#   entende como ordem de pintar, e não como letra.
#   "\033["  -> começo do código (\033 é o caractere ESC)
#   "1;31m"  -> 1 = negrito/brilhante, 31 = vermelho (32 verde, 33 amarelo)
#   "\033[0m" -> RESET, volta a cor normal. Se esquecer o reset, todo o
#               resto da tela fica vermelho!
#   Funciona no terminal do VS Code e no Google Colab. Se a saída for
#   jogada num arquivo de texto, aparece o código cru tipo [1;31m.
# NO NOSSO CÓDIGO:
#   VERMELHO = "\033[1;31m"
#   RESET = "\033[0m"
#   print(VERMELHO + "=" * LARGURA + RESET)
#   -> linha vermelha separando o holerite de uma pessoa da próxima
# ---------------------------------------------------------------------
VERMELHO = "\033[1;31m"
RESET = "\033[0m"
print("ANSI ->", VERMELHO + "esta parte sai vermelha" + RESET, "e esta volta ao normal")


# #####################################################################
# PARTE 3 - ORIENTAÇÃO A OBJETOS (POO)
# #####################################################################
print("\n--- PARTE 3: ORIENTACAO A OBJETOS ---")


# ---------------------------------------------------------------------
# class  (classe) e objeto
# NA PRÁTICA: a classe é o MOLDE, o objeto é o que sai do molde.
#   Ex: a classe ColaboradorCLT diz que todo CLT tem nome, cpf,
#   salário... e sabe calcular INSS, IRRF... Cada pessoa cadastrada
#   é um OBJETO diferente feito com esse molde.
#   Criar um objeto = INSTANCIAR. Faz chamando o nome da classe:
#   ColaboradorCLT("Ana", "12345678901", 5000, 2, True)
# NO NOSSO CÓDIGO:
#   class Colaborador:                      -> a classe pai
#   colaborador = ColaboradorCLT(nome, cpf, salario, dependentes, vale_transporte)
#                                           -> instancia (cria) o objeto
# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
# __init__  (construtor)
# NA PRÁTICA: método especial que roda SOZINHO na hora que o objeto é
#   criado. Serve pra guardar os valores iniciais (nome, cpf...).
#   São 2 underlines antes e 2 depois: __init__
# NO NOSSO CÓDIGO:
#   def __init__(self, nome, cpf):
#       self.__nome = nome
#       self.__cpf = cpf
# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
# self
# NA PRÁTICA: significa "o próprio objeto", "eu mesmo".
#   Como a mesma classe gera vários objetos (Ana, Lucas, Bia...), o
#   self diz DE QUAL objeto estamos falando. self.__nome = o nome
#   DESTE objeto. Todo método da classe recebe o self como primeiro
#   parâmetro, mas na hora de chamar o Python passa ele sozinho:
#   ana.get_nome()  -> por dentro vira get_nome(ana)
# NO NOSSO CÓDIGO:
#   def get_nome(self):
#       return self.__nome
# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
# Atributos privados  (__ dois underlines) -> ENCAPSULAMENTO
# NA PRÁTICA: atributo é uma característica do objeto (nome, salário).
#   Com __ na frente ele fica PRIVADO: de fora da classe não dá pra
#   acessar direto (dá erro). Isso é o ENCAPSULAMENTO: protege os
#   dados, pra ninguém colocar um salário negativo, por exemplo.
# NO NOSSO CÓDIGO:
#   self.__salario_base = salario_base
#   self.__dependentes = dependentes
# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
# Getters e Setters (métodos de acesso)
# NA PRÁTICA: como o atributo é privado, a gente cria "portas" pra
#   mexer nele:
#   GETTER (get_) -> só LÊ e devolve o valor
#   SETTER (set_) -> ALTERA o valor, mas antes confere se é válido
# NO NOSSO CÓDIGO:
#   def get_salario_base(self):
#       return self.__salario_base
#   def set_salario_base(self, salario_base):
#       if salario_base > 0:              -> não aceita salário negativo
#           self.__salario_base = salario_base
# ---------------------------------------------------------------------
class ExemploColaborador:
    def __init__(self, nome, salario):
        self.__nome = nome          # privado
        self.__salario = salario    # privado

    def get_salario(self):          # getter
        return self.__salario

    def set_salario(self, salario):  # setter com validação
        if salario > 0:
            self.__salario = salario

    def get_nome(self):
        return self.__nome


ana = ExemploColaborador("Ana", 5000)    # instanciando o objeto
ana.set_salario(-100)                    # setter recusa (negativo)
print("setter -> salario continua", ana.get_salario())

try:
    print(ana.__salario)                 # acesso direto dá erro
except AttributeError:
    print("privado -> nao da pra acessar ana.__salario de fora da classe")


# ---------------------------------------------------------------------
# HERANÇA
# NA PRÁTICA: a classe FILHA aproveita tudo que a classe PAI tem e só
#   acrescenta (ou muda) o que é dela. Lê-se "um CLT É UM Colaborador".
#   No Python a classe pai vai entre parênteses: class Filha(Pai):
#   super().__init__(...) chama o construtor da pai, pra ela cuidar
#   do nome e do cpf e a filha não repetir esse código.
# NO NOSSO CÓDIGO:
#   class ColaboradorCLT(Colaborador):
#       def __init__(self, nome, cpf, salario_base, dependentes, vale_transporte):
#           super().__init__(nome, cpf)     -> a pai guarda nome e cpf
#           self.__salario_base = salario_base
#   -> o CLT ganha get_nome() e get_cpf() da pai sem escrever de novo
#
#   class ColaboradorAprendiz(ColaboradorCLT):
#   -> o aprendiz herda do CLT (que herda do Colaborador). Ele usa os
#      mesmos cálculos de INSS e IRRF e só muda: tipo, jornada e FGTS 2%
#
#   ÁRVORE DE HERANÇA DO PROJETO (5 vínculos):
#   Colaborador (pai)
#    |-- ColaboradorCLT
#    |     |-- ColaboradorAprendiz   (filho do CLT, "neto" do Colaborador)
#    |-- ColaboradorEstagiario
#    |-- ColaboradorPJ
#    |-- ColaboradorDiretor          (CEO / C-Level)
# ---------------------------------------------------------------------
class ExemploCLT(ExemploColaborador):    # herda da classe de cima
    def get_tipo(self):
        return "CLT"


bruno = ExemploCLT("Bruno", 3000)
print("heranca ->", bruno.get_nome(), "usou get_nome() que veio da classe pai")


# ---------------------------------------------------------------------
# POLIMORFISMO (e sobrescrita de método)
# NA PRÁTICA: "muitas formas". Várias classes têm um método com o
#   MESMO NOME, mas cada uma faz do seu jeito. Isso é SOBRESCREVER
#   (a filha reescreve o método que veio da pai).
#   Aí dá pra tratar todo mundo igual: chamo o mesmo método e cada
#   objeto responde com a sua regra, sem precisar de if pra perguntar
#   "é CLT ou PJ?".
# NO NOSSO CÓDIGO:
#   a classe pai tem:  def calcular_salario_liquido(self): return 0.0
#   CLT sobrescreve:   salário - INSS - IRRF - VT
#   Estagiário:        bolsa - IRRF
#   PJ:                horas x valor + bônus + ajuda - 6% da nota
#   Diretor:           pró-labore + bônus PLR - IRRF (sem INSS e FGTS)
#   e na folha:
#   for colaborador in lista:
#       liquido = colaborador.calcular_salario_liquido()
#       colaborador.mostrar_itens()
#   -> a MESMA linha calcula certo pra qualquer tipo de vínculo
# ---------------------------------------------------------------------
class ExemploPessoa:
    def calcular_liquido(self):
        return 0.0


class ExemploPessoaCLT(ExemploPessoa):
    def calcular_liquido(self):        # sobrescreve
        return 5000 - 509.59           # salário - INSS (simplificado)


class ExemploPessoaPJ(ExemploPessoa):
    def calcular_liquido(self):        # sobrescreve
        return 8000 - 8000 * 0.06      # nota - 6%


folha = [ExemploPessoaCLT(), ExemploPessoaPJ()]
for pessoa in folha:
    print(f"polimorfismo -> mesmo metodo, resultado: {pessoa.calcular_liquido():.2f}")


# #####################################################################
# EXTRAS (aparecem no código e podem cair na pergunta)
# #####################################################################
print("\n--- EXTRAS ---")

# import os / import sys
#   traz ferramentas prontas do Python. os.system("cls") limpa a tela
#   no Windows, e sys.modules mostra quais módulos estão carregados
#   (é assim que o limpar_tela() descobre se está no Google Colab).

# True e False (booleano)
#   tipo que só tem dois valores: verdadeiro ou falso.
#   ler_sim_nao() devolve True se a pessoa digitou S.
#   vale_transporte = True -> desconta os 6%

# round(valor, 2)
#   arredonda pra 2 casas decimais (centavos).
print("round ->", round(249.5367, 2))

# .upper()
#   deixa o texto em maiúsculo: "s" vira "S" (no ler_sim_nao)
print("upper ->", "s".upper())

# Constantes (nomes em MAIÚSCULO)
#   VALOR_VA = 740.00 e VALOR_VR = 2000.00 ficam no topo do arquivo.
#   Mudou o valor do benefício? Muda só ali e vale pro sistema todo.


# #####################################################################
# COLA RÁPIDA (pra revisar antes da prova)
# #####################################################################
#   class ............ molde dos objetos
#   objeto ........... o que é criado a partir da classe (instância)
#   __init__ ......... construtor, roda quando cria o objeto
#   self ............. o próprio objeto
#   __atributo ....... privado (encapsulamento)
#   get_ / set_ ...... ler / alterar atributo privado (com validação)
#   class Filha(Pai) . herança
#   super() .......... chama a classe pai
#   mesmo método,
#   regra diferente .. polimorfismo (sobrescrita)
#   [] / .append() ... lista na memória / adiciona no final
#   for + if ......... varrer a lista (ex: achar CPF repetido)
#   \033[1;31m ....... código ANSI: pinta de vermelho (\033[0m volta)
#   try/except ....... trata erro sem fechar o programa
#   while / for ...... repete (enquanto / pra cada item)
#   if/elif/else ..... decide o caminho
#   return ........... devolve o resultado da função
# #####################################################################

print("\n" + "=" * 60)
print("Fim do resumo. Bons estudos!")
print("=" * 60)
