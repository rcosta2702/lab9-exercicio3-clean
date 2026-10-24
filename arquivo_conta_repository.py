import json
from decimal import Decimal
from pathlib import Path

from models.cliente import Cliente
from models.conta import Conta
from models.i_conta_repository import IContaRepository


class ArquivoContaRepository(IContaRepository):
    """Persiste uma conta por linha em um arquivo TXT no formato JSON Lines."""

    def __init__(self, caminho: str | Path) -> None:
        self.caminho = Path(caminho)
        self.caminho.touch(exist_ok=True)

    def salvar(self, conta: Conta) -> None:
        contas = self._carregar_todas()
        contas[conta.numero] = conta
        temporario = self.caminho.with_suffix(".tmp")
        with temporario.open("w", encoding="utf-8") as arquivo:
            for numero in sorted(contas):
                arquivo.write(json.dumps(self._para_dict(contas[numero]), ensure_ascii=False) + "\n")
        temporario.replace(self.caminho)

    def buscar(self, numero: int) -> Conta | None:
        return self._carregar_todas().get(numero)

    def _carregar_todas(self) -> dict[int, Conta]:
        contas: dict[int, Conta] = {}
        with self.caminho.open("r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                if not linha.strip():
                    continue
                dados = json.loads(linha)
                cliente = Cliente(dados["nome"], dados["cpf"])
                conta = Conta(
                    numero=int(dados["numero"]),
                    cliente=cliente,
                    saldo=Decimal(dados["saldo"]),
                    historico=list(dados.get("historico", [])),
                )
                contas[conta.numero] = conta
        return contas

    @staticmethod
    def _para_dict(conta: Conta) -> dict[str, object]:
        return {
            "numero": conta.numero,
            "nome": conta.cliente.nome,
            "cpf": conta.cliente.cpf,
            "saldo": str(conta.saldo),
            "historico": conta.historico,
        }
