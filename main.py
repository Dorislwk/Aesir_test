import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

df = pd.read_csv('/Users/lauwaikwan/Documents/Data engineer/AESIR/gamdata (1).csv', delimiter='|', skiprows=2)

# Q1 Data Manipulation
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
df.columns = ['game_id', 'player_id', 'score', 'level', 'timestamp']
df['timestamp'] = pd.to_datetime(df['timestamp'])

print(df.info())

def score_category(score):
    if score < 50:
        return 'Low'
    elif 50 <= score < 80:
        return 'Medium'
    elif score >= 80:
        return 'High'

df['score_category'] = df['score'].apply(score_category)

# Group data by level and calculate the average score
average_score_lv = df.groupby('level')['score'].mean().reset_index()
print(average_score_lv)

# Q2 Data Analysis
# What is the average score of players across all levels?
average_score = df['score'].mean()
print(f"The average score of players across all levels is: {average_score}")

# Which level has the highest average score?
highest_avg_score_level = average_score_lv.loc[average_score_lv['score'].idxmax()]
highest_level = int(highest_avg_score_level['level'])
print(f"Level {highest_level} has the highest average score.")

# How many players scored in the 'High' category?
high_players_count = df[df['score_category'] == 'High'].shape[0]
print(f'{high_players_count} players scored in the High category.')

# Q3 Data Visualization
# Create a bar chart that shows the average score for each level
plt.figure(figsize=(10, 6))
plt.bar(average_score_lv['level'], average_score_lv['score'], color='skyblue')
plt.title('Average Score for Each Level')
plt.xlabel('Level')
plt.ylabel('Average Score')
plt.xticks(rotation=0)
plt.tight_layout()

# Create a pie chart that displays the distribution of score categories ('Low', 'Medium', 'High')
category_counts = df['score_category'].value_counts()

fig, ax = plt.subplots()
ax.pie(category_counts, labels=category_counts.index,autopct='%1.1f%%')
plt.title('Distribution of Score Categories')

plt.show()

# Write a function that takes a player_id as input and returns the player's highest score and the level at which it was achieved.
def search_player_id(player_id):
    """
    Searches for a player's highest score and achieved level based on the provided player ID.

    Parameters:
    player_id (int): The ID of the player to search for.

    Outputs:
    - Prints an error message if no data is found for the given player ID.
    - Prints the highest score and level achieved by the player if data exists.
    """

    player_data = df[df['player_id'] == player_id]
    if player_data.empty:
        print('Please try again for no result found.')
        return
    
    player_data = df[df['player_id'] == player_id]
    highest_score_row = player_data.loc[player_data['score'].idxmax()]
    print(f"Player ID: {player_id}, Highest Score: {highest_score_row['score']}, Level Achieved: {highest_score_row['level']}")

def main():
    
    while True:
        player_id = int(input("What player's highest score and achieved level would you like to search for? Enter player ID: "))       
        search_player_id(player_id)

if __name__ == "__main__":
    main()