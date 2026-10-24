from dataclasses import dataclass


@dataclass(frozen=True)
class Cliente:
    nome: str
    cpf: str

    def __post_init__(self) -> None:
        if not self.nome.strip() or not self.cpf.strip():
            raise ValueError("Nome e CPF sao obrigatorios.")
