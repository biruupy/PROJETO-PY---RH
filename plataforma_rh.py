# Vanguard Solutions - Sistema de Folha de Pagamento (A3)
# Cadastro de colaboradores CLT, Jovem Aprendiz, Estagiario, PJ e Diretoria
# Os dados ficam so na memoria (na lista), quando fecha o programa eles somem
# Funciona no terminal do VS Code e no Google Colab

import os
import sys

EMPRESA = "VANGUARD SOLUTIONS"
LARGURA = 72  # largura das linhas do holerite

# Codigos de cor ANSI (o terminal entende e pinta o texto)
VERMELHO = "\033[1;31m"  # 1 = negrito/brilhante, 31 = vermelho
RESET = "\033[0m"  # volta pra cor normal

# Pacote iFood Beneficios (padrao da empresa)
VALOR_VA = 740.00  # vale alimentacao
VALOR_VR = 2000.00  # vale refeicao

DEDUCAO_DEPENDENTE = 189.59  # cada dependente abate isso da base do IR


# Limpa a tela (no Colab e no terminal o jeito e diferente)
def limpar_tela():
    if "google.colab" in sys.modules:  # se esse modulo ta carregado, e Colab
        from google.colab import output
        output.clear()
    elif os.name == "nt":
        os.system("cls")  # Windows
    else:
        os.system("clear")  # Linux / Mac


# Segura a tela ate o usuario apertar ENTER (senao limpa antes de ler)
def pausar():
    input("\nPressione ENTER para voltar ao menu...")


# Cabecalho padrao da empresa em todas as telas
def imprimir_cabecalho(titulo):
    print("=" * LARGURA)
    print(f"{EMPRESA:^{LARGURA}}")  # ^ centraliza o texto
    print(f"{'Sistema Corporativo de Recursos Humanos':^{LARGURA}}")
    print("-" * LARGURA)
    print(f"{titulo:^{LARGURA}}")
    print("=" * LARGURA)


# Formata numero no padrao brasileiro: 10000.5 -> 10.000,50
def formatar_valor(valor):
    texto = f"{valor:,.2f}"  # padrao americano: 10,000.50
    texto = texto.replace(",", "#")  # guarda a virgula num simbolo temporario
    texto = texto.replace(".", ",")  # ponto vira virgula
    texto = texto.replace("#", ".")  # simbolo vira ponto
    return texto


# Mesma coisa mas com cifrao: R$ 10.000,50
def formatar_moeda(valor):
    return "R$ " + formatar_valor(valor)


# Porcentagem: 0.08 -> 8,00%
def formatar_percentual(valor):
    return formatar_valor(valor * 100) + "%"


# Coloca pontos e traco no cpf: 12345678901 -> 123.456.789-01
def formatar_cpf(cpf):
    return cpf[0:3] + "." + cpf[3:6] + "." + cpf[6:9] + "-" + cpf[9:11]


# Uma linha do holerite: codigo, descricao, referencia, provento e desconto
# se o valor for zero deixa a coluna em branco (igual holerite de verdade)
def imprimir_item(codigo, descricao, referencia, provento, desconto):
    texto_provento = ""
    if provento > 0:
        texto_provento = formatar_valor(provento)
    texto_desconto = ""
    if desconto > 0:
        texto_desconto = formatar_valor(desconto)
    print(f" {codigo:<6}{descricao:<28}{referencia:>9}{texto_provento:>14}{texto_desconto:>14}")


# Linha das bases e encargos (so informativo)
def imprimir_base(codigo, descricao, valor):
    print(f" {codigo:<6}{descricao:<40}{valor:>25}")


# Linha simples: descricao na esquerda e valor na direita
def imprimir_linha(descricao, valor):
    print(f" {descricao:<45}{valor:>26}")


# Tabela progressiva do INSS (2025)
# cada faixa paga so a sua parte, os numeros fixos sao as faixas de baixo cheias
def calcular_inss_tabela(salario):
    if salario <= 1518.00:
        inss = salario * 0.075
    elif salario <= 2793.88:
        inss = 113.85 + (salario - 1518.00) * 0.09  # 113,85 = faixa 1 cheia
    elif salario <= 4190.83:
        inss = 228.68 + (salario - 2793.88) * 0.12  # faixas 1 e 2 cheias
    elif salario <= 8157.41:
        inss = 396.31 + (salario - 4190.83) * 0.14  # faixas 1, 2 e 3 cheias
    else:
        inss = 951.63  # teto, ninguem paga mais que isso
    return round(inss, 2)


