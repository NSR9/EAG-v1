import os
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import asyncio
import google.generativeai as genai

from concurrent.futures import TimeoutError
from functools import partial

# Load environment variables from .env file
load_dotenv()

# Access your API key and initialize Gemini client correctly
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
client = genai

# Verify email configuration
email_address = os.getenv("EMAIL_ADDRESS")
email_password = os.getenv("EMAIL_PASSWORD")
if not email_address or not email_password:
    print("Warning: Email configuration not found in .env file")
    print(f"EMAIL_ADDRESS: {'set' if email_address else 'not set'}")
    print(f"EMAIL_PASSWORD: {'set' if email_password else 'not set'}")

max_iterations = 8
last_response = None
iteration = 0
iteration_response = []

async def generate_with_timeout(client, prompt, timeout=10):
    """Generate content with a timeout"""
    print("Starting LLM generation...")
    try:
        loop = asyncio.get_event_loop()
        response = await asyncio.wait_for(
            loop.run_in_executor(
                None, 
                lambda: client.GenerativeModel('gemini-2.0-flash').generate_content(
                    prompt
                )
            ),
            timeout=timeout
        )
        print("LLM generation completed")
        return response
    except TimeoutError:
        print("LLM generation timed out!")
        raise
    except Exception as e:
        print(f"Error in LLM generation: {e}")
        raise

def reset_state():
    """Reset all global variables to their initial state"""
    global last_response, iteration, iteration_response
    last_response = None
    iteration = 0
    iteration_response = []

