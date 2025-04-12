from typing_extensions import Annotated, Sequence, TypedDict

import operator
from langchain_core.messages import BaseMessage
from deep_translator import GoogleTranslator

import json


def merge_dicts(a: dict[str, any], b: dict[str, any]) -> dict[str, any]:
    return {**a, **b}

def translate_to_chinese(text):
    try:
        return GoogleTranslator(source='auto', target='zh-CN').translate(text)
    except Exception:
        return "[翻译失败]"

# Define agent state
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    data: Annotated[dict[str, any], merge_dicts]
    metadata: Annotated[dict[str, any], merge_dicts]


def show_agent_reasoning(output, agent_name):
    print(f"\n{'=' * 10} {agent_name.center(28)} {'=' * 10}")

    def convert_to_serializable(obj):
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        elif hasattr(obj, "__dict__"):
            return obj.__dict__
        elif isinstance(obj, (int, float, bool, str)):
            return obj
        elif isinstance(obj, (list, tuple)):
            return [convert_to_serializable(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: convert_to_serializable(value) for key, value in obj.items()}
        else:
            return str(obj)

    if isinstance(output, (dict, list)):
        serializable_output = convert_to_serializable(output)
        print(json.dumps(serializable_output, indent=2))

        # 🌟 加入中文翻译的部分
        if isinstance(serializable_output, dict):
            for ticker, data in serializable_output.items():
                if isinstance(data, dict) and "reasoning" in data:
                    reasoning = data["reasoning"]
                    chinese_reasoning = translate_to_chinese(reasoning)
                    print(f"\n【{ticker} 推理翻译】\n{chinese_reasoning}")

    else:
        try:
            parsed_output = json.loads(output)
            print(json.dumps(parsed_output, indent=2))
        except json.JSONDecodeError:
            print(output)

    print("=" * 48)