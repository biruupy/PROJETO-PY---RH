# Vanguard Solutions - Interface grafica do sistema de RH (A3)
# Feita com Tkinter, que ja vem junto com o Python (nao precisa instalar nada)
# As classes ficam no sistema_rh.py, aqui e so a parte da janela
# Rodar com: python interface_rh.py

import tkinter as tk
from tkinter import ttk  # widgets mais bonitos (tabela, abas, combobox)
from tkinter import messagebox  # caixinhas de aviso

from sistema_rh import ColaboradorCLT, ColaboradorAprendiz, ColaboradorEstagiario
from sistema_rh import ColaboradorPJ, ColaboradorDiretor
from sistema_rh import VALOR_VA, VALOR_VR
from sistema_rh import formatar_valor, formatar_moeda, formatar_cpf

# Cores da empresa
AZUL_ESCURO = "#1f2a44"
AZUL = "#2f6fed"
AZUL_CLARO = "#eef2fb"  # fundo das linhas alternadas da tabela
VERDE = "#1e8e3e"
FUNDO = "#f4f6fa"
BRANCO = "#ffffff"
CINZA = "#6b7280"

FONTE = "Segoe UI"

TIPOS = ["CLT Comum", "Jovem Aprendiz", "Estagiário", "Prestador PJ", "Diretoria (C-Level)"]

colaboradores = []  # lista que guarda os objetos na memoria


# ---------------------------------------------------------------------
# Funcoes de apoio
# ---------------------------------------------------------------------

# Converte o texto digitado em numero, devolve None se for invalido
def converter_numero(texto, aceita_zero):
    texto = texto.strip().replace(",", ".")  # aceita virgula tambem
    if texto == "" and aceita_zero:
        return 0.0  # campo opcional em branco conta como zero
    try:
        numero = float(texto)
    except ValueError:
        return None
    if numero > 0:
        return numero
    elif numero == 0 and aceita_zero:
        return numero
    return None


def aviso(mensagem):
    messagebox.showwarning("Atenção", mensagem)


# Igual no holerite do terminal: se o valor for zero a coluna fica em branco
def valor_ou_vazio(valor):
    if valor > 0:
        return formatar_valor(valor)
    return ""


# Cria um rotulo + caixa de texto numa linha do formulario
def criar_campo(pai, texto, linha):
    rotulo = tk.Label(pai, text=texto, width=22, anchor="w", bg=BRANCO, fg=CINZA, font=(FONTE, 10))
    rotulo.grid(row=linha, column=0, sticky="w", pady=6)
    entrada = ttk.Entry(pai, width=36, font=(FONTE, 10))
    entrada.grid(row=linha, column=1, sticky="ew", pady=6)
    return entrada


# Texto do quadro "Sobre o vinculo" (muda conforme o tipo escolhido)
def texto_do_vinculo(tipo):
    if tipo == "CLT Comum":
        return ("Jornada de 44h semanais.\n\n"
                "Descontos: INSS pela tabela progressiva, IRRF com dedução de "
                "R$ 189,59 por dependente e vale transporte de 6% (opcional).\n\n"
                "FGTS de 8% pago pela empresa.")
    elif tipo == "Jovem Aprendiz":
        return ("Jornada de 30h semanais.\n\n"
                "Mesmos descontos do CLT: INSS, IRRF e vale transporte (opcional).\n\n"
                "FGTS reduzido de 2% pago pela empresa.")
    elif tipo == "Estagiário":
        return ("Jornada de até 30h semanais.\n\n"
                "Recebe bolsa-auxílio. Não tem INSS nem FGTS, só paga IRRF "
                "se a bolsa passar da faixa de isenção.")
    elif tipo == "Prestador PJ":
        return ("Pago por hora trabalhada.\n\n"
                "Retenção de 6% sobre a nota fiscal (horas + bônus). "
                "A ajuda de custo de benefícios é isenta.\n\n"
                "Não tem INSS, FGTS nem cartão iFood.")
    else:
        return ("Diretor estatutário.\n\n"
                "Recebe pró-labore com IRRF. O bônus de performance (PLR) "
                "entra isento.\n\n"
                "Sem INSS e sem FGTS. O cartão iFood é opcional.")


# ---------------------------------------------------------------------
# Aba 1 - Cadastro
# ---------------------------------------------------------------------

