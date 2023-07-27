import pytest
import os
from dotenv import load_dotenv
from twitter_fetcher_haystack.twitter_fetcher import TwitterFethcer
from haystack import Pipeline
from haystack.nodes import PromptNode, PromptTemplate, AnswerParser

load_dotenv()
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
twitter_fetcher = TwitterFethcer(bearer_token=TWITTER_BEARER_TOKEN)

class TestTwitterFetcher():
    
    @pytest.mark.integration
    def test_twitter_fetcher(self):
       twitter_fetcher.run(query="tuanacelik")

    @pytest.mark.integration
    def test_twitter_fetcher_in_pipeline(self):
       promot_template = PromptTemplate(prompt="Given the follwing tweet stream, indicate whether the twitter user has a positive or negative tone. Tweet stream: {join(documents)};\n Answer:",
                                        output_parser=AnswerParser())
       prompt_node = PromptNode(prompt_template = promot_template, model_name_or_path="text-davinci-003", api_key=OPENAI_API_KEY)

       pipe = Pipeline()
       pipe.add_node(component=twitter_fetcher, name="TwitterFetcher", inputs=["Query"])
       pipe.add_node(component=prompt_node, name="PromptNode", inputs=["TwitterFetcher"])
       result = pipe.run(query="tuanacelik")
       print(result)