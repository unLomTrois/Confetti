define confettiai = Character('Confetti AI', color="#831557")

init python:
    import json
    import websocket
    from confetti import Confetti

    confetti = Confetti("127.0.0.1:8188")
    confetti.connect()

    def generate(workflow_name: str):
        # block user input
        global blocked, last_prompt_id
        blocked = True

        with open(renpy.loader.transfn(f"workflows/{workflow_name}.json")) as f:
            renpy.notify("load workflow")
            workflow = json.load(f)

        renpy.notify("queue prompt")

        prompt_id = confetti.queue_prompt(workflow)["prompt_id"]        
        last_prompt_id = prompt_id

        progress = 1
        max_progress = 0
        while True:
            message = confetti.get_message()
            print("message", message)
            if message is None:
                # binary data
                continue
            
            renpy.notify(message["type"])

            data = message["data"]

            if message["type"] == "progress":
                progress = data["value"]
                max_progress = data["max"]
                renpy.notify(f"{message['type']} {progress}/{max_progress}")

            if message["type"] == "executed":
                output = data["output"]
                images = output["images"]

                images_output = []
                for image in images:
                    renpy.notify("saving image...")
                    image_data = confetti.get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
                    with open(os.path.join(renpy.config.gamedir, "images", f"{prompt_id}.png"), 'wb' ) as f:
                        f.write(image_data)
                        renpy.notify("image saved")

                break

        # unblock input
        blocked = False


# You can load images dynamically with screens
screen background(img):
    add img xalign 0.5 yalign 0.5


label start:
    scene white
    confettiai "Hi! This is a prototype of a library to connect Ren'Py and ComfyUI."

label gen:

    python:
        renpy.notify("Start generation")
        renpy.invoke_in_thread(generate, "witch")
    
    while blocked:
        confettiai "Your image is being generated.{w=0.5}{nw}"
        confettiai "Your image is being generated..{w=0.5}{nw}"
        confettiai "Your image is being generated...{w=0.5}{nw}"

    $ renpy.show_screen("background", f"images/{last_prompt_id}.png")

    confettiai "Image generation complete!"

    menu:
        "Generate a new image?"
        "Yes":
            jump gen
        "No":
            pass

    confettiai "The End."

    return
