#!/usr/bin/env python3
"""Print the first 10 Fibonacci numbers."""


def fibonacci(n: int) -> list[int]:
    """Generate the first n Fibonacci numbers.
    
    Args:
        n: Number of Fibonacci numbers to generate.
        
    Returns:
        List of the first n Fibonacci numbers.
    """
    if n <= 0:
        return []
    if n == 1:
        return [0]
    
    fib = [0, 1]
    for _ in range(2, n):
        fib.append(fib[-1] + fib[-2])
    return fib


def main() -> None:
    """Print the first 10 Fibonacci numbers."""
    numbers = fibonacci(10)
    print(" ".join(str(num) for num in numbers))


if __name__ == "__main__":
    main()
