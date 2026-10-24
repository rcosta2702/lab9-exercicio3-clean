import tkinter as tk
from decimal import Decimal, InvalidOperation
from tkinter import messagebox, ttk
from typing import Callable

from models.conta import Conta


class ContaView:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Exercicio 3 - Clean Architecture")
        self.root.geometry("760x640")

        principal = ttk.Frame(self.root, padding=20)
        principal.pack(fill="both", expand=True)
        ttk.Label(principal, text="Banco com persistencia TXT", font=("Segoe UI", 20, "bold")).pack(anchor="w")

        abas = ttk.Notebook(principal)
        abas.pack(fill="x", pady=15)
        cadastro = ttk.Frame(abas, padding=16)
        movimento = ttk.Frame(abas, padding=16)
        abas.add(cadastro, text="Criar conta")
        abas.add(movimento, text="Operacoes")

        self.numero_cadastro = self._campo(cadastro, "Numero da conta", 0)
        self.nome = self._campo(cadastro, "Nome", 1)
        self.cpf = self._campo(cadastro, "CPF", 2)
        self.saldo_inicial = self._campo(cadastro, "Saldo inicial (R$)", 3)
        self.botao_criar = ttk.Button(cadastro, text="Criar e salvar no TXT")
        self.botao_criar.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(12, 0))

        self.numero_operacao = self._campo(movimento, "Numero da conta", 0)
        self.valor_operacao = self._campo(movimento, "Valor (R$)", 1)
        botoes = ttk.Frame(movimento)
        botoes.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(12, 0))
        self.botao_depositar = ttk.Button(botoes, text="Depositar")
        self.botao_sacar = ttk.Button(botoes, text="Sacar")
        self.botao_consultar = ttk.Button(botoes, text="Consultar dados no TXT")
        for botao in (self.botao_depositar, self.botao_sacar, self.botao_consultar):
            botao.pack(side="left", expand=True, fill="x", padx=4)

        self.resultado = tk.Text(principal, height=17, state="disabled", font=("Consolas", 10))
        self.resultado.pack(fill="both", expand=True)

    @staticmethod
    def _campo(pai: ttk.Frame, rotulo: str, linha: int) -> ttk.Entry:
        ttk.Label(pai, text=rotulo).grid(row=linha, column=0, sticky="w", padx=(0, 12), pady=5)
        entrada = ttk.Entry(pai, width=48)
        entrada.grid(row=linha, column=1, sticky="ew", pady=5)
        pai.columnconfigure(1, weight=1)
        return entrada

    def configurar_acoes(
        self,
        criar: Callable[[], None],
        depositar: Callable[[], None],
        sacar: Callable[[], None],
        consultar: Callable[[], None],
    ) -> None:
        self.botao_criar.configure(command=criar)
        self.botao_depositar.configure(command=depositar)
        self.botao_sacar.configure(command=sacar)
        self.botao_consultar.configure(command=consultar)

    def cadastro(self) -> tuple[int, str, str, Decimal]:
        return (
            self._inteiro(self.numero_cadastro.get()),
            self.nome.get().strip(),
            self.cpf.get().strip(),
            self._decimal(self.saldo_inicial.get()),
        )

    def numero(self) -> int:
        return self._inteiro(self.numero_operacao.get())

    def valor(self) -> Decimal:
        return self._decimal(self.valor_operacao.get())

    def selecionar_conta(self, numero: int) -> None:
        self.numero_operacao.delete(0, "end")
        self.numero_operacao.insert(0, str(numero))

    @staticmethod
    def _inteiro(texto: str) -> int:
        try:
            return int(texto)
        except ValueError as exc:
            raise ValueError("Numero da conta invalido.") from exc

    @staticmethod
    def _decimal(texto: str) -> Decimal:
        try:
            return Decimal(texto.replace(",", "."))
        except InvalidOperation as exc:
            raise ValueError("Valor invalido.") from exc

    def exibir(self, conta: Conta, titulo: str = "Dados da conta") -> None:
        linhas = [
            titulo,
            "",
            f"Conta {conta.numero} | {conta.cliente.nome}",
            f"CPF: {conta.cliente.cpf}",
            f"Saldo: R$ {conta.saldo:.2f}",
            "",
            "Historico:",
        ]
        linhas.extend(conta.historico or ["Nenhuma movimentacao."])
        self.resultado.configure(state="normal")
        self.resultado.delete("1.0", "end")
        self.resultado.insert("1.0", "\n".join(linhas))
        self.resultado.configure(state="disabled")

    def exibir_erro(self, mensagem: str) -> None:
        messagebox.showerror("Erro", mensagem, parent=self.root)

    def iniciar(self) -> None:
        self.root.mainloop()
