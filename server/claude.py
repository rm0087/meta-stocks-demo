import anthropic
from dotenv import load_dotenv
import os

load_dotenv()

client = anthropic.Anthropic(
    api_key= os.getenv('CLAUDE_KEY')
)



test_msg = 'PROSPECTUS 7,850,000 Units, with each Unit consisting of: One Share of Common Stock One Series A Warrant to Purchase One Share of Common Stock One Series B Warrant to Purchase One Share of Common Stock 92,150,000 Pre-Funded Units, with each Pre-Funded Unit consisting of: One Pre-Funded Warrant to Purchase One Share of Common Stock One Series A Warrant to Purchase One Share of Common Stock One Series B Warrant to Purchase One Share of Common Stock 92,150,000 Shares of Common Stock Underlying the Pre-Funded Warrants 100,000,000 Shares of Common Stock Underlying the Series A Warrants 100,000,000 Shares of Common Stock Underlying the Series B Warrants'

message = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": f'Please summarize the extent of shares being issued in this offering: {test_msg}'}
    ]
)

print(message.content)