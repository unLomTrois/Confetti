import websocket # websocket-client 
import uuid
import json
import urllib.request
import urllib.parse
import random
from typing import Any

class Confetti:
    def __init__(self, server_address: str):
        self.server_address = server_address
        self.client_id = str(uuid.uuid4())
        self.ws = websocket.WebSocket()
        
    def connect(self) -> None:
        """Connects to ComfyUI API
        """
        url = f"ws://{self.server_address}/ws?clientId={self.client_id}"
        self.ws.connect(url)

    def get_message(self):
        out = self.ws.recv()
        if not isinstance(out, str):
            # previews are binary data
            return
        message = json.loads(out)
        return message

    def queue_prompt(self, worklflow: dict[Any, Any]):
        worklflow["7"]["inputs"]["seed"] = random.getrandbits(64)
        p = {"prompt": worklflow, "client_id": self.client_id}
        data = json.dumps(p).encode('utf-8')
        url = f"http://{self.server_address}/prompt"
        req =  urllib.request.Request(url, data=data)
        return json.loads(urllib.request.urlopen(req).read())

    def get_image(self, filename: str, subfolder: str, folder_type: str):
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        url = "http://{}/view?{}".format(self.server_address, url_values)
        print("url to preview", url)
        with urllib.request.urlopen(url) as response:
            return response.read()

    def get_history(self, prompt_id: str):
        url = "http://{}/history/{}".format(self.server_address, prompt_id)
        print("url to history", url)
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
            return data[prompt_id]

    def get_image_from_history(self, history):
        outputs = history['outputs']
        output_images = []
        for node_id in outputs:
            node_output = outputs[node_id]
            if "images" not in node_output:
                continue
            image_output = []
            for image in node_output["images"]:
                image_data = self.get_image(image['filename'], image['subfolder'], image['type'])
                image_output.append(image_data)
            
            output_images.append(image_output)

        return output_images

    def get_images(self, prompt: str):
        prompt_id = self.queue_prompt(prompt)['prompt_id']
        i = 0
        images_data = []
        print("prompt_id", prompt_id)
        while True:
            out = self.ws.recv()
            if not isinstance(out, str):
                continue
            
            message = json.loads(out)
            print(i, message)
            i += 1
            if message['type'] == 'executed':
                data = message["data"]
                output = data["output"]
                images_data = output["images"]
                break
    
        images_output = []
        for image in images_data:
            image_data = self.get_image(image['filename'], image['subfolder'], image['type'])
            images_output.append(image_data)
    
        return prompt_id, images_output
