import re


class Usuario:
    def __init__(self, cpf, email, nome, senha):
        self.cpf: str = ''.join(filter(str.isdigit, cpf))
        self.email: str = email
        self.nome: str = nome
        self.senha: str = senha

        self._raise_if_invalid_cpf()
        self._raise_if_invalid_email()
        self._raise_if_invalid_senha()

    def _raise_if_invalid_cpf(self) -> None:
        if self._is_invalid_cpf():
            raise ValueError('CPF inválido')

    def _raise_if_invalid_email(self) -> None:
        if self._is_invalid_email():
            raise ValueError('Email inválido')

    def _raise_if_invalid_senha(self) -> None:
        if self._is_invalid_senha():
            raise ValueError('Senha inválida')

    def _is_cpf_invalid(self) -> bool:
        if (not isinstance(self.cpf, str)
                or len(self.cpf) != 11
                or self.cpf == self.cpf[0] * 11):
            return True

        def is_equal_to_verifying_digit(cpf_digit: int, remainder: int) -> bool:
            return cpf_digit == 0 if remainder < 2 else cpf_digit == 11 - remainder

        cpf_int_digits = [(int(digit)) for digit in self.cpf]
        first_remainder = sum(cpf_digit * weight for cpf_digit, weight in zip(cpf_int_digits, range(10, 1, -1))) % 11
        second_remainder = sum(cpf_digit * weight for cpf_digit, weight in zip(cpf_int_digits, range(11, 1, -1))) % 11
        return (is_equal_to_verifying_digit(cpf_int_digits[9], first_remainder)
                and is_equal_to_verifying_digit(cpf_int_digits[10], second_remainder))

    def _is_invalid_email(self) -> bool:
        if not isinstance(self.email, str):
            return True
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(email_pattern, self.email) is None

    def _is_invalid_senha(self) -> bool:
        if not isinstance(self.senha, str):
            return True
        return len(self.senha) < 8
