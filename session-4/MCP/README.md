# Mac Drawing MCP

A multimodal application that combines mathematical computing with visualization capabilities using the Multimodal Conversational Protocol (MCP) framework.

## Overview

Mac Drawing MCP is a client-server application that:
- Processes natural language queries (both math and general knowledge questions)
- Computes answers using appropriate mathematical operations
- Visualizes responses by drawing them on screen using Paintbrush
- Sends results via email

## Features

- **Mathematical Operations**: Addition, subtraction, multiplication, division, powers, roots, and other mathematical functions
- **Visualization Tools**: Create drawings, rectangles, and add text to visualize answers
- **Email Integration**: Send computed results via email
- **Natural Language Processing**: Using Google's Gemini AI model to interpret user queries

## Requirements

- Python 3.x
- macOS with Paintbrush application installed
- Google Gemini API key
- Email account for sending results

## Dependencies

This project requires the following Python packages:
- mcp (Multimodal Conversational Protocol)
- google-generativeai
- pyautogui
- pillow
- python-dotenv
- asyncio
- And others listed in requirements.txt

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project directory with the following variables:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   EMAIL_ADDRESS=your_email_address
   EMAIL_PASSWORD=your_email_password
   ```

## Usage

1. Start the server:
   ```
   python mac_drawing_server.py
   ```

2. In a separate terminal, run the client:
   ```
   python mac_drawing_client.py
   ```

3. The client will send a default query "What is 15 + 27 and capital of India?" to demonstrate functionality

4. You can modify the query in mac_drawing_client.py to ask different questions

## How It Works

1. The client sends a query to the Gemini AI model
2. Gemini interprets the query and generates appropriate function calls
3. The client sends these function calls to the server
4. The server executes the functions (calculations, drawing, emails)
5. Results are displayed graphically using Paintbrush and sent via email

## Coordinate System

For drawing functions:
- All positions are percentages (0.0 to 1.0) of screen size
- (0.0, 0.0) is top-left corner
- (1.0, 1.0) is bottom-right corner
- Example: (0.5, 0.5) is center of screen

## Example Queries

- Mathematical: "What is 5 + 3?"
- General knowledge: "What is the capital of France?"
- Combined: "What is 15 + 27 and capital of India?"

## Last Updated

April 4, 2025
