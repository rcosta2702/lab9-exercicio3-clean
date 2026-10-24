from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal

from models.cliente import Cliente


@dataclass
class Conta:
    numero: int
    cliente: Cliente
    saldo: Decimal = Decimal("0")
    historico: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.saldo = Decimal(str(self.saldo))
        if self.numero <= 0:
            raise ValueError("O numero da conta deve ser positivo.")
        if self.saldo < 0:
            raise ValueError("O saldo nao pode ser negativo.")

    def depositar(self, valor: Decimal) -> None:
        quantia = self._valor_positivo(valor)
        self.saldo += quantia
        self._registrar("DEPOSITO", quantia)

    def sacar(self, valor: Decimal) -> None:
        quantia = self._valor_positivo(valor)
        if quantia > self.saldo:
            raise ValueError("Saldo insuficiente.")
        self.saldo -= quantia
        self._registrar("SAQUE", quantia)

    def _registrar(self, tipo: str, valor: Decimal) -> None:
        instante = datetime.now().isoformat(timespec="seconds")
        self.historico.append(f"{instante}|{tipo}|{valor}")

    @staticmethod
    def _valor_positivo(valor: Decimal) -> Decimal:
        quantia = Decimal(str(valor))
        if quantia <= 0:
            raise ValueError("O valor deve ser maior que zero.")
        return quantia
