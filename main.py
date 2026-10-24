from pathlib import Path

from controllers.conta_controller import ContaController
from arquivo_conta_repository import ArquivoContaRepository
from consultar_conta import ConsultarContaUseCase
from criar_conta import CriarContaUseCase
from realizar_deposito import RealizarDepositoUseCase
from realizar_saque import RealizarSaqueUseCase
from views.conta_view import ContaView


def main() -> None:
    caminho = Path(__file__).resolve().parent / "contas.txt"
    repository = ArquivoContaRepository(caminho)
    controller = ContaController(
        view=ContaView(),
        criar=CriarContaUseCase(repository),
        depositar=RealizarDepositoUseCase(repository),
        sacar=RealizarSaqueUseCase(repository),
        consultar=ConsultarContaUseCase(repository),
    )
    controller.executar()


if __name__ == "__main__":
    main()
