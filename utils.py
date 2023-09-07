def index_of_coincidence(input):
    """Calculates the IoC"""

    if not input.isalpha():
        print("Called IoC on non-alpha string")
        return None

    # Sum occurances of letters
    letters = {}
    for i in input:
        if i in letters:
            letters[i] += 1
        else:
            letters[i] = 1

    # Calculate using algorithm from class
    sigma_f = 0
    for f in letters.items():
        sigma_f += f*(f - 1)
    big_n = len(input)
    return sigma_f/(big_n * (big_n - 1))
