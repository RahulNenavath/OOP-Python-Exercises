import time
import functools

attempt_count = 0

def validate_types(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        required_annotations = func.__annotations__
        
        for k, v in zip(args, required_annotations.values()):
            if not isinstance(k, v):
                raise TypeError(f"{k} type is {type(k)}, but not {v}")
        
        return func(*args)
    return wrapper

def execution_timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args)
        end = time.time() - start
        print(f'[EXECUTION TIME]: {end}')
        return result
    return wrapper

def retry_on_failure(max_attempts=3, delay_seconds=0.5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):                       # layer 3: runs on each call
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise  # re-raise after final attempt
                    print(f"[RETRY] Attempt {attempt} failed: {e}. Retrying in {delay_seconds}s...")
                    time.sleep(delay_seconds)
                    
        return wrapper
    return decorator


@retry_on_failure(max_attempts=3, delay_seconds=0.5)
def unstable_api_call() -> str:
    global attempt_count
    attempt_count += 1
    if attempt_count < 3:
        raise ConnectionError("Network timeout")
    return "success"

@validate_types
def transfer_funds(amount: float, account_id: int, description: str) -> bool:
    return True

@execution_timer
def heavy_computation(n: int) -> int:
    return sum(range(n))

if __name__ == "__main__":
    transfer_funds(100.0, 42, "rent")       # works fine
    # transfer_funds("hundred", 42, "rent")   # TypeError: 'amount' expected float, got str
    # transfer_funds(100.0, "42", "rent")     # TypeError: 'account_id' expected int, got str
    
    result = heavy_computation(10_000_000)
    print(result)
    
    result = unstable_api_call()
    print(result)