# Tabela progressiva do IRRF (aliquota e parcela a deduzir)
def calcular_irrf_tabela(base):
    if base <= 2428.80:
        imposto = 0.0  # isento
    elif base <= 2826.65:
        imposto = base * 0.075 - 182.16
    elif base <= 3751.05:
        imposto = base * 0.15 - 394.16
    elif base <= 4664.68:
        imposto = base * 0.225 - 675.49
    else:
        imposto = base * 0.275 - 908.73
    return round(imposto, 2)


# Classe pai
class Colaborador:

    # Construtor
    def __init__(self, nome, cpf):
        self.__nome = nome  # atributo privado (dois underlines)
        self.__cpf = cpf

    # Getters e setters
    def get_nome(self):
        return self.__nome

    def set_nome(self, nome):
        if nome != "":  # nao deixa salvar nome vazio
            self.__nome = nome

    def get_cpf(self):
        return self.__cpf

    def set_cpf(self, cpf):
        if len(cpf) == 11:  # cpf tem que ter 11 numeros
            self.__cpf = cpf

    # Metodos que as classes filhas vao sobrescrever (polimorfismo)
    def calcular_salario_bruto(self):
        return 0.0

    def calcular_salario_liquido(self):
        return 0.0

    def get_tipo(self):
        return "Colaborador"

    def get_jornada(self):
        return "-"

    # FGTS e encargo da empresa, nao sai do salario (so CLT e aprendiz tem)
    def calcular_fgts(self):
        return 0.0

    # Saldo do cartao iFood (PJ nao tem)
    def get_saldo_beneficios(self):
        return 0.0

    # Linhas do holerite (proventos e descontos)
    def mostrar_itens(self):
        print(" Sem lancamentos.")

    # Bases de calculo e encargos
    def mostrar_bases(self):
        print(" Sem bases de calculo.")

    # Igual pra todo mundo, entao fica na classe pai (heranca)
    def calcular_total_descontos(self):
        return self.calcular_salario_bruto() - self.calcular_salario_liquido()


# Classe filha CLT comum, herda de Colaborador
class ColaboradorCLT(Colaborador):

    def __init__(self, nome, cpf, salario_base, dependentes, vale_transporte):
        super().__init__(nome, cpf)  # chama o construtor da classe pai
        self.__salario_base = salario_base
        self.__dependentes = dependentes  # numero inteiro
        self.__vale_transporte = vale_transporte  # True ou False

    def get_salario_base(self):
        return self.__salario_base

    def set_salario_base(self, salario_base):
        if salario_base > 0:
            self.__salario_base = salario_base

    def get_dependentes(self):
        return self.__dependentes

    def set_dependentes(self, dependentes):
        if dependentes >= 0:  # pode ter zero dependentes
            self.__dependentes = dependentes

    def get_vale_transporte(self):
        return self.__vale_transporte

    def set_vale_transporte(self, vale_transporte):
        self.__vale_transporte = vale_transporte

    def calcular_inss(self):
        return calcular_inss_tabela(self.__salario_base)

    def calcular_deducao_dependentes(self):
        return self.__dependentes * DEDUCAO_DEPENDENTE

    # Base do IR = salario - INSS - dependentes
    def calcular_base_irrf(self):
        base = self.__salario_base - self.calcular_inss() - self.calcular_deducao_dependentes()
        if base < 0:
            base = 0.0  # base nao pode ficar negativa
        return base

    def calcular_irrf(self):
        return calcular_irrf_tabela(self.calcular_base_irrf())

    # Vale transporte: desconta 6% do salario se optou
    def calcular_vale_transporte(self):
        if self.__vale_transporte:
            return round(self.__salario_base * 0.06, 2)
        else:
            return 0.0

    # CLT comum = 8% de FGTS (o aprendiz sobrescreve isso)
    def get_percentual_fgts(self):
        return 0.08

    def calcular_fgts(self):
        return round(self.__salario_base * self.get_percentual_fgts(), 2)

    # Recebe o pacote inteiro, sem desconto
    def get_saldo_beneficios(self):
        return VALOR_VA + VALOR_VR

    def calcular_salario_bruto(self):
        return self.__salario_base

    # Regra do CLT: salario - INSS - IRRF - VT
    def calcular_salario_liquido(self):
        liquido = self.__salario_base
        liquido = liquido - self.calcular_inss()
        liquido = liquido - self.calcular_irrf()
        liquido = liquido - self.calcular_vale_transporte()
        return liquido

    def get_tipo(self):
        return "CLT"

    def get_jornada(self):
        return "44h/sem"

    def mostrar_itens(self):
        imprimir_item("0010", "Salario Base", self.get_jornada(), self.__salario_base, 0)

        inss = self.calcular_inss()
        aliquota_inss = inss / self.__salario_base  # aliquota efetiva
        imprimir_item("5560", "INSS", formatar_percentual(aliquota_inss), 0, inss)

        irrf = self.calcular_irrf()
        if irrf > 0:
            imprimir_item("5600", "IRRF", str(self.__dependentes) + " dep", 0, irrf)
        else:
            imprimir_item("5600", "IRRF", "isento", 0, 0)

        if self.__vale_transporte:
            imprimir_item("5620", "Vale Transporte", "6,00%", 0, self.calcular_vale_transporte())

    def mostrar_bases(self):
        texto_dep = "Deducao dependentes (" + str(self.__dependentes) + " x 189,59)"
        texto_fgts = "FGTS do mes " + formatar_percentual(self.get_percentual_fgts()) + " (pago p/ empresa)"
        imprimir_base("5502", "Base INSS", formatar_moeda(self.__salario_base))
        imprimir_base("5505", texto_dep, formatar_moeda(self.calcular_deducao_dependentes()))
        imprimir_base("5501", "Base IR (salario - INSS - dependentes)", formatar_moeda(self.calcular_base_irrf()))
        imprimir_base("1340", "Base FGTS", formatar_moeda(self.__salario_base))
        imprimir_base("1330", texto_fgts, formatar_moeda(self.calcular_fgts()))


