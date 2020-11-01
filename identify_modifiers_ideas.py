"""
Identifies modifiers in common/ideas folder

Idea
EU4 has a specific structure regarding it's idea modifiers that can make it easy to figure out where the modifiers are.
The previous naive implementation, which is looking at every line for specific features, catches conditions and AI
factors as well, which requires filtering out, resulting in a large and slow filter list. A new implementation that
can well where the modifiers based on the whole file's contents should let the whole program run far smoother and cut
down on the amount of words in the filter list.

Notes
I plan on relegating this script only to files in the common/ideas folder, but if the rest of the Eu4 modifiers carry
the same structure, I will expand this script to those as well.
"""

if __name__ == '__main__':
    """
    If run directly, returns a list of all modifiers found in a file, including line number.
    Of course right now it doesn't do that since I haven't written it yet.
    """
    print("Hello!")  # Test function
