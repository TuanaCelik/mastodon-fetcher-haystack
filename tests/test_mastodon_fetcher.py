import pytest
import os
from dotenv import load_dotenv
from mastodon_fetcher_haystack.mastodon_fetcher import MastodonFetcher
from haystack import Pipeline
from haystack.nodes import PromptNode, PromptTemplate, AnswerParser

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
mastodon_fetcher = MastodonFetcher()

class TestMastodonFetcher():
    
    @pytest.mark.integration
    def test_mastodon_fetcher(self):
       mastodon_fetcher.run(query="gogs@mas.to")

    @pytest.mark.integration
    def test_mastodon_fetcher_in_pipeline(self):
       prompt_template = PromptTemplate(prompt="Given the follwing Mastodon posts, indicate whether the account has a positive or negative tone. Mastodon posts {join(documents)};\n Answer:",
                                        output_parser=AnswerParser())
       prompt_node = PromptNode(default_prompt_template = prompt_template, model_name_or_path="text-davinci-003", api_key=OPENAI_API_KEY)

       pipe = Pipeline()
       pipe.add_node(component=mastodon_fetcher, name="MastodonFetcher", inputs=["Query"])
       pipe.add_node(component=prompt_node, name="PromptNode", inputs=["MastodonFetcher"])
       result = pipe.run(query="clonehenge@mas.to")
       assert "answers" in result
