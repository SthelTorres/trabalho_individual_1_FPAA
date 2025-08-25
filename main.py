# main.py
from __future__ import annotations
from typing import Tuple


def _split_int(n: int, m: int) -> Tuple[int, int]:
    """Divide |n| em (alto, baixo) usando base = 10**m."""
    base = 10 ** m
    high, low = divmod(abs(n), base)
    return high, low


def karatsuba(x: int, y: int, threshold_digits: int = 16) -> int:
    """
    Multiplicação de inteiros via Karatsuba.
    - Suporta números negativos.
    - Usa multiplicação direta quando ambos os operandos têm <= threshold_digits dígitos.
    """
    # Regras de entrada (para permitir testes com falha)
    if not isinstance(x, int) or not isinstance(y, int):
        raise TypeError("x e y devem ser inteiros (int).")
    if not isinstance(threshold_digits, int):
        raise TypeError("threshold_digits deve ser int.")
    if threshold_digits < 1:
        raise ValueError("threshold_digits deve ser >= 1.")

    sign = -1 if (x < 0) ^ (y < 0) else 1
    x, y = abs(x), abs(y)

    # Casos base rápidos
    if x == 0 or y == 0:
        return 0
    if x < 10 or y < 10:
        return sign * (x * y)

    nx = len(str(x))
    ny = len(str(y))
    n = max(nx, ny)

    # Troca para multiplicação direta se "pequeno" o suficiente
    if nx <= threshold_digits and ny <= threshold_digits:
        return sign * (x * y)

    # Metade em dígitos (>=1)
    m = max(1, n // 2)

    # Split decimal
    xh, xl = _split_int(x, m)
    yh, yl = _split_int(y, m)

    # Karatsuba
    z2 = karatsuba(xh, yh, threshold_digits)
    z0 = karatsuba(xl, yl, threshold_digits)
    z1 = karatsuba(xh + xl, yh + yl, threshold_digits) - z2 - z0

    base_m = 10 ** m
    result = (z2 * (base_m ** 2)) + (z1 * base_m) + z0
    return sign * result


def _self_test() -> None:
    """
    Testes com UMA ÚNICA lista:
    - Cada item é (a, b, threshold, expect)
      * expect = "ok"   -> deve calcular normalmente e bater com a*b
      * expect = "erro" -> deve levantar ValueError/TypeError (falha natural)
    """
    tests = [
        # ------ VÁLIDOS ("ok") ------
        (1, 1, 16, "ok"),
        (9999, 9999, 16, "ok"),
        (10**20, 10**20, 16, "ok"),
        (12345678901234567890, 98765432109876543210, 16, "ok"),
        (-10**30, -10**25, 16, "ok"),
        (2, 3, 16, "ok"),
        (1234, 5678, 16, "ok"),
        (2**1000, 2**1000, 16, "ok"),
        (10**100 + 1, 10**100 + 1, 16, "ok"),

        # ------ INVÁLIDOS ("erro") -> falha natural por violar regra ------
        (12, 34, 0, "erro"),        # threshold inválido => ValueError
        ("7", 8, 16, "erro"),       # x não int          => TypeError
        (3.14, 2, 16, "erro"),      # x não int          => TypeError
        (5, 5, 16.0, "erro"),       # threshold não int  => TypeError
    ]

    for a, b, t, expect in tests:
        try:
            got = karatsuba(a, b, threshold_digits=t)
            if expect == "erro":
                raise AssertionError(
                    f"Esperava erro com entrada inválida: a={a}, b={b}, threshold={t}"
                )
            exp = a * b
            assert got == exp, f"Falhou: {a} * {b} => {got} != {exp}"
        except (ValueError, TypeError) as e:
            # Só é OK lançar erro quando o teste marcava "erro"
            assert expect == "erro", (
                f"Não esperava erro para a={a}, b={b}, threshold={t}. "
                f"Recebi {type(e).__name__}: {e}"
            )

    print("OK: todos os testes (válidos e inválidos) se comportaram como esperado.")


def _run_cli() -> None:
    """
    CLI:
    - Sem argumentos: roda _self_test().
    - 2 args: x y
    - 3º arg opcional: threshold_digits (int)
    """
    import sys

    argv = sys.argv[1:]
    if len(argv) == 0:
        _self_test()
        return
    if len(argv) not in (2, 3):
        print("Uso: python main.py <x> <y> [threshold_digits]")
        sys.exit(2)

    x = int(argv[0])
    y = int(argv[1])
    threshold = int(argv[2]) if len(argv) == 3 else 16
    print(karatsuba(x, y, threshold))


if __name__ == "__main__":
    _run_cli()
