## Problem Statement

- Create a Gemini MCP that whenever, receives a request to upload an invoice, it populates the data on a google sheet. Also be able to answer user’s query based on invoice number, fetching data from google sheets and giving the needed details.

## To-Do List:

### Client:

- [x] Parse invoice data (image to text) VLM (Gemini)
- [ ] Connect Gemini API with our MCP server
- [ ] Answer user’s query based on the data received

### Sever:

- [x] Upload invoice data in google sheet (Service account)
- [ ] Upload item data in google sheet
- [ ] MCP Endpoints for uploading data
- [ ] Retrieve based on invoice number
- [ ] Allow different query strategies for model to get data for particular use-cases
- [ ] Create additional endpoints to do analysis (forecasting) on invoice data uploaded on sheets

### User Interface:

- [ ] Streamlit application as an interface

## Note:

To use with Claude Desktop update the configuration as below:

```json
{
  "mcpServers": {
    "invoice_parser": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/folder/with/server_file",
        "run",
        "python",
        "-W",
        "ignore",
        "server.py"
      ],
      "cwd": "/path/to/folder/with/server_file"
    }
  }
}
```
