import gradio as gr
import random
import time
import modules.scripts as scripts
from modules import processing
from modules.processing import Processed
from modules.shared import state

class Script(scripts.Script):
    def __init__(self):
        # Defining Default Resolution Values as Class Properties
        self.default_resolutions = [
            (1024, 1024),
            (1344, 768),
            (1216, 832),
            (1152, 896),
            (896, 1152),
            (832, 1216),
            (768, 1334),
            (0, 0),
            (0, 0)
        ]

    def title(self):
        return "Random-Resolution"

    def show(self, is_img2img):
        return True
    
    def ui(self, is_img2img):
        with gr.Group():
            with gr.Row():
                enable_random = gr.Checkbox(label="Enable Random Resolution", value=False)
            
            # UI components for nine resolution settings
            resolution_rows = []
            
            for i in range(9):
                with gr.Row():
                    with gr.Column(scale=1):
                        use_resolution = gr.Checkbox(label=f"#{i+1}", value=True if i < 7 else False)
                    with gr.Column(scale=4):
                        with gr.Row():
                            width = gr.Number(
                                label="Width",
                                value=self.default_resolutions[i][0], 
                                precision=0,
                                step=8
                            )
                            gr.HTML("×", elem_classes="resolution-separator")
                            height = gr.Number(
                                label="Height",
                                value=self.default_resolutions[i][1], 
                                precision=0,
                                step=8
                            )
                    resolution_rows.append((use_resolution, width, height))
            
            with gr.Row():
                batch_count = gr.Slider(minimum=1, maximum=999, step=1, label="Number of Batches", value=1)
                delay_time = gr.Number(label="Delay between batches (seconds)", value=0, precision=1)

            # Add CSS Style
            gr.HTML("""
                <style>
                    .resolution-separator {
                        padding: 0 5px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    }
                    /* Number Adjust the width of the input field */
                    input[type=number] {
                        width: 6em !important;
                    }
                </style>
            """)
        
        # Consolidate UI components into one list
        return [enable_random, batch_count, delay_time] + [item for row in resolution_rows for item in row]

    def run(self, p, enable_random, batch_count, delay_time, *resolution_args):
        # Reconfigure resolution_args for ease of use
        resolutions = []
        for i in range(0, len(resolution_args), 3):
            use_res = resolution_args[i]
            width = int(resolution_args[i + 1]) if resolution_args[i + 1] is not None else 0
            height = int(resolution_args[i + 2]) if resolution_args[i + 2] is not None else 0
            
            if use_res and width > 0 and height > 0:
                resolutions.append((width, height))
        
        if not resolutions:
            print("No valid resolutions selected. Using default resolution.")
            return processing.process_images(p)
        
        batch_count = int(batch_count)
        state.job_count = batch_count

        images_list = []
        all_prompts = []
        infotexts = []
        
        # Processing by each batch
        for i in range(batch_count):
            state.job = f"{i+1} out of {batch_count}"
            
            if state.interrupted:
                break
                
            # Random selection only when random resolution selection is enabled
            if enable_random and resolutions:
                selected_width, selected_height = random.choice(resolutions)
                p.width = selected_width
                p.height = selected_height
            
            # Image creation processing
            proc = processing.process_images(p)
            
            # Save results
            images_list.extend(proc.images)
            all_prompts.extend(proc.all_prompts)
            infotexts.extend(proc.infotexts)
            
            # Apply delay only if it is not the last batch
            if i < batch_count - 1:
                time.sleep(delay_time)
            
            # Update seed value (for next batch)
            p.seed = random.randint(0, 2**32 - 1)
        
        return Processed(
            p,
            images_list,
            p.seed,
            "",
            all_prompts=all_prompts,
            infotexts=infotexts
        )