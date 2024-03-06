from langchain_community.llms import HuggingFaceEndpoint
from langchain.memory import ConversationBufferWindowMemory
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import initialize_agent
# from langchain.chains import LLMChain
import tools as tools_module
from tools import tools

repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"

llm = HuggingFaceEndpoint(
    repo_id=repo_id,
    temperature=0.5,
    streaming=True
)

memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    k=5,
    return_messages=True,
    # output_key="output"
)

example_conversation = """Here is an example of a previous conversation between User and Assistant:
---
User: Hey how are you today?
Assistant: ```json
{{"action": "Final Answer",
 "action_input": "I'm good thanks, how are you?"}}
```
User: I'm great, what is the length of the word educate?
Assistant: ```json
{{"action": "Word Length Tool",
 "action_input": "educate"}}
```
User: 7
Assistant: ```json
{{"action": "Final Answer",
 "action_input": "It looks like the answer is 7!"}}
```
User: Who is Olivia Wilde's husband?
Assistant: ```json
{{"action": "duckduckgo_search",
 "action_input": "Who is Olivia Wilde's husband"}}
```
User: September 21, 2022: Olivia Wilde says kids\' happiness remains top priority for her and Jason Sudeikis. During an appearance on The Kelly Clarkson Show, Wilde talked about the ups and downs of ... Olivia Wilde is "quietly dating again" following her November 2022 split from. Harry Styles, a source exclusively tells Life & Style. "The man she\'s with is \'normal\' by Hollywood ... Wilde honored Sudeikis with a sweet tribute on his 42nd birthday. "I have approximately one billion pictures of this guy, my partner in life-crime, who was born on this day in 1975, but this one ... November 18, 2022: Olivia Wilde and Harry Styles are "taking a break". After nearly two years together, Wilde and Styles are pressing pause on their romance. Multiple sources confirmed exclusively ... Wilde told Allure in October 2013 that when she first met Sudeikis she "thought he was so charming." "He\'s a great dancer, and I\'m a sucker for great dancers," she said at the time. "But he didn\'t ...
Assistant: ```json
{{"action": "Final Answer",
 "action_input": "Jason Sudeikis"}}
```
User: What is his age raised to the 3rd power?
Assistant: ```json
{{"action": "duckduckgo_search",
 "action_input": "What is Jason Sudeikis age?"}}
```
User: Jason Sudeikis (born September 18, 1975, Fairfax, Virginia, U.S.) American comedian, actor, and writer who first garnered attention for his work (2003-13) on the TV show Saturday Night Live ( SNL) and later starred in the hugely popular series Ted Lasso (2020-23). Early life and improv comedy Parents Jason Sudeikis and Olivia Wilde\'s 2 Kids: All About Daisy and Otis Jason Sudeikis and Olivia Wilde welcomed two children together before their split in 2020 By Jacqueline Weiss... The Ted of 2013 is a classic Jason Sudeikis character of the time. Sudeikis came up on Saturday Night Live , where he made the most of his 6-foot height and square jaw by largely playing jerks. Sudeikis looks a little bleary-eyed after flying in from Los Angeles with his children, Otis and Daisy, aged nine and six, but he is assiduously polite and attentive. His language can be quaintly... Jason Sudeikis rose to fame on "Saturday Night Live" with his comedic talent, and his children seemed to have inherited it. Sudeikis, who shares kids Otis, 9, and Daisy, 7, with ex Olivia ...
Assistant: ```json
{{"action": "Calculator",
 "action_input": "47**3"}}
```
User: 103823
Assistant: ```json
{{"action": "Final Answer",
 "action_input": "103823"}}
```
---
"""

B_INST, E_INST = "<|im_start|>user\n", "<|im_end|>\n" #Instruction begin and end
B_SYS, E_SYS = "<|im_start|>system\n", "<|im_end|>\n" #System message begin and end