# Jovem Aprendiz e um CLT especial, entao herda do CLT
# usa o mesmo construtor e os mesmos calculos, so muda o que e diferente
class ColaboradorAprendiz(ColaboradorCLT):

    def get_tipo(self):
        return "JOVEM APRENDIZ"

    def get_jornada(self):
        return "30h/sem"

    # Aprendiz e so 2% de FGTS
    def get_percentual_fgts(self):
        return 0.02


# Classe filha Estagiario, herda de Colaborador
# nao e CLT: nao tem INSS nem FGTS
class ColaboradorEstagiario(Colaborador):

    def __init__(self, nome, cpf, bolsa_auxilio):
        super().__init__(nome, cpf)
        self.__bolsa_auxilio = bolsa_auxilio

    def get_bolsa_auxilio(self):
        return self.__bolsa_auxilio

    def set_bolsa_auxilio(self, bolsa):
        if bolsa > 0:
            self.__bolsa_auxilio = bolsa

    # Bolsa de estagio paga IR se passar da faixa de isencao
    def calcular_irrf(self):
        return calcular_irrf_tabela(self.__bolsa_auxilio)

    def get_saldo_beneficios(self):
        return VALOR_VA + VALOR_VR

    def calcular_salario_bruto(self):
        return self.__bolsa_auxilio

    def calcular_salario_liquido(self):
        return self.__bolsa_auxilio - self.calcular_irrf()

    def get_tipo(self):
        return "ESTAGIARIO"

    def get_jornada(self):
        return "30h/sem"

    def mostrar_itens(self):
        imprimir_item("0015", "Bolsa-Auxilio", self.get_jornada(), self.__bolsa_auxilio, 0)
        imprimir_item("5560", "INSS", "isento", 0, 0)
        irrf = self.calcular_irrf()
        if irrf > 0:
            imprimir_item("5600", "IRRF", "tabela", 0, irrf)
        else:
            imprimir_item("5600", "IRRF", "isento", 0, 0)

    def mostrar_bases(self):
        imprimir_base("5502", "Base INSS", "isento (sem vinculo CLT)")
        imprimir_base("5501", "Base IR", formatar_moeda(self.__bolsa_auxilio))
        imprimir_base("1330", "FGTS", "isento (sem vinculo CLT)")


