from mcp.server.fastmcp import FastMCP
import requests
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create an MCP server
mcp = FastMCP("Wordpress")

# WordPress configuration from environment variables
WORDPRESS_URL = os.getenv("WORDPRESS_URL", "https://your-wordpress-site.com")
WORDPRESS_USERNAME = os.getenv("WORDPRESS_USERNAME", "")
WORDPRESS_PASSWORD = os.getenv("WORDPRESS_PASSWORD", "")


def get_auth():
    """Get authentication tuple for WordPress API"""
    return (WORDPRESS_USERNAME, WORDPRESS_PASSWORD) if WORDPRESS_USERNAME and WORDPRESS_PASSWORD else None


@mcp.tool()
def create_post(title: str, content: str, status: str = "draft") -> str:
    """
    Create a new WordPress post.

    Args:
        title: The title of the post
        content: The content of the post (HTML allowed)
        status: Post status (draft, publish, pending, private). Default is 'draft'

    Returns:
        A message with the created post details
    """
    url = f"{WORDPRESS_URL}/wp-json/wp/v2/posts"

    data = {
        "title": title,
        "content": content,
        "status": status
    }

    try:
        response = requests.post(url, json=data, auth=get_auth())
        response.raise_for_status()

        post = response.json()
        return f"Post created successfully! ID: {post['id']}, Title: {post['title']['rendered']}, Status: {post['status']}, Link: {post['link']}"
    except requests.exceptions.RequestException as e:
        return f"Error creating post: {str(e)}"


@mcp.tool()
def delete_post(post_id: int, force: bool = False) -> str:
    """
    Delete a WordPress post by ID.

    Args:
        post_id: The ID of the post to delete
        force: Whether to bypass trash and force deletion. Default is False (moves to trash)

    Returns:
        A message confirming deletion or error
    """
    url = f"{WORDPRESS_URL}/wp-json/wp/v2/posts/{post_id}"

    params = {"force": force}

    try:
        response = requests.delete(url, params=params, auth=get_auth())
        response.raise_for_status()

        result = response.json()
        if force:
            return f"Post {post_id} permanently deleted successfully!"
        else:
            return f"Post {post_id} moved to trash successfully!"
    except requests.exceptions.RequestException as e:
        return f"Error deleting post: {str(e)}"


@mcp.resource("post://by-id/{post_id}")
def get_post_by_id(post_id: int) -> str:
    """
    Get a WordPress post by its ID.

    Args:
        post_id: The ID of the post to retrieve

    Returns:
        The post data as a formatted string
    """
    url = f"{WORDPRESS_URL}/wp-json/wp/v2/posts/{post_id}"

    try:
        response = requests.get(url, auth=get_auth())
        response.raise_for_status()

        post = response.json()
        return f"""Post ID: {post['id']}
Title: {post['title']['rendered']}
Status: {post['status']}
Date: {post['date']}
Modified: {post['modified']}
Slug: {post['slug']}
Link: {post['link']}

Content:
{post['content']['rendered']}"""
    except requests.exceptions.RequestException as e:
        return f"Error retrieving post: {str(e)}"


@mcp.resource("post://by-slug/{slug}")
def get_post_by_slug(slug: str) -> str:
    """
    Get a WordPress post by its slug.

    Args:
        slug: The slug of the post to retrieve

    Returns:
        The post data as a formatted string
    """
    url = f"{WORDPRESS_URL}/wp-json/wp/v2/posts"
    params = {"slug": slug}

    try:
        response = requests.get(url, params=params, auth=get_auth())
        response.raise_for_status()

        posts = response.json()
        if not posts:
            return f"No post found with slug: {slug}"

        post = posts[0]  # Get the first matching post
        return f"""Post ID: {post['id']}
Title: {post['title']['rendered']}
Status: {post['status']}
Date: {post['date']}
Modified: {post['modified']}
Slug: {post['slug']}
Link: {post['link']}

Content:
{post['content']['rendered']}"""
    except requests.exceptions.RequestException as e:
        return f"Error retrieving post: {str(e)}"


@mcp.prompt()
def wordpress_post_creation_guide() -> str:
    """
    Guide for creating WordPress posts with best practices
    """
    return """# WordPress Post Creation Guide

When creating WordPress posts, consider:

1. **Title**: Clear, descriptive, and SEO-friendly
2. **Content**: Well-formatted HTML or plain text
3. **Status Options**:
   - draft: Save without publishing
   - publish: Make live immediately
   - pending: Submit for review
   - private: Visible only to editors/admins

Example workflow:
1. Create a draft post first
2. Review the post using get_post_by_id resource
3. Update status to 'publish' when ready

Remember to set WORDPRESS_URL, WORDPRESS_USERNAME, and WORDPRESS_PASSWORD in your .env file."""


@mcp.prompt()
def wordpress_content_management() -> str:
    """
    WordPress content management workflow and tips
    """
    return """# WordPress Content Management Workflow

## Creating Posts
Use the create_post tool with:
- Compelling titles that grab attention
- Rich HTML content (paragraphs, headings, lists, images)
- Appropriate status (draft for review, publish for immediate release)

## Managing Posts
- Retrieve posts by ID or slug to review content
- Delete posts (moves to trash by default, use force=True for permanent deletion)
- Posts in trash can be restored from WordPress admin

## Best Practices
- Always create drafts first for important content
- Use meaningful slugs for SEO
- Include proper HTML formatting in content
- Review posts before publishing

## Common Tasks
1. Create new blog post: create_post(title="...", content="...", status="publish")
2. Check post details: Use post://by-id/{id} or post://by-slug/{slug}
3. Remove old post: delete_post(post_id=123)"""


@mcp.prompt()
def wordpress_troubleshooting() -> str:
    """
    Troubleshooting common WordPress MCP server issues
    """
    return """# WordPress MCP Server Troubleshooting

## Authentication Issues
If you get 401 or 403 errors:
1. Verify WORDPRESS_URL is correct (include https://)
2. Check WORDPRESS_USERNAME is valid
3. Ensure WORDPRESS_PASSWORD is an Application Password, not regular password
   - Generate in WordPress: Users → Profile → Application Passwords

## Connection Issues
If you can't connect:
1. Verify WordPress site is accessible
2. Check REST API is enabled: Visit {your-site}/wp-json/wp/v2/posts
3. Ensure no security plugins are blocking REST API

## Post Creation Failures
If posts aren't created:
1. Check user has 'edit_posts' capability
2. Verify content format is valid HTML
3. Try with status="draft" first

## Environment Setup
Required .env variables:
- WORDPRESS_URL: Full URL including https://
- WORDPRESS_USERNAME: WordPress admin username
- WORDPRESS_PASSWORD: Application password (not regular password)"""


if __name__ == "__main__":
    mcp.run()
