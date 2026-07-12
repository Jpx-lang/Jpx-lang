class Print:
    def __call__(self, s):
        print(s)

    def string(self, s=""):
        # Sebelumnya method ini hanya `return self` tanpa pernah mencetak
        # apapun, sehingga `print.string("hello")` tidak menghasilkan output.
        print(s)
        return self

    def empty(self):
        print()
        return self

exports = {
    'print': Print()
}