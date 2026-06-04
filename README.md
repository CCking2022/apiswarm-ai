```markdown
# Apiswarm AI
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
Languages: [简体中文](README.zh-CN.md)

## Introduction
**Apiswarm AI（Apis + Swarm）**: Apis is Latin for honeybee, and Swarm stands for bee colony.
Apiswarm AI is a lightweight multi-instance task scheduling platform developed in Python. It does not run large language models locally; it only manages task queuing, forwards instructions to cloud LLMs, receives and organizes returned data to keep local device load low.

Users can split complex jobs into task lists in advance, and the platform schedules dozens of worker instances named "Little Bee" to process tasks in parallel.
Cross-platform deployment is supported on Windows, Linux and macOS. It can also be installed on low-power devices such as TV boxes after Linux flashing for 24/7 unattended running. Tasks can be submitted locally or via remote email, and results can be retrieved on demand, widely used in software development, novel & script writing, comic creation and various batch processing scenarios.

## Key Features
- Cross-platform: Pure Python implementation, available for Windows/Linux/macOS; TV boxes with Linux flashed are also supported
- Ultra-low resource consumption: All heavy computation runs on cloud LLMs; local side only handles scheduling, forwarding and data sorting
- 24/7 continuous runtime: All compatible devices support long-time idle service; low-power hardware like TV boxes provides outstanding cost performance
- Multi-instance parallel execution: Dozens of worker instances run concurrently to speed up bulk tasks drastically
- Custom task workflow: Users split tasks and define execution order & dependencies freely
- File-level task dependency: Subsequent tasks delay automatically if required pre-files are missing
- Standardized output catalog: All results are auto-classified and stored under preset folders
- Dual task submission: Local file import or remote email delivery
- Remote email interaction: Submit tasks, check status and download results via email with full user privacy control
- Dependency verification: Avoid interface conflict and formatting errors for parallel tasks

## Application Scenarios
### Software Development
Split project modules into task lists → parallel LLM code generation → execute following dependency rules → auto archive output for project development and Linux driver programming.

### Content Creation
Divide novels, screenplays or comic frames into subtasks → cluster parallel content generation → automatic categorized file storage for serial content production.

### General Automated Workflow
Batch copywriting, document sorting and material processing can be automated by predefined task lists with neatly sorted output files.

## Quick Start
### Environment Requirements
| Item | Specification |
|------|--------------|
| OS | Windows / Linux / macOS; TV Box(Linux flashed), Android(Termux), Mini Industrial PC |
| Python | 3.10 or higher |
| Network | Internet access for email service and cloud LLM API |
| Extra | Email account with POP3/SMTP enabled; LLM API Key (e.g. DeepSeek) |

### Installation
1. Clone source code
```bash
git clone https://github.com/CCking2022/apiswarm-ai.git
```

2. Install dependencies

```bash
cd apiswarm-ai
pip install -r requirements.txt
```

3. Configure project

- Copy `config.yaml.example` to `config.yaml`, set LLM endpoint, email credentials, task directory / output directory

- Copy `.env.example` to `.env`, fill your LLM API keys and email credentials before running.


4. Launch program

```bash
python main.py
```

### Submit Tasks

#### Option1: Local submission

Place task files into the assigned task folder defined in config.

#### Option2: Remote email submission

- New task: Send email with title `newtask`, attach task files as attachments

- Check running status: Email subject `status`

- Download output: Email subject `download:FolderName` (e.g. `download:story`), server will zip target directory and reply via mail

### Get Results

- Local access: Browse files directly from configured output folder

- Remote access: Send dedicated download request via email

## Workflow

### Local Task Mode

1. Preprocess: Split requirements, configure dependencies / output rules, write task lists

2. Keep service running: Program monitors task folder and incoming emails persistently

3. Put task files into target directory

4. Dependency check: Postpone tasks if prerequisite files missing

5. Forward requests to cloud LLM and fetch responses

6. Sort and save all generated files into specified folders

7. Check output locally or request files via email

### Remote Email Task Mode

1. Preprocess tasks and make task lists

2. Keep program online for mail monitoring

3. Send formatted email (title `newtask` + attached task files)

4. Dependency check, scheduling and file archiving same as local mode

5. Request result package via dedicated download mail

## Advantages

- 🚀 Full cross-platform & easy deployment

- 🛠️ Minimal hardware resource usage, works well on low-end devices

- ⚡ Parallel processing greatly improves batch task efficiency

- 🔋 Low-power hardware saves cost for long-running service

- 📧 Flexible dual submission via local directory or remote mail

- 📂 Complete dependency control + standardized file management

## Troubleshooting & Logs

Full runtime logs are generated to diagnose issues including:

- Task execution exceptions

- Failed dependency validation

- Email or API connection failures

- Parallel instance scheduling errors

## License

This open-source project is available under the MIT License. See [LICENSE](LICENSE) for full license terms.

## Contributing

- Submit Issues for bug reports or feature suggestions

- Create Pull Requests for code optimization or bug fixes

- Improve documentation and supplement usage cases

## FAQ

### Q1: How to deploy on TV box?

A1: Flash compatible Linux OS (such as Armbian) first, then install Python and project dependencies following standard steps.

### Q2: What LLMs are supported?

A2: Any LLM providing official API access (e.g. DeepSeek). Configure API address and key inside `config`.

### Q3: No reply after sending command email?

A3: 1. Confirm POP3/SMTP enabled for your mailbox; 2. Check network access to mail server; 3. Verify email parameters in config file.