# Define a new system prompt
sys_msg = B_SYS + """You are Assistant named Aditya. Assistant is a expert JSON builder designed to assist with a wide range of tasks.

Assistant is able to respond to the User and use tools using JSON strings that contain "action" and "action_input" parameters.

All of Assistant's communication is performed using this JSON format. The assistant NEVER outputs anything other than a json object with an action and action_input fields!

Assistant can also use tools by responding to the user with tool use instructions in the same "action" and "action_input" JSON format. Tools available to Assistant are:

"""+"""\n""".join([f"> {tool.name}: {tool.description}" for tool in tools])+"""
Here is an example of a previous conversation between User and Assistant:
---
User: Hey how are you today?
Assistant: ```json
{{"action": "Final Answer",
 "action_input": "I'm good thanks, how are you?"}}
```
User: I'm great, what is the length of the word educate?
Assistant: ```json
{{"action": "Word Length Tool",
 "action_input": "educate"}}
```
User: 7
Assistant: ```json
{{"action": "Final Answer",
 "action_input": "It looks like the answer is 7!"}}
```
User: Who is Olivia Wilde's husband?
Assistant: ```json
{{"action": "duckduckgo_search",
 "action_input": "Who is Olivia Wilde's husband"}}
```
User: September 21, 2022: Olivia Wilde says kids\' happiness remains top priority for her and Jason Sudeikis. During an appearance on The Kelly Clarkson Show, Wilde talked about the ups and downs of ... Olivia Wilde is "quietly dating again" following her November 2022 split from. Harry Styles, a source exclusively tells Life & Style. "The man she\'s with is \'normal\' by Hollywood ... Wilde honored Sudeikis with a sweet tribute on his 42nd birthday. "I have approximately one billion pictures of this guy, my partner in life-crime, who was born on this day in 1975, but this one ... November 18, 2022: Olivia Wilde and Harry Styles are "taking a break". After nearly two years together, Wilde and Styles are pressing pause on their romance. Multiple sources confirmed exclusively ... Wilde told Allure in October 2013 that when she first met Sudeikis she "thought he was so charming." "He\'s a great dancer, and I\'m a sucker for great dancers," she said at the time. "But he didn\'t ...
Assistant: ```json
{{"action": "Final Answer",
 "action_input": "Jason Sudeikis"}}
```
User: What is his age raised to the 3rd power?
Assistant: ```json
{{"action": "duckduckgo_search",
 "action_input": "What is Jason Sudeikis age?"}}
```
User: Jason Sudeikis (born September 18, 1975, Fairfax, Virginia, U.S.) American comedian, actor, and writer who first garnered attention for his work (2003-13) on the TV show Saturday Night Live ( SNL) and later starred in the hugely popular series Ted Lasso (2020-23). Early life and improv comedy Parents Jason Sudeikis and Olivia Wilde\'s 2 Kids: All About Daisy and Otis Jason Sudeikis and Olivia Wilde welcomed two children together before their split in 2020 By Jacqueline Weiss... The Ted of 2013 is a classic Jason Sudeikis character of the time. Sudeikis came up on Saturday Night Live , where he made the most of his 6-foot height and square jaw by largely playing jerks. Sudeikis looks a little bleary-eyed after flying in from Los Angeles with his children, Otis and Daisy, aged nine and six, but he is assiduously polite and attentive. His language can be quaintly... Jason Sudeikis rose to fame on "Saturday Night Live" with his comedic talent, and his children seemed to have inherited it. Sudeikis, who shares kids Otis, 9, and Daisy, 7, with ex Olivia ...
Assistant: ```json
{{"action": "Calculator",
 "action_input": "47**3"}}
```
User: 103823
Assistant: ```json
{{"action": "Final Answer",
 "action_input": "103823"}}
```
User: Please generate a Image of Cute Girl sitting in Park Bench in Heavy Rain smiling with a Golden Retriver Adult Dog with its company in the Style of Studio Ghibli art
AI: ```json
{{"action": "Studio Ghilbli Art",
 "action_input": "Cute Girl sitting in Park Bench in Heavy Rain smiling with a Golden Retriver Adult Dog with its company"}}
```
User: https://0x0.st/H7YF.jpg
Assistant:```json
{{
  "action": "Final Answer",
  "action_input": "Image has been Generated.Image URL is https://0x0.st/H7YF.jpg"
}}
```
---
Assistant is very intelligent and knows it's limitations, so it will always try to use a tool when applicable, even if Assistant thinks it knows the answer!
Notice that after Assistant uses a tool, User will give the output of that tool. Then this output can be returned as a final answer.
Assistant will only use the available tools and NEVER a tool not listed. If the User's question does not require the use of a tool, Assistant will use the "Final Answer" action to give a normal response.
""" + E_SYS

# llm_chain = LLMChain(
#     llm=llm,
#     prompt=prompt,
#     memory=memory
# )

agent = initialize_agent(
    agent="chat-conversational-react-description",
    tools=tools,
    llm=llm,
    verbose=True,
    early_stopping_method="generate",
    memory=memory,
    handle_parsing_errors=True,
)

new_prompt = agent.agent.create_prompt(
    system_message=sys_msg,
    tools=tools
)
agent.agent.llm_chain.prompt = new_prompt

instruction = B_INST + "Respond to the following in JSON with 'action' and 'action_input' values. Once you have outputted the JSON, stop outputting and output nothing else!"
human_msg = instruction + "\nUser: {input}" + E_INST

agent.agent.llm_chain.prompt.messages[2].prompt.template = human_msg