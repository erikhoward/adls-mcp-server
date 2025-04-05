# ADLS2 MCP Server 🚀
![License](https://img.shields.io/github/license/erikhoward/adls-mcp-server)
A Model Context Protocol (MCP) server implementation for Azure Data Lake Storage Gen2. This service provides a standardized interface for interacting with ADLS2 storage, enabling file operations through MCP tools.
## Setup 🛠️
### Installation 📦
```bash
# Using pippip install adls2-mcp-server
# Using uv (recommended)
uv pip install adls2-mcp-server```
Requires Python 3.13 or higher.
### Configuration ⚙️
1. Copy `.env.example` to `.env`
2. Configure the following environment variables:
```bashAZURE_STORAGE_ACCOUNT_NAME=your_azure_adls2_storage_account_name
DOWNLOAD_ROOT=/path/to/download/folderUPLOAD_ROOT=/path/to/upload/folder
READ_ONLY_MODE=TrueLOG_LEVEL=INFO
```
Azure authentication uses DefaultAzureCredential. Ensure you have valid Azure credentials configured.
### Available Tools 🔧
#### Filesystem Operations- `list_filesystems` - List all filesystems in the storage account
- `create_filesystem` - Create a new filesystem- `delete_filesystem` - Delete an existing filesystem
#### File Operations
- `upload_file` - Upload a file to ADLS2- `download_file` - Download a file from ADLS2
- `file_exists` - Check if a file exists- `rename_file` - Rename/move a file
- `get_file_properties` - Get file properties- `get_file_metadata` - Get file metadata
- `set_file_metadata` - Set file metadata- `set_file_metadata_json` - Set multiple metadata key-value pairs using JSON
#### Directory Operations
- `create_directory` - Create a new directory- Additional directory operations coming soon
## Development 💻
### Local Development Setup
1. Clone the repository:
```bashgit clone https://github.com/erikhoward/adls2-mcp-server.git
cd adls2-mcp-server```
2. Create and activate virtual environment:
```bashpython -m venv .venv
source .venv/bin/activate  # Linux/macOS.venv\Scripts\activate     # Windows
```
3. Install dependencies:```bash
uv pip install -e ".[dev]"```
4. Copy and configure environment variables:
```bashcp .env.example .env
# Edit .env with your settings```
## Contributions 🤝
Contributions are welcome! Please feel free to submit a Pull Request.
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)3. Commit your changes (`git commit -m '✨ Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)5. Open a Pull Request
## License ⚖️

Licensed under MIT - see [LICENSE.md](LICENSE) file. This is not an official Microsoft product.

















































