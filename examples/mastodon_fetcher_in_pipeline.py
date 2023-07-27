import os
from dotenv import load_dotenv
from haystack import Pipeline
from haystack.nodes import PromptNode, PromptTemplate, AnswerParser
from haystack.utils import print_answers
from mastodon_fetcher_haystack.mastodon_fetcher import MastodonFetcher

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
mastodon_fetcher = MastodonFetcher()

promot_template = PromptTemplate(prompt="Given the follwing Mastodon posts stream, create a short summary of the topics the account posts about. Mastodon posts stream: {join(documents)};\n Answer:",
                                        output_parser=AnswerParser())
prompt_node = PromptNode(default_prompt_template= promot_template, model_name_or_path="text-davinci-003", api_key=OPENAI_API_KEY)

pipe = Pipeline()
pipe.add_node(component=mastodon_fetcher, name="MastodonFetcher", inputs=["Query"])
pipe.add_node(component=prompt_node, name="PromptNode", inputs=["MastodonFetcher"])
result = pipe.run(query="rossng@indieweb.social")
print_answers(result, details="minimum")