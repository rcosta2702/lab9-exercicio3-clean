from models.conta import Conta
from models.i_conta_repository import IContaRepository


class ConsultarContaUseCase:
    def __init__(self, repository: IContaRepository) -> None:
        self.repository = repository

    def executar(self, numero: int) -> Conta:
        conta = self.repository.buscar(numero)
        if conta is None:
            raise ValueError("Conta nao encontrada.")
        return conta
