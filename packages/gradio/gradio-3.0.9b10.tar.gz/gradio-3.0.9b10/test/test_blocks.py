import asyncio
import random
import time
import unittest

import pytest

import gradio as gr
from gradio.routes import PredictBody
from gradio.test_data.blocks_configs import XRAY_CONFIG

pytest_plugins = ("pytest_asyncio",)


class TestBlocks(unittest.TestCase):
    maxDiff = None

    def test_xray(self):
        def fake_func():
            return "Hello There"

        xray_model = lambda diseases, img: {
            disease: random.random() for disease in diseases
        }
        ct_model = lambda diseases, img: {disease: 0.1 for disease in diseases}

        with gr.Blocks() as demo:
            gr.Markdown(
                """
            # Detect Disease From Scan
            With this model you can lorem ipsum
            - ipsum 1
            - ipsum 2
            """
            )
            disease = gr.CheckboxGroup(
                choices=["Covid", "Malaria", "Lung Cancer"], label="Disease to Scan For"
            )

            with gr.Tabs():
                with gr.TabItem("X-ray"):
                    with gr.Row():
                        xray_scan = gr.Image()
                        xray_results = gr.JSON()
                    xray_run = gr.Button("Run")
                    xray_run.click(
                        xray_model, inputs=[disease, xray_scan], outputs=xray_results
                    )

                with gr.TabItem("CT Scan"):
                    with gr.Row():
                        ct_scan = gr.Image()
                        ct_results = gr.JSON()
                    ct_run = gr.Button("Run")
                    ct_run.click(
                        ct_model, inputs=[disease, ct_scan], outputs=ct_results
                    )
            textbox = gr.Textbox()
            demo.load(fake_func, [], [textbox])

        config = demo.get_config_file()
        config.pop("version")  # remove version key
        self.assertDictEqual(XRAY_CONFIG, config)

    @pytest.mark.asyncio
    async def test_async_function(self):
        async def wait():
            await asyncio.sleep(0.01)
            return True

        with gr.Blocks() as demo:
            text = gr.Textbox()
            button = gr.Button()
            button.click(wait, [text], [text])

            body = PredictBody(data=1, fn_index=0)
            start = time.time()
            result = await demo.process_api(body)
            end = time.time()
            difference = end - start
            assert difference >= 0.01
            assert result


if __name__ == "__main__":
    unittest.main()
