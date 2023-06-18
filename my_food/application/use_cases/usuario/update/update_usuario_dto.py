from dataclasses import dataclass


@dataclass
class InputCreateUsuarioDto:
    cpf: str
    email: str
    nome: str
    senha: str


@dataclass
class OutputCreateUsuarioDto:
    cpf: str
    email: str
    nome: str
