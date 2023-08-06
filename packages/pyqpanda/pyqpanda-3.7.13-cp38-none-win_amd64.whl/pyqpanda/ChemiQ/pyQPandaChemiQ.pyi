from typing import Any, ClassVar, List

from typing import Set
from typing import overload
Bravyi_Ktaev: TransFormType
Jordan_Wigner: TransFormType
Parity: TransFormType
UCCS: UccType
UCCSD: UccType

class ChemiQ:
    """
    """
    def __init__(self) -> None:
        """
        """
        ...

    @overload
    def exec(self) -> bool:
        """
        """
        ...

    @overload
    def exec(self) -> bool:
        """
        """
        ...

    def finalize(self) -> None:
        """
        """
        ...

    def getEnergies(self) -> List[float]:
        """
        """
        ...

    def getLastError(self) -> str:
        """
        """
        ...

    def get_energies(self) -> List[float]:
        """
        """
        ...

    def get_last_error(self) -> str:
        """
        """
        ...

    def initialize(self, arg0: str) -> None:
        """
        """
        ...

    def setBasis(self, arg0: str) -> None:
        """
        """
        ...

    def setCharge(self, arg0: int) -> None:
        """
        """
        ...

    def setDefaultOptimizedPara(self, arg0: List[float]) -> None:
        """
        """
        ...

    def setEvolutionTime(self, arg0: float) -> None:
        """
        """
        ...

    def setHamiltonianGenerationOnly(self, arg0: bool) -> None:
        """
        """
        ...

    def setHamiltonianSimulationSlices(self, arg0: int) -> None:
        """
        """
        ...

    def setLearningRate(self, arg0: float) -> None:
        """
        """
        ...

    def setMolecule(self, arg0: str) -> None:
        """
        """
        ...

    def setMolecules(self, arg0: List[str]) -> None:
        """
        """
        ...

    def setMultiplicity(self, arg0: int) -> None:
        """
        """
        ...

    def setOptimizerDisp(self, arg0: bool) -> None:
        """
        """
        ...

    def setOptimizerFatol(self, arg0: float) -> None:
        """
        """
        ...

    def setOptimizerFuncCallNum(self, arg0: int) -> None:
        """
        """
        ...

    def setOptimizerIterNum(self, arg0: int) -> None:
        """
        """
        ...

    def setOptimizerType(self, arg0) -> None:
        """
        """
        ...

    def setOptimizerXatol(self, arg0: float) -> None:
        """
        """
        ...

    def setRandomPara(self, arg0: bool) -> None:
        """
        """
        ...

    def setSaveDataDir(self, arg0: str) -> None:
        """
        """
        ...

    def setToGetHamiltonianFromFile(self, arg0: bool) -> None:
        """
        """
        ...

    def setTransformType(self, arg0: TransFormType) -> None:
        """
        """
        ...

    def setUccType(self, arg0: UccType) -> None:
        """
        """
        ...

    def set_basis(self, arg0: str) -> None:
        """
        """
        ...

    def set_charge(self, arg0: int) -> None:
        """
        """
        ...

    def set_default_optimized_para(self, arg0: List[float]) -> None:
        """
        """
        ...

    def set_evolution_time(self, arg0: float) -> None:
        """
        """
        ...

    def set_hamiltonian_generation_only(self, arg0: bool) -> None:
        """
        """
        ...

    def set_hamiltonian_simulation_slices(self, arg0: int) -> None:
        """
        """
        ...

    def set_learning_rate(self, arg0: float) -> None:
        """
        """
        ...

    def set_molecule(self, arg0: str) -> None:
        """
        """
        ...

    def set_molecules(self, arg0: List[str]) -> None:
        """
        """
        ...

    def set_multiplicity(self, arg0: int) -> None:
        """
        """
        ...

    def set_optimizer_disp(self, arg0: bool) -> None:
        """
        """
        ...

    def set_optimizer_fatol(self, arg0: float) -> None:
        """
        """
        ...

    def set_optimizer_func_call_num(self, arg0: int) -> None:
        """
        """
        ...

    def set_optimizer_iter_num(self, arg0: int) -> None:
        """
        """
        ...

    def set_optimizer_type(self, arg0) -> None:
        """
        """
        ...

    def set_optimizer_xatol(self, arg0: float) -> None:
        """
        """
        ...

    def set_random_para(self, arg0: bool) -> None:
        """
        """
        ...

    def set_save_data_dir(self, arg0: str) -> None:
        """
        """
        ...

    def set_to_get_hamiltonian_from_file(self, arg0: bool) -> None:
        """
        """
        ...

    def set_transform_type(self, arg0: TransFormType) -> None:
        """
        """
        ...

    def set_ucc_type(self, arg0: UccType) -> None:
        """
        """
        ...


