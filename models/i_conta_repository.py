from abc import ABC, abstractmethod

from models.conta import Conta


class IContaRepository(ABC):
    """Porta de persistencia usada pelo nucleo, conforme o DIP."""

    @abstractmethod
    def salvar(self, conta: Conta) -> None:
        raise NotImplementedError

    @abstractmethod
    def buscar(self, numero: int) -> Conta | None:
        raise NotImplementedError
