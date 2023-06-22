import string


class StringShifter:

    def __init__(self):
        valid_chars = f'{string.ascii_letters}{string.digits}{string.punctuation}'
        self.characters = [x for x in valid_chars]

    def shift(self, character: str, shift_value: int) -> str:
        try:
            current_index = self.characters.index(character)
            shifted_index = current_index + shift_value
            if shifted_index > len(self.characters) - 1:
                shifted_index = shifted_index - len(self.characters)
            return self.characters[shifted_index]
        except Exception as e:
            raise e

    def __len__(self):
        return len(self.characters)


if __name__ == '__main__':
    shifter = StringShifter()
    # ch = shifter.shift('v', 2)
    # print(shifter.characters)

    # print(f'{len(shifter)=}')
    # print(f'{ch=}')

    ch_shift = shifter.shift('a', -1)
    ch_unshift = shifter.shift(ch_shift, 1)
    print(f'{ch_shift=}')
    print(f'{ch_unshift=}')