class TransFormType:
    """
    Members:
    
      Jordan_Wigner
    
      Bravyi_Ktaev
    
      Parity
    """
    __doc__: ClassVar[str] = ...  # read-only
    __members__: ClassVar[dict] = ...  # read-only
    Bravyi_Ktaev: ClassVar[TransFormType] = ...
    Jordan_Wigner: ClassVar[TransFormType] = ...
    Parity: ClassVar[TransFormType] = ...
    __entries: ClassVar[dict] = ...
    def __init__(self, arg0: int) -> None:
        """
        """
        ...

    def __eq__(self, other) -> Any:
        """
        """
        ...

    def __ge__(self, other) -> Any:
        """
        """
        ...

    def __getstate__(self) -> Any:
        """
        """
        ...

    def __gt__(self, other) -> Any:
        """
        """
        ...

    def __hash__(self) -> Any:
        """
        """
        ...

    def __index__(self) -> int:
        """
        """
        ...

    def __int__(self) -> int:
        """
        """
        ...

    def __le__(self, other) -> Any:
        """
        """
        ...

    def __lt__(self, other) -> Any:
        """
        """
        ...

    def __ne__(self, other) -> Any:
        """
        """
        ...

    def __setstate__(self, state) -> Any:
        """
        """
        ...

    @property
    def name(self) -> str: ...

class UccType:
    """
    Members:
    
      UCCS
    
      UCCSD
    """
    __doc__: ClassVar[str] = ...  # read-only
    __members__: ClassVar[dict] = ...  # read-only
    UCCS: ClassVar[UccType] = ...
    UCCSD: ClassVar[UccType] = ...
    __entries: ClassVar[dict] = ...
    def __init__(self, arg0: int) -> None:
        """
        """
        ...

    def __eq__(self, other) -> Any:
        """
        """
        ...

    def __ge__(self, other) -> Any:
        """
        """
        ...

    def __getstate__(self) -> Any:
        """
        """
        ...

    def __gt__(self, other) -> Any:
        """
        """
        ...

    def __hash__(self) -> Any:
        """
        """
        ...

    def __index__(self) -> int:
        """
        """
        ...

    def __int__(self) -> int:
        """
        """
        ...

    def __le__(self, other) -> Any:
        """
        """
        ...

    def __lt__(self, other) -> Any:
        """
        """
        ...

    def __ne__(self, other) -> Any:
        """
        """
        ...

    def __setstate__(self, state) -> Any:
        """
        """
        ...

    @property
    def name(self) -> str: ...

def JordanWignerTransform(*args, **kwargs) -> Any:
    """
    Jordan-Wigner transform from FermionOperator to PauliOperator.
    """
    ...

def JordanWignerTransformVar(*args, **kwargs) -> Any:
    """
    Jordan-Wigner transform from VarFermionOperator to VarPauliOperator.
    """
    ...

def getCCSD_N_Trem(arg0: int, arg1: int) -> int:
    """
    get CCSD term number.
    """
    ...

