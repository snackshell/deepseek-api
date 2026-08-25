#!/usr/bin/env python3
"""
test_client.py
Test the proxy with a simple request.
"""

import httpx
import json
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = f"http://{os.getenv('HOST', '127.0.0.1')}:{os.getenv('PORT', '8080')}/v1"
API_KEY = os.getenv("PROXY_API_KEY", "sk-darkgpt-api")
MODEL = os.getenv("CUSTOM_MODEL_NAME", "deepseek-dark")

async def test_models():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/models",
            headers={"Authorization": f"Bearer {API_KEY}"}
        )
        print(f"Models: {response.status_code}")
        print(json.dumps(response.json(), indent=2))

async def test_chat():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "model": MODEL,
                "messages": [
                    {"role": "user", "content": "Who are you? Explain in one line."}
                ],
                "temperature": 0.7,
                "max_tokens": 100,
            }
        )
        print(f"Chat: {response.status_code}")
        data = response.json()
        if "choices" in data:
            print(f"Response: {data['choices'][0]['message']['content']}")
        else:
            print(json.dumps(data, indent=2))

async def test_stream():
    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST",
            f"{BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "model": MODEL,
                "messages": [
                    {"role": "user", "content": "Say hello in 3 words."}
                ],
                "stream": True,
            }
        ) as response:
            print(f"Stream: {response.status_code}")
            async for chunk in response.aiter_text():
                print(chunk, end="", flush=True)
            print()

async def main():
    await test_models()
    await test_chat()
    await test_stream()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