# Classe filha PJ, herda de Colaborador
class ColaboradorPJ(Colaborador):

    def __init__(self, nome, cpf, horas_trabalhadas, valor_hora, adicional_bonus, ajuda_custo):
        super().__init__(nome, cpf)
        self.__horas_trabalhadas = horas_trabalhadas
        self.__valor_hora = valor_hora
        self.__adicional_bonus = adicional_bonus  # valor em R$
        self.__ajuda_custo = ajuda_custo  # True se negociou ajuda de beneficios

    def get_horas_trabalhadas(self):
        return self.__horas_trabalhadas

    def set_horas_trabalhadas(self, horas):
        if horas > 0:
            self.__horas_trabalhadas = horas

    def get_valor_hora(self):
        return self.__valor_hora

    def set_valor_hora(self, valor):
        if valor > 0:
            self.__valor_hora = valor

    def get_adicional_bonus(self):
        return self.__adicional_bonus

    def set_adicional_bonus(self, bonus):
        if bonus >= 0:  # bonus pode ser zero
            self.__adicional_bonus = bonus

    def get_ajuda_custo(self):
        return self.__ajuda_custo

    def set_ajuda_custo(self, ajuda_custo):
        self.__ajuda_custo = ajuda_custo

    def calcular_valor_horas(self):
        return self.__horas_trabalhadas * self.__valor_hora

    # Ajuda de custo = pacote inteiro (VA + VR), sem desconto
    def calcular_ajuda_custo(self):
        if self.__ajuda_custo:
            return VALOR_VA + VALOR_VR
        else:
            return 0.0

    # O que entra na nota fiscal (horas + bonus, a ajuda e isenta)
    def calcular_base_nota(self):
        return self.calcular_valor_horas() + self.__adicional_bonus

    def calcular_salario_bruto(self):
        return self.calcular_base_nota() + self.calcular_ajuda_custo()

    # 6% da nota fiscal (nao pega a ajuda de custo)
    def calcular_taxa_nota(self):
        return round(self.calcular_base_nota() * 0.06, 2)

    def calcular_salario_liquido(self):
        return self.calcular_salario_bruto() - self.calcular_taxa_nota()

    def get_tipo(self):
        return "PJ"

    def get_jornada(self):
        return "por hora"

    def mostrar_itens(self):
        horas = f"{self.__horas_trabalhadas:.1f}".replace(".", ",") + "h"  # 160.0 -> 160,0h
        imprimir_item("0020", "Honorarios (horas x valor)", horas, self.calcular_valor_horas(), 0)
        if self.__adicional_bonus > 0:
            imprimir_item("0025", "Bonus / Adicional", "", self.__adicional_bonus, 0)
        if self.__ajuda_custo:
            imprimir_item("0030", "Ajuda Custo Beneficios", "isenta", self.calcular_ajuda_custo(), 0)
        imprimir_item("5700", "Retencao Nota Fiscal", "6,00%", 0, self.calcular_taxa_nota())

    def mostrar_bases(self):
        imprimir_base("0021", "Valor da hora", formatar_moeda(self.__valor_hora))
        imprimir_base("5710", "Base Nota Fiscal (horas + bonus)", formatar_moeda(self.calcular_base_nota()))
        imprimir_base("1330", "INSS / FGTS", "nao se aplica (PJ)")


# Classe filha Diretor (CEO / C-Level), herda de Colaborador
# diretor estatutario: recebe pro-labore e so paga IRRF (sem INSS e sem FGTS)
class ColaboradorDiretor(Colaborador):

    def __init__(self, nome, cpf, pro_labore, bonus_plr, beneficios):
        super().__init__(nome, cpf)
        self.__pro_labore = pro_labore
        self.__bonus_plr = bonus_plr  # bonus de performance / PLR
        self.__beneficios = beneficios  # True se optou pelo cartao iFood

    def get_pro_labore(self):
        return self.__pro_labore

    def set_pro_labore(self, pro_labore):
        if pro_labore > 0:
            self.__pro_labore = pro_labore

    def get_bonus_plr(self):
        return self.__bonus_plr

    def set_bonus_plr(self, bonus):
        if bonus >= 0:  # pode nao ter bonus
            self.__bonus_plr = bonus

    def get_beneficios(self):
        return self.__beneficios

    def set_beneficios(self, beneficios):
        self.__beneficios = beneficios

    # IR so em cima do pro-labore (o bonus entra isento)
    def calcular_irrf(self):
        return calcular_irrf_tabela(self.__pro_labore)

    # Diretor escolhe se quer o cartao ou nao
    def get_saldo_beneficios(self):
        if self.__beneficios:
            return VALOR_VA + VALOR_VR
        else:
            return 0.0

    def calcular_salario_bruto(self):
        return self.__pro_labore + self.__bonus_plr

    def calcular_salario_liquido(self):
        return self.calcular_salario_bruto() - self.calcular_irrf()

    def get_tipo(self):
        return "DIRETOR (C-LEVEL)"

    def get_jornada(self):
        return "estatutario"

    def mostrar_itens(self):
        imprimir_item("0040", "Pro-Labore", "mensal", self.__pro_labore, 0)
        if self.__bonus_plr > 0:
            imprimir_item("0045", "Bonus Performance / PLR", "isento", self.__bonus_plr, 0)
        imprimir_item("5560", "INSS", "isento", 0, 0)
        irrf = self.calcular_irrf()
        if irrf > 0:
            imprimir_item("5600", "IRRF", "tabela", 0, irrf)
        else:
            imprimir_item("5600", "IRRF", "isento", 0, 0)

    def mostrar_bases(self):
        imprimir_base("5502", "Base INSS", "isento (estatutario)")
        imprimir_base("5501", "Base IR (so o pro-labore)", formatar_moeda(self.__pro_labore))
        imprimir_base("1330", "FGTS", "isento (estatutario)")
        if not self.__beneficios:
            imprimir_base("9000", "Cartao iFood Beneficios", "nao optou")


