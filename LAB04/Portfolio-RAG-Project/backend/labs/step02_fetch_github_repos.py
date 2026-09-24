import urllib.request
import json
import os

def main():
    url = "https://api.github.com/users/Automatic28m/repos"
    print(f"Fetching data from {url}...")
    
    headers = {'User-Agent': 'Python/urllib'}
    # Optional: Use a GitHub token to bypass rate limits if provided
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        headers['Authorization'] = f'token {token}'
        
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
    except Exception as e:
        print(f"Failed to fetch GitHub data: {e}")
        print("Note: If you are hitting rate limits, you can set the GITHUB_TOKEN environment variable.")
        return

    output_lines = []
    for repo in data:
        # Skip forks
        if repo.get("fork"):
            continue
            
        name = repo.get("name")
        description = repo.get("description")
        if not description:
            description = "various technical implementations"
            
        language = repo.get("language")
        if not language:
            language = "various programming languages"
            
        topics_list = repo.get("topics", [])
        if topics_list:
            topics = ", ".join(topics_list)
        else:
            topics = "software development and engineering"
            
        html_url = repo.get("html_url")
        
        block = (
            f"[Category: GitHub Projects]\n"
            f"Q: What are your technical interests and expertise in {language} or {topics}? Do you have any projects related to this?\n"
            f"A: I have expertise in {language} and {topics}. For example, I built the {name} project, which focuses on {description}. You can view the repository here: {html_url}"
        )
        
        output_lines.append(block)

    file_path = os.path.join(os.path.dirname(__file__), "data", "portfolio_qa_en.txt")
    
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, "a", encoding="utf-8") as f:
        f.write("\n\n" + "\n\n".join(output_lines) + "\n")
    
    print(f"Successfully appended {len(output_lines)} repositories to data/portfolio_qa_en.txt")

if __name__ == "__main__":
    main()
