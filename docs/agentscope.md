# agentscope.message

The message module in agentscope.

*class*TextBlock[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/message/_message_block.html#TextBlock)基类：`<span class="pre">TypedDict</span>`

The text block.

**type***:**Required**[**Literal**[**'text'**]**]***The type of the block

**text***:**str***The text content

*class*ThinkingBlock[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/message/_message_block.html#ThinkingBlock)基类：`<span class="pre">TypedDict</span>`

The thinking block.

**type***:**Required**[**Literal**[**'thinking'**]**]***The type of the block

**thinking***:**str***

*class*Base64Source[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/message/_message_block.html#Base64Source)基类：`<span class="pre">TypedDict</span>`

The base64 source

**type***:**Required**[**Literal**[**'base64'**]**]***The type of the src, must be base64

**media_type***:**Required**[**str**]*The media type of the data, e.g. image/jpeg or audio/mpeg

**data***:**Required**[**str**]*The base64 data, in format of RFC 2397

*class*URLSource[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/message/_message_block.html#URLSource)基类：`<span class="pre">TypedDict</span>`

The URL source

**type***:**Required**[**Literal**[**'url'**]**]***The type of the src, must be url

**url***:**Required**[**str**]*The URL of the image or audio

*class*ImageBlock[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/message/_message_block.html#ImageBlock)基类：`<span class="pre">TypedDict</span>`

The image block

**type***:**Required**[**Literal**[**'image'**]**]***The type of the block

**source***:**Required**[[Base64Source](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Base64Source "agentscope.message._message_block.Base64Source")|[URLSource](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.URLSource "agentscope.message._message_block.URLSource")]*The src of the image

*class*AudioBlock[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/message/_message_block.html#AudioBlock)基类：`<span class="pre">TypedDict</span>`

The audio block

**type***:**Required**[**Literal**[**'audio'**]**]***The type of the block

**source***:**Required**[[Base64Source](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Base64Source "agentscope.message._message_block.Base64Source")|[URLSource](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.URLSource "agentscope.message._message_block.URLSource")]*The src of the audio

*class*VideoBlock[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/message/_message_block.html#VideoBlock)基类：`<span class="pre">TypedDict</span>`

The video block

**type***:**Required**[**Literal**[**'video'**]**]***The type of the block

**source***:**Required**[[Base64Source](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Base64Source "agentscope.message._message_block.Base64Source")|[URLSource](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.URLSource "agentscope.message._message_block.URLSource")]*The src of the audio

*class*ToolUseBlock[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/message/_message_block.html#ToolUseBlock)基类：`<span class="pre">TypedDict</span>`

The tool use block.

**type***:**Required**[**Literal**[**'tool_use'**]**]***The type of the block, must be tool_use

**id***:**Required**[**str**]*The identity of the tool call

**name***:**Required**[**str**]*The name of the tool

**input***:**Required**[**dict**[**str**,**object**]**]***The input of the tool

*class*ToolResultBlock[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/message/_message_block.html#ToolResultBlock)基类：`<span class="pre">TypedDict</span>`

The tool result block.

**type***:**Required**[**Literal**[**'tool_result'**]**]***The type of the block

**id***:**Required**[**str**]*The identity of the tool call result

**output***:**Required**[**str**|**List**[[TextBlock](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.TextBlock "agentscope.message._message_block.TextBlock")|[ImageBlock](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.ImageBlock "agentscope.message._message_block.ImageBlock")|[AudioBlock](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.AudioBlock "agentscope.message._message_block.AudioBlock")]**]***The output of the tool function

**name***:**Required**[**str**]*The name of the tool function

*class*Msg[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/message/_message_base.html#Msg)基类：`<span class="pre">object</span>`

The message class in agentscope.

**__init__**( *name* ,  *content* ,  *role* ,  *metadata**=**None* ,  *timestamp**=**None* ,  *invocation_id**=**None* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/message/_message_base.html#Msg.__init__)Initialize the Msg object.

参数**:**

* **name** (str) -- The name of the message sender.
* **content** (str | list[ContentBlock]) -- The content of the message.
* **role** (Literal["user", "assistant", "system"]) -- The role of the message sender.
* **metadata** (dict[str, JSONSerializableObject] | None, optional) -- The metadata of the message, e.g. structured output.
* **timestamp** (str | None, optional) -- The created timestamp of the message. If not given, the
  timestamp will be set automatically.
* **invocation_id** (str | None, optional) -- The related API invocation id, if any. This is useful for
  tracking the message in the context of an API call.

返回类型**:**
None

**to_dict**(**)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/message/_message_base.html#Msg.to_dict)Convert the message into JSON dict data.

返回类型**:**
dict

*classmethod*from_dict**(** *json_data* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/message/_message_base.html#Msg.from_dict)Load a message object from the given JSON data.

参数**:**
**json_data** ( *dict* )

返回类型**:**
[*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message._message_base.Msg")

**has_content_blocks**( *block_type**=**None* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/message/_message_base.html#Msg.has_content_blocks)Check if the message has content blocks of the given type.

参数**:**
**block_type** ( *Literal*  *[*  *"text"*  *, *  *"tool_use"*  *, *  *"tool_result"*  *, *  *"image"*  *,             *  *"audio"*  *, *  *"video"*  *] * *| * *None* *, * *defaults to None* ) -- The type of the block to be checked. If None, it will
check if there are any content blocks.

返回类型**:**
bool

**get_text_content**(**)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/message/_message_base.html#Msg.get_text_content)Get the pure text blocks from the message content.

返回类型**:**
str | None

**get_content_blocks**( *block_type**:**Literal**[**'text'**]*** **)** **→** **List**[[TextBlock](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.TextBlock "agentscope.message._message_block.TextBlock")][[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/message/_message_base.html#Msg.get_content_blocks)
**get_content_blocks**( *block_type**:**Literal**[**'tool_use'**]*** **)** **→** **List**[[ToolUseBlock](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.ToolUseBlock "agentscope.message._message_block.ToolUseBlock")]

**get_content_blocks**( *block_type**:**Literal**[**'tool_result'**]*** **)** **→** **List**[[ToolResultBlock](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.ToolResultBlock "agentscope.message._message_block.ToolResultBlock")]

**get_content_blocks**( *block_type**:**Literal**[**'image'**]*** **)** **→** **List**[[ImageBlock](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.ImageBlock "agentscope.message._message_block.ImageBlock")]

**get_content_blocks**( *block_type**:**Literal**[**'audio'**]*** **)** **→** **List**[[AudioBlock](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.AudioBlock "agentscope.message._message_block.AudioBlock")]

**get_content_blocks**( *block_type**:**Literal**[**'video'**]*** **)** **→** **List**[[VideoBlock](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.VideoBlock "agentscope.message._message_block.VideoBlock")]

**get_content_blocks**( *block_type**:**None**=**None* **)** **→** **List**[[ToolUseBlock](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.ToolUseBlock "agentscope.message._message_block.ToolUseBlock")|[ToolResultBlock](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.ToolResultBlock "agentscope.message._message_block.ToolResultBlock")|[TextBlock](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.TextBlock "agentscope.message._message_block.TextBlock")|[ThinkingBlock](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.ThinkingBlock "agentscope.message._message_block.ThinkingBlock")|[ImageBlock](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.ImageBlock "agentscope.message._message_block.ImageBlock")|[AudioBlock](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.AudioBlock "agentscope.message._message_block.AudioBlock")|[VideoBlock](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.VideoBlock "agentscope.message._message_block.VideoBlock")]
Get the content in block format. If the content is a string,
it will be converted to a text block.

参数**:**
**block_type** (Literal["text", "thinking", "tool_use",             "tool_result", "image", "audio", "video"] | None, optional) -- The type of the block to be extracted. If None, all blocks
will be returned.

返回**:**
The content blocks.

返回类型**:**
List[ContentBlock]



# agentscope.model

The model module.

*class*ChatModelBase[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_model_base.html#ChatModelBase)基类：`<span class="pre">object</span>`

Base class for chat models.

**__init__**( *model_name* ,  *stream* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_model_base.html#ChatModelBase.__init__)Initialize the chat model base class.

参数**:**

* **model_name** (str) -- The name of the model
* **stream** (bool) -- Whether the model output is streaming or not

返回类型**:**
None

**model_name***:**str***The model name

**stream***:**bool***Is the model output streaming or not

 *abstract**async*** **__call__**( ****args*** ,  ***kwargs* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_model_base.html#ChatModelBase.__call__)Call self as a function.

参数**:**

* **args** ( *Any* )
* **kwargs** ( *Any* )

返回类型**:**
[*ChatResponse*](https://doc.agentscope.io/zh_CN/api/agentscope.model.html#agentscope.model.ChatResponse "agentscope.model._model_response.ChatResponse") |  *AsyncGenerator* [[*ChatResponse*](https://doc.agentscope.io/zh_CN/api/agentscope.model.html#agentscope.model.ChatResponse "agentscope.model._model_response.ChatResponse"), None]

*class*ChatResponse[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_model_response.html#ChatResponse)基类：`<span class="pre">DictMixin</span>`

The response of chat models.

**content***:**Sequence**[[TextBlock](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.TextBlock "agentscope.message._message_block.TextBlock")|[ToolUseBlock](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.ToolUseBlock "agentscope.message._message_block.ToolUseBlock")|[ThinkingBlock](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.ThinkingBlock "agentscope.message._message_block.ThinkingBlock")|[AudioBlock](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.AudioBlock "agentscope.message._message_block.AudioBlock")]*The content of the chat response, which can include text blocks,
tool use blocks, or thinking blocks.

**id***:**str***The unique identifier formatter

**created_at***:**str***When the response was created

**__init__**( *content* ,  *id=`<factory>`* ,  *created_at=`<factory>`* ,  *type=`<factory>`* ,  *usage=`<factory>`* ,  *metadata=`<factory>`* **)**
参数**:**

* **content** ( *Sequence*  *[* [*TextBlock*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.TextBlock "agentscope.message._message_block.TextBlock")* | *[*ToolUseBlock*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.ToolUseBlock "agentscope.message._message_block.ToolUseBlock")* | *[*ThinkingBlock*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.ThinkingBlock "agentscope.message._message_block.ThinkingBlock")* | *[*AudioBlock*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.AudioBlock "agentscope.message._message_block.AudioBlock") *]* )
* **id** ( *str* )
* **created_at** ( *str* )
* **type** ( *Literal*  *[*  *'chat'*  *]* )
* **usage** (*ChatUsage** | * *None* )
* **metadata** ( *dict*  *[*  *str* *, **str** | **int** | **float** | **bool** | **None** | * *list*  *[*  *JSONSerializableObject*  *] * *| * *dict*  *[*  *str* *, * *JSONSerializableObject*  *]*  *] * *| * *None* )

返回类型**:**
None

**type***:**Literal**[**'chat'**]*The type of the response, which is always 'chat'.

**usage***:**ChatUsage**|**None***The usage information of the chat response, if available.

**metadata***:**dict**[**str**,**str**|**int**|**float**|**bool**|**None**|**list**[**JSONSerializableObject**]**|**dict**[**str**,**JSONSerializableObject**]**]**|**None*The metadata of the chat response

*class*DashScopeChatModel[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_dashscope_model.html#DashScopeChatModel)基类：[`<span class="pre">ChatModelBase</span>`](https://doc.agentscope.io/zh_CN/api/agentscope.model.html#agentscope.model.ChatModelBase "agentscope.model._model_base.ChatModelBase")

The DashScope chat model class, which unifies the Generation and
MultimodalConversation APIs into one method.

**__init__**( *model_name* ,  *api_key* ,  *stream**=**True* ,  *enable_thinking**=**None* ,  *generate_kwargs**=**None* ,  *base_http_api_url**=**None* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_dashscope_model.html#DashScopeChatModel.__init__)Initialize the DashScope chat model.

参数**:**

* **model_name** (str) -- The model names.
* **api_key** (str) -- The dashscope API key.
* **stream** (bool) -- The streaming output or not
* **enable_thinking** (bool | None, optional) -- Enable thinking or not, only support Qwen3, QwQ, DeepSeek-R1.
  Refer to [DashScope documentation](https://help.aliyun.com/zh/model-studio/deep-thinking)
  for more details.
* **generate_kwargs** (dict[str, JSONSerializableObject] | None,             optional) -- The extra keyword arguments used in DashScope API generation,
  e.g. temperature, seed.
* **base_http_api_url** (str | None, optional) -- The base URL for DashScope API requests. If not provided,
  the default base URL from the DashScope SDK will be used.

返回类型**:**
None

 *async* **__call__**( *messages* ,  *tools**=**None* ,  *tool_choice**=**None* ,  *structured_model**=**None* ,  ***kwargs* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_dashscope_model.html#DashScopeChatModel.__call__)Get the response from the dashscope
Generation/MultimodalConversation API by the given arguments.

备注

We unify the dashscope generation and multimodal conversation
APIs into one method, since they support similar arguments and share
the same functionality.

参数**:**

* **messages** (list[dict[str, Any]]) -- A list of dictionaries, where role and content fields are
  required.
* **tools** (list[dict] | None, default None) -- The tools JSON schemas that the model can use.
* **tool_choice** (Literal["auto", "none", "any", "required"] | str              |  None,  default None) --

  Controls which (if any) tool is called by the model.Can be "auto", "none", or specific tool name.
  For more details, please refer to
  [https://help.aliyun.com/zh/model-studio/qwen-function-calling](https://help.aliyun.com/zh/model-studio/qwen-function-calling)
* **structured_model** (Type[BaseModel] | None, default None) --
  A Pydantic BaseModel class that defines the expected structure
  for the model's output. When provided, the model will be forced
  to return data that conforms to this schema by automatically
  converting the BaseModel to a tool function and setting
  tool_choice to enforce its usage. This enables structured
  output generation.

  备注

  When structured_model is specified,
  both tools and tool_choice parameters are ignored,
  and the model will only perform structured output
  generation without calling any other tools.
* ****kwargs** (Any) --
  The keyword arguments for DashScope chat completions API,
  e.g. temperature, max_tokens, top_p, etc. Please
  refer to [DashScope documentation](https://help.aliyun.com/zh/dashscope/developer-reference/api-details)
  for more detailed arguments.

返回类型**:**
[*ChatResponse*](https://doc.agentscope.io/zh_CN/api/agentscope.model.html#agentscope.model.ChatResponse "agentscope.model._model_response.ChatResponse") |  *AsyncGenerator* [[*ChatResponse*](https://doc.agentscope.io/zh_CN/api/agentscope.model.html#agentscope.model.ChatResponse "agentscope.model._model_response.ChatResponse"), None]

*class*OpenAIChatModel[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_openai_model.html#OpenAIChatModel)基类：[`<span class="pre">ChatModelBase</span>`](https://doc.agentscope.io/zh_CN/api/agentscope.model.html#agentscope.model.ChatModelBase "agentscope.model._model_base.ChatModelBase")

The OpenAI chat model class.

**__init__**( *model_name* ,  *api_key**=**None* ,  *stream**=**True* ,  *reasoning_effort**=**None* ,  *organization**=**None* ,  *client_args**=**None* ,  *generate_kwargs**=**None* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_openai_model.html#OpenAIChatModel.__init__)Initialize the openai client.

参数**:**

* **model_name** (str, default None) -- The name of the model to use in OpenAI API.
* **api_key** (str, default None) -- The API key for OpenAI API. If not specified, it will
  be read from the environment variable OPENAI_API_KEY.
* **stream** (bool, default True) -- Whether to use streaming output or not.
* **reasoning_effort** (Literal["low", "medium", "high"] | None,             optional) -- Reasoning effort, supported for o3, o4, etc. Please refer to
  [OpenAI documentation](https://platform.openai.com/docs/guides/reasoning?api-mode=chat)
  for more details.
* **organization** (str, default None) -- The organization ID for OpenAI API. If not specified, it will
  be read from the environment variable OPENAI_ORGANIZATION.
* **client_args** (dict, default None) -- The extra keyword arguments to initialize the OpenAI client.
* **generate_kwargs** (dict[str, JSONSerializableObject] | None,              optional) --

  The extra keyword arguments used in OpenAI API generation,e.g. temperature, seed.

返回类型**:**
None

 *async* **__call__**( *messages* ,  *tools**=**None* ,  *tool_choice**=**None* ,  *structured_model**=**None* ,  ***kwargs* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_openai_model.html#OpenAIChatModel.__call__)Get the response from OpenAI chat completions API by the given
arguments.

参数**:**

* **messages** (list[dict]) -- A list of dictionaries, where role and content fields are
  required, and name field is optional.
* **tools** (list[dict], default None) -- The tools JSON schemas that the model can use.
* **tool_choice** (Literal["auto", "none", "any", "required"] | str             | None, default None) --

  Controls which (if any) tool is called by the model.Can be "auto", "none", "any", "required", or specific tool
  name. For more details, please refer to
  [https://platform.openai.com/docs/api-reference/responses/create#responses_create-tool_choice](https://platform.openai.com/docs/api-reference/responses/create#responses_create-tool_choice)
* **structured_model** (Type[BaseModel] | None, default None) --
  A Pydantic BaseModel class that defines the expected structure
  for the model's output. When provided, the model will be forced
  to return data that conforms to this schema by automatically
  converting the BaseModel to a tool function and setting
  tool_choice to enforce its usage. This enables structured
  output generation.

  备注

  When structured_model is specified,
  both tools and tool_choice parameters are ignored,
  and the model will only perform structured output
  generation without calling any other tools.

  For more details, please refer to the [official document](https://platform.openai.com/docs/guides/structured-outputs)
* ****kwargs** (Any) -- The keyword arguments for OpenAI chat completions API,
  e.g. temperature, max_tokens, top_p, etc. Please
  refer to the OpenAI API documentation for more details.

返回**:**
The response from the OpenAI chat completions API.

返回类型**:**
ChatResponse | AsyncGenerator[ChatResponse, None]

*class*AnthropicChatModel[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_anthropic_model.html#AnthropicChatModel)基类：[`<span class="pre">ChatModelBase</span>`](https://doc.agentscope.io/zh_CN/api/agentscope.model.html#agentscope.model.ChatModelBase "agentscope.model._model_base.ChatModelBase")

The Anthropic model wrapper for AgentScope.

**__init__**( *model_name* ,  *api_key**=**None* ,  *max_tokens**=**2048* ,  *stream**=**True* ,  *thinking**=**None* ,  *client_args**=**None* ,  *generate_kwargs**=**None* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_anthropic_model.html#AnthropicChatModel.__init__)Initialize the Anthropic chat model.

参数**:**

* **model_name** (str) -- The model names.
* **api_key** (str) -- The anthropic API key.
* **stream** (bool) -- The streaming output or not
* **max_tokens** (int) -- Limit the maximum token count the model can generate.
* **thinking** (dict | None, default None) --
  Configuration for Claude's internal reasoning process.

  **Example of thinking**
* ```
  {
      "type": "enabled" | "disabled",
      "budget_tokens": 1024
  }
  ```
* **client_args** (dict | None, optional) -- The extra keyword arguments to initialize the Anthropic client.
* **generate_kwargs** (dict[str, JSONSerializableObject] | None,              optional) -- The extra keyword arguments used in Gemini API generation,
  e.g. temperature, seed.

返回类型**:**
None

 *async* **__call__**( *messages* ,  *tools**=**None* ,  *tool_choice**=**None* ,  *structured_model**=**None* ,  ***generate_kwargs* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_anthropic_model.html#AnthropicChatModel.__call__)Get the response from Anthropic chat completions API by the given
arguments.

参数**:**

* **messages** (list[dict]) -- A list of dictionaries, where role and content fields are
  required, and name field is optional.
* **tools** (list[dict], default None) --
  The tools JSON schemas that in format of:

  **Example of tools JSON schemas**
* ```
  [
      {
          "type": "function",
          "function": {
              "name": "xxx",
              "description": "xxx",
              "parameters": {
                  "type": "object",
                  "properties": {
                      "param1": {
                          "type": "string",
                          "description": "..."
                      },
                      # Add more parameters as needed
                  },
                  "required": ["param1"]
          }
      },
      # More schemas here
  ]
  ```
* **tool_choice** (Literal["auto", "none", "any", "required"] | str             | None, default None) --

  Controls which (if any) tool is called by the model.Can be "auto", "none", "any", "required", or specific tool
  name. For more details, please refer to
  [https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implement-tool-use](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implement-tool-use)
* **structured_model** (Type[BaseModel] | None, default None) --
  A Pydantic BaseModel class that defines the expected structure
  for the model's output. When provided, the model will be forced
  to return data that conforms to this schema by automatically
  converting the BaseModel to a tool function and setting
  tool_choice to enforce its usage. This enables structured
  output generation.

  备注

  When structured_model is specified,
  both tools and tool_choice parameters are ignored,
  and the model will only perform structured output
  generation without calling any other tools.
* ****generate_kwargs** (Any) -- The keyword arguments for Anthropic chat completions API,
  e.g. temperature, top_p, etc. Please
  refer to the Anthropic API documentation for more details.

返回**:**
The response from the Anthropic chat completions API.

返回类型**:**
ChatResponse | AsyncGenerator[ChatResponse, None]

*class*OllamaChatModel[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_ollama_model.html#OllamaChatModel)基类：[`<span class="pre">ChatModelBase</span>`](https://doc.agentscope.io/zh_CN/api/agentscope.model.html#agentscope.model.ChatModelBase "agentscope.model._model_base.ChatModelBase")

The Ollama chat model class in agentscope.

**__init__**( *model_name* ,  *stream**=**False* ,  *options**=**None* ,  *keep_alive**=**'5m'* ,  *enable_thinking**=**None* ,  *host**=**None* ,  ***kwargs* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_ollama_model.html#OllamaChatModel.__init__)Initialize the Ollama chat model.

参数**:**

* **model_name** (str) -- The name of the model.
* **stream** (bool, default True) -- Streaming mode or not.
* **options** (dict, default None) -- Additional parameters to pass to the Ollama API. These can
  include temperature etc.
* **keep_alive** (str, default "5m") -- Duration to keep the model loaded in memory. The format is a
  number followed by a unit suffix (s for seconds, m for minutes
  , h for hours).
* **enable_thinking** (bool | None, default None) -- Whether enable thinking or not, only for models such as qwen3,
  deepseek-r1, etc. For more details, please refer to
  [https://ollama.com/search?c=thinking](https://ollama.com/search?c=thinking)
* **host** (str | None, default None) -- The host address of the Ollama server. If None, uses the
  default address (typically [http://localhost:11434](http://localhost:11434)).
* ****kwargs** (Any) -- Additional keyword arguments to pass to the base chat model
  class.

返回类型**:**
None

 *async* **__call__**( *messages* ,  *tools**=**None* ,  *tool_choice**=**None* ,  *structured_model**=**None* ,  ***kwargs* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_ollama_model.html#OllamaChatModel.__call__)Get the response from Ollama chat completions API by the given
arguments.

参数**:**

* **messages** (list[dict]) -- A list of dictionaries, where role and content fields are
  required, and name field is optional.
* **tools** (list[dict], default None) -- The tools JSON schemas that the model can use.
* **tool_choice** (Literal["auto", "none", "any", "required"] | str                 | None, default None) --

  Controls which (if any) tool is called by the model.Can be "auto", "none", "any", "required", or specific tool
  name.
* **structured_model** (Type[BaseModel] | None, default None) -- A Pydantic BaseModel class that defines the expected structure
  for the model's output.
* ****kwargs** (Any) -- The keyword arguments for Ollama chat completions API,
  e.g. [`](https://doc.agentscope.io/zh_CN/api/agentscope.model.html#id2)think`etc. Please refer to the Ollama API
  documentation for more details.

返回**:**
The response from the Ollama chat completions API.

返回类型**:**
ChatResponse | AsyncGenerator[ChatResponse, None]

*class*GeminiChatModel[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_gemini_model.html#GeminiChatModel)基类：[`<span class="pre">ChatModelBase</span>`](https://doc.agentscope.io/zh_CN/api/agentscope.model.html#agentscope.model.ChatModelBase "agentscope.model._model_base.ChatModelBase")

The Google Gemini chat model class in agentscope.

**__init__**( *model_name* ,  *api_key* ,  *stream**=**True* ,  *thinking_config**=**None* ,  *client_args**=**None* ,  *generate_kwargs**=**None* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_gemini_model.html#GeminiChatModel.__init__)Initialize the Gemini chat model.

参数**:**

* **model_name** (str) -- The name of the Gemini model to use, e.g. "gemini-2.5-flash".
* **api_key** (str) -- The API key for Google Gemini.
* **stream** (bool, default True) -- Whether to use streaming output or not.
* **thinking_config** (dict | None, optional) --
  Thinking config, supported models are 2.5 Pro, 2.5 Flash, etc.
  Refer to [https://ai.google.dev/gemini-api/docs/thinking](https://ai.google.dev/gemini-api/docs/thinking) for
  more details.

  **Example of thinking_config**
* ```
  {
      "include_thoughts": True, # enable thoughts or not
      "thinking_budget": 1024   # Max tokens for reasoning
  }
  ```
* **client_args** (dict, default None) -- The extra keyword arguments to initialize the OpenAI client.
* **generate_kwargs** (dict[str, JSONSerializableObject] | None,              optional) -- The extra keyword arguments used in Gemini API generation,
  e.g. temperature, seed.

返回类型**:**
None

 *async* **__call__**( *messages* ,  *tools**=**None* ,  *tool_choice**=**None* ,  *structured_model**=**None* ,  ***config_kwargs* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/model/_gemini_model.html#GeminiChatModel.__call__)Call the Gemini model with the provided arguments.

参数**:**

* **messages** (list[dict[str, Any]]) -- A list of dictionaries, where role and content fields are
  required.
* **tools** (list[dict] | None, default None) -- The tools JSON schemas that the model can use.
* **tool_choice** (Literal["auto", "none", "any", "required"] | str             | None, default None) --

  Controls which (if any) tool is called by the model.Can be "auto", "none", "any", "required", or specific tool
  name. For more details, please refer to
  [https://ai.google.dev/gemini-api/docs/function-calling?hl=en&amp;example=meeting#function_calling_modes](https://ai.google.dev/gemini-api/docs/function-calling?hl=en&example=meeting#function_calling_modes)
* **structured_model** (Type[BaseModel] | None, default None) --
  A Pydantic BaseModel class that defines the expected structure
  for the model's output.

  备注

  When structured_model is specified,
  both tools and tool_choice parameters are ignored,
  and the model will only perform structured output
  generation without calling any other tools.

  For more details, please refer to[https://ai.google.dev/gemini-api/docs/structured-output](https://ai.google.dev/gemini-api/docs/structured-output)
* ****config_kwargs** (Any) -- The keyword arguments for Gemini chat completions API.

返回类型**:**
[*ChatResponse*](https://doc.agentscope.io/zh_CN/api/agentscope.model.html#agentscope.model.ChatResponse "agentscope.model._model_response.ChatResponse") |  *AsyncGenerator* [[*ChatResponse*](https://doc.agentscope.io/zh_CN/api/agentscope.model.html#agentscope.model.ChatResponse "agentscope.model._model_response.ChatResponse"), None]



# agentscope.tool

The tool module in agentscope.

*class*Toolkit[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_toolkit.html#Toolkit)基类：[`<span class="pre">StateModule</span>`](https://doc.agentscope.io/zh_CN/api/agentscope.module.html#agentscope.module.StateModule "agentscope.module._state_module.StateModule")

The class that supports both function- and group-level tool management.

Use the following methods to manage the tool functions:

* register_tool_function
* remove_tool_function

For group-level management:

* create_tool_group
* update_tool_groups
* remove_tool_groups

MCP related methods:

* register_mcp_server
* remove_mcp_servers

To run the tool functions or get the data from the activated tools:

* call_tool_function
* get_json_schemas
* get_tool_group_notes

**__init__**(**)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_toolkit.html#Toolkit.__init__)Initialize the toolkit.

返回类型**:**
None

**create_tool_group**( *group_name* ,  *description* ,  *active**=**False* ,  *notes**=**None* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_toolkit.html#Toolkit.create_tool_group)Create a tool group to organize tool functions

参数**:**

* **group_name** (str) -- The name of the tool group.
* **description** (str) -- The description of the tool group.
* **active** (bool, defaults to False) -- If the group is active, meaning the tool functions in this
  group are included in the JSON schema.
* **notes** (str | None, optional) -- The notes used to remind the agent how to use the tool
  functions properly, which can be combined into the system
  prompt.

返回类型**:**
None

**update_tool_groups**( *group_names* ,  *active* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_toolkit.html#Toolkit.update_tool_groups)Update the activation status of the given tool groups.

参数**:**

* **group_names** (list[str]) -- The list of tool group names to be updated.
* **active** (bool) -- If the tool groups should be activated or deactivated.

返回类型**:**
None

**remove_tool_groups**( *group_names* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_toolkit.html#Toolkit.remove_tool_groups)Remove tool functions from the toolkit by their group names.

参数**:**
**group_names** (str | list[str]) -- The group names to be removed from the toolkit.

返回类型**:**
None

**register_tool_function**( *tool_func* ,  *group_name**=**'basic'* ,  *preset_kwargs**=**None* ,  *func_description**=**None* ,  *json_schema**=**None* ,  *include_long_description**=**True* ,  *include_var_positional**=**False* ,  *include_var_keyword**=**False* ,  *postprocess_func**=**None* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_toolkit.html#Toolkit.register_tool_function)Register a tool function to the toolkit.

参数**:**

* **tool_func** (ToolFunction) -- The tool function, which can be async or sync, streaming or
  not-streaming, but the response must be a ToolResponse
  object.
* **group_name** (str | Literal["basic"], defaults to "basic") -- The belonging group of the tool function. Tools in "basic"
  group is always included in the JSON schema, while the others
  are only included when their group is active.
* **preset_kwargs** (dict[str, JSONSerializableObject] | None,             optional) -- Preset arguments by the user, which will not be included in
  the JSON schema, nor exposed to the agent.
* **func_description** (str | None, optional) -- The function description. If not provided, the description
  will be extracted from the docstring automatically.
* **json_schema** (dict | None, optional) -- Manually provided JSON schema for the tool function, which
  should be {"type": "function", "function": {"name":
  "function_name": "xx", "description": "xx",
  "parameters": {...}}}
* **include_long_description** (bool, defaults to True) -- When extracting function description from the docstring, if
  the long description will be included.
* **include_var_positional** (bool, defaults to False) -- Whether to include the variable positional arguments (*args)
  in the function schema.
* **include_var_keyword** (bool, defaults to False) -- Whether to include the variable keyword arguments (**kwargs)
  in the function schema.
* **postprocess_func** (Callable[[ToolUseBlock, ToolResponse],             ToolResponse | None] | None, optional) -- A post-processing function that will be called after the tool
  function is executed, taking the tool call block and tool
  response as arguments. If it returns None, the tool
  result will be returned as is. If it returns a
  ToolResponse, the returned block will be used as the
  final tool result.

返回类型**:**
None

**remove_tool_function**( *tool_name* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_toolkit.html#Toolkit.remove_tool_function)Remove tool function from the toolkit by its name.

参数**:**
**tool_name** (str) -- The name of the tool function to be removed.

返回类型**:**
None

**get_json_schemas**(**)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_toolkit.html#Toolkit.get_json_schemas)Get the JSON schemas from the tool functions that belong to the
active groups.

备注

The preset keyword arguments is removed from the JSON
schema, and the extended model is applied if it is set.

示例

**Example of tool function JSON schemas**

```
[
{
"type":"function",
"function":{
"name":"google_search",
"description":"Search on Google.",
"parameters":{
"type":"object",
"properties":{
"query":{
"type":"string",
"description":"The search query."
}
},
"required":["query"]
}
}
},
...
]
```

返回**:**
A list of function JSON schemas.

返回类型**:**
list[dict]

**set_extended_model**( *func_name* ,  *model* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_toolkit.html#Toolkit.set_extended_model)Set the extended model for a tool function, so that the original
JSON schema will be extended.

参数**:**

* **func_name** (str) -- The name of the tool function.
* **model** (Union[Type[BaseModel], None]) -- The extended model to be set.

返回类型**:**
None

*async*remove_mcp_clients**(** *client_names* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_toolkit.html#Toolkit.remove_mcp_clients)Remove tool functions from the MCP clients by their names.

参数**:**
**client_names** (list[str]) -- The names of the MCP client, which used to initialize the
client instance.

返回类型**:**
None

*async*call_tool_function**(** *tool_call* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_toolkit.html#Toolkit.call_tool_function)Execute the tool function by the ToolUseBlock and return the
tool response chunk in unified streaming mode, i.e. an async
generator of ToolResponse objects.

备注

The tool response chunk is  **accumulated** .

参数**:**
**tool_call** (ToolUseBlock) -- A tool call block.

生成器**:**
ToolResponse --     The tool response chunk, in accumulative manner.

返回类型**:**
 *AsyncGenerator* [[*ToolResponse*](https://doc.agentscope.io/zh_CN/api/agentscope.tool.html#agentscope.tool.ToolResponse "agentscope.tool._response.ToolResponse"), None]

*async*register_mcp_client**(** *mcp_client* ,  *group_name**=**'basic'* ,  *enable_funcs**=**None* ,  *disable_funcs**=**None* ,  *preset_kwargs_mapping**=**None* ,  *postprocess_func**=**None* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_toolkit.html#Toolkit.register_mcp_client)Register tool functions from an MCP client.

参数**:**

* **mcp_client** (MCPClientBase) -- The MCP client instance to connect to the MCP server.
* **group_name** (str, defaults to "basic") -- The group name that the tool functions will be added to.
* **enable_funcs** (list[str] | None, optional) -- The functions to be added into the toolkit. If None, all
  tool functions within the MCP servers will be added.
* **disable_funcs** (list[str] | None, optional) -- The functions that will be filtered out. If None, no
  tool functions will be filtered out.
* **preset_kwargs_mapping** ( *dict*  *[*  *str* *, * *dict*  *[*  *str* *, * *Any*  *]*  *] * *| * *None* ) -- (Optional[dict[str, dict[str, Any]]],             defaults to None):
  The preset keyword arguments mapping, whose keys are the tool
  function names and values are the preset keyword arguments.
* **postprocess_func** (Callable[[ToolUseBlock, ToolResponse],             ToolResponse | None] | None, optional) -- A post-processing function that will be called after the tool
  function is executed, taking the tool call block and tool
  response as arguments. If it returns None, the tool
  result will be returned as is. If it returns a
  ToolResponse, the returned block will be used as the
  final tool result.

返回类型**:**
None

**state_dict**(**)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_toolkit.html#Toolkit.state_dict)Get the state dictionary of the toolkit.

返回**:**
A dictionary containing the active tool group names.

返回类型**:**
dict[str, Any]

**load_state_dict**( *state_dict* ,  *strict**=**True* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_toolkit.html#Toolkit.load_state_dict)Load the state dictionary into the toolkit.

参数**:**

* **state_dict** (dict) -- The state dictionary to load, which should have "active_groups"
  key and its value must be a list of group names.
* **strict** (bool, defaults to True) -- If True, raises an error if any key in the module is not
  found in the state_dict. If False, skips missing keys.

返回类型**:**
None

**get_activated_notes**(**)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_toolkit.html#Toolkit.get_activated_notes)Get the notes from the active tool groups, which can be used to
construct the system prompt for the agent.

返回**:**
The combined notes from the active tool groups.

返回类型**:**
str

**reset_equipped_tools**( ***kwargs* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_toolkit.html#Toolkit.reset_equipped_tools)Choose appropriate tools to equip yourself with, so that you can
finish your task. Each argument in this function represents a group
of related tools, and the value indicates whether to activate the
group or not. Besides, the tool response of this function will
contain the precaution notes for using them, which you
 **MUST pay attention to and follow** . You can also reuse this function
to check the notes of the tool groups.

Note this function will reset the tools, so that the original tools
will be removed first.

参数**:**
**kwargs** ( *Any* )

返回类型**:**
[*ToolResponse*](https://doc.agentscope.io/zh_CN/api/agentscope.tool.html#agentscope.tool.ToolResponse "agentscope.tool._response.ToolResponse")

**clear**(**)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_toolkit.html#Toolkit.clear)Clear the toolkit, removing all tool functions and groups.

返回类型**:**
None

*class*ToolResponse[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_response.html#ToolResponse)基类：`<span class="pre">object</span>`

The result chunk of a tool call.

**content***:**List**[[TextBlock](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.TextBlock "agentscope.message._message_block.TextBlock")|[ImageBlock](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.ImageBlock "agentscope.message._message_block.ImageBlock")|[AudioBlock](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.AudioBlock "agentscope.message._message_block.AudioBlock")]*The execution output of the tool function.

**metadata** *:**dict**|**None*** *=**None***The metadata to be accessed within the agent, so that we don't need to
parse the tool result block.

**stream** *:**bool*** *=**False***Whether the tool output is streamed.

**__init__**( *content* ,  *metadata=None* ,  *stream=False* ,  *is_last=True* ,  *is_interrupted=False* ,  *id=`<factory>`* **)**
参数**:**

* **content** ( *List*  *[* [*TextBlock*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.TextBlock "agentscope.message._message_block.TextBlock")* | *[*ImageBlock*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.ImageBlock "agentscope.message._message_block.ImageBlock")* | *[*AudioBlock*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.AudioBlock "agentscope.message._message_block.AudioBlock") *]* )
* **metadata** (*dict** | * *None* )
* **stream** ( *bool* )
* **is_last** ( *bool* )
* **is_interrupted** ( *bool* )
* **id** ( *str* )

返回类型**:**
None

**is_last** *:**bool*** *=**True***Whether this is the last response in a stream tool execution.

**is_interrupted** *:**bool*** *=**False***Whether the tool execution is interrupted.

**id***:**str***The identity of the tool response.

*async*execute_python_code**(** *code* ,  *timeout**=**300* ,  ***kwargs* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_coding/_python.html#execute_python_code)Execute the given python code in a temp file and capture the return
code, standard output and error. Note you must print the output to get
the result, and the tmp file will be removed right after the execution.

参数**:**

* **code** (str) -- The Python code to be executed.
* **timeout** (float, defaults to 300) -- The maximum time (in seconds) allowed for the code to run.
* **kwargs** ( *Any* )

返回**:**
The response containing the return code, standard output, and
standard error of the executed code.

返回类型**:**
ToolResponse

*async*execute_shell_command**(** *command* ,  *timeout**=**300* ,  ***kwargs* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_coding/_shell.html#execute_shell_command)Execute given command and return the return code, standard output and
error within `<returncode></returncode>`, `<stdout></stdout>` and
`<stderr></stderr>` tags.

参数**:**

* **command** (str) -- The shell command to execute.
* **timeout** (float, defaults to 300) -- The maximum time (in seconds) allowed for the command to run.
* **kwargs** ( *Any* )

返回**:**
The tool response containing the return code, standard output, and
standard error of the executed command.

返回类型**:**
ToolResponse

*async*view_text_file**(** *file_path* ,  *ranges**=**None* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_text_file/_view_text_file.html#view_text_file)View the file content in the specified range with line numbers. If ranges is not provided, the entire file will be returned.

参数**:**

* **file_path** (str) -- The target file path.
* **ranges** ( *list*  *[*  *int*  *] * *| * *None* )
  -- The range of lines to be viewed (e.g. lines 1 to 100: [1, 100]),
  inclusive. If not provided, the entire file will be returned. To view
  the last 100 lines, use [-100, -1].

返回**:**
The tool response containing the file content or an error message.

返回类型**:**
ToolResponse

*async*write_text_file**(** *file_path* ,  *content* ,  *ranges**=**None* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_text_file/_write_text_file.html#write_text_file)Create/Replace/Overwrite content in a text file. When ranges is provided, the content will be replaced in the specified range. Otherwise, the entire file (if exists) will be overwritten.

参数**:**

* **file_path** (str) -- The target file path.
* **content** (str) -- The content to be written.
* **ranges** (list[int] | None, defaults to None) -- The range of lines to be replaced. If None, the entire file will
  be overwritten.

返回**:**
The tool response containing the result of the writing operation.

返回类型**:**
ToolResponse

*async*insert_text_file**(** *file_path* ,  *content* ,  *line_number* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_text_file/_write_text_file.html#insert_text_file)Insert the content at the specified line number in a text file.

参数**:**

* **file_path** (str) -- The target file path.
* **content** (str) -- The content to be inserted.
* **line_number** (int) -- The line number at which the content should be inserted, starting
  from 1. If exceeds the number of lines in the file, it will be
  appended to the end of the file.

返回**:**
The tool response containing the result of the insertion operation.

返回类型**:**
ToolResponse

**dashscope_text_to_image**( *prompt* ,  *api_key* ,  *n**=**1* ,  *size**=**'1024*1024'* ,  *model**=**'wanx-v1'* ,  *use_base64**=**False* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_multi_modality/_dashscope_tools.html#dashscope_text_to_image)Generate image(s) based on the given prompt, and return image url(s)
or base64 data.

参数**:**

* **prompt** (str) -- The text prompt to generate image.
* **api_key** (str) -- The api key for the dashscope api.
* **n** (int, defaults to 1) -- The number of images to generate.
* **size** (Literal["1024*1024", "720*1280", "1280*720"], defaults to          "1024*1024") -- Size of the image.
* **model** (str, defaults to '"wanx-v1"') -- The model to use, such as "wanx-v1", "qwen-image",
  "wan2.2-t2i-flash", etc.
* **use_base64** (bool, defaults to 'False') -- Whether to use base64 data for images.

返回**:**
A ToolResponse containing the generated content
(ImageBlock/TextBlock/AudioBlock) or error information if the
operation failed.

返回类型**:**
ToolResponse

**dashscope_text_to_audio**( *text* ,  *api_key* ,  *model**=**'sambert-zhichu-v1'* ,  *sample_rate**=**48000* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_multi_modality/_dashscope_tools.html#dashscope_text_to_audio)Convert the given text to audio.

参数**:**

* **text** (str) -- The text to be converted into audio.
* **api_key** (str) -- The api key for the dashscope API.
* **model** (str, defaults to 'sambert-zhichu-v1') -- The model to use. Full model list can be found in the
  [official document](https://help.aliyun.com/zh/model-studio/sambert-python-sdk).
* **sample_rate** (int, defaults to 48000) -- Sample rate of the audio.

返回**:**
A ToolResponse containing the generated content
(ImageBlock/TextBlock/AudioBlock) or error information if the
operation failed.

返回类型**:**
ToolResponse

**dashscope_image_to_text**( *image_urls* ,  *api_key* ,  *prompt**=**'Describe** **the** **image'* ,  *model**=**'qwen-vl-plus'* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_multi_modality/_dashscope_tools.html#dashscope_image_to_text)Generate text based on the given images.

参数**:**

* **image_urls** (str | Sequence[str]) -- The url of single or multiple images.
* **api_key** (str) -- The api key for the dashscope api.
* **prompt** (str, defaults to 'Describe the image') -- The text prompt.
* **model** (str, defaults to 'qwen-vl-plus') -- The model to use in DashScope MultiModal API.

返回**:**
A ToolResponse containing the generated content
(ImageBlock/TextBlock/AudioBlock) or error information if the
operation failed.

返回类型**:**
ToolResponse

**openai_text_to_image**( *prompt* ,  *api_key* ,  *n**=**1* ,  *model**=**'dall-e-2'* ,  *size**=**'256x256'* ,  *quality**=**'auto'* ,  *style**=**'vivid'* ,  *response_format**=**'url'* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_multi_modality/_openai_tools.html#openai_text_to_image)Generate image(s) based on the given prompt, and return image URL(s) or
base64 data.

参数**:**

* **prompt** (str) -- The text prompt to generate images.
* **api_key** (str) -- The API key for the OpenAI API.
* **n** (int, defaults to 1) -- The number of images to generate.
* **model** (Literal["dall-e-2", "dall-e-3"], defaults to "dall-e-2") -- The model to use for image generation.
* **size** (Literal["256x256", "512x512", "1024x1024", "1792x1024",         "1024x1792"], defaults to "256x256") -- The size of the generated images.
  Must be one of 1024x1024, 1536x1024 (landscape), 1024x1536 (
  portrait), or auto (default value) for gpt-image-1,
  one of 256x256, 512x512, or 1024x1024 for dall-e-2,
  and one of 1024x1024, 1792x1024, or 1024x1792 for dall-e-3.
* **quality** (Literal["auto", "standard", "hd", "high", "medium",         "low"],  defaults to "auto") --
  The quality of the image that will be generated.
  * auto (default value) will automatically select the best
    quality for the given model.
  * high, medium and low are supported for gpt-image-1.
  * hd and standard are supported for dall-e-3.
  * standard is the only option for dall-e-2.
* **style** (Literal["vivid", "natural"], defaults to "vivid") --
  The style of the generated images.
  This parameter is only supported for dall-e-3.
  Must be one of vivid or natural.
  * Vivid causes the model to lean towards generating hyper-real
    and dramatic images.
  * Natural causes the model to produce more natural,
    less hyper-real looking images.
* **response_format** (Literal["url", "b64_json"], defaults to "url") --
  The format in which generated images with dall-e-2 and dall-e-3
  are returned.
  * Must be one of "url" or "b64_json".
  * URLs are only valid for 60 minutes after the image has been
    generated.
  * This parameter isn't supported for gpt-image-1 which will always
    return base64-encoded images.

返回**:**
A ToolResponse containing the generated content
(ImageBlock/TextBlock/AudioBlock) or error information if the
operation failed.

返回类型**:**
ToolResponse

**openai_text_to_audio**( *text* ,  *api_key* ,  *model**=**'tts-1'* ,  *voice**=**'alloy'* ,  *speed**=**1.0* ,  *res_format**=**'mp3'* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_multi_modality/_openai_tools.html#openai_text_to_audio)Convert text to an audio file using a specified model and voice.

参数**:**

* **text** (str) -- The text to convert to audio.
* **api_key** (str) -- The API key for the OpenAI API.
* **model** (Literal["tts-1", "tts-1-hd"], defaults to "tts-1") -- The model to use for text-to-speech conversion.
* **voice** (Literal["alloy", "echo", "fable", "onyx", "nova",         "shimmer"], defaults to "alloy") -- The voice to use for the audio output.
* **speed** (float, defaults to 1.0) -- The speed of the audio playback. A value of 1.0 is normal speed.
* **res_format** (Literal["mp3", "wav", "opus", "aac", "flac",         "wav", "pcm"], defaults to "mp3") -- The format of the audio file.

返回**:**
A ToolResponse containing the generated content
(ImageBlock/TextBlock/AudioBlock) or error information if the
operation failed.

返回类型**:**
ToolResponse

**openai_edit_image**( *image_url* ,  *prompt* ,  *api_key* ,  *model**=**'dall-e-2'* ,  *mask_url**=**None* ,  *n**=**1* ,  *size**=**'256x256'* ,  *response_format**=**'url'* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_multi_modality/_openai_tools.html#openai_edit_image)Edit an image based on the provided mask and prompt, and return the edited
image URL(s) or base64 data.

参数**:**

* **image_url** (str) -- The file path or URL to the image that needs editing.
* **prompt** (str) -- The text prompt describing the edits to be made to the image.
* **api_key** (str) -- The API key for the OpenAI API.
* **model** (Literal["dall-e-2", "gpt-image-1"], defaults to "dall-e-2") -- The model to use for image generation.
* **mask_url** (str | None, defaults to None) -- The file path or URL to the mask image that specifies the regions
  to be edited.
* **n** (int, defaults to 1) -- The number of edited images to generate.
* **size** (Literal["256x256", "512x512", "1024x1024"], defaults to         "256x256") -- The size of the edited images.
* **response_format** (Literal["url", "b64_json"], defaults to "url") --
  The format in which generated images are returned.
  * Must be one of "url" or "b64_json".
  * URLs are only valid for 60 minutes after generation.
  * This parameter isn't supported for gpt-image-1 which will
    always return base64-encoded images.

返回**:**
A ToolResponse containing the generated content
(ImageBlock/TextBlock/AudioBlock) or error information if the
operation failed.

返回类型**:**
ToolResponse

**openai_create_image_variation**( *image_url* ,  *api_key* ,  *n**=**1* ,  *model**=**'dall-e-2'* ,  *size**=**'256x256'* ,  *response_format**=**'url'* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_multi_modality/_openai_tools.html#openai_create_image_variation)Create variations of an image and return the image URL(s) or base64 data.

参数**:**

* **image_url** (str) -- The file path or URL to the image from which variations will be
  generated.
* **api_key** (str) -- The API key for the OpenAI API.
* **n** (int, defaults to 1) -- The number of image variations to generate.
* **model** (` Literal["dall-e-2"]`, default to dall-e-2) -- The model to use for image variation.
* **size** (Literal["256x256", "512x512", "1024x1024"], defaults to         "256x256") -- The size of the generated image variations.
* **response_format** (Literal["url", "b64_json"], defaults to "url") --
  The format in which generated images are returned.
  * Must be one of url or b64_json.
  * URLs are only valid for 60 minutes after the image has been
    generated.

返回**:**
A ToolResponse containing the generated content
(ImageBlock/TextBlock/AudioBlock) or error information if the
operation failed.

返回类型**:**
ToolResponse

**openai_image_to_text**( *image_urls* ,  *api_key* ,  *prompt**=**'Describe** **the** **image'* ,  *model**=**'gpt-4o'* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_multi_modality/_openai_tools.html#openai_image_to_text)Generate descriptive text for given image(s) using a specified model, and
return the generated text.

参数**:**

* **image_urls** (str | list[str]) -- The URL or list of URLs pointing to the images that need to be
  described.
* **api_key** (str) -- The API key for the OpenAI API.
* **prompt** (str, defaults to "Describe the image") -- The prompt that instructs the model on how to describe
  the image(s).
* **model** (str, defaults to "gpt-4o") -- The model to use for generating the text descriptions.

返回**:**
A ToolResponse containing the generated content
(ImageBlock/TextBlock/AudioBlock) or error information if the
operation failed.

返回类型**:**
ToolResponse

**openai_audio_to_text**( *audio_file_url* ,  *api_key* ,  *language**=**'en'* ,  *temperature**=**0.2* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/tool/_multi_modality/_openai_tools.html#openai_audio_to_text)Convert an audio file to text using OpenAI's transcription service.

参数**:**

* **audio_file_url** (str) -- The file path or URL to the audio file that needs to be
  transcribed.
* **api_key** (str) -- The API key for the OpenAI API.
* **language** (str, defaults to "en") -- The language of the input audio in
  [ISO-639-1 format](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)
  (e.g., "en", "zh", "fr"). Improves accuracy and latency.
* **temperature** (float, defaults to 0.2) -- The temperature for the transcription, which affects the
  randomness of the output.

返回**:**
A ToolResponse containing the generated content
(ImageBlock/TextBlock/AudioBlock) or error information if the
operation failed.

返回类型**:**
ToolResponse


# agentscope.memory

The memory module.

*class*MemoryBase[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_memory_base.html#MemoryBase)基类：[`<span class="pre">StateModule</span>`](https://doc.agentscope.io/zh_CN/api/agentscope.module.html#agentscope.module.StateModule "agentscope.module._state_module.StateModule")

The base class for memory in agentscope.

*abstract**async***add**(** ****args*** ,  ***kwargs* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_memory_base.html#MemoryBase.add)Add items to the memory.

参数**:**

* **args** ( *Any* )
* **kwargs** ( *Any* )

返回类型**:**
None

*abstract**async***delete**(** ****args*** ,  ***kwargs* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_memory_base.html#MemoryBase.delete)Delete items from the memory.

参数**:**

* **args** ( *Any* )
* **kwargs** ( *Any* )

返回类型**:**
None

*abstract**async***retrieve**(** ****args*** ,  ***kwargs* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_memory_base.html#MemoryBase.retrieve)Retrieve items from the memory.

参数**:**

* **args** ( *Any* )
* **kwargs** ( *Any* )

返回类型**:**
None

*abstract**async***size**(**)[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_memory_base.html#MemoryBase.size)Get the size of the memory.

返回类型**:**
int

*abstract**async***clear**(**)[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_memory_base.html#MemoryBase.clear)Clear the memory content.

返回类型**:**
None

*abstract**async***get_memory**(** ****args*** ,  ***kwargs* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_memory_base.html#MemoryBase.get_memory)Get the memory content.

参数**:**

* **args** ( *Any* )
* **kwargs** ( *Any* )

返回类型**:**
list[[*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message._message_base.Msg")]

*abstract*state_dict**(**)[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_memory_base.html#MemoryBase.state_dict)Get the state dictionary of the memory.

返回类型**:**
dict

*abstract*load_state_dict**(** *state_dict* ,  *strict**=**True* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_memory_base.html#MemoryBase.load_state_dict)Load the state dictionary of the memory.

参数**:**

* **state_dict** ( *dict* )
* **strict** ( *bool* )

返回类型**:**
None

*class*InMemoryMemory[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_in_memory_memory.html#InMemoryMemory)基类：[`<span class="pre">MemoryBase</span>`](https://doc.agentscope.io/zh_CN/api/agentscope.memory.html#agentscope.memory.MemoryBase "agentscope.memory._memory_base.MemoryBase")

The in-memory memory class for storing messages.

**__init__**(**)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_in_memory_memory.html#InMemoryMemory.__init__)Initialize the in-memory memory object.

返回类型**:**
None

**state_dict**(**)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_in_memory_memory.html#InMemoryMemory.state_dict)Convert the current memory into JSON data format.

返回类型**:**
dict

**load_state_dict**( *state_dict* ,  *strict**=**True* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_in_memory_memory.html#InMemoryMemory.load_state_dict)Load the memory from JSON data.

参数**:**

* **state_dict** (dict) -- The state dictionary to load, which should have a "content"
  field.
* **strict** (bool, defaults to True) -- If True, raises an error if any key in the module is not
  found in the state_dict. If False, skips missing keys.

返回类型**:**
None

*async*size**(**)[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_in_memory_memory.html#InMemoryMemory.size)The size of the memory.

返回类型**:**
int

*async*retrieve**(** ****args*** ,  ***kwargs* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_in_memory_memory.html#InMemoryMemory.retrieve)Retrieve items from the memory.

参数**:**

* **args** ( *Any* )
* **kwargs** ( *Any* )

返回类型**:**
None

*async*delete**(** *index* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_in_memory_memory.html#InMemoryMemory.delete)Delete the specified item by index(es).

参数**:**
**index** (Union[Iterable, int]) -- The index to delete.

返回类型**:**
None

*async*add**(** *memories* ,  *allow_duplicates**=**False* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_in_memory_memory.html#InMemoryMemory.add)Add message into the memory.

参数**:**

* **memories** (Union[list[Msg], Msg, None]) -- The message to add.
* **allow_duplicates** (bool, defaults to False) -- If allow adding duplicate messages (with the same id) into
  the memory.

返回类型**:**
None

*async*get_memory**(**)[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_in_memory_memory.html#InMemoryMemory.get_memory)Get the memory content.

返回类型**:**
list[[*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message._message_base.Msg")]

*async*clear**(**)[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_in_memory_memory.html#InMemoryMemory.clear)Clear the memory content.

返回类型**:**
None

*class*LongTermMemoryBase[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_long_term_memory_base.html#LongTermMemoryBase)基类：[`<span class="pre">StateModule</span>`](https://doc.agentscope.io/zh_CN/api/agentscope.module.html#agentscope.module.StateModule "agentscope.module._state_module.StateModule")

The long-term memory base class, which should be a time-series
memory management system.

The record_to_memory and retrieve_from_memory methods are two tool
functions for agent to manage the long-term memory voluntarily. You can
choose not to implement these two functions.

The record and retrieve methods are for developers to use. For example,
retrieving/recording memory at the beginning of each reply, and adding
the retrieved memory to the system prompt.

*async*record**(** *msgs* ,  ***kwargs* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_long_term_memory_base.html#LongTermMemoryBase.record)A developer-designed method to record information from the given
input message(s) to the long-term memory.

参数**:**

* **msgs** ( *list*  *[* [*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message._message_base.Msg")* | * *None*  *]* )
* **kwargs** ( *Any* )

返回类型**:**
None

*async*retrieve**(** *msg* ,  ***kwargs* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_long_term_memory_base.html#LongTermMemoryBase.retrieve)A developer-designed method to retrieve information from the
long-term memory based on the given input message(s). The retrieved
information will be added to the system prompt of the agent.

参数**:**

* **msg** ([*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message._message_base.Msg")* | * *list*  *[* [*Msg*](https://doc.agentscope.io/zh_CN/api/agentscope.message.html#agentscope.message.Msg "agentscope.message._message_base.Msg") *] * *| * *None* )
* **kwargs** ( *Any* )

返回类型**:**
str

*async*record_to_memory**(** *thinking* ,  *content* ,  ***kwargs* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_long_term_memory_base.html#LongTermMemoryBase.record_to_memory)Use this function to record important information that you may
need later. The target content should be specific and concise, e.g.
who, when, where, do what, why, how, etc.

参数**:**

* **thinking** (str) -- Your thinking and reasoning about what to record
* **content** (list[str]) -- The content to remember, which is a list of strings.
* **kwargs** ( *Any* )

返回类型**:**
[*ToolResponse*](https://doc.agentscope.io/zh_CN/api/agentscope.tool.html#agentscope.tool.ToolResponse "agentscope.tool._response.ToolResponse")

*async*retrieve_from_memory**(** *keywords* ,  ***kwargs* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_long_term_memory_base.html#LongTermMemoryBase.retrieve_from_memory)Retrieve the memory based on the given keywords.

参数**:**

* **keywords** (list[str]) -- The keywords to search for in the memory, which should be
  specific and concise, e.g. the person's name, the date, the
  location, etc.
* **kwargs** ( *Any* )

返回**:**
A list of messages that match the keywords.

返回类型**:**
list[Msg]

*class*Mem0LongTermMemory[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_mem0_long_term_memory.html#Mem0LongTermMemory)基类：[`<span class="pre">LongTermMemoryBase</span>`](https://doc.agentscope.io/zh_CN/api/agentscope.memory.html#agentscope.memory.LongTermMemoryBase "agentscope.memory._long_term_memory_base.LongTermMemoryBase")

A class that implements the LongTermMemoryBase interface using mem0.

**__init__**( *agent_name**=**None* ,  *user_name**=**None* ,  *run_name**=**None* ,  *model**=**None* ,  *embedding_model**=**None* ,  *vector_store_config**=**None* ,  *mem0_config**=**None* ,  *default_memory_type**=**None* ,  ***kwargs* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_mem0_long_term_memory.html#Mem0LongTermMemory.__init__)Initialize the Mem0LongTermMemory instance

参数**:**

* **agent_name** (str | None, optional) -- The name of the agent. Default is None.
* **user_name** (str | None, optional) -- The name of the user. Default is None.
* **run_name** (str | None, optional) -- The name of the run/session. Default is None.
* **model** ([*ChatModelBase*](https://doc.agentscope.io/zh_CN/api/agentscope.model.html#agentscope.model.ChatModelBase "agentscope.model._model_base.ChatModelBase")* | * *None* )
* **embedding_model** ([*EmbeddingModelBase*](https://doc.agentscope.io/zh_CN/api/agentscope.embedding.html#agentscope.embedding.EmbeddingModelBase "agentscope.embedding._embedding_base.EmbeddingModelBase")* | * *None* )
* **vector_store_config** (*Any** | * *None* )
* **mem0_config** (*Any** | * *None* )
* **default_memory_type** (*str** | * *None* )
* **kwargs** ( *Any* )

返回类型**:**
None

备注

1. At least one of agent_name, user_name, or run_name is
   required.
2. During memory recording, these parameters become metadata
   for the stored memories.
3. **Important** : mem0 will extract memories from messages
   containing role of "user" by default. If you want to
   extract memories from messages containing role of
   "assistant", you need to provide agent_name.
4. During memory retrieval, only memories with matching
   metadata values will be returned.

model (ChatModelBase | None, optional):The chat model to use for the long-term memory. If
mem0_config is provided, this will override the LLM
configuration. If mem0_config is None, this is required.

embedding_model (EmbeddingModelBase | None, optional):The embedding model to use for the long-term memory. If
mem0_config is provided, this will override the embedder
configuration. If mem0_config is None, this is required.

vector_store_config (VectorStoreConfig | None, optional):The vector store config to use for the long-term memory.
If mem0_config is provided, this will override the vector store
configuration. If mem0_config is None and this is not
provided, defaults to Qdrant with on_disk=True.

mem0_config (MemoryConfig | None, optional):The mem0 config to use for the long-term memory.
If provided, individual
model/embedding_model/vector_store_config parameters will
override the corresponding configurations in mem0_config. If
None, a new MemoryConfig will be created using the provided
parameters.

default_memory_type (str | None, optional):The type of memory to use. Default is None, to create a
semantic memory.

抛出**:**
**ValueError** -- If mem0_config is None and either model or
    embedding_model is None.

参数**:**

* **agent_name** (*str** | * *None* )
* **user_name** (*str** | * *None* )
* **run_name** (*str** | * *None* )
* **model** ([*ChatModelBase*](https://doc.agentscope.io/zh_CN/api/agentscope.model.html#agentscope.model.ChatModelBase "agentscope.model._model_base.ChatModelBase")* | * *None* )
* **embedding_model** ([*EmbeddingModelBase*](https://doc.agentscope.io/zh_CN/api/agentscope.embedding.html#agentscope.embedding.EmbeddingModelBase "agentscope.embedding._embedding_base.EmbeddingModelBase")* | * *None* )
* **vector_store_config** (*Any** | * *None* )
* **mem0_config** (*Any** | * *None* )
* **default_memory_type** (*str** | * *None* )
* **kwargs** ( *Any* )

返回类型**:**
None

*async*record_to_memory**(** *thinking* ,  *content* ,  ***kwargs* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_mem0_long_term_memory.html#Mem0LongTermMemory.record_to_memory)Use this function to record important information that you may
need later. The target content should be specific and concise, e.g.
who, when, where, do what, why, how, etc.

参数**:**

* **thinking** (str) -- Your thinking and reasoning about what to record.
* **content** (list[str]) -- The content to remember, which is a list of strings.
* **kwargs** ( *Any* )

返回类型**:**
[*ToolResponse*](https://doc.agentscope.io/zh_CN/api/agentscope.tool.html#agentscope.tool.ToolResponse "agentscope.tool._response.ToolResponse")

*async*retrieve_from_memory**(** *keywords* ,  *limit**=**5* ,  ***kwargs* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_mem0_long_term_memory.html#Mem0LongTermMemory.retrieve_from_memory)Retrieve the memory based on the given keywords.

参数**:**

* **keywords** (list[str]) -- The keywords to search for in the memory, which should be
  specific and concise, e.g. the person's name, the date, the
  location, etc.
* **limit** (int, optional) -- The maximum number of memories to retrieve per search.
* **kwargs** ( *Any* )

返回**:**
A ToolResponse containing the retrieved memories as JSON text.

返回类型**:**
ToolResponse

*async*record**(** *msgs* ,  *memory_type**=**None* ,  *infer**=**True* ,  ***kwargs* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_mem0_long_term_memory.html#Mem0LongTermMemory.record)Record the content to the long-term memory.

参数**:**

* **msgs** (list[Msg | None]) -- The messages to record to memory.
* **memory_type** (str | None, optional) -- The type of memory to use. Default is None, to create a
  semantic memory. "procedural_memory" is explicitly used for
  procedural memories.
* **infer** (bool, optional) -- Whether to infer memory from the content. Default is True.
* ****kwargs** (Any) -- Additional keyword arguments for the mem0 recording.

返回类型**:**
None

*async*retrieve**(** *msg* ,  *limit**=**5* ,  ***kwargs* **)**[[源代码]](https://doc.agentscope.io/zh_CN/_modules/agentscope/memory/_mem0_long_term_memory.html#Mem0LongTermMemory.retrieve)Retrieve the content from the long-term memory.

参数**:**

* **msg** (Msg | list[Msg] | None) -- The message to search for in the memory, which should be
  specific and concise, e.g. the person's name, the date, the
  location, etc.
* **limit** (int, optional) -- The maximum number of memories to retrieve per search.
* ****kwargs** (Any) -- Additional keyword arguments.

返回**:**
The retrieved memory

返回类型**:**
str