# Funcao para ler um numero sem o programa quebrar
# aceita_zero = True quando o valor pode ser zero (ex: bonus)
def ler_numero(mensagem, aceita_zero):
    while True:
        texto = input(mensagem).strip()  # tira espacos do comeco e do fim
        texto = texto.replace(",", ".")  # aceita virgula tambem
        try:
            numero = float(texto)  # converte para float
            if numero > 0:
                return numero
            elif numero == 0 and aceita_zero:
                return numero
            else:
                print("Valor invalido para este campo!")
        except ValueError:
            print("Valor invalido! Digite so numeros.")


# Funcao para ler numero inteiro (quantidade de dependentes)
def ler_inteiro(mensagem):
    while True:
        texto = input(mensagem).strip()
        if texto.isdigit():  # so aceita numeros inteiros positivos ou zero
            return int(texto)  # converte para int
        print("Digite um numero inteiro (ex: 0, 1, 2).")


# Funcao para pergunta de sim ou nao
def ler_sim_nao(mensagem):
    resposta = input(mensagem).strip().upper()  # .upper() deixa maiusculo (s vira S)
    while resposta != "S" and resposta != "N":
        print("Digite S para sim ou N para nao.")
        resposta = input(mensagem).strip().upper()
    return resposta == "S"  # devolve True se for S


# Funcao para ler o nome sem deixar vazio
def ler_nome():
    nome = input("Nome: ").strip()  # assim "   " vira "" e cai no while
    while nome == "":
        print("O nome nao pode ficar vazio!")
        nome = input("Nome: ").strip()
    return nome


# Funcao para ler o cpf com 11 numeros
def ler_cpf():
    cpf = input("CPF (so numeros): ").strip()
    while len(cpf) != 11 or not cpf.isdigit():
        print("CPF invalido! Digite os 11 numeros sem ponto e traco.")
        cpf = input("CPF (so numeros): ").strip()
    return cpf


# Confere se o cpf ja ta na lista (nao pode ter 2 pessoas com o mesmo cpf)
def cpf_ja_cadastrado(lista, cpf):
    for colaborador in lista:  # passa por todo mundo cadastrado
        if colaborador.get_cpf() == cpf:
            print("\nERRO: o CPF " + formatar_cpf(cpf) + " ja pertence a " + colaborador.get_nome() + "!")
            print("Cadastro cancelado, voltando ao menu principal.")
            return True
    return False  # rodou a lista toda e nao achou


# CLT comum e aprendiz pedem as mesmas coisas, so muda a classe
def cadastrar_clt(lista, eh_aprendiz):
    if eh_aprendiz:
        imprimir_cabecalho("CADASTRO DE JOVEM APRENDIZ (30h semanais)")
    else:
        imprimir_cabecalho("CADASTRO DE COLABORADOR CLT (44h semanais)")

    nome = ler_nome()
    cpf = ler_cpf()
    if cpf_ja_cadastrado(lista, cpf):
        return  # sai da funcao e volta pro menu
    salario = ler_numero("Salario base: R$ ", False)
    dependentes = ler_inteiro("Quantidade de dependentes: ")
    vale_transporte = ler_sim_nao("Simular desconto de vale transporte (6%)? (S/N): ")

    if eh_aprendiz:
        colaborador = ColaboradorAprendiz(nome, cpf, salario, dependentes, vale_transporte)  # cria o objeto
    else:
        colaborador = ColaboradorCLT(nome, cpf, salario, dependentes, vale_transporte)
    lista.append(colaborador)  # guarda na lista

    print("\n" + colaborador.get_tipo() + " cadastrado com sucesso!")
    print("Cartao iFood Beneficios liberado: " + formatar_moeda(VALOR_VA + VALOR_VR))


