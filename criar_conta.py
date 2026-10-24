from decimal import Decimal

from models.cliente import Cliente
from models.conta import Conta
from models.i_conta_repository import IContaRepository


class CriarContaUseCase:
    def __init__(self, repository: IContaRepository) -> None:
        self.repository = repository

    def executar(self, numero: int, nome: str, cpf: str, saldo: Decimal) -> Conta:
        if self.repository.buscar(numero) is not None:
            raise ValueError("Ja existe uma conta com esse numero.")
        conta = Conta(numero, Cliente(nome, cpf), saldo)
        if conta.saldo > 0:
            conta.historico.append(f"ABERTURA|{conta.saldo}")
        self.repository.salvar(conta)
        return conta