# Mostra so os campos do tipo de vinculo escolhido
def trocar_tipo(event=None):
    quadro_clt.pack_forget()  # esconde todos
    quadro_estagio.pack_forget()
    quadro_pj.pack_forget()
    quadro_diretor.pack_forget()

    tipo = combo_tipo.get()
    if tipo == "CLT Comum" or tipo == "Jovem Aprendiz":
        quadro_clt.pack(fill="x")
    elif tipo == "Estagiário":
        quadro_estagio.pack(fill="x")
    elif tipo == "Prestador PJ":
        quadro_pj.pack(fill="x")
    else:
        quadro_diretor.pack(fill="x")

    rotulo_info.config(text=texto_do_vinculo(tipo))


def limpar_formulario():
    campos = [entrada_nome, entrada_cpf, entrada_salario, entrada_bolsa, entrada_horas,
              entrada_valor_hora, entrada_bonus_pj, entrada_pro_labore, entrada_plr]
    for campo in campos:
        campo.delete(0, "end")  # apaga do comeco ate o fim
    spin_dependentes.set(0)
    var_vt.set(False)
    var_ajuda.set(False)
    var_beneficios.set(False)
    entrada_nome.focus()


def cadastrar():
    nome = entrada_nome.get().strip()
    cpf = entrada_cpf.get().strip()
    tipo = combo_tipo.get()

    if nome == "":
        aviso("O nome não pode ficar vazio!")
        return
    if len(cpf) != 11 or not cpf.isdigit():
        aviso("CPF inválido! Digite os 11 números sem ponto e traço.")
        return
    # nao pode ter 2 pessoas com o mesmo cpf
    for colaborador in colaboradores:
        if colaborador.get_cpf() == cpf:
            messagebox.showerror("CPF duplicado", "O CPF " + formatar_cpf(cpf) + " já pertence a " + colaborador.get_nome() + "!")
            return

    if tipo == "CLT Comum" or tipo == "Jovem Aprendiz":
        salario = converter_numero(entrada_salario.get(), False)
        if salario is None:
            aviso("Digite um salário base válido.")
            return
        texto_dep = spin_dependentes.get().strip()
        if not texto_dep.isdigit():
            aviso("Dependentes tem que ser um número inteiro (0, 1, 2...).")
            return
        dependentes = int(texto_dep)
        if tipo == "CLT Comum":
            novo = ColaboradorCLT(nome, cpf, salario, dependentes, var_vt.get())  # cria o objeto
        else:
            novo = ColaboradorAprendiz(nome, cpf, salario, dependentes, var_vt.get())

    elif tipo == "Estagiário":
        bolsa = converter_numero(entrada_bolsa.get(), False)
        if bolsa is None:
            aviso("Digite um valor de bolsa-auxílio válido.")
            return
        novo = ColaboradorEstagiario(nome, cpf, bolsa)

    elif tipo == "Prestador PJ":
        horas = converter_numero(entrada_horas.get(), False)
        valor_hora = converter_numero(entrada_valor_hora.get(), False)
        bonus = converter_numero(entrada_bonus_pj.get(), True)
        if horas is None or valor_hora is None or bonus is None:
            aviso("Confira as horas, o valor da hora e o bônus.")
            return
        novo = ColaboradorPJ(nome, cpf, horas, valor_hora, bonus, var_ajuda.get())

    else:
        pro_labore = converter_numero(entrada_pro_labore.get(), False)
        bonus = converter_numero(entrada_plr.get(), True)
        if pro_labore is None or bonus is None:
            aviso("Confira o pró-labore e o bônus PLR.")
            return
        novo = ColaboradorDiretor(nome, cpf, pro_labore, bonus, var_beneficios.get())

    colaboradores.append(novo)  # guarda na lista
    atualizar_telas()
    messagebox.showinfo("Cadastro", novo.get_tipo() + " cadastrado com sucesso!")
    limpar_formulario()


# ---------------------------------------------------------------------
# Aba 2 - Colaboradores e resumo da folha
# ---------------------------------------------------------------------

def atualizar_lista():
    for linha in tabela.get_children():  # apaga o que ja tinha
        tabela.delete(linha)

    posicao = 0
    for colaborador in colaboradores:
        if posicao % 2 == 0:
            cor = "par"
        else:
            cor = "impar"
        # polimorfismo: mesmos metodos, cada objeto calcula do seu jeito
        tabela.insert("", "end", iid=str(posicao), tags=(cor,), values=(
            colaborador.get_nome(),
            formatar_cpf(colaborador.get_cpf()),
            colaborador.get_tipo(),
            formatar_moeda(colaborador.calcular_salario_bruto()),
            formatar_moeda(colaborador.calcular_total_descontos()),
            formatar_moeda(colaborador.calcular_salario_liquido()),
        ))
        posicao = posicao + 1


