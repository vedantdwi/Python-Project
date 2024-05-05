def count_words(text):
    """
    Function to count the number of words in the input text.
    
    Parameters:
    text (str): The input text to count words from.
    
    Returns:
    int: The number of words in the input text.
    """
    # Split the text into words using whitespace as separator
    words = text.split()
    # Return the length of the list of words
    return len(words)

def main():
    # User input prompt
    print("Welcome to Word Counter!")
    text = input("Please enter a sentence or paragraph: ").strip()  # Remove leading/trailing whitespace
    
    # Check for empty input
    if not text:
        print("Error: Input is empty. Please provide some text.")
        return
    
    # Count words
    word_count = count_words(text)
    
    # Output display
    print(f"\nWord count: {word_count}")

if __name__ == "__main__":
    main()