def cadastrar_estagiario(lista):
    imprimir_cabecalho("CADASTRO DE ESTAGIARIO (ate 30h semanais)")
    nome = ler_nome()
    cpf = ler_cpf()
    if cpf_ja_cadastrado(lista, cpf):
        return
    bolsa = ler_numero("Bolsa-auxilio: R$ ", False)

    colaborador = ColaboradorEstagiario(nome, cpf, bolsa)  # cria o objeto
    lista.append(colaborador)  # guarda na lista

    print("\nEstagiario cadastrado com sucesso!")
    print("Cartao iFood Beneficios liberado: " + formatar_moeda(VALOR_VA + VALOR_VR))


def cadastrar_pj(lista):
    imprimir_cabecalho("CADASTRO DE PRESTADOR DE SERVICO PJ")
    nome = ler_nome()
    cpf = ler_cpf()
    if cpf_ja_cadastrado(lista, cpf):
        return
    horas = ler_numero("Horas trabalhadas: ", False)
    valor_hora = ler_numero("Valor da hora: R$ ", False)
    bonus = ler_numero("Adicional / bonus (0 se nao tiver): R$ ", True)
    ajuda_custo = ler_sim_nao("Contrato tem ajuda de custo de beneficios (R$ 2.740,00)? (S/N): ")

    colaborador = ColaboradorPJ(nome, cpf, horas, valor_hora, bonus, ajuda_custo)  # cria o objeto
    lista.append(colaborador)  # guarda na lista
    print("\nPrestador PJ cadastrado com sucesso!")


def cadastrar_diretor(lista):
    imprimir_cabecalho("CADASTRO DE DIRETORIA (CEO / C-LEVEL)")
    nome = ler_nome()
    cpf = ler_cpf()
    if cpf_ja_cadastrado(lista, cpf):
        return
    pro_labore = ler_numero("Pro-labore mensal: R$ ", False)
    bonus = ler_numero("Bonus de performance / PLR (0 se nao tiver): R$ ", True)
    beneficios = ler_sim_nao("Optar pelo cartao iFood Beneficios (R$ 2.740,00)? (S/N): ")

    colaborador = ColaboradorDiretor(nome, cpf, pro_labore, bonus, beneficios)  # cria o objeto
    lista.append(colaborador)  # guarda na lista

    print("\nDiretor cadastrado com sucesso!")
    if beneficios:
        print("Cartao iFood Beneficios liberado: " + formatar_moeda(VALOR_VA + VALOR_VR))


# Opcao 1 do menu: escolhe o tipo de vinculo antes de cadastrar
def cadastrar_colaborador(lista):
    imprimir_cabecalho("CADASTRO DE COLABORADOR")
    print(" 1 - CLT Comum (44h semanais)")
    print(" 2 - Jovem Aprendiz (30h semanais)")
    print(" 3 - Estagiario (ate 30h semanais)")
    print(" 4 - Diretoria (CEO / C-Level)")
    print("-" * LARGURA)
    tipo = input(" Escolha o tipo de vinculo: ").strip()

    limpar_tela()
    if tipo == "1":
        cadastrar_clt(lista, False)
    elif tipo == "2":
        cadastrar_clt(lista, True)
    elif tipo == "3":
        cadastrar_estagiario(lista)
    elif tipo == "4":
        cadastrar_diretor(lista)
    else:
        print("Tipo de vinculo invalido!")