def atualizar_resumo():
    total_proventos = 0.0
    total_descontos = 0.0
    total_liquido = 0.0
    total_fgts = 0.0
    total_cartoes = 0.0

    for colaborador in colaboradores:
        total_proventos = total_proventos + colaborador.calcular_salario_bruto()
        total_descontos = total_descontos + colaborador.calcular_total_descontos()
        total_liquido = total_liquido + colaborador.calcular_salario_liquido()
        total_fgts = total_fgts + colaborador.calcular_fgts()
        total_cartoes = total_cartoes + colaborador.get_saldo_beneficios()

    resumo_qtd.config(text=str(len(colaboradores)))
    resumo_proventos.config(text=formatar_moeda(total_proventos))
    resumo_descontos.config(text=formatar_moeda(total_descontos))
    resumo_liquido.config(text=formatar_moeda(total_liquido))
    resumo_cartoes.config(text=formatar_moeda(total_cartoes))
    resumo_fgts.config(text=formatar_moeda(total_fgts))


# Um bloquinho do resumo: titulo pequeno em cima e valor grande embaixo
def criar_indicador(pai, titulo, coluna):
    tk.Label(pai, text=titulo, bg=AZUL_ESCURO, fg="#aab4c8", font=(FONTE, 9)).grid(row=0, column=coluna, sticky="w", padx=12)
    valor = tk.Label(pai, text="-", bg=AZUL_ESCURO, fg=BRANCO, font=(FONTE, 13, "bold"))
    valor.grid(row=1, column=coluna, sticky="w", padx=12)
    pai.columnconfigure(coluna, weight=1)
    return valor


def ver_holerite_selecionado(event=None):
    selecionado = tabela.selection()
    if len(selecionado) == 0:
        aviso("Selecione um colaborador na lista.")
        return
    indice = int(selecionado[0])  # o iid da linha e a posicao na lista
    combo_holerite.current(indice)
    mostrar_holerite()
    abas.select(aba_folha)


# ---------------------------------------------------------------------
# Aba 3 - Holerite individual
# ---------------------------------------------------------------------

def mostrar_holerite(event=None):
    indice = combo_holerite.current()
    if indice < 0:
        return  # ninguem escolhido ainda
    colaborador = colaboradores[indice]

    rotulo_nome.config(text=colaborador.get_nome())
    rotulo_cpf.config(text=formatar_cpf(colaborador.get_cpf()))
    rotulo_vinculo.config(text=colaborador.get_tipo())
    rotulo_jornada.config(text=colaborador.get_jornada())

    # Lancamentos (proventos e descontos)
    for linha in tabela_itens.get_children():
        tabela_itens.delete(linha)
    for item in colaborador.get_itens():
        # item = (codigo, descricao, referencia, provento, desconto)
        tabela_itens.insert("", "end", values=(item[0], item[1], item[2], valor_ou_vazio(item[3]), valor_ou_vazio(item[4])))

    rotulo_totais.config(text="Total de proventos:  " + formatar_moeda(colaborador.calcular_salario_bruto())
                         + "        Total de descontos:  " + formatar_moeda(colaborador.calcular_total_descontos()))
    rotulo_liquido.config(text=formatar_moeda(colaborador.calcular_salario_liquido()))

    # Bases de calculo
    for linha in tabela_bases.get_children():
        tabela_bases.delete(linha)
    for base in colaborador.get_bases():
        tabela_bases.insert("", "end", values=base)

    # Cartao de beneficios
    cartao = colaborador.get_saldo_beneficios()
    if cartao > 0:
        rotulo_cartao.config(text="Cartão iFood Benefícios:  VA " + formatar_moeda(VALOR_VA) + "  +  VR "
                             + formatar_moeda(VALOR_VR) + "  =  " + formatar_moeda(cartao) + "  (sem desconto em folha)")
    elif colaborador.get_tipo() == "PJ":
        rotulo_cartao.config(text="Cartão iFood Benefícios:  não se aplica (PJ)")
    else:
        rotulo_cartao.config(text="Cartão iFood Benefícios:  não optou")


