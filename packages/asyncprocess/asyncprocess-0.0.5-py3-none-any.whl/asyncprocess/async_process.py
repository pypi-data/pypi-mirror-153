import asyncio
from asyncprocess.async_task import AsyncTask

class AsyncProcess:
    def __init__(self, debug: bool = False):
        self._debug = debug
        self._init_coros = []
        self._coros = []
        self._stop_coros = []

    def register(self, at: AsyncTask) -> None:
        self._init_coros.append(at.initialize_async())
        self._coros.append(at.run_async())
        self._stop_coros.append(at.stop_async())
    
    def run(self) -> None:
        try:
            asyncio.run(self._run_async())
        except KeyboardInterrupt:
            pass
        except SystemExit:
            pass
        except Exception as ex:
            print(f'EXCEPTION: {ex}')

    async def _run_async(self):
        try:
            if self._debug:
                asyncio.get_event_loop().set_debug(self._debug)
            await asyncio.gather(*self._init_coros)

            if self._debug:
                asyncio.get_event_loop().set_debug(self._debug)
            await asyncio.gather(*self._coros)
        except KeyboardInterrupt:
            pass
        except SystemExit:
            pass
        except Exception as ex:
            print(f'EXCEPTION: {ex}')
        finally:
            if self._debug:
                asyncio.get_event_loop().set_debug(self._debug)
            await asyncio.gather(*self._stop_coros)
