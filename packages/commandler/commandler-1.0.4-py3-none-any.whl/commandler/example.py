#!/usr/bin/env python3
# encoding: utf-8
#
#
# -----------------------------------------------------------------------------

import inspect

from command import (
    register,
    execute,
    enable_debug,
    func_name,
    list_commands,
)

# -----------------------------------------------------------------------------

@register
def one():
    print(f"invoked - {func_name():20}")

# -----------------------------------------------------------------------------

@register
def two():
    print(f"invoked - {func_name():20}")

# -----------------------------------------------------------------------------

@register
def three():
    print(f"invoked - {func_name():20}")

# -----------------------------------------------------------------------------

@register
def four():
    print(f"invoked - {func_name():20}")

# -----------------------------------------------------------------------------

@register
def slack():
    print(f"invoked - {func_name():20}")

# -----------------------------------------------------------------------------

@register
def something(args=None):
    print(f"invoked - {func_name():20}   with args - '{args}'")

# -----------------------------------------------------------------------------

@register
def test():
    print(f"invoked - {func_name():20}")

# -----------------------------------------------------------------------------

@register
def tasty():
    print(f"invoked - {func_name():20}")

# -----------------------------------------------------------------------------

@register
def testy():
    print(f"invoked - {func_name():20}")

# -----------------------------------------------------------------------------

def otherthing(args=None):
    print(f"invoked - {func_name():20}   with args - '{args}'")

# -----------------------------------------------------------------------------

register(otherthing)

# -----------------------------------------------------------------------------

def test_functions():

    print()
    print("Invoking functions to test them")
    print()

    one()
    two()
    three()
    four()
    test()
    tasty()
    testy()
    slack()
    something()
    otherthing()

# -----------------------------------------------------------------------------

def test_execution():
    print()
    print("Testing execution")
    print()


    # execute('testy')
    # execute('tasty')
    execute('something')
    execute('something comes')
    execute('something comes and goes')
    execute('otherthing came and went')

# -----------------------------------------------------------------------------

def main():
    test_execution()

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main()

# -----------------------------------------------------------------------------