# Atualiza tudo que depende da lista depois de um cadastro
def atualizar_telas():
    atualizar_lista()
    atualizar_resumo()

    nomes = []
    for colaborador in colaboradores:
        nomes.append(colaborador.get_nome() + "   -   " + colaborador.get_tipo())
    combo_holerite["values"] = nomes

    if len(colaboradores) == 1:
        rotulo_contador.config(text="1 colaborador")
    else:
        rotulo_contador.config(text=str(len(colaboradores)) + " colaboradores")


# ---------------------------------------------------------------------
# Montagem da janela
# ---------------------------------------------------------------------

janela = tk.Tk()
janela.title("Vanguard Solutions - Sistema de RH")
janela.geometry("1080x790")
janela.minsize(1000, 760)
janela.configure(bg=FUNDO)

# Estilo dos widgets ttk
estilo = ttk.Style()
estilo.theme_use("clam")
estilo.configure("TNotebook", background=FUNDO, borderwidth=0)
estilo.configure("TNotebook.Tab", padding=(20, 8), font=(FONTE, 10, "bold"), background="#dfe4ee", foreground=CINZA)
estilo.map("TNotebook.Tab", background=[("selected", BRANCO)], foreground=[("selected", AZUL)], padding=[("selected", (20, 8))])
estilo.configure("Treeview", rowheight=26, font=(FONTE, 10), background=BRANCO, fieldbackground=BRANCO, borderwidth=0)
estilo.configure("Treeview.Heading", font=(FONTE, 10, "bold"), background=AZUL_ESCURO, foreground=BRANCO, relief="flat")
estilo.map("Treeview.Heading", background=[("active", AZUL)])
estilo.map("Treeview", background=[("selected", AZUL)], foreground=[("selected", BRANCO)])
estilo.configure("Principal.TButton", font=(FONTE, 10, "bold"), background=AZUL, foreground=BRANCO, padding=(18, 8), borderwidth=0)
estilo.map("Principal.TButton", background=[("active", AZUL_ESCURO)])
estilo.configure("Secundario.TButton", font=(FONTE, 10), padding=(18, 8))

# Faixa de cima com o nome da empresa
topo = tk.Frame(janela, bg=AZUL_ESCURO)
topo.pack(fill="x")
tk.Label(topo, text="VANGUARD SOLUTIONS", bg=AZUL_ESCURO, fg=BRANCO, font=(FONTE, 20, "bold")).pack(side="left", padx=(24, 14), pady=16)
tk.Label(topo, text="Sistema Corporativo de\nRecursos Humanos", justify="left", bg=AZUL_ESCURO, fg="#aab4c8", font=(FONTE, 10)).pack(side="left")
rotulo_contador = tk.Label(topo, text="0 colaboradores", bg=AZUL, fg=BRANCO, font=(FONTE, 10, "bold"), padx=14, pady=6)
rotulo_contador.pack(side="right", padx=24)

# Abas
abas = ttk.Notebook(janela)
abas.pack(fill="both", expand=True, padx=16, pady=16)
aba_cadastro = tk.Frame(abas, bg=FUNDO)
aba_lista = tk.Frame(abas, bg=FUNDO)
aba_folha = tk.Frame(abas, bg=FUNDO)
abas.add(aba_cadastro, text="Cadastro")
abas.add(aba_lista, text="Colaboradores")
abas.add(aba_folha, text="Folha de Pagamento")

# --- Aba 1: formulario na esquerda, explicacao do vinculo na direita ---
cartao_form = tk.Frame(aba_cadastro, bg=BRANCO, padx=28, pady=22)
cartao_form.pack(side="left", fill="both", expand=True, padx=(16, 8), pady=16)

cartao_info = tk.Frame(aba_cadastro, bg=BRANCO, padx=24, pady=22, width=330)
cartao_info.pack(side="right", fill="y", padx=(8, 16), pady=16)
cartao_info.pack_propagate(False)  # mantem a largura fixa

tk.Label(cartao_form, text="Novo colaborador", bg=BRANCO, fg=AZUL_ESCURO, font=(FONTE, 14, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 14))

tk.Label(cartao_form, text="Tipo de vínculo", width=22, anchor="w", bg=BRANCO, fg=CINZA, font=(FONTE, 10)).grid(row=1, column=0, sticky="w", pady=6)
combo_tipo = ttk.Combobox(cartao_form, values=TIPOS, state="readonly", font=(FONTE, 10))
combo_tipo.grid(row=1, column=1, sticky="ew", pady=6)
combo_tipo.current(0)
combo_tipo.bind("<<ComboboxSelected>>", trocar_tipo)

