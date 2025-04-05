from mcp.server.fastmcp import FastMCP, Image
from mcp.server.fastmcp.prompts import base
from mcp.types import TextContent
from mcp import types
import pyautogui
import time
import subprocess
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime
from typing import Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# Verify email configuration on startup
email_address = os.getenv("EMAIL_ADDRESS")
email_password = os.getenv("EMAIL_PASSWORD")
if not email_address or not email_password:
    print("Warning: Email configuration not found in .env file")
    print(f"EMAIL_ADDRESS: {'set' if email_address else 'not set'}")
    print(f"EMAIL_PASSWORD: {'set' if email_password else 'not set'}")

# Instantiate an MCP server client
mcp = FastMCP("MacPaintbrush")

# Global variables
from PIL import Image as PILImage, ImageDraw, ImageFont
from pathlib import Path

# Global variables
current_image = None
current_draw = None
image_path = None


#addition tool15 = 27 = 42
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print("CALLED: add(a: int, b: int) -> int:")
    return int(a + b)

@mcp.tool()
def add_list(l: list) -> int:
    """Add all numbers in a list"""
    print("CALLED: add(l: list) -> int:")
    return sum(l)

# subtraction tool
@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    print("CALLED: subtract(a: int, b: int) -> int:")
    return int(a - b)

# multiplication tool
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    print("CALLED: multiply(a: int, b: int) -> int:")
    return int(a * b)

#  division tool
@mcp.tool() 
def divide(a: int, b: int) -> float:
    """Divide two numbers"""
    print("CALLED: divide(a: int, b: int) -> float:")
    return float(a / b)

# power tool
@mcp.tool()
def power(a: int, b: int) -> int:
    """Power of two numbers"""
    print("CALLED: power(a: int, b: int) -> int:")
    return int(a ** b)

# square root tool
@mcp.tool()
def sqrt(a: int) -> float:
    """Square root of a number"""
    print("CALLED: sqrt(a: int) -> float:")
    return float(a ** 0.5)

# cube root tool
@mcp.tool()
def cbrt(a: int) -> float:
    """Cube root of a number"""
    print("CALLED: cbrt(a: int) -> float:")
    return float(a ** (1/3))

# factorial tool
@mcp.tool()
def factorial(a: int) -> int:
    """factorial of a number"""
    print("CALLED: factorial(a: int) -> int:")
    return int(math.factorial(a))

# log tool
@mcp.tool()
def log(a: int) -> float:
    """log of a number"""
    print("CALLED: log(a: int) -> float:")
    return float(math.log(a))

# remainder tool
@mcp.tool()
def remainder(a: int, b: int) -> int:
    """remainder of two numbers divison"""
    print("CALLED: remainder(a: int, b: int) -> int:")
    return int(a % b)

# sin tool
@mcp.tool()
def sin(a: int) -> float:
    """sin of a number"""
    print("CALLED: sin(a: int) -> float:")
    return float(math.sin(a))

# cos tool
@mcp.tool()
def cos(a: int) -> float:
    """cos of a number"""
    print("CALLED: cos(a: int) -> float:")
    return float(math.cos(a))

# tan tool
@mcp.tool()
def tan(a: int) -> float:
    """tan of a number"""
    print("CALLED: tan(a: int) -> float:")
    return float(math.tan(a))

# mine tool
@mcp.tool()
def mine(a: int, b: int) -> int:
    """special mining tool"""
    print("CALLED: mine(a: int, b: int) -> int:")
    return int(a - b - b)

@mcp.tool()
def create_thumbnail(image_path: str) -> Image:
    """Create a thumbnail from an image"""
    print("CALLED: create_thumbnail(image_path: str) -> Image:")
    img = PILImage.open(image_path)
    img.thumbnail((100, 100))
    return Image(data=img.tobytes(), format="png")

@mcp.tool()
def strings_to_chars_to_int(string: str) -> list[int]:
    """Return the ASCII values of the characters in a word"""
    print("CALLED: strings_to_chars_to_int(string: str) -> list[int]:")
    return [int(ord(char)) for char in string]

@mcp.tool()
def int_list_to_exponential_sum(int_list: list) -> float:
    """Return sum of exponentials of numbers in a list"""
    print("CALLED: int_list_to_exponential_sum(int_list: list) -> float:")
    return sum(math.exp(i) for i in int_list)

