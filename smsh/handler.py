from typing import Any, Callable, Dict, Generator, List

from smsh.config import cfg
from smsh.printer import MarkdownPrinter, Printer, TextPrinter
from smsh.role import SystemRole

completion: Callable[..., Any] = lambda *args, **kwargs: Generator[Any, None, None]
base_url = cfg.get("API_BASE_URL")
use_litellm = cfg.get("USE_LITELLM") == "true"
additional_kwargs = {
    "timeout": int(cfg.get("REQUEST_TIMEOUT")),
    "api_key": cfg.get("OPENAI_API_KEY"),
    "base_url": None if base_url == "default" else base_url,
}

if use_litellm:
    import litellm

    completion = litellm.completion
    litellm.suppress_debug_info = False
else:
    from openai import OpenAI

    client = OpenAI(**additional_kwargs)  # type: ignore
    completion = client.chat.completions.create
    additional_kwargs = {}


class Handler:

    def __init__(self, role: SystemRole, markdown: bool) -> None:
        self.role = role

        api_base_url = cfg.get("API_BASE_URL")
        self.base_url = None if api_base_url == "default" else api_base_url
        self.timeout = int(cfg.get("REQUEST_TIMEOUT"))

        self.markdown = "APPLY MARKDOWN" in self.role.role and markdown
        self.color = cfg.get("DEFAULT_COLOR")
        self.code_theme = cfg.get("CODE_THEME")

    @property
    def printer(self) -> Printer:
        return (
            MarkdownPrinter(self.code_theme)
            if self.markdown
            else TextPrinter(self.color)
        )

    def make_messages(self, prompt: str) -> List[Dict[str, str]]:
        messages = [
            {"role": "system", "content": self.role.role},
            {"role": "user", "content": prompt},
        ]
        return messages

    def get_completion(
            self,
            model: str,
            temperature: float,
            top_p: float,
            messages: List[Dict[str, Any]],
    ) -> Generator[str, None, None]:

        response = completion(
            model=model,
            temperature=temperature,
            top_p=top_p,
            messages=messages,
            stream=True,
            **additional_kwargs,
        )

        try:
            for chunk in response:
                delta = chunk.choices[0].delta
                yield delta.content or ""
        except KeyboardInterrupt:
            response.close()

    def handle(
            self,
            prompt: str,
            model: str,
            temperature: float,
            top_p: float,
    ) -> str:
        disable_stream = cfg.get("DISABLE_STREAMING") == "true"
        messages = self.make_messages(prompt.strip())
        generator = self.get_completion(
            model=model,
            temperature=temperature,
            top_p=top_p,
            messages=messages,
        )
        return self.printer(generator, not disable_stream)