def emitir_folha(lista):
    imprimir_cabecalho("FOLHA DE PAGAMENTO GERAL")

    if len(lista) == 0:
        print("Nenhum colaborador cadastrado.")
        return

    total_proventos = 0.0
    total_descontos = 0.0
    total_liquido = 0.0
    total_fgts = 0.0
    total_cartoes = 0.0

    # Polimorfismo: chama os mesmos metodos e cada objeto responde do seu jeito
    for colaborador in lista:
        proventos = colaborador.calcular_salario_bruto()
        descontos = colaborador.calcular_total_descontos()
        liquido = colaborador.calcular_salario_liquido()
        fgts = colaborador.calcular_fgts()
        cartao = colaborador.get_saldo_beneficios()

        # vai somando pro resumo final
        total_proventos = total_proventos + proventos
        total_descontos = total_descontos + descontos
        total_liquido = total_liquido + liquido
        total_fgts = total_fgts + fgts
        total_cartoes = total_cartoes + cartao

        # Cabecalho do holerite
        print()
        print("=" * LARGURA)
        print(f"{EMPRESA + '  |  DEMONSTRATIVO DE PAGAMENTO':^{LARGURA}}")
        print("=" * LARGURA)
        print(f" {'Colaborador: ' + colaborador.get_nome():<45}{'CPF: ' + formatar_cpf(colaborador.get_cpf()):>26}")
        print(f" {'Vinculo: ' + colaborador.get_tipo():<45}{'Jornada: ' + colaborador.get_jornada():>26}")

        # Lancamentos
        print("-" * LARGURA)
        print(f" {'Cod':<6}{'Descricao':<28}{'Ref.':>9}{'Proventos':>14}{'Descontos':>14}")
        print("-" * LARGURA)
        colaborador.mostrar_itens()  # cada vinculo mostra os seus codigos
        print("-" * LARGURA)
        print(f" {'TOTAIS':<43}{formatar_valor(proventos):>14}{formatar_valor(descontos):>14}")
        print("=" * LARGURA)
        imprimir_linha(">>> LIQUIDO A RECEBER (conta corrente)", formatar_moeda(liquido))
        print("=" * LARGURA)

        # Bases e encargos
        print(" BASES DE CALCULO E ENCARGOS (informativo)")
        colaborador.mostrar_bases()

        # Cartao de beneficios
        if cartao > 0:
            print("-" * LARGURA)
            print(" [Cartao iFood Beneficios]")
            imprimir_base("9001", "Vale Alimentacao (VA)", formatar_moeda(VALOR_VA))
            imprimir_base("9002", "Vale Refeicao (VR)", formatar_moeda(VALOR_VR))
            imprimir_base("", "Saldo Disponivel (sem desconto em folha)", formatar_moeda(cartao))

        # Linha vermelha separando um holerite do proximo
        print(VERMELHO + "=" * LARGURA + RESET)

    # Resumo final da empresa
    print()
    print("#" * LARGURA)
    print(f"{'RESUMO GERAL DA FOLHA - ' + EMPRESA:^{LARGURA}}")
    print("#" * LARGURA)
    imprimir_linha("Colaboradores na folha", str(len(lista)))
    imprimir_linha("Total de proventos", formatar_moeda(total_proventos))
    imprimir_linha("Total de descontos", formatar_moeda(total_descontos))
    imprimir_linha("Total liquido pago em conta", formatar_moeda(total_liquido))
    imprimir_linha("Total creditado em cartoes iFood", formatar_moeda(total_cartoes))
    imprimir_linha("FGTS recolhido pela empresa (encargo)", formatar_moeda(total_fgts))
    print("#" * LARGURA)


# Programa principal
colaboradores = []  # lista que guarda os objetos na memoria
opcao = ""

while opcao != "4":
    limpar_tela()
    imprimir_cabecalho("MENU PRINCIPAL")
    print(" 1 - Cadastrar Colaborador (CLT / Aprendiz / Estagiario / Diretoria)")
    print(" 2 - Cadastrar Prestador de Servico PJ")
    print(" 3 - Emitir Folha de Pagamento Geral")
    print(" 4 - Sair")
    print("-" * LARGURA)
    print(" Colaboradores cadastrados:", len(colaboradores))
    opcao = input(" Escolha uma opcao: ").strip()

    limpar_tela()  # limpa o menu antes de mostrar a opcao escolhida

    if opcao == "1":
        cadastrar_colaborador(colaboradores)
        pausar()
    elif opcao == "2":
        cadastrar_pj(colaboradores)
        pausar()
    elif opcao == "3":
        emitir_folha(colaboradores)
        pausar()
    elif opcao == "4":
        imprimir_cabecalho("ATE LOGO!")
        print(" Sistema encerrado. Os dados da memoria foram descartados.")
    else:
        print("Opcao invalida!")
        pausar()
