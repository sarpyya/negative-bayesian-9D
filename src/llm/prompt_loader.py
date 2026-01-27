import os

class SystemPromptLoader:
    """Loads and caches markdown system prompts from the systemprompts directory."""
    
    def __init__(self, prompts_dir="src/systemprompts"):
        self.prompts_dir = prompts_dir
        self.cache = {}

    def load_prompt(self, prompt_name: str) -> str:
        """Loads a specific system prompt by filename (without extension)."""
        if prompt_name in self.cache:
            return self.cache[prompt_name]
        
        file_path = os.path.join(self.prompts_dir, f"{prompt_name}.md")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.cache[prompt_name] = content
                return content
        except FileNotFoundError:
            return f" [SYSTEM ERROR]: Prompt file {prompt_name}.md not found. Reverting to Default Bayes Persona."

prompt_loader = SystemPromptLoader()