@mcp.tool()
def fibonacci_numbers(n: int) -> list:
    """Return the first n Fibonacci Numbers"""
    print("CALLED: fibonacci_numbers(n: int) -> list:")
    if n <= 0:
        return []
    fib_sequence = [0, 1]
    for _ in range(2, n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence[:n]


@mcp.tool()
async def get_screen_size() -> Dict[str, int]:
    """Get the screen size in pixels"""
    width, height = pyautogui.size()
    return {
        "width": width,
        "height": height
    }

@mcp.tool()
async def open_paintbrush() -> dict:
    """Create a new image and open it in Paintbrush"""
    try:
        global current_image, current_draw, image_path
        
        # Create a new blank image
        screen_width, screen_height = pyautogui.size()
        current_image = PILImage.new('RGB', (screen_width, screen_height), 'white')
        current_draw = ImageDraw.Draw(current_image)
        
        # Save the image
        image_path = os.path.expanduser('~/Documents/drawing.png')
        current_image.save(image_path)
        
        # Open in Paintbrush and wait for it to load
        subprocess.run(['open', '-a', 'Paintbrush', image_path])
        time.sleep(3)  # Wait longer for app to open
        
        # Activate and maximize Paintbrush using AppleScript
        window_script = '''
        tell application "Paintbrush"
            activate
        end tell
        
        tell application "System Events"
            tell process "Paintbrush"
                set frontmost to true
                tell window 1
                    set {size, position} to {{1920, 1080}, {0, 0}}
                end tell
            end tell
        end tell
        '''
        subprocess.run(['osascript', '-e', window_script])
        time.sleep(2)
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text="New image created and opened in Paintbrush"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error creating image: {str(e)}"
                )
            ]
        }

@mcp.tool()
async def draw_rectangle(x1_percent: float, y1_percent: float, x2_percent: float, y2_percent: float) -> dict:
    """Draw a rectangle using percentages of screen size"""
    try:
        global current_image, current_draw, image_path
        if not current_draw:
            return {"content": [TextContent(type="text", text="Please open Paintbrush first using open_paintbrush()")]}
            
        # Convert string percentages to floats if needed
        x1_percent = float(x1_percent)
        y1_percent = float(y1_percent)
        x2_percent = float(x2_percent)
        y2_percent = float(y2_percent)
        
        # Get screen size
        screen_width, screen_height = pyautogui.size()
        print(f"Screen size: {screen_width}x{screen_height}")
        
        # Calculate coordinates (no padding, use full percentages)
        x1 = int(screen_width * x1_percent)
        y1 = int(screen_height * y1_percent)
        x2 = int(screen_width * x2_percent)
        y2 = int(screen_height * y2_percent)
            
        print(f"Drawing rectangle from ({x1},{y1}) to ({x2},{y2})")
        
        # Ensure Paintbrush is active and select rectangle tool
        activate_script = '''
        tell application "Paintbrush"
            activate
        end tell
        '''
        subprocess.run(['osascript', '-e', activate_script])
        time.sleep(1)
        
        # Move mouse to the rectangle tool button position (near top-left)
        screen_width, screen_height = pyautogui.size()
        pyautogui.moveTo(30, 200)  # Approximate position of rectangle tool
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(1)
        
        # Draw rectangle by clicking and dragging
        pyautogui.moveTo(x1, y1)
        time.sleep(1)
        
        # Click and hold at start point
        pyautogui.mouseDown()
        time.sleep(0.5)
        
        # Drag to end point slowly
        pyautogui.moveTo(x2, y2, duration=2.0)
        time.sleep(0.5)
        
        # Release to complete rectangle
        pyautogui.mouseUp()
        time.sleep(1)
        
        # Switch back to selection tool
        pyautogui.press('v')
        time.sleep(0.5)
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Rectangle drawn from ({x1},{y1}) to ({x2},{y2})"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error drawing rectangle: {str(e)}"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error drawing rectangle: {str(e)}"
                )
            ]
        }

@mcp.tool()
async def add_text(text: str, x_percent: float, y_percent: float) -> dict:
    """Add text at specified position"""
    try:
        global current_image, current_draw, image_path
        if not current_draw or not image_path:
            return {"content": [TextContent(type="text", text="Please open Paintbrush first using open_paintbrush()")]}

        # Convert string percentages to floats if needed
        x_percent = float(x_percent)
        y_percent = float(y_percent)
        
        # Get screen size and convert percentages to actual coordinates
        screen_width, screen_height = pyautogui.size()
        
        # Calculate text position relative to the rectangle
        # Rectangle is from 10% to 90% of screen
        rect_left = int(screen_width * 0.1)
        rect_top = int(screen_height * 0.1)
        rect_width = int(screen_width * 0.8)  # 90% - 10%
        rect_height = int(screen_height * 0.8)
        
        # Calculate text position relative to rectangle
        x = rect_left + int(rect_width * x_percent)
        y = rect_top + int(rect_height * y_percent)
        
        print(f"Adding text at ({x},{y})")

        # Ensure Paintbrush is active
        activate_script = '''
        tell application "Paintbrush"
            activate
        end tell
        '''
        subprocess.run(['osascript', '-e', activate_script])
        time.sleep(1)
        
        # Click the Text button in toolbar at exact coordinates
        pyautogui.moveTo(51, 236)  # Exact text tool position
        time.sleep(1)
        pyautogui.click()
        time.sleep(1)
        
        # # Small circular movement to ensure we're on the button
        # pyautogui.moveRel(-2, -2)
        # time.sleep(0.2)
        # pyautogui.moveRel(4, 0)
        # time.sleep(0.2)
        # pyautogui.moveRel(-2, 2)
        # time.sleep(0.2)
        # pyautogui.click()
        # time.sleep(1)
        
        # Calculate center position for text
        screen_width, screen_height = pyautogui.size()
        center_x = int(screen_width * 0.5)
        center_y = int(screen_height * 0.5)
        
        # Move to center of canvas and click to place text
        pyautogui.moveTo(center_x, center_y)
        time.sleep(1)
        pyautogui.click()
        time.sleep(1)
        
        # Type the text slowly
        for char in text:
            pyautogui.write(char)
            time.sleep(0.1)
        time.sleep(1)
        
        # Click 'Place' button (rightmost button)
        pyautogui.moveTo(center_x + 100, center_y + 100)  # Move to Place button on the right
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(1)
        
        # Move to specified position and click to place text
        target_x = int(screen_width * x_percent)  # Convert x percentage to pixels
        target_y = int(screen_height * y_percent)  # Convert y percentage to pixels
        pyautogui.moveTo(target_x, target_y)
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(1)
        
        # Move back to selection tool at top of toolbar
        pyautogui.moveTo(25, 25)  # Selection tool is first icon in toolbar
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(0.5)
        # Move slightly and click again to ensure selection
        pyautogui.moveRel(2, 2)
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(0.5)

        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Added text '{text}' at position ({x},{y})"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error adding text: {str(e)}"
                )
            ]
        }

