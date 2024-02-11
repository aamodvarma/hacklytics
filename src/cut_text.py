def get_first_two_sentences(text):
    """
    This function takes a string as input and returns the first two complete sentences,
    excluding upper case letters followed by another upper case letter.

    Args:
        text: The input string.

    Returns:
        A list containing the first two complete sentences from the input string.
    """

    sentences = []
    start = 0
    for i, char in enumerate(text):
        if char.isupper():
            # Check if next character is also uppercase
            if i + 1 < len(text) and text[i + 1].isupper():
                continue    # Skip this potential sentence start
            else:
                if i > start:
                    sentences.append(text[start:i])
                    start = i
        if len(sentences) == 4:
            break
    return sentences




if __name__ == "__main__":
        main();