async def main():
    reset_state()
    print("Starting main execution...")
    try:
        print("Establishing connection to MCP server...")
        server_params = StdioServerParameters(
            command="python",
            args=["mac_drawing_server.py"]
        )

        async with stdio_client(server_params) as (read, write):
            print("Connection established, creating session...")
            async with ClientSession(read, write) as session:
                print("Session created, initializing...")
                await session.initialize()
                
                print("Requesting tool list...")
                tools_result = await session.list_tools()
                tools = tools_result.tools
                print(f"Successfully retrieved {len(tools)} tools")

                print("Creating system prompt...")
                tools_description = []
                for i, tool in enumerate(tools):
                    try:
                        params = tool.inputSchema
                        desc = getattr(tool, 'description', 'No description available')
                        name = getattr(tool, 'name', f'tool_{i}')
                        
                        if 'properties' in params:
                            param_details = []
                            for param_name, param_info in params['properties'].items():
                                param_type = param_info.get('type', 'unknown')
                                param_details.append(f"{param_name}: {param_type}")
                            params_str = ', '.join(param_details)
                        else:
                            params_str = 'no parameters'

                        tool_desc = f"{i+1}. {name}({params_str}) - {desc}"
                        tools_description.append(tool_desc)
                    except Exception as e:
                        print(f"Error processing tool {i}: {e}")
                        tools_description.append(f"{i+1}. Error processing tool")
                
                tools_description = "\n".join(tools_description)
                
                system_prompt = f"""You are an AI assistant that can solve questions and visualize answers.

Available tools:
{tools_description}

For ANY question:
1. If it's a MATH question:
   - Use the appropriate math tool (add, subtract, multiply, etc.) to calculate the result
   - Wait for the tool to return the answer
   - Then visualize the answer (see step 3)

2. If it's a GENERAL question:
   - Determine the answer
   - Then visualize the answer (see step 3)

3. VISUALIZATION steps (do this after getting the answer):
   a. Call send_text_email with the answer text
   b. Call open_paintbrush to create a new window
   c. Call draw_rectangle (use 0.1 to 0.1 to 0.9 to 0.9 for good visibility)
   d. Call add_text to write the answer at position (0.3, 0.5) for center-left alignment

Coordinate System:
- All positions are percentages (0.0 to 1.0) of screen size
- (0.0, 0.0) is top-left corner
- (1.0, 1.0) is bottom-right corner
- Example: (0.5, 0.5) is center of screen

You must respond with EXACTLY ONE line at a time (no additional text):
1. For function calls:
   FUNCTION_CALL: function_name|param1|param2|...

2. For final answer after drawing:
   FINAL_ANSWER: Drawing completed successfully

Examples:
Math Question: "What is 5 + 3?"
1. Calculate result:
   FUNCTION_CALL: add|5|3
   [Tool returns: 8]
   FUNCTION_CALL: send_text_email|The answer to 5 + 3 is 8

2. Visualize answer:
   FUNCTION_CALL: open_paintbrush
   FUNCTION_CALL: draw_rectangle|0.1|0.1|0.9|0.9
   FUNCTION_CALL: add_text|5 + 3 = 8|0.3|0.5

General Question: "What is the capital of France?"
1. Know answer: Paris
   FUNCTION_CALL: send_text_email|The capital of France is Paris

2. Visualize answer:
   FUNCTION_CALL: open_paintbrush
   FUNCTION_CALL: draw_rectangle|0.1|0.1|0.9|0.9
   FUNCTION_CALL: add_text|Capital of France: Paris|0.3|0.5
- FINAL_ANSWER: Drawing completed successfully

Note: For draw_rectangle, coordinates are percentages of screen size (e.g., 0.1 = 10% from left/top, 0.9 = 90% from left/top)

DO NOT include any explanations or additional text.
Your entire response should be a single line starting with either FUNCTION_CALL: or FINAL_ANSWER:"""

                # Initialize Google Gemini client
                genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
                client = genai
                
                query = "What is 15 + 27 and capital of India?"
                global iteration, last_response
                
                while iteration < max_iterations:
                    print(f"\n--- Iteration {iteration + 1} ---")
                    if last_response is None:
                        current_query = query
                    else:
                        current_query = current_query + "\n\n" + " ".join(iteration_response)
                        current_query = current_query + "  What should I do next?"

                    print("Preparing to generate LLM response...")
                    prompt = f"{system_prompt}\n\nQuery: {current_query}"
                    try:
                        response = await generate_with_timeout(client, prompt)
                        response_text = response.text.strip()
                        print(f"LLM Response: {response_text}")
                        
                        for line in response_text.split('\n'):
                            line = line.strip()
                            if line.startswith("FUNCTION_CALL:") or line.startswith("FINAL_ANSWER:"):
                                response_text = line
                                break
                    except Exception as e:
                        print(f"Error generating response: {e}")
                        break
                    
                    print("LLM generation completed")
                    print(f"LLM Response: {response_text}")

                    if response_text.startswith("FUNCTION_CALL:"):
                        _, function_info = response_text.split(":", 1)
                        parts = [p.strip() for p in function_info.split("|")]
                        func_name, params = parts[0], parts[1:]
                        
                        try:
                            tool = next((t for t in tools if t.name == func_name), None)
                            if not tool:
                                raise ValueError(f"Unknown tool: {func_name}")

                            arguments = {}
                            if 'properties' in tool.inputSchema:
                                properties = tool.inputSchema['properties']
                                for i, (param_name, _) in enumerate(properties.items()):
                                    if i < len(params):
                                        # Convert parameter to appropriate type
                                        param_value = params[i]
                                        if properties[param_name].get('type') == 'integer':
                                            param_value = int(param_value)
                                        arguments[param_name] = param_value

                            print(f"Calling {func_name} with arguments: {arguments}")
                            result = await session.call_tool(func_name, arguments)
                            
                            # Get the full result content
                            if hasattr(result, 'content'):
                                print(f"Result has content attribute")
                                # Handle multiple content items
                                if isinstance(result.content, list):
                                    iteration_result = [item.text if hasattr(item, 'text') else str(item) for item in result.content]
                                else:
                                    iteration_result = str(result.content)
                            else:
                                print(f"Result has no content attribute")
                                iteration_result = str(result)
                                
                            print(f"Final iteration result: {iteration_result}")
                            
                            # Format the response based on result type
                            if isinstance(iteration_result, list):
                                result_str = f"[{', '.join(iteration_result)}]"
                            else:
                                result_str = str(iteration_result)
                            
                            iteration_response.append(
                                f"In iteration {iteration + 1} you called {func_name} with {arguments} parameters, "
                                f"and the function returned {result_str}."
                            )
                            last_response = {'result': result_str}
                            
                        except Exception as e:
                            print(f"Error executing function: {e}")
                            iteration_response.append(f"Error: {str(e)}")
                            last_response = None
                            
                    elif response_text.startswith("FINAL_ANSWER:"):
                        print("Task completed!")
                        break
                        
                    iteration += 1

    except Exception as e:
        print(f"Error in main: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
