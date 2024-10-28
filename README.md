# SmartShell

## 介绍

传统的命令行界面虽然功能强大，但对于不熟悉计算机操作的用户来说，使用起来较为复杂。本项目旨在开发一个基于 LangChain 和 ReAct 的智能 Shell 命令执行工具。该系统结合了 LangChain 的自然语言处理能力和 ReAct 的推理与行动能力，为用户提供更加智能、便捷的 Shell 命令执行体验。

## 软件环境要求

- **操作系统**：Linux, macOS, Windows, EulerOS
- **Python 版本**：Python 3.9 及以上
- 依赖库：
  - `typer`
  - `click`
  - `openai`
  - `litellm` (可选，用于使用 LiteLLM)
  - `rich`
  - `distro`

## 安装教程

1. **[openEuler]通过 dnf 包管理器安装**：

   ```bash
   sudo dnf install python-smart_shell
   pip install click==8.1.7 distro==1.9.0 litellm==1.42.5 openai==1.36.1 rich==13.7.1 typer==0.12.3
   smsh
   ```

2. **下载源码并运行**：

   ```bash
   git clone https://gitee.com/Delthin/smart_shell.git
   pip install -r requirements.txt
   cd smart_shell/smsh
   python app.py
   ```

3. **设置 OpenAI API Key及其他配置项**：
   在第一次运行时，系统会提示输入 OpenAI API Key，你也可以在 `.config/smart_shell/.smsh` 文件中设置 `OPENAI_API_KEY`和其他配置项。

## 功能展示

1. **智能命令生成**：根据用户的自然语言输入，智能生成相应的Shell命令。
2. **角色定制**：允许用户定义特定角色，以适应不同的命令生成需求。
3. **配置模式**：用户可以进入配置模式，实时修改和测试配置项。
4. **交互模式**：支持交互式命令生成，用户可以持续与系统交互，生成所需的Shell命令。
5. **本地大模型接入**：支持用户使用本地大模型接口使用此工具，比如Ollama等。

## 使用说明

以下是一些示例命令：

```bash
smsh 列出当前目录下的所有文件
# ls -a
# [E]xecute, [D]escribe, [C]ancel, [Q]uit: 
```
```bash
smsh 创建一个名为new_folder的新目录 --describe-shell
#命令：`mkdir new_folder`
#
#描述：创建一个名为`new_folder`的新目录。
#
#参数和选项：
#- `mkdir`：命令，用于创建新目录。
#- `new_folder`：要创建的新目录的名称。
#
#简短响应：使用`mkdir new_folder`命令可以在当前路径下创建一个名为`new_folder`的新目录。
```
```bash
smsh --config
#Entering configuration mode.
#Current configuration:
#CHAT_CACHE_LENGTH = 100
#REQUEST_TIMEOUT = 60
#DEFAULT_MODEL = gpt-4o
#DEFAULT_COLOR = magenta
#ROLE_STORAGE_PATH = /home/xxx/.config/smart_shell/roles
#DEFAULT_EXECUTE_SHELL_CMD = false
#DISABLE_STREAMING = false
#CODE_THEME = dracula
#API_BASE_URL = https://xxx
#PRETTIFY_MARKDOWN = true
#USE_LITELLM = false
#OPENAI_API_KEY = xxx
#Enter the config key you want to edit, or press 'q' to exit.: 
REQUEST_TIMEOUT
#Enter the new value for REQUEST_TIMEOUT: 
61
#Configuration for REQUEST_TIMEOUT has been updated to 61
```
本地大模型的接入需要修改配置文件，以ollama/qwen举例：
```
DEFAULT_MODEL = ollama/qwen,
API_BASE_URL = http://localhost:11434,
USE_LITELLM = true
```

你可以使用以下选项来控制命令的生成和执行：

 ``````bash
 ╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────╮
 │   prompt      [PROMPT]  The prompt to generate completions for.                                          │
 ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────╯
 ╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────╮
 │ --model            TEXT                       Large language model to use. [default: gpt-4o]             │
 │ --temperature      FLOAT RANGE [0.0<=x<=2.0]  Randomness of generated output. [default: 0.0]             │
 │ --top-p            FLOAT RANGE [0.0<=x<=1.0]  Limits highest probable tokens (words). [default: 1.0]     │
 │ --md             --no-md                      Prettify markdown output. [default: md]                    │
 │ --version                                     Show version.                                              │
 │ --help                                        Show this message and exit.                                │
 ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────╯
 ╭─ Assistance Options ─────────────────────────────────────────────────────────────────────────────────────╮
 │ --shell           -s                      Generate and execute shell commands.                           │
 │ --interaction     -i        Interactive mode for --shell option.                                         | 
 │ --describe-shell  -d        Describe a shell command.                                                    │
 │ --config          -c        Enter configuration edit mode.                        					   │
 ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────╯
 ╭─ Role Options ───────────────────────────────────────────────────────────────────────────────────────────╮
 │ --role                  TEXT  System role for GPT model. [default: None]                                 │
 │ --create-role           TEXT  Create role. [default: None]                                               │
 │ --show-role             TEXT  Show role. [default: None]                                                 │
 │ --list-roles   -lr            List roles.                                                                │
 ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────╯
 ``````

## 参与贡献

1. Fork 本仓库
2. 新建 feature_xxx 分支
3. 提交代码
4. 新建 Pull Request

## 许可证

本项目采用Mulan2.0开源。