entrada_nome = criar_campo(cartao_form, "Nome completo", 2)
entrada_cpf = criar_campo(cartao_form, "CPF (só números)", 3)

ttk.Separator(cartao_form).grid(row=4, column=0, columnspan=2, sticky="ew", pady=16)

area_vinculo = tk.Frame(cartao_form, bg=BRANCO)
area_vinculo.grid(row=5, column=0, columnspan=2, sticky="ew")
cartao_form.columnconfigure(1, weight=1)

# Campos do CLT e do Jovem Aprendiz (os dois pedem a mesma coisa)
quadro_clt = tk.Frame(area_vinculo, bg=BRANCO)
quadro_clt.columnconfigure(1, weight=1)
entrada_salario = criar_campo(quadro_clt, "Salário base (R$)", 0)
tk.Label(quadro_clt, text="Dependentes", width=22, anchor="w", bg=BRANCO, fg=CINZA, font=(FONTE, 10)).grid(row=1, column=0, sticky="w", pady=6)
spin_dependentes = ttk.Spinbox(quadro_clt, from_=0, to=20, width=6, font=(FONTE, 10))
spin_dependentes.grid(row=1, column=1, sticky="w", pady=6)
spin_dependentes.set(0)
var_vt = tk.BooleanVar()
tk.Checkbutton(quadro_clt, text="Descontar vale transporte (6%)", variable=var_vt, bg=BRANCO, activebackground=BRANCO, font=(FONTE, 10)).grid(row=2, column=1, sticky="w", pady=6)

# Campos do Estagiario
quadro_estagio = tk.Frame(area_vinculo, bg=BRANCO)
quadro_estagio.columnconfigure(1, weight=1)
entrada_bolsa = criar_campo(quadro_estagio, "Bolsa-auxílio (R$)", 0)

# Campos do PJ
quadro_pj = tk.Frame(area_vinculo, bg=BRANCO)
quadro_pj.columnconfigure(1, weight=1)
entrada_horas = criar_campo(quadro_pj, "Horas trabalhadas", 0)
entrada_valor_hora = criar_campo(quadro_pj, "Valor da hora (R$)", 1)
entrada_bonus_pj = criar_campo(quadro_pj, "Bônus / adicional (R$)", 2)
var_ajuda = tk.BooleanVar()
tk.Checkbutton(quadro_pj, text="Ajuda de custo de benefícios (R$ 2.740,00)", variable=var_ajuda, bg=BRANCO, activebackground=BRANCO, font=(FONTE, 10)).grid(row=3, column=1, sticky="w", pady=6)

# Campos da Diretoria
quadro_diretor = tk.Frame(area_vinculo, bg=BRANCO)
quadro_diretor.columnconfigure(1, weight=1)
entrada_pro_labore = criar_campo(quadro_diretor, "Pró-labore mensal (R$)", 0)
entrada_plr = criar_campo(quadro_diretor, "Bônus PLR (R$)", 1)
var_beneficios = tk.BooleanVar()
tk.Checkbutton(quadro_diretor, text="Optar pelo cartão iFood Benefícios (R$ 2.740,00)", variable=var_beneficios, bg=BRANCO, activebackground=BRANCO, font=(FONTE, 10)).grid(row=2, column=1, sticky="w", pady=6)

botoes = tk.Frame(cartao_form, bg=BRANCO)
botoes.grid(row=6, column=0, columnspan=2, sticky="w", pady=(22, 0))
ttk.Button(botoes, text="Cadastrar", style="Principal.TButton", command=cadastrar).pack(side="left")
ttk.Button(botoes, text="Limpar campos", style="Secundario.TButton", command=limpar_formulario).pack(side="left", padx=10)

tk.Label(cartao_info, text="Sobre o vínculo", bg=BRANCO, fg=AZUL_ESCURO, font=(FONTE, 14, "bold")).pack(anchor="w", pady=(0, 14))
rotulo_info = tk.Label(cartao_info, text="", bg=BRANCO, fg="#374151", font=(FONTE, 10), justify="left", wraplength=280)
rotulo_info.pack(anchor="w")

