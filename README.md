# WordPress MCP Server

A Model Context Protocol (MCP) server that provides tools for managing WordPress content. This server enables AI assistants to create, retrieve, and delete WordPress posts through the WordPress REST API.

## Features

- **Create Posts**: Create WordPress posts with customizable titles, content, and status
- **Delete Posts**: Remove posts or move them to trash
- **Retrieve Posts**: Get post details by ID or slug
- **Built-in Prompts**: Access guides for post creation, content management, and troubleshooting

## Installation

### Prerequisites

- Python 3.12.11
- A WordPress site with REST API enabled
- WordPress Application Password for authentication

### Setup

1. **Create a virtual environment with Python 3.12.11:**
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install uv:**
   ```bash
   pipx install uv
   ```

4. **Configure environment variables:**

   Create a `.env` file in the project root:
   ```
   WORDPRESS_URL=https://your-wordpress-site.com
   WORDPRESS_USERNAME=your_username
   WORDPRESS_PASSWORD=your_application_password
   ```

   Note: Use an Application Password (generated from WordPress admin under Users → Profile → Application Passwords), not your regular WordPress password.

## Usage

### Development Mode

Run the MCP inspector for testing:
```bash
mcp dev server.py
```

### Running the Server

```bash
python server.py
```

## Available Tools

- `create_post(title, content, status)` - Create a new WordPress post
- `delete_post(post_id, force)` - Delete a post by ID

## Available Resources

- `post://by-id/{post_id}` - Retrieve a post by its ID
- `post://by-slug/{slug}` - Retrieve a post by its slug

## Available Prompts

- `create_new_post(topic, post_type, target_audience)` - Generate a complete WordPress post about a specific topic with structured content and formatting guidance

## License

MIT
