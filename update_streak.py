import json
import os

def update_streak(user_id, is_sustainable):
    """Update user streak in the JSON file"""
    json_path = 'user_streaks.json'
    
    try:
        # Read current streaks
        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                user_streaks = json.load(f)
        else:
            user_streaks = {}
        
        # Update streak
        if is_sustainable:
            user_streaks[user_id] = user_streaks.get(user_id, 0) + 1
        else:
            user_streaks[user_id] = 0
        
        # Write back to file
        with open(json_path, 'w') as f:
            json.dump(user_streaks, f)
        
        return user_streaks[user_id]
    except Exception as e:
        print(f"Error updating streak: {e}")
        return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python update_streak.py <user_id> <is_sustainable>")
        sys.exit(1)
    
    user_id = sys.argv[1]
    is_sustainable = sys.argv[2].lower() == 'true'
    
    new_streak = update_streak(user_id, is_sustainable)
    if new_streak is not None:
        print(f"Updated streak for user {user_id}: {new_streak}")
    else:
        print("Failed to update streak") 