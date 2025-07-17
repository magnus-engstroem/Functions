from typing import List, Union, Generator, Iterator

class Pipeline:
    def __init__(self):
        self.name = "Test_pipeline"
        pass

    async def on_startup(self):
        # This function is called when the server is started.
        print(f"on_startup:{__name__}")
        pass

    async def on_shutdown(self):
        # This function is called when the server is shutdown.
        print(f"on_shutdown:{__name__}")
        pass

    
    def pipe(self, user_message: str, model_id: str, messages: List[dict], body: dict) -> Union[str, Generator, Iterator]:
        # This function is called when a new user_message is receieved.
        
        print(f"received message from user: {user_message}") #user_message to logs
        return (f"I am a pipeline. Your message was: '{user_message}'. I'm not going to do anything with it tough.") #user_message to the UI