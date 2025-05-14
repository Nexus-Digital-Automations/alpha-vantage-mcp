from . import server_backup
import asyncio

def main():
    """Main entry point for the package."""
    asyncio.run(server_backup.main())

# Optionally expose other important items at package level
__all__ = ['main', 'server_backup']