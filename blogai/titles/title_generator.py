from transformers import pipeline, set_seed

# Load GPT-2 model
generator = pipeline("text-generation", model="gpt2")
set_seed(42)

def generate_titles(blog_content, num_titles=3):
    # Well-structured prompt with few-shot examples
    prompt = (
        "You're an AI that writes short, catchy blog titles. Avoid generic 'How to' or question formats. "
        "Do not include author names, punctuation, or full sentences. Just give 3 creative and specific titles.\n\n"
        
        "Example:\n"
        "Blog content: Exploring automation's role in software teams.\n"
        "Titles:\n"
        "- Automate Your Code Life\n"
        "- Dev Teams Reimagined\n"
        "- Robots Write Code Too\n\n"
        
        "Example:\n"
        "Blog content: How AI agents boost productivity and reshape workflows.\n"
        "Titles:\n"
        "- AI That Gets Stuff Done\n"
        "- Smarter Workdays with AI\n"
        "- Reinventing Teamwork with Bots\n\n"
        
        f"Blog content: {blog_content.strip()}\n"
        "Titles:\n"
        "-"
    )


    # Generate text
    output = generator(
        prompt,
        max_length=len(prompt.split()) + 40,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.9,
        num_return_sequences=1
    )[0]["generated_text"]

    # Extract lines after the last "Suggested titles:"
    lines = output.split("Suggested titles:")[-1].strip().split("\n")

    # Clean and filter the title list
    titles = []
    for line in lines:
        if line.startswith("-"):
            title = line.lstrip("-• ").strip()
            title = title.split(", by")[0]  # remove any author junk
            title = title.split(".")[0].strip()  # keep first sentence only
            if len(title.split()) >= 3 and "http" not in title.lower():
                titles.append(title)

    return titles[:num_titles]
