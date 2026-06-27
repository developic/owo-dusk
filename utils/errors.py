# This file is part of owo-dusk.
#
# Copyright (c) 2024-present EchoQuill
#
# Portions of this file are based on code by EchoQuill, licensed under the
# GNU General Public License v3.0 (GPL-3.0).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

from contextlib import contextmanager
from functools import wraps


def suppress_and_log(resource_name="Not mentioned"):
    """
    This is an error wraper decurator with resource_name argument to wrap functions instead of using try-except
    """

    def decorator(func):
        # Ensure doc strings works correctly
        # .. If i ever use any ;)
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except KeyError as e:
                print(f"[ERROR] Missing expected data key '{e}' in {resource_name}")
            except TypeError as e:
                print(f"[ERROR] Type mismatch in {resource_name}: {e}")
            except Exception as e:
                print(f"[ERROR] Unexpected failure in {resource_name}: {e}")
            return None

        return wrapper

    return decorator


@contextmanager
def suppress_and_log_block(resource_name="Not mentioned"):
    """
    Similar to `suppress_and_log` decorator, but for contextlib's `with` blocks
    """
    try:
        # Everything before yield happens when entering the with block
        yield
        # Everything after yield happens if the block finishes successfully

    except KeyError as e:
        print(f"[ERROR] Missing expected data key '{e}' in {resource_name}")
    except TypeError as e:
        print(f"[ERROR] Type mismatch in {resource_name}: {e}")
    except Exception as e:
        print(f"[ERROR] Unexpected failure in {resource_name}: {e}")
