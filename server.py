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


if __name__ == "__main__":
    mcp.run()
