import concurrent.futures
import time
import contextlib
import asyncio

def run_with_timeout(func, *args, timeout_seconds: int = 45, **kwargs):
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(func, *args, **kwargs)
        try:
            return future.result(timeout=timeout_seconds)
        except concurrent.futures.TimeoutError:
            raise TimeoutError(f"Agent {func.__name__} timed out after {timeout_seconds}s")

def run_with_retry(func, *args, max_retries: int = 2, timeout_seconds: int = 45, retry_delay: float = 2.0, **kwargs):
    attempts = 0
    last_exception = None
    
    while attempts <= max_retries:
        try:
            return run_with_timeout(func, *args, timeout_seconds=timeout_seconds, **kwargs)
        except Exception as e:
            attempts += 1
            last_exception = e
            if attempts <= max_retries:
                print(f"Attempt {attempts} for {func.__name__} failed: {e}. Retrying in {retry_delay}s...")
                time.sleep(retry_delay)
            else:
                print(f"Attempt {attempts} for {func.__name__} failed: {e}. Max retries reached.")
                
    raise last_exception

@contextlib.contextmanager
def with_loading_state(agent_name: str, job_id: str = None):
    # Conditionally import to avoid circular imports
    from store.job_store import job_store
    from store.event_bus import event_bus
    
    def _publish_update(status, message):
        if not job_id: return
        job_store.update_agent_status(job_id, agent_name, status, message)
        job = job_store.get_job(job_id)
        if hasattr(event_bus, 'publish'):
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    asyncio.run_coroutine_threadsafe(
                        event_bus.publish(job_id, {
                            "type": "agent_update",
                            "node": agent_name,
                            "agent_statuses": {k: v.model_dump() for k, v in job.agent_statuses.items()}
                        }), loop
                    )
            except Exception:
                pass

    _publish_update("running", "Processing...")
    try:
        yield
        _publish_update("done", "Completed successfully")
    except Exception as e:
        msg = str(e)
        if len(msg) > 200:
            msg = msg[:197] + "..."
        _publish_update("failed", msg)
        raise
