from typing import List, Union, Generator, Iterator
from pydantic import BaseModel, Field

from utils.pipelines.main import (
    get_last_user_message,
    add_or_update_system_message,
    get_tools_specs,
)


from utils.pipelines.auth import (
    get_current_user,
)

class Pipeline:
    class Valves(BaseModel):
        MODEL: str = Field(
            default = 'smollm'
        )

    def __init__(self):
        self.name = "Test_pipeline_2"
        self.valves = self.Valves()
        pass

    async def on_startup(self):
        # This function is called when the server is started.
        print(f"on_startup:{__name__}")
        return(f"Your model is {self.valves.MODEL}")

    async def on_shutdown(self):
        # This function is called when the server is shutdown.
        print(f"on_shutdown:{__name__}")
        pass

    
    def pipe(self, user_message: str, model_id: str, messages: List[dict], body: dict) -> Union[str, Generator, Iterator]:
        # This function is called when a new user_message is receieved.

        return(str(body))