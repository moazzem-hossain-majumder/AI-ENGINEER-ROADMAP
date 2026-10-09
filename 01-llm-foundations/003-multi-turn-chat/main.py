"""
Project 003: Multi-Turn Chat & Context Buffer
Phase 01: LLM Foundations & Prompt Engineering

Demonstrates how conversation state is maintained on the client side,
how context accumulation works, and how to manage a sliding window buffer.
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv
from groq import Groq
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Ensure Windows terminals support UTF-8 characters and emojis
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Find and load root .env
root_dir = Path(__file__).resolve().parent.parent.parent
load_dotenv(root_dir / ".env")

console = Console(force_terminal=True)


class ChatSession:
    """Manages chat conversation history with sliding window buffer pruning."""

    def __init__(self, system_prompt: str, max_turns: int = 5, model: str = "qwen/qwen3.8-27b"):
        self.system_prompt = system_prompt
        self.max_turns = max_turns  # Max (user, assistant) pairs to retain
        self.model = model
        self.history: List[Dict[str, str]] = []
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env")
        self.client = Groq(api_key=api_key)

    def _build_payload(self) -> List[Dict[str, str]]:
        """Constructs the payload: System prompt + truncated history."""
        # Calculate maximum messages to keep (each turn = 1 user + 1 assistant)
        max_messages = self.max_turns * 2
        trimmed_history = self.history[-max_messages:]
        return [{"role": "system", "content": self.system_prompt}] + trimmed_history

    def send_message(self, user_message: str) -> str:
        """Sends user message, appends to history, and returns assistant reply."""
        # 1. Append user turn to history
        self.history.append({"role": "user", "content": user_message})

        # 2. Build full context payload
        payload = self._build_payload()

        # 3. Request LLM completion
        response = self.client.chat.completions.create(
            model=self.model,
            messages=payload,
            temperature=0.7,
            max_tokens=250
        )

        assistant_reply = response.choices[0].message.content.strip()

        # 4. Append assistant response to history
        self.history.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply

    def get_history_summary(self) -> Table:
        """Visualizes the current conversation history buffer."""
        table = Table(title="📜 Current Context Buffer (Memory State)", border_style="cyan")
        table.add_column("Turn #", style="bold dim", width=8)
        table.add_column("Role", style="bold yellow", width=12)
        table.add_column("Snippet", style="white")

        table.add_row("0 (Pinned)", "system", self.system_prompt[:60] + "...")
        for i, msg in enumerate(self.history, 1):
            role_style = "green" if msg["role"] == "user" else "magenta"
            table.add_row(str(i), f"[{role_style}]{msg['role']}[/]", msg["content"][:60] + "...")
        return table

    def clear(self):
        """Resets the conversation history."""
        self.history = []


def run_demonstration():
    """Runs an automated multi-turn conversation showing memory recall."""
    console.print("\n[bold cyan]🤖 Running Multi-Turn Demonstration Scenario...[/]\n")

    session = ChatSession(
        system_prompt="You are a helpful, concise AI study tutor. Remember all facts given.",
        max_turns=4
    )

    # Turn 1: Teach a fact
    t1_input = "Hi! Remember that my favorite programming language is Rust."
    console.print(f"[bold green]User (Turn 1):[/] {t1_input}")
    reply1 = session.send_message(t1_input)
    console.print(f"[bold magenta]AI:[/]\n{reply1}\n")

    # Turn 2: Unrelated question
    t2_input = "What is the capital of Japan?"
    console.print(f"[bold green]User (Turn 2):[/] {t2_input}")
    reply2 = session.send_message(t2_input)
    console.print(f"[bold magenta]AI:[/]\n{reply2}\n")

    # Turn 3: Test memory recall
    t3_input = "Based on our conversation earlier, what is my favorite programming language?"
    console.print(f"[bold green]User (Turn 3):[/] {t3_input}")
    reply3 = session.send_message(t3_input)
    console.print(f"[bold magenta]AI:[/]\n{reply3}\n")

    # Display the buffer table
    console.print(session.get_history_summary())


def run_interactive_cli():
    """Launches interactive chat loop."""
    console.print("\n[bold green]Type your message below. Commands: /history, /clear, /exit[/]\n")
    session = ChatSession(
        system_prompt="You are a friendly, knowledgeable AI Engineering assistant. Be concise.",
        max_turns=6
    )

    while True:
        try:
            user_input = console.input("[bold green]You > [/]").strip()
            if not user_input:
                continue

            if user_input in ["/exit", "/quit"]:
                console.print("[dim]Goodbye![/]")
                break
            elif user_input == "/clear":
                session.clear()
                console.print("[bold yellow]🧹 Conversation memory cleared![/]")
                continue
            elif user_input == "/history":
                console.print(session.get_history_summary())
                continue

            reply = session.send_message(user_input)
            console.print(f"\n[bold magenta]AI >[/] {reply}\n")

        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Session closed.[/]")
            break


def main():
    console.print("[bold yellow]===========================================================[/]")
    console.print("[bold green]  AI ENGINEER ROADMAP - PROJECT 003: MULTI-TURN CHAT BOT   [/]")
    console.print("[bold yellow]===========================================================[/]")

    # Check if run with interactive flag or default demo
    if "--interactive" in sys.argv or "-i" in sys.argv:
        run_interactive_cli()
    else:
        run_demonstration()
        console.print("[dim]\nTip: Run with --interactive or -i to chat live in the terminal![/dim]")


if __name__ == "__main__":
    main()