@mcp.tool()
async def send_text_email(text: str) -> dict:
    """Send the answer text via email"""
    try:
        # Email configuration
        sender_email = os.getenv('EMAIL_ADDRESS')
        if not sender_email:
            raise ValueError("EMAIL_ADDRESS not set in .env file")
            
        sender_password = os.getenv('EMAIL_PASSWORD')
        if not sender_password:
            raise ValueError("EMAIL_PASSWORD not set in .env file")
            
        receiver_email = 'chaynandam@gmail.com'
        print(f"Sending email from {sender_email} to {receiver_email}")

        # Create the email
        msg = MIMEMultipart()
        msg['Subject'] = 'Answer from Paintbrush'
        msg['From'] = sender_email
        msg['To'] = receiver_email

        # Add body
        body = f'The answer is: {text}'
        msg.attach(MIMEText(body, 'plain'))

        try:
            # Send email
            print("Connecting to SMTP server...")
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                print("Attempting login...")
                server.login(sender_email, sender_password)
                print("Login successful, sending message...")
                server.send_message(msg)
                print("Message sent successfully")
        except smtplib.SMTPAuthenticationError as e:
            raise ValueError(
                "Email authentication failed. For Gmail, you need to use an App Password:\n" +
                "1. Go to your Google Account settings\n" +
                "2. Search for 'App Passwords'\n" +
                "3. Generate a new App Password for 'Mail'\n" +
                "4. Use that 16-character password in your .env file\n" +
                f"Error details: {str(e)}")
        except Exception as e:
            raise ValueError(f"SMTP error: {str(e)}")

        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Answer sent to {receiver_email}"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error sending screenshot: {str(e)}"
                )
            ]
        }

# @mcp.tool()
# async def save_document(filename: str) -> dict:
#     """Save the current document"""
#     try:
#         # Get the user's home directory
#         home_dir = os.path.expanduser('~')
#         # Create Documents directory if it doesn't exist
#         documents_dir = os.path.join(home_dir, 'Documents', 'PaintbrushDrawings')
#         os.makedirs(documents_dir, exist_ok=True)
        
#         # Full path for the file
#         full_path = os.path.join(documents_dir, filename)
        
#         # AppleScript to save the document
#         save_script = '''
#         tell application "Paintbrush"
#             activate
#             delay 1
#             tell application "System Events"
#                 keystroke "s" using command down
#                 delay 1
#                 keystroke "g" using {command down, shift down}
#                 delay 1
#                 keystroke "''' + documents_dir.replace('"', '\"') + '''"
#                 delay 1
#                 click button "Go" of sheet 1 of window 1 of application process "Paintbrush"
#                 delay 1
#                 keystroke "''' + filename.replace('"', '\"') + '''"
#                 delay 1
#                 click button "Save" of sheet 1 of window 1 of application process "Paintbrush"
#                 delay 1
#                 if (exists button "Replace" of sheet 1 of window 1 of application process "Paintbrush") then
#                     click button "Replace" of sheet 1 of window 1 of application process "Paintbrush"
#                 end if
#             end tell
#         end tell
#         '''
        
#         # Run the AppleScript
#         subprocess.run(['osascript', '-e', save_script])
#         time.sleep(2)
        
#         return {
#             "content": [
#                 TextContent(
#                     type="text",
#                     text=f"Document saved as {full_path}"
#                 )
#             ]
#         }
#     except Exception as e:
#         return {
#             "content": [
#                 TextContent(
#                     type="text",
#                     text=f"Error saving document: {str(e)}"
#                 )
#             ]
#         }

if __name__ == "__main__":
    import sys
    print("STARTING")
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        mcp.run_dev()
    else:
        mcp.run()
