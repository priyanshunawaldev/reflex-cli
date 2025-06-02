def clean_user_input(text: str) -> str:
    """Clean user input - nothing fancy, just prevent obvious problems"""
    if not text:
        return ""
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    # Limit ridiculous lengths (who writes 5000 char tasks anyway?)
    if len(text) > 1000:
        text = text[:1000] + "..."
    
    # Just escape quotes to prevent basic SQL issues
    # Yeah, we should use prepared statements everywhere but this is a quick fix
    text = text.replace("'", "''")
    
    return text

def is_reasonable_input(text: str) -> bool:
    """Check if input looks reasonable - not trying to catch everything"""
    if not text or len(text.strip()) == 0:
        return False
    
    # Basic sanity checks
    if len(text) > 1000:
        return False
        
    # Block obvious script attempts (most hackers aren't targeting CLI productivity tools anyway)
    suspicious = ['<script', 'javascript:', 'DROP TABLE', '--', ';DELETE']
    text_lower = text.lower()
    
    for sus in suspicious:
        if sus.lower() in text_lower:
            return False
    
    return True