def getCCSD_Normal(*args, **kwargs) -> Any:
    """
    get Coupled cluster single and double model.
    """
    ...

def getCCSD_Var(*args, **kwargs) -> Any:
    """
    get Coupled cluster single and double model with variational parameters.
    """
    ...

def getCCS_N_Trem(arg0: int, arg1: int) -> int:
    """
    get CCS term number.
    """
    ...

def getCCS_Normal(*args, **kwargs) -> Any:
    """
    get Coupled cluster single model.
    """
    ...

def getCCS_Var(*args, **kwargs) -> Any:
    """
    get Coupled cluster single model with variational parameters.
    """
    ...

def getElectronNum(arg0: str) -> int:
    """
    get the electron number of the atom.
    """
    ...

def get_ccs_n_trem(arg0: int, arg1: int) -> int:
    """
    get CCS term number.
    """
    ...

def get_ccs_normal(*args, **kwargs) -> Any:
    """
    get Coupled cluster single model.
    """
    ...

def get_ccs_var(*args, **kwargs) -> Any:
    """
    get Coupled cluster single model with variational parameters.
    """
    ...

def get_ccsd_n_trem(arg0: int, arg1: int) -> int:
    """
    get CCSD term number.
    """
    ...

def get_ccsd_normal(*args, **kwargs) -> Any:
    """
    get Coupled cluster single and double model.
    """
    ...

def get_ccsd_var(*args, **kwargs) -> Any:
    """
    get Coupled cluster single and double model with variational parameters.
    """
    ...

def get_electron_num(arg0: str) -> int:
    """
    get the electron number of the atom.
    """
    ...

def jordan_wigner_transform(*args, **kwargs) -> Any:
    """
    Jordan-Wigner transform from FermionOperator to PauliOperator.
    """
    ...

def jordan_wigner_transform_var(*args, **kwargs) -> Any:
    """
    Jordan-Wigner transform from VarFermionOperator to VarPauliOperator.
    """
    ...

def parsePsi4DataToFermion(*args, **kwargs) -> Any:
    """
    Parse psi4 data to fermion operator.
    """
    ...

def parse_psi4_data_to_fermion(*args, **kwargs) -> Any:
    """
    Parse psi4 data to fermion operator.
    """
    ...

def simulateHamiltonian_Var(*args, **kwargs) -> Any:
    """
    Simulate a general case of hamiltonian by Trotter-Suzuki approximation.U = exp(-iHt) = (exp(-iH1t/n) * exp(-iH2t/n))^n
    """
    ...

def simulate_hamiltonian_var(*args, **kwargs) -> Any:
    """
    Simulate a general case of hamiltonian by Trotter-Suzuki approximation.U = exp(-iHt) = (exp(-iH1t/n) * exp(-iH2t/n))^n
    """
    ...

def transCC2UCC_Normal(*args, **kwargs) -> Any:
    """
    Generate Hamiltonian form of unitary coupled cluster based on coupled cluster, H = 1j * (T-dagger(T)), then exp(-jHt) = exp(T-dagger(T)).
    """
    ...

def transCC2UCC_Var(*args, **kwargs) -> Any:
    """
    Generate Hamiltonian form of unitary coupled cluster based on coupled cluster, H = 1j * (T-dagger(T)), then exp(-jHt) = exp(T-dagger(T)).
    """
    ...

def trans_cc_2_ucc_normal(*args, **kwargs) -> Any:
    """
    Generate Hamiltonian form of unitary coupled cluster based on coupled cluster, H = 1j * (T-dagger(T)), then exp(-jHt) = exp(T-dagger(T)).
    """
    ...

def trans_cc_2_ucc_var(*args, **kwargs) -> Any:
    """
    Generate Hamiltonian form of unitary coupled cluster based on coupled cluster, H = 1j * (T-dagger(T)), then exp(-jHt) = exp(T-dagger(T)).
    """
    ...

