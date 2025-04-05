# ADLS2 MCP Server 🚀

![License](https://img.shields.io/github/license/erikhoward/adls-mcp-server)
A Model Context Protocol (MCP) server implementation for Azure Data Lake Storage Gen2. This service provides a standardized interface for interacting with ADLS2 storage, enabling file operations through MCP tools.

## Setup 🛠️

### Installation 📦
Requires Python 3.13 or higher.

```bash
# Use pip or uv (recommen) adls2-mcp-server
uv pip install adls2-mcp-server
```

### Configuration ⚙️

1. Copy `.env.example` to `.env`
2. Configure the following environment variables:

```bash
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

uv pip install -e ".[dev]"
```

4 - Copy and configure environment variables:

```bash
cp .env.example .env
```

Edit .env with your settings.

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
