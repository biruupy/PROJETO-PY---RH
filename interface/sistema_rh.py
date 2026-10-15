# Vanguard Solutions - Classes do sistema de RH
# Sao as mesmas classes do plataforma_rh.py, so que sem o menu do terminal
# Aqui o holerite vira uma LISTA de linhas (tuplas), assim a janela consegue mostrar

# Pacote iFood Beneficios (padrao da empresa)
VALOR_VA = 740.00  # vale alimentacao
VALOR_VR = 2000.00  # vale refeicao

DEDUCAO_DEPENDENTE = 189.59  # cada dependente abate isso da base do IR


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

    # Linhas do holerite: cada linha e (codigo, descricao, referencia, provento, desconto)
    def get_itens(self):
        return []

    # Bases de calculo: cada linha e (codigo, descricao, valor em texto)
    def get_bases(self):
        return []

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

    def get_itens(self):
        itens = []
        itens.append(("0010", "Salário Base", self.get_jornada(), self.__salario_base, 0))

        inss = self.calcular_inss()
        aliquota_inss = inss / self.__salario_base  # aliquota efetiva
        itens.append(("5560", "INSS", formatar_percentual(aliquota_inss), 0, inss))

        irrf = self.calcular_irrf()
        if irrf > 0:
            itens.append(("5600", "IRRF", str(self.__dependentes) + " dep", 0, irrf))
        else:
            itens.append(("5600", "IRRF", "isento", 0, 0))

        if self.__vale_transporte:
            itens.append(("5620", "Vale Transporte", "6,00%", 0, self.calcular_vale_transporte()))
        return itens

    def get_bases(self):
        texto_dep = "Dedução dependentes (" + str(self.__dependentes) + " x 189,59)"
        texto_fgts = "FGTS do mês " + formatar_percentual(self.get_percentual_fgts()) + " (pago pela empresa)"
        bases = []
        bases.append(("5502", "Base INSS", formatar_moeda(self.__salario_base)))
        bases.append(("5505", texto_dep, formatar_moeda(self.calcular_deducao_dependentes())))
        bases.append(("5501", "Base IR (salário - INSS - dependentes)", formatar_moeda(self.calcular_base_irrf())))
        bases.append(("1340", "Base FGTS", formatar_moeda(self.__salario_base)))
        bases.append(("1330", texto_fgts, formatar_moeda(self.calcular_fgts())))
        return bases


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
        return "ESTAGIÁRIO"

    def get_jornada(self):
        return "30h/sem"

    def get_itens(self):
        itens = []
        itens.append(("0015", "Bolsa-Auxílio", self.get_jornada(), self.__bolsa_auxilio, 0))
        itens.append(("5560", "INSS", "isento", 0, 0))
        irrf = self.calcular_irrf()
        if irrf > 0:
            itens.append(("5600", "IRRF", "tabela", 0, irrf))
        else:
            itens.append(("5600", "IRRF", "isento", 0, 0))
        return itens

    def get_bases(self):
        bases = []
        bases.append(("5502", "Base INSS", "isento (sem vínculo CLT)"))
        bases.append(("5501", "Base IR", formatar_moeda(self.__bolsa_auxilio)))
        bases.append(("1330", "FGTS", "isento (sem vínculo CLT)"))
        return bases


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

    def get_itens(self):
        horas = f"{self.__horas_trabalhadas:.1f}".replace(".", ",") + "h"  # 160.0 -> 160,0h
        itens = []
        itens.append(("0020", "Honorários (horas x valor)", horas, self.calcular_valor_horas(), 0))
        if self.__adicional_bonus > 0:
            itens.append(("0025", "Bônus / Adicional", "", self.__adicional_bonus, 0))
        if self.__ajuda_custo:
            itens.append(("0030", "Ajuda Custo Benefícios", "isenta", self.calcular_ajuda_custo(), 0))
        itens.append(("5700", "Retenção Nota Fiscal", "6,00%", 0, self.calcular_taxa_nota()))
        return itens

    def get_bases(self):
        bases = []
        bases.append(("0021", "Valor da hora", formatar_moeda(self.__valor_hora)))
        bases.append(("5710", "Base Nota Fiscal (horas + bônus)", formatar_moeda(self.calcular_base_nota())))
        bases.append(("1330", "INSS / FGTS", "não se aplica (PJ)"))
        return bases


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
        return "estatutário"

    def get_itens(self):
        itens = []
        itens.append(("0040", "Pró-Labore", "mensal", self.__pro_labore, 0))
        if self.__bonus_plr > 0:
            itens.append(("0045", "Bônus Performance / PLR", "isento", self.__bonus_plr, 0))
        itens.append(("5560", "INSS", "isento", 0, 0))
        irrf = self.calcular_irrf()
        if irrf > 0:
            itens.append(("5600", "IRRF", "tabela", 0, irrf))
        else:
            itens.append(("5600", "IRRF", "isento", 0, 0))
        return itens

    def get_bases(self):
        bases = []
        bases.append(("5502", "Base INSS", "isento (estatutário)"))
        bases.append(("5501", "Base IR (só o pró-labore)", formatar_moeda(self.__pro_labore)))
        bases.append(("1330", "FGTS", "isento (estatutário)"))
        return bases
