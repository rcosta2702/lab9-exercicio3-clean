from decimal import Decimal

from models.conta import Conta
from models.i_conta_repository import IContaRepository


class RealizarSaqueUseCase:
    """Depende apenas da abstracao IContaRepository, nao do arquivo TXT."""

    def __init__(self, repository: IContaRepository) -> None:
        self.repository = repository

    def executar(self, numero: int, valor: Decimal) -> Conta:
        conta = self.repository.buscar(numero)
        if conta is None:
            raise ValueError("Conta nao encontrada.")
        conta.sacar(valor)
        self.repository.salvar(conta)
        return conta
