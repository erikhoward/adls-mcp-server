# ADLS2 MCP Server 🚀

A Model Context Protocol (MCP) server implementation for Azure Data Lake Storage Gen2. This service provides a standardized interface for interacting with ADLS2 storage, enabling file operations through MCP tools.

[![License](https://img.shields.io/github/license/erikhoward/adls-mcp-server)](https://opensource.org/licenses/MIT) [![Python Version](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/) [![uv](https://img.shields.io/badge/uv-package%20manager-blueviolet)](https://docs.astral.sh/uv/) [![MCP](https://img.shields.io/badge/MCP-compatible-green.svg)](https://github.com/modelcontextprotocol/spec)

## Setup 🛠️

### Installation 📦

Requires Python 3.13 or higher.

Install the package using `uv`:

```bash
uv pip install adls2-mcp-server
```

### MCP Configuration ⚙️

### Claude Desktop Configuration

1 - Edit Claude Desktop Configuration:

Open `claude_desktop_config.json` and add the following configuration.

On MacOs, the file is located here:
`~/Library/Application Support/Claude Desktop/claude_desktop_config.json`.

On Windows, the file is located here:
`%APPDATA%\Claude Desktop\claude_desktop_config.json`.

```json
{
    "mcpServers": {
        "adls2": {
            "command": "adls2-mcp-server",
            "env": {
                "LOG_LEVEL": "DEBUG",
                "UPLOAD_ROOT": "/path/to/store/uploads",
                "DOWNLOAD_ROOT": "/path/to/store/downloads",
                "AZURE_STORAGE_ACCOUNT_NAME": "your-azure-adls2-storage-account-name",
                "READ_ONLY_MODE": "false"
            }
        }
    }
}
```

The following is a table of available environment configuration variables:

| Variable | Description | Default |
| --- | --- | --- |
| `LOG_LEVEL` | Logging level | `INFO` |
| `UPLOAD_ROOT` | Root directory for file uploads | `./uploads` |
| `DOWNLOAD_ROOT` | Root directory for file downloads | `./downloads` |
| `AZURE_STORAGE_ACCOUNT_NAME` | Azure ADLS2 storage account name | `None` |
| `AZURE_STORAGE_ACCOUNT_KEY` | Azure ADLS2 storage account key (optional) | `None` |
| `READ_ONLY_MODE` | Whether the server should operate in read-only mode | `true` |


If `AZURE_STORAGE_ACCOUNT_KEY` is not set, the server will attempt to authenticate using Azure CLI credentials. Ensure you have logged in with Azure CLI before running the server:

```bash
az login
```

2 - Restart Claude Desktop.

### Available Tools 🔧

#### Filesystem (container) Operations

- `list_filesystems` - List all filesystems in the storage account
- `create_filesystem` - Create a new filesystem
- `delete_filesystem` - Delete an existing filesystem

#### File Operations

- `upload_file` - Upload a file to ADLS2
- `download_file` - Download a file from ADLS2
- `file_exists` - Check if a file exists
- `rename_file` - Rename/move a file
- `get_file_properties` - Get file properties
- `get_file_metadata` - Get file metadata
- `set_file_metadata` - Set file metadata
- `set_file_metadata_json` - Set multiple metadata key-value pairs using JSON

#### Directory Operations

- `create_directory` - Create a new directory
- `delete_directory` - Delete a directory
- `rename_directory` - Rename/move a directory
- `directory_exists` - Check if a directory exists
- `directory_get_paths` - Get all paths under the specified directory

## Development 💻

### Local Development Setup

1 - Clone the repository:

```bash
git clone https://github.com/erikhoward/adls2-mcp-server.git
cd adls2-mcp-server
```

2 - Create and activate virtual environment:

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

3 - Install dependencies:

```bash
pip install -e ".[dev]"
```

4 - Copy and configure environment variables:

```bash
cp .env.example .env
```

Edit .env with your settings.

```bash
AZURE_STORAGE_ACCOUNT_NAME=your_azure_adls2_storage_account_name
AZURE_STORAGE_ACCOUNT_KEY=your_azure_adls2_storage_key (optional)
DOWNLOAD_ROOT=/path/to/download/folder
UPLOAD_ROOT=/path/to/upload/folder
READ_ONLY_MODE=True
LOG_LEVEL=INFO
```

If `AZURE_STORAGE_ACCOUNT_KEY` is not set, the server will attempt to authenticate using Azure CLI credentials. Ensure you have logged in with Azure CLI before running the server:

```bash
az login
```

5 - Claude Desktop Configuration

Open `claude_desktop_config.json` and add the following configuration.

On MacOs, the file is located here:
`~/Library/Application Support/Claude Desktop/claude_desktop_config.json`.

On Windows, the file is located here:
`%APPDATA%\Claude Desktop\claude_desktop_config.json`.

```json
{
    "mcpServers": {
        "adls2": {
            "command": "uv",
            "args": [
                "--directory",
                "/path/to/adls2-mcp-server/repo",
                "run",
                "adls2-mcp-server"
            ],
            "env": {
                "LOG_LEVEL": "DEBUG",
                "UPLOAD_ROOT": "/path/to/store/uploads",
                "DOWNLOAD_ROOT": "/path/to/store/downloads",
                "AZURE_STORAGE_ACCOUNT_NAME": "your-azure-adls2-storage-account-name",
                "READ_ONLY_MODE": "false"
            }
        }
    }
}
```

6 - Restart Claude Desktop.

## Contributions 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m '✨ Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License ⚖️

Licensed under MIT - see [LICENSE.md](LICENSE) file.

**This is not an official Microsoft product.**
