"""dspyfun REST API."""

import asyncio
import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import coloredlogs
import dspy
from fastapi import FastAPI
from pydantic import BaseModel, Field


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Handle FastAPI startup and shutdown events."""
    # Startup events:
    # - Remove all handlers associated with the root logger object.
    for handler in logging.root.handlers:
        logging.root.removeHandler(handler)
    # - Add coloredlogs' colored StreamHandler to the root logger.
    coloredlogs.install()
    yield
    # Shutdown events.


app = FastAPI(lifespan=lifespan)


def fibonacci(n: int, memo=None) -> int:
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fibonacci(n - 1, memo) + fibonacci(n - 2, memo)
    return memo[n]


@app.get("/compute")
async def compute(n: int = 42) -> int:
    """Compute the result of a CPU-bound function."""

    result = await asyncio.to_thread(fibonacci, n, {})
    return result


class LastFibInt(BaseModel):
    last_fib_int: int = Field(..., description="The last Fibonacci number.")


@app.get("/io")
async def io(n: int = 42) -> int:
    """Compute the result of an I/O-bound function."""
    from dspygen.utils.dspy_tools import init_dspy
    init_dspy()

    from dspygen.modules.json_module import json_call
    last = json_call(LastFibInt, text=f"What is the {n}th Fibonacci number?")
    # print(f"Last Fibonacci number for {n=}: {fibonacci(n, {})}")

    # fib = dspy.Predict("n -> last_fib_int")(n=str(n)).last_fib_int

    return last.last_fib_int
