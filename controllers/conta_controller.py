from consultar_conta import ConsultarContaUseCase
from criar_conta import CriarContaUseCase
from realizar_deposito import RealizarDepositoUseCase
from realizar_saque import RealizarSaqueUseCase
from views.conta_view import ContaView


class ContaController:
    def __init__(
        self,
        view: ContaView,
        criar: CriarContaUseCase,
        depositar: RealizarDepositoUseCase,
        sacar: RealizarSaqueUseCase,
        consultar: ConsultarContaUseCase,
    ) -> None:
        self.view = view
        self.criar = criar
        self.depositar = depositar
        self.sacar = sacar
        self.consultar = consultar
        self.view.configurar_acoes(self._criar, self._depositar, self._sacar, self._consultar)

    def executar(self) -> None:
        self.view.iniciar()

    def _criar(self) -> None:
        try:
            conta = self.criar.executar(*self.view.cadastro())
            self.view.selecionar_conta(conta.numero)
            self.view.exibir(conta, "Conta criada e salva em contas.txt")
        except ValueError as exc:
            self.view.exibir_erro(str(exc))

    def _depositar(self) -> None:
        self._executar(
            lambda: self.depositar.executar(self.view.numero(), self.view.valor()),
            "Deposito realizado e salvo em contas.txt",
        )

    def _sacar(self) -> None:
        self._executar(
            lambda: self.sacar.executar(self.view.numero(), self.view.valor()),
            "Saque realizado e salvo em contas.txt",
        )

    def _consultar(self) -> None:
        self._executar(
            lambda: self.consultar.executar(self.view.numero()),
            "Dados carregados de contas.txt",
        )

    def _executar(self, acao, titulo: str) -> None:
        try:
            self.view.exibir(acao(), titulo)
        except ValueError as exc:
            self.view.exibir_erro(str(exc))
