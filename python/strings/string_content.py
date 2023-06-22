import string


class StringShifter:

    def __init__(self):
        valid_chars = f'{string.ascii_letters}{string.digits}{string.punctuation}'
        self.characters = [x for x in valid_chars]

    def shift_character(self, character: str, shift_value: int) -> str:
        if len(character) != 1 or character is None:
            raise ValueError('Max length of characters is one.')
        try:
            current_index = self.characters.index(character)
            shifted_index = current_index + shift_value
            if shifted_index > len(self.characters) - 1:
                shifted_index = shifted_index - len(self.characters)
            return self.characters[shifted_index]
        except Exception as e:
            raise e

    def shift_string(self, string_to_shift: str, shift_value: int) -> str:
        shifted = []
        for ch in string_to_shift:
            shifted_char = self.shift_character(ch, shift_value)
            shifted.append(shifted_char)
        return ''.join(shifted)

    def calculate_shift(self, value: int) -> int:
        # TODO Not working remainder calculations is wr0ng
        new_value = len(self.characters) % value
        return new_value

    def __len__(self):
        return len(self.characters)


if __name__ == '__main__':
    shifter = StringShifter()
    # ch = shifter.shift('v', 2)
    # print(shifter.characters)

    # print(f'{len(shifter)=}')s
    # print(f'{ch=}')

    # ch_shift = shifter.shift_character('a', -1)
    # ch_unshift = shifter.shift_character(ch_shift, 1)
    # print(f'{ch_shift=}')
    # print(f'{ch_unshift=}')

    string_2_shift = '_MyLovelyGirl1923*'
    shift = 2
    shifted_string = shifter.shift_string(string_2_shift, shift)

    shifted_back = shifter.shift_string(shifted_string, -shift)

    print(f'{string_2_shift=}')
    print(f'{shifted_string=}')
    print(f'{shifted_back=}')

    shift = 1001
    n = shifter.calculate_shift(shift)
    print(f'{n=}')
