import os
import sys
import httpx
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_files_content import schema_get_files_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from call_function import call_function


def main():

    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan using the available tools. You can perform the following operations:

    - List files and directories to explore the codebase

    - Read file contents to understand code logic

    - Execute Python files with optional arguments if needed

    - Write or overwrite files for modifications

    Always think step-by-step and use multiple function calls if necessary to gather full information before providing a final response.

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    if len(sys.argv) < 2:
        print("I need a prompt buddie!")
        sys.exit(1)
    verbose_flag = False

    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose_flag = True
    prompt = sys.argv[1]

    msg = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_files_content,
        schema_write_file,
        schema_run_python_file
    ])

    try:
        res = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=msg,
            config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt
            )
        )
    except (httpx.ConnectError, ConnectionError) as e:
        print(f"Connection error: {e}")
        print("Please check your internet connection or network settings and try again.")
        return
    
    if res is None or res.usage_metadata is None:
        print("No usage metadata available.")
        return
    if verbose_flag:
        print(f"User prompt: {prompt}")
        print(f"Prompt Tokens: {res.usage_metadata.prompt_token_count}")
        print(f"Response Tokens: {res.usage_metadata.candidates_token_count}")

    if res.function_calls:
        msg.append(types.Content(role="model", parts=res.candidates[0].content.parts))
        function_responses = []
        for function_call_part in res.function_calls:
            function_call_result = call_function(function_call_part, verbose_flag)

            if (
                not function_call_result.parts
                or not function_call_result.parts[0].function_response
            ):
                raise Exception("empty function call result")

            if verbose_flag:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            function_responses.append(function_call_result)

        msg.extend(function_responses)

        final_res = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=msg,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            )
        )

        if final_res.text:
            print(final_res.text)
        else:
            print("No final response generated.")
    else:
        if verbose_flag:
            print(f"User prompt: {prompt}")
            print(f"Prompt Tokens: {res.usage_metadata.prompt_token_count}")
            print(f"Response Tokens: {res.usage_metadata.candidates_token_count}")

        print(res.text)


if __name__ == "__main__":
    main()