caixa_ifood = tk.Frame(cartao_info, bg=AZUL_CLARO, padx=14, pady=12)
caixa_ifood.pack(side="bottom", fill="x")
tk.Label(caixa_ifood, text="Cartão iFood Benefícios", bg=AZUL_CLARO, fg=AZUL_ESCURO, font=(FONTE, 10, "bold")).pack(anchor="w")
tk.Label(caixa_ifood, text="Vale Alimentação:  " + formatar_moeda(VALOR_VA) + "\nVale Refeição:  " + formatar_moeda(VALOR_VR),
         bg=AZUL_CLARO, fg="#374151", font=(FONTE, 10), justify="left").pack(anchor="w", pady=(4, 0))

# --- Aba 2: tabela de colaboradores + resumo ---
cartao_lista = tk.Frame(aba_lista, bg=BRANCO, padx=20, pady=16)
cartao_lista.pack(fill="both", expand=True, padx=16, pady=(16, 8))

cabecalho_lista = tk.Frame(cartao_lista, bg=BRANCO)
cabecalho_lista.pack(fill="x", pady=(0, 12))
tk.Label(cabecalho_lista, text="Colaboradores cadastrados", bg=BRANCO, fg=AZUL_ESCURO, font=(FONTE, 14, "bold")).pack(side="left")
ttk.Button(cabecalho_lista, text="Ver holerite", style="Principal.TButton", command=ver_holerite_selecionado).pack(side="right")

colunas = ("nome", "cpf", "vinculo", "bruto", "descontos", "liquido")
tabela = ttk.Treeview(cartao_lista, columns=colunas, show="headings", selectmode="browse")
tabela.heading("nome", text="Nome")
tabela.heading("cpf", text="CPF")
tabela.heading("vinculo", text="Vínculo")
tabela.heading("bruto", text="Bruto")
tabela.heading("descontos", text="Descontos")
tabela.heading("liquido", text="Líquido")
tabela.column("nome", width=230)
tabela.column("cpf", width=120, anchor="center")
tabela.column("vinculo", width=150, anchor="center")
tabela.column("bruto", width=120, anchor="e")
tabela.column("descontos", width=120, anchor="e")
tabela.column("liquido", width=120, anchor="e")
tabela.tag_configure("par", background=BRANCO)
tabela.tag_configure("impar", background=AZUL_CLARO)
tabela.bind("<Double-1>", ver_holerite_selecionado)  # duplo clique abre o holerite

barra_rolagem = ttk.Scrollbar(cartao_lista, orient="vertical", command=tabela.yview)
tabela.configure(yscrollcommand=barra_rolagem.set)
barra_rolagem.pack(side="right", fill="y")
tabela.pack(fill="both", expand=True)

cartao_resumo = tk.Frame(aba_lista, bg=AZUL_ESCURO, padx=12, pady=14)
cartao_resumo.pack(fill="x", padx=16, pady=(8, 16))
resumo_qtd = criar_indicador(cartao_resumo, "Colaboradores", 0)
resumo_proventos = criar_indicador(cartao_resumo, "Total de proventos", 1)
resumo_descontos = criar_indicador(cartao_resumo, "Total de descontos", 2)
resumo_liquido = criar_indicador(cartao_resumo, "Líquido pago em conta", 3)
resumo_cartoes = criar_indicador(cartao_resumo, "Cartões iFood", 4)
resumo_fgts = criar_indicador(cartao_resumo, "FGTS (encargo)", 5)

# --- Aba 3: holerite ---
barra_folha = tk.Frame(aba_folha, bg=FUNDO)
barra_folha.pack(fill="x", padx=16, pady=(14, 0))
tk.Label(barra_folha, text="Colaborador:", bg=FUNDO, fg=AZUL_ESCURO, font=(FONTE, 10, "bold")).pack(side="left")
combo_holerite = ttk.Combobox(barra_folha, state="readonly", width=55, font=(FONTE, 10))
combo_holerite.pack(side="left", padx=10)
combo_holerite.bind("<<ComboboxSelected>>", mostrar_holerite)

holerite = tk.Frame(aba_folha, bg=BRANCO)
holerite.pack(fill="both", expand=True, padx=16, pady=14)

tk.Label(holerite, text="VANGUARD SOLUTIONS   |   DEMONSTRATIVO DE PAGAMENTO", bg=AZUL_ESCURO, fg=BRANCO, font=(FONTE, 11, "bold"), pady=8).pack(fill="x")

dados = tk.Frame(holerite, bg=BRANCO, padx=20, pady=10)
dados.pack(fill="x")
tk.Label(dados, text="Colaborador:", bg=BRANCO, fg=CINZA, font=(FONTE, 10)).grid(row=0, column=0, sticky="w")
rotulo_nome = tk.Label(dados, text="-", bg=BRANCO, fg=AZUL_ESCURO, font=(FONTE, 10, "bold"))
rotulo_nome.grid(row=0, column=1, sticky="w", padx=(6, 40))
tk.Label(dados, text="CPF:", bg=BRANCO, fg=CINZA, font=(FONTE, 10)).grid(row=0, column=2, sticky="w")
rotulo_cpf = tk.Label(dados, text="-", bg=BRANCO, fg=AZUL_ESCURO, font=(FONTE, 10, "bold"))
rotulo_cpf.grid(row=0, column=3, sticky="w", padx=6)
tk.Label(dados, text="Vínculo:", bg=BRANCO, fg=CINZA, font=(FONTE, 10)).grid(row=1, column=0, sticky="w")
rotulo_vinculo = tk.Label(dados, text="-", bg=BRANCO, fg=AZUL_ESCURO, font=(FONTE, 10, "bold"))
rotulo_vinculo.grid(row=1, column=1, sticky="w", padx=(6, 40))
tk.Label(dados, text="Jornada:", bg=BRANCO, fg=CINZA, font=(FONTE, 10)).grid(row=1, column=2, sticky="w")
rotulo_jornada = tk.Label(dados, text="-", bg=BRANCO, fg=AZUL_ESCURO, font=(FONTE, 10, "bold"))
rotulo_jornada.grid(row=1, column=3, sticky="w", padx=6)

colunas_itens = ("cod", "descricao", "ref", "proventos", "descontos")
tabela_itens = ttk.Treeview(holerite, columns=colunas_itens, show="headings", height=4)
tabela_itens.heading("cod", text="Cód")
tabela_itens.heading("descricao", text="Descrição", anchor="w")
tabela_itens.heading("ref", text="Ref.")
tabela_itens.heading("proventos", text="Proventos")
tabela_itens.heading("descontos", text="Descontos")
tabela_itens.column("cod", width=70, anchor="center")
tabela_itens.column("descricao", width=300)
tabela_itens.column("ref", width=110, anchor="center")
tabela_itens.column("proventos", width=140, anchor="e")
tabela_itens.column("descontos", width=140, anchor="e")
tabela_itens.pack(fill="x", padx=20)

rotulo_totais = tk.Label(holerite, text="", bg=BRANCO, fg="#374151", font=(FONTE, 10))
rotulo_totais.pack(anchor="e", padx=20, pady=6)

faixa_liquido = tk.Frame(holerite, bg=VERDE, padx=16, pady=8)
faixa_liquido.pack(fill="x", padx=20)
tk.Label(faixa_liquido, text="LÍQUIDO A RECEBER (conta corrente)", bg=VERDE, fg=BRANCO, font=(FONTE, 11, "bold")).pack(side="left")
rotulo_liquido = tk.Label(faixa_liquido, text="R$ 0,00", bg=VERDE, fg=BRANCO, font=(FONTE, 16, "bold"))
rotulo_liquido.pack(side="right")

tk.Label(holerite, text="Bases de cálculo e encargos (informativo)", bg=BRANCO, fg=AZUL_ESCURO, font=(FONTE, 10, "bold")).pack(anchor="w", padx=20, pady=(12, 4))
colunas_bases = ("cod", "descricao", "valor")
tabela_bases = ttk.Treeview(holerite, columns=colunas_bases, show="headings", height=5)
tabela_bases.heading("cod", text="Cód")
tabela_bases.heading("descricao", text="Descrição", anchor="w")
tabela_bases.heading("valor", text="Valor")
tabela_bases.column("cod", width=70, anchor="center")
tabela_bases.column("descricao", width=450)
tabela_bases.column("valor", width=240, anchor="e")
tabela_bases.pack(fill="x", padx=20)

rotulo_cartao = tk.Label(holerite, text="", bg=BRANCO, fg=AZUL, font=(FONTE, 10, "bold"))
rotulo_cartao.pack(anchor="w", padx=20, pady=10)

# Programa principal
trocar_tipo()  # mostra os campos do primeiro tipo (CLT)
atualizar_telas()
entrada_nome.focus()
janela.mainloop()